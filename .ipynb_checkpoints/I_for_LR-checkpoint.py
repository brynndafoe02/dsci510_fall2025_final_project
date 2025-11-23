import os
import csv
import math
from statistics import mean, pstdev
from collections import defaultdict

# ---------- CONFIG ----------
# If True: only read first N rows of each WC CSV (helps avoid messy lower rows)
LIMIT_ROWS_PER_FILE = 30

# Map cycle suffix -> Olympic year
CYCLE_YEAR = { "1": 2018, "2": 2022, "3": 2026 }

# Names for output
TRAIN_OUT = "Training_Data.csv"
TEST_OUT = "Testing_Data.csv"

# Top-level cleaned folder (script assumes you run it from inside cleaned/)
ROOT = "."

# Possible AthleteData filenames (tries both)
ATHLETE_FILES = ["AthleteData.csv", "Athlete_Data.csv", "AthleteData .csv"]

# Olympic results folder name
OLYMPIC_FOLDER = "olympic_results"

# Columns expected in world cup files (we'll match tolerant to leading/trailing spaces)
EXPECTED_FIELDS = {
    "fisc": ["FIS Code", "FISCode", "FIS", " FIS Code", "FIS Code "],
    "final": ["Final Score", "Final score", "FinalScore", "Total Score", " Score"],
    "time": ["Time Points", "TimePoints", "Time Points "],
    "air": ["Air Points", "AirPoints", "Air Points "],
    "turn": ["Turn Points", "TurnPoints", "Turn Points "],
    "rank": ["Rank", "rank", "Position", "Pos"],
    "name": ["Name", " Name", "Name "],
    "nation": ["Nation", "Nation ", "Country", "Country "],
    "birth": ["Birth Year", "BirthYear", "YB"],
}

# --------- helper functions ----------
def find_athlete_file():
    for fname in ATHLETE_FILES:
        if os.path.isfile(os.path.join(ROOT, fname)):
            return os.path.join(ROOT, fname)
    # fallback: look for any file containing "Athlete" prefix
    for fname in os.listdir(ROOT):
        if fname.lower().startswith("athlete") and fname.lower().endswith(".csv"):
            return os.path.join(ROOT, fname)
    raise FileNotFoundError("AthleteData.csv not found in cleaned/ — make sure file is present.")

def normalize_fieldnames(fieldnames):
    """Strip whitespace from each header and return cleaned list."""
    if fieldnames is None:
        return []
    return [f.strip() for f in fieldnames]

def multi_get(row, candidates):
    """Try to get a value from row for any candidate header (strip keys too)."""
    for key in candidates:
        # try exact
        if key in row:
            return row[key]
    # try stripped keys
    for k in row.keys():
        if k and k.strip() in candidates:
            return row[k]
    return None

def find_header_key_map(fieldnames):
    """
    Given a list of fieldnames, return a map of normalized keys we can use to fetch from a row.
    Example return: { "fisc": "FIS Code", "final": "Final Score", ... }
    """
    fn_strip = [f.strip() for f in fieldnames]
    keymap = {}
    for logical, candidates in EXPECTED_FIELDS.items():
        for c in candidates:
            if c.strip() in fn_strip:
                # find the original raw name that matches this stripped one
                for raw in fieldnames:
                    if raw and raw.strip() == c.strip():
                        keymap[logical] = raw
                        break
                break
    return keymap

def safe_float(x):
    if x is None:
        return None
    if isinstance(x, float) or isinstance(x, int):
        return float(x)
    s = str(x).strip()
    if s == "" or s.lower() in ("nan", "na", "n/a", "-"):
        return None
    # remove commas
    s = s.replace(",", "")
    try:
        return float(s)
    except:
        return None

