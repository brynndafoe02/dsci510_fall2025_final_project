import csv
import glob
import os
import numpy as np

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
        "Nation" : None,
        "Age" : None,
        "Avg Final Score" : None,
        "Avg Turn Points" : None,
        "Avg Air Points" : None,
        "Avg Time Points" : None,
        "Avg Rank" : None,
        "SD of FS" : None,
        "Olympic Year" : str(olympic_year),
        "Made Top 5" : None}
    
    ########## get olympic data for athlete
    
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
        skier_dict["Nation"] = olympic_data_rows[0][' Country'].strip()
        rank_at_olympics = int(olympic_data_rows[0]['Rank'].strip())
        if rank_at_olympics <= 5:
            skier_dict["Made Top 5"] = 1
        else:
            skier_dict["Made Top 5"] = 0
    else:
        skier_dict["Made Top 5"] = 0

    ########## get world cup data for athlete

    base_directory_wc = "cleaned"
    folders = [f for f in glob.glob(os.path.join(base_directory_wc, "*")) if os.path.isdir(f) and f.endswith(f"_{olympic_cycle}")]
    wc_data_rows = []
    for folder in folders:
        csv_files = glob.glob(os.path.join(folder, "*.csv"))
        for file_path in csv_files:
            with open(file=file_path, mode="r") as f:
                csv_read = csv.DictReader(f)
                for row in csv_read:
                    code = row.get("FIS Code") or row.get(" FIS Code")
                    if code and code.strip() == fis_code:
                        wc_data_rows.append(row)
    # [{'Rank': '1', ' FIS Code': ' 2484937', ' Name': ' Mikael KINGSBURY', ' Nation': ' CAN', ' Birth Year': ' 1992', ' Final Score': ' 90.25', ' Time Points': ' 16.18', ' Air Points': ' 17.67', ' Turn Points': ' 56.4'}, 
    # {'Rank': '1', ' FIS Code': ' 2484937', ' Name': ' Mikael KINGSBURY', ' Nation': ' CAN', ' Birth Year': ' 1992', ' Final Score': ' 88.31', ' Time Points': ' 17.39', ' Air Points': ' 16.22', ' Turn Points': ' 54.7'},
    # etc...
    
    # Rank, FIS Code, Name, Nation, Birth Year, Final Score, Time Points, Air Points, Turn Points

    rank_list = []
    final_scores_list = []
    time_points_list = []
    air_points_list = []
    turn_points_list = []
    
    if wc_data_rows:
        if skier_dict.get("Name") is None:
            skier_dict["Name"] = wc_data_rows[0][' Name'].strip()
        if skier_dict.get("Nation") is None:
            skier_dict["Nation"] = wc_data_rows[0][' Nation'].strip()
        birth_year = wc_data_rows[0][' Birth Year'].strip()
        age = olympic_year - int(birth_year)
        skier_dict["Age"] = age

        i = 0
        while i < len(wc_data_rows):
            rank = wc_data_rows[i]['Rank'].strip()
            rank_list.append(int(rank))
            
            final_score = wc_data_rows[i][' Final Score'].strip()
            final_scores_list.append(float(final_score))

            time_points = wc_data_rows[i][' Time Points'].strip()
            time_points_list.append(float(time_points))

            air_points = wc_data_rows[i][' Air Points'].strip()
            air_points_list.append(float(air_points))

            turn_points = wc_data_rows[i][' Turn Points'].strip()
            turn_points_list.append(float(turn_points))

            average_rank = round(np.mean(rank_list), 2)
            average_final_score = round(np.mean(final_scores_list), 2)
            average_time_points = round(np.mean(time_points_list), 2)
            average_air_points = round(np.mean(air_points_list), 2)
            average_turn_points = round(np.mean(turn_points_list), 2)
            standard_deviation_final_scores = round(np.std(final_scores_list, ddof=1), 2)
    
            skier_dict["Avg Rank"] = average_rank
            skier_dict["Avg Final Score"] = average_final_score
            skier_dict["Avg Time Points"] = average_time_points
            skier_dict["Avg Air Points"] = average_air_points
            skier_dict["Avg Turn Points"] = average_turn_points
            skier_dict["SD of FS"] = standard_deviation_final_scores
            i+=1
    else:
        return None
    
    return skier_dict
# numpy -> data = []
    # avg = np.mean(data)
    # std = np.std(data, ddof=1) -> SAMPLE, not POP