import csv
import glob
import os

def get_fis_code():

    file_path = "cleaned/AthleteData.csv"

    fis_codes = []

    with open (file=file_path, mode="r") as f:
        csv_read = csv.DictReader(f)
    
        for row in csv_read:
            fis_code = row.get("FIS Code") or row.get(" FIS Code")
            fis_codes.append(fis_code.strip())

    unique_fis_codes = list(set(fis_codes))

    return unique_fis_codes

def pull_data_for_athlete(fis_code: str, olympic_cycle: int):
    if olympic_cycle == 1:
        olympic_year = 2018
    elif olympic_cycle == 2:
        olympic_year = 2022
    elif olympic_cycle == 3:
        olympic_year = 2026
        
    skier_dict = {
        "FIS Code": fis_code,
        "Name": None,
        "Age" : None,
        "Avg Final Score" : None,
        "Avg Turn Points" : None,
        "Avg Air Points" : None,
        "Avg Time Points" : None,
        "Avg Rank" : None,
        "SD of FS" : None,
        "Olympic Year" : str(olympic_cycle),
        "Made Top 5" : None}
    
    ##### get olympic data for athlete
    
    base_directory_or = os.path.join("cleaned", "olympic_results")
    csv_files = glob.glob(os.path.join(base_directory_or, "*.csv"))
    o_year_file = f"_{olympic_cycle}.csv"
    csv_files = [f for f in csv_files if f.endswith(o_year_file)]
    olympic_data_rows = []
    for file_path in csv_files:
        with open(file=file_path, mode="r") as f:
            csv_read = csv.DictReader(f)
            for row in csv_read:
                code = row.get("FIS Code") or row.get(" FIS Code")
                if code and code.strip() == fis_code:
                    olympic_data_rows.append(row)
    # [{'Rank': '1', ' FIS Code': ' 2484937', ' Name': ' Mikael KINGSBURY', ' Country': ' CAN'}]
    if olympic_data_rows:
        skier_dict["Name"] = olympic_data_rows[0][' Name'].strip()
        rank_at_olympics = int(olympic_data_rows[0]['Rank'].strip())
        if rank_at_olympics <= 5:
            skier_dict["Made Top 5"] = 1
        else:
            skier_dict["Made Top 5"] = 0
    else:
        skier_dict["Made Top 5"] = 0

    ##### get world cup data for athlete
        
    
    return skier_dict