def compute_avg(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    return mean(vals)

def compute_std(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    if len(vals) == 1:
        return 0.0
    try:
        return pstdev(vals)  # population std, use stdev if you prefer sample sd
    except:
        return None

# ---------- Load athlete master list ----------
athlete_file = find_athlete_file()
print("Using athlete file:", athlete_file)

athletes = {}   # key: FIS Code (as str) -> dict with Name, Birth Year, Gender
with open(athlete_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = normalize_fieldnames(reader.fieldnames)
    # find column names robustly
    name_key = None
    fis_key = None
    birth_key = None
    gender_key = None
    for raw in reader.fieldnames:
        r = raw.strip()
        if r.lower() == "name":
            name_key = raw
        elif r.lower().replace(" ", "") in ("fiscalcode","fiscalcode","fisscode","fiscode","fisc" ,"fiscocode","fisc code"):
            fis_key = raw
        elif "fis" in r.lower() and "code" in r.lower():
            fis_key = raw
        elif r.lower().replace(" ", "") in ("birthyear","yob","yb"):
            birth_key = raw
        elif r.lower() in ("gender", "sex"):
            gender_key = raw
    # fallback guesses
    if not fis_key:
        for raw in reader.fieldnames:
            if "fis" in raw.lower() and "code" in raw.lower():
                fis_key = raw
                break
    if not birth_key:
        for raw in reader.fieldnames:
            if "birth" in raw.lower():
                birth_key = raw
                break
    if not name_key:
        for raw in reader.fieldnames:
            if "name" in raw.lower():
                name_key = raw
                break
    if not gender_key:
        for raw in reader.fieldnames:
            if "gender" in raw.lower() or raw.lower().strip()=="g":
                gender_key = raw
                break

    # read rows
    f.seek(0)
    reader = csv.DictReader(f)
    for row in reader:
        # try to be robust to header spaces
        fis = None
        if fis_key and row.get(fis_key) is not None:
            fis = str(row.get(fis_key)).strip()
        else:
            # try likely alternatives
            for k in row:
                if k and "fis" in k.lower() and "code" in k.lower():
                    fis = str(row[k]).strip()
                    break
        if not fis:
            continue
        name = (row.get(name_key) or "").strip() if name_key else ""
        birth = (row.get(birth_key) or "").strip() if birth_key else ""
        gender = (row.get(gender_key) or "").strip() if gender_key else ""
        # normalize gender to "M" or "F"
        g = None
        if gender:
            if gender.lower().startswith("m"):
                g = "M"
            elif gender.lower().startswith("f"):
                g = "W"
            else:
                g = "M" if gender.lower() == "male" else ("W" if gender.lower()=="female" else gender.upper())
        athletes[fis] = {
            "Name": name,
            "Birth Year": (int(birth) if birth and birth.isdigit() else None),
            "Gender": g
        }

print(f"Loaded {len(athletes)} athletes from master list.")

# ---------- Build olympic top-5 sets ----------
# For cycles 1 and 2 we need to know which FIS codes made top5
top5_by_cycle_gender = defaultdict(lambda: set())  # key: (cycle_str, 'M' or 'W') -> set of fis codes

oly_dir = os.path.join(ROOT, OLYMPIC_FOLDER)
if os.path.isdir(oly_dir):
    for fname in os.listdir(oly_dir):
        if not fname.endswith(".csv"):
            continue
        path = os.path.join(oly_dir, fname)
        # determine cycle & gender from filename like M_2018_1.csv or W_2022_2.csv
        base = os.path.splitext(fname)[0]
        parts = base.split("_")
        # try to infer cycle suffix: last part should be cycle number (1/2/3)
        cycle = None
        gender_flag = None
        if len(parts) >= 3:
            # parts like ["M","2018","1"]
            gender_flag = parts[0].upper()
            cycle = parts[-1]
        else:
            # fallback: check startswith
            if base.startswith("M_"):
                gender_flag = "M"
            elif base.startswith("W_"):
                gender_flag = "W"
            # try to find '2018' or '2022' and map to cycle
            if "2018" in base:
                cycle = "1"
            elif "2022" in base:
                cycle = "2"
            elif "2026" in base:
                cycle = "3"
        if cycle is None or gender_flag is None:
            # try parse more smartly
            continue

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # normalize headers
            headers = normalize_fieldnames(reader.fieldnames)
            # find rank and fis columns
            rank_key = None
            fis_key = None
            for raw in reader.fieldnames:
                rs = raw.strip().lower()
                if rs == "rank" or "rank" in rs:
                    rank_key = raw
                if "fis" in rs and "code" in rs:
                    fis_key = raw
            if not fis_key:
                # try any numeric code-like column name
                for raw in reader.fieldnames:
                    if raw.strip().lower().startswith("code"):
                        fis_key = raw
            # iterate rows
            for row in reader:
                rank_val = row.get(rank_key) if rank_key else None
                fis_val = None
                if fis_key and row.get(fis_key):
                    fis_val = str(row.get(fis_key)).strip()
                # sometimes FIS is in Name column parentheses, skip for now
                try:
                    rank_int = int(str(rank_val).strip())
                except:
                    rank_int = None
                if rank_int is not None and 1 <= rank_int <= 5 and fis_val:
                    top5_by_cycle_gender[(cycle, gender_flag)].add(fis_val)
else:
    print("No olympic_results folder found; MadeTop5 will not be set.")

# ---------- Traverse all gender folders and collect stats ----------
# We'll create for each athlete a dictionary per cycle to store lists
# structure: athlete_cycle_data[fis][cycle] = { 'final': [...], 'turn': [...], ... }
athlete_cycle_data = defaultdict(lambda: defaultdict(lambda: {
    "final": [], "turn": [], "air": [], "time": [], "rank": []
}))

for entry in os.listdir(ROOT):
    folder_path = os.path.join(ROOT, entry)
    if not os.path.isdir(folder_path):
        continue
    # skip olympic_results folder and any non M_/W_ folders
    if entry == OLYMPIC_FOLDER:
        continue
    if not (entry.startswith("M_") or entry.startswith("W_")):
        continue

    # extract cycle suffix (assume name like M_2015_1)
    parts = entry.split("_")
    cycle_suffix = parts[-1] if len(parts) >= 2 else None
    if cycle_suffix not in ("1","2","3"):
        # skip unexpected
        continue

    gender_flag = "M" if entry.startswith("M_") else "W"

    # iterate csv files in this folder
    for fname in os.listdir(folder_path):
        if not fname.endswith(".csv"):
            continue
        csv_path = os.path.join(folder_path, fname)
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                continue
            # build a keymap from logical field -> actual header name
            keymap = find_header_key_map(reader.fieldnames)
            # fallback if missing keys: use stripped matching
            # We'll read rows up to LIMIT_ROWS_PER_FILE if set
            row_count = 0
            for row in reader:
                if LIMIT_ROWS_PER_FILE and row_count >= LIMIT_ROWS_PER_FILE:
                    break
                row_count += 1

                # get FIS code
                fis_val = None
                for candidate in EXPECTED_FIELDS["fisc"]:
                    v = None
                    if candidate in row:
                        v = row.get(candidate)
                    else:
                        # try stripped keys
                        for k in row:
                            if k and k.strip() == candidate.strip():
                                v = row.get(k)
                                break
                    if v:
                        fis_val = str(v).strip()
                        break
                # if not found via candidates, try any column that looks like a FIS code
                if not fis_val:
                    for k in row:
                        if k and "fis" in k.lower() and "code" in k.lower():
                            if row.get(k):
                                fis_val = str(row.get(k)).strip()
                                break

                if not fis_val:
                    # skip rows without FIS code
                    continue

                # only process if this athlete exists in our master athletes list
                if fis_val not in athletes:
                    # skip unknown FIS codes (or you could still include)
                    continue

                # collect numeric fields (use keymap if present)
                def fetch_field(logical):
                    # try keymap first
                    if logical in keymap:
                        val = row.get(keymap[logical])
                        return safe_float(val)
                    # otherwise try candidate names
                    for cand in EXPECTED_FIELDS[logical]:
                        # try raw key
                        if cand in row:
                            val = row.get(cand)
                            v = safe_float(val)
                            if v is not None:
                                return v
                        # try strip-match
                        for k in row:
                            if k and k.strip() == cand.strip():
                                v = safe_float(row.get(k))
                                if v is not None:
                                    return v
                    return None

                final_v = fetch_field("final")
                turn_v = fetch_field("turn")
                air_v = fetch_field("air")
                time_v = fetch_field("time")
                rank_v = fetch_field("rank")

                # store values
                data_bucket = athlete_cycle_data[fis_val][cycle_suffix]
                if final_v is not None:
                    data_bucket["final"].append(final_v)
                if turn_v is not None:
                    data_bucket["turn"].append(turn_v)
                if air_v is not None:
                    data_bucket["air"].append(air_v)
                if time_v is not None:
                    data_bucket["time"].append(time_v)
                if rank_v is not None:
                    # rank stored as numeric if possible
                    try:
                        data_bucket["rank"].append(int(rank_v))
                    except:
                        try:
                            data_bucket["rank"].append(int(float(rank_v)))
                        except:
                            pass

print("Finished scanning world-cup CSVs.")

# ---------- Build output rows ----------
train_rows = []
test_rows = []

for fis, info in athletes.items():
    name = info.get("Name", "")
    birth_year = info.get("Birth Year")
    gender_flag = info.get("Gender")  # "M" or "W" or None

    # Determine which folders to look in based on gender
    if gender_flag == "M":
        folder_prefix = "M_"
    elif gender_flag == "W":
        folder_prefix = "W_"
    else:
        # if unknown, skip athlete
        continue

    # for cycles 1,2,3 build a row if there is any data for that athlete/cycle
    for cycle in ("1","2","3"):
        bucket = athlete_cycle_data.get(fis, {}).get(cycle, {})
        # if no data at all, we may still include a row (with Nones) or skip; we'll include but with None fields
        final_list = bucket.get("final", [])
        turn_list = bucket.get("turn", [])
        air_list = bucket.get("air", [])
        time_list = bucket.get("time", [])
        rank_list = bucket.get("rank", [])

        # if nothing at all for this cycle, skip creating a row
        if not (final_list or turn_list or air_list or time_list or rank_list):
            continue

        # compute stats
        avg_final = compute_avg(final_list)
        sd_final = compute_std(final_list)
        avg_turn = compute_avg(turn_list)
        avg_air = compute_avg(air_list)
        avg_time = compute_avg(time_list)
        avg_rank = compute_avg(rank_list)

        # compute age by olympic year
        year = CYCLE_YEAR[cycle]
        age = None
        if birth_year:
            try:
                age = int(year) - int(birth_year)
            except:
                age = None

        # nation: try to find from one of the WC files (we didn't store nation per fis earlier)
        # We'll attempt to find a nation by searching one of the WC files quickly:
        nation = None
        # search through world cup folders of this cycle for the athlete and pick nation if present
        for folder_entry in os.listdir(ROOT):
            if not (folder_entry.startswith(folder_prefix) and folder_entry.endswith("_" + cycle)):
                continue
            folder_path = os.path.join(ROOT, folder_entry)
            for fname in os.listdir(folder_path):
                if not fname.endswith(".csv"):
                    continue
                with open(os.path.join(folder_path, fname), newline="", encoding="utf-8") as f:
                    r = csv.DictReader(f)
                    # find the nation column name
                    headers = r.fieldnames or []
                    headers_norm = normalize_fieldnames(headers)
                    nation_key = None
                    for raw in headers:
                        if raw.strip().lower() in ("nation","country"):
                            nation_key = raw
                            break
                    for row in r:
                        # try to find the fis in this file
                        # robust fetch
                        fis_candidate = None
                        for k in row:
                            if k and "fis" in k.lower() and "code" in k.lower():
                                fis_candidate = row.get(k)
                                break
                        if fis_candidate and str(fis_candidate).strip() == fis:
                            nation = (row.get(nation_key) or "").strip() if nation_key else None
                            break
                if nation:
                    break
            if nation:
                break

        olympic_year_label = cycle  # 1,2,3
        row = {
            "FIS Code": fis,
            "Name": name,
            "Age": age,
            "Nation": nation,
            "Avg_Final_Score": avg_final,
            "Avg_Turn_Points": avg_turn,
            "Avg_Air_Points": avg_air,
            "Avg_Time_Points": avg_time,
            "Avg_Rank": avg_rank,
            "Std_Final_Score": sd_final,
            "Olympic_Cycle": cycle,
            "Olympic_Year": year
        }

        if cycle in ("1","2"):
            # determine Made_Top_5 using top5_by_cycle_gender
            made_top5 = 0
            key = (cycle, gender_flag)
            if fis in top5_by_cycle_gender.get(key, set()):
                made_top5 = 1
            row["Made_Top_5"] = made_top5
            train_rows.append(row)
        else:
            test_rows.append(row)

# ---------- Write outputs ----------
train_fields = ["FIS Code","Name","Age","Nation",
                "Avg_Final_Score","Avg_Turn_Points","Avg_Air_Points","Avg_Time_Points",
                "Avg_Rank","Std_Final_Score","Olympic_Cycle","Olympic_Year","Made_Top_5"]

test_fields = ["FIS Code","Name","Age","Nation",
               "Avg_Final_Score","Avg_Turn_Points","Avg_Air_Points","Avg_Time_Points",
               "Avg_Rank","Std_Final_Score","Olympic_Cycle","Olympic_Year"]

# Write training CSV
with open(os.path.join(ROOT, TRAIN_OUT), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=train_fields)
    writer.writeheader()
    for r in train_rows:
        # ensure all fields exist
        out = {k: r.get(k) for k in train_fields}
        writer.writerow(out)

# Write testing CSV
with open(os.path.join(ROOT, TEST_OUT), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=test_fields)
    writer.writeheader()
    for r in test_rows:
        out = {k: r.get(k) for k in test_fields}
        writer.writerow(out)

print(f"Done. Wrote {len(train_rows)} training rows to {TRAIN_OUT} and {len(test_rows)} testing rows to {TEST_OUT}.")
