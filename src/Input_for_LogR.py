import csv
import glob
import os
import numpy as np

def get_fis_code():

    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")
    cleaned_folder = os.path.join(data_directory, "cleaned")

    file_path = os.path.join(cleaned_folder, "AthleteData.csv")

    fis_codes = []

    with open (file=file_path, mode="r") as f:
        csv_read = csv.DictReader(f) # read file as dictionary
    
        for row in csv_read:
            fis_code = row.get("FIS Code") or row.get(" FIS Code")
            fis_codes.append(fis_code.strip())

    # in collecting the urls I am pretty sure I repeated some by accident
    # so turning into set back to list removes all the duplicates
    unique_fis_codes = list(set(fis_codes))

    return unique_fis_codes

def pull_data_for_athlete(fis_code: str, olympic_cycle: int):
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")
    cleaned_folder = os.path.join(data_directory, "cleaned")
    
    if olympic_cycle == 1:
        olympic_year = 2018
    elif olympic_cycle == 2:
        olympic_year = 2022
    elif olympic_cycle == 3:
        olympic_year = 2026

    # setting with defaults in case of missing data
    skier_dict = {
        "FIS Code": fis_code,
        "Name": None,
        "Nation" : None,
        "Age" : None,
        "Gender" : None,
        "Avg Final Score" : None,
        "Avg Turn Points" : None,
        "Avg Air Points" : None,
        "Avg Time Points" : None,
        "Avg Rank" : None,
        "SD of FS" : None,
        "Olympic Year" : str(olympic_year),
        "Made Top 5" : None}
    
    ########## get gender of athlete

    athlete_data_file_path = os.path.join(cleaned_folder, "AthleteData.csv")
    with open(file=athlete_data_file_path, mode="r") as f:
        csv_read = csv.DictReader(f)
        for row in csv_read:
            code = row.get("FIS Code") or row.get(" FIS Code")
            gender = row.get("Gender") or row.get(" Gender")
            if code:
                if code.strip() == str(fis_code):
                    gender = gender.strip()
                    skier_dict["Gender"] = gender
    
    ########## get olympic data for athlete
    
    olympic_results_folder_path = os.path.join(cleaned_folder, "olympic_results")
    
    csv_files_paths = glob.glob(os.path.join(olympic_results_folder_path, "*.csv"))
    o_year_file = f"_{olympic_cycle}.csv"
    csv_files = [f for f in csv_files_paths if f.endswith(o_year_file)]
    # gather ALL csv files from olympic results folder
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
    
    all_items_in_cleaned = glob.glob(os.path.join(cleaned_folder, "*"))
    all_folders_in_cleaned = [f for f in all_items_in_cleaned if os.path.isdir(f)]
    wc_folder_names = f"_{olympic_cycle}"
    wc_folders = [f for f in all_folders_in_cleaned if f.endswith(wc_folder_names)]

    wc_data_rows = []
    for folder in wc_folders:
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
            nation = wc_data_rows[0][' Nation'].strip()
            if nation == "ROC": # some files list Russia as ROC and some as RUS, so standardizing
                nation = "RUS"
            skier_dict["Nation"] = nation
        birth_year = wc_data_rows[0][' Birth Year'].strip()
        age = olympic_year - int(birth_year)
        skier_dict["Age"] = age

        i = 0
        while i < len(wc_data_rows):
            rank = wc_data_rows[i]['Rank']
            if rank:
                rank_list.append(int(rank.strip()))
            else:
                return None
            
            final_score = wc_data_rows[i][' Final Score']
            if final_score:
                final_scores_list.append(float(final_score.strip()))
            else:
                return None

            time_points = wc_data_rows[i][' Time Points']
            if time_points:
                time_points_list.append(float(time_points.strip()))
            else:
                return None

            air_points = wc_data_rows[i][' Air Points']
            if air_points:
                air_points_list.append(float(air_points.strip()))
            else: 
                return None

            turn_points = wc_data_rows[i][' Turn Points']
            if turn_points:
                turn_points_list.append(float(turn_points.strip()))
            else:
                return None

            average_rank = round(np.mean(rank_list), 2)
            average_final_score = round(np.mean(final_scores_list), 2)
            average_time_points = round(np.mean(time_points_list), 2)
            average_air_points = round(np.mean(air_points_list), 2)
            average_turn_points = round(np.mean(turn_points_list), 2)
            standard_deviation_final_scores = round(np.std(final_scores_list, ddof=1), 2)
            # std = np.std(data, ddof=1) -> SAMPLE, not POP
    
            skier_dict["Avg Rank"] = average_rank
            skier_dict["Avg Final Score"] = average_final_score
            skier_dict["Avg Time Points"] = average_time_points
            skier_dict["Avg Air Points"] = average_air_points
            skier_dict["Avg Turn Points"] = average_turn_points
            skier_dict["SD of FS"] = standard_deviation_final_scores
            i+=1
    else:
        return None

    if olympic_cycle == 3:
        del skier_dict["Made Top 5"]
    
    return skier_dict

def update_train_test_files(skier_data, season: int):

    # I need to split this up by gender, but if there is no gender it means the row is most likely not one I want to use so skip
    if skier_data["Gender"] == None:
        return

    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")

    # seasons 1 and 2 are for training the model, and season 3 is what I want to predict on
    # 1 = 2018, 2 = 2022, 3 = 2026
    if (season == 1) or (season == 2):
        men_file = os.path.join(data_directory, "Training_Data_Men.csv")
        women_file = os.path.join(data_directory, "Training_Data_Women.csv")
    elif season == 3:
        men_file = os.path.join(data_directory, "Testing_Data_Men.csv")
        women_file = os.path.join(data_directory, "Testing_Data_Women.csv")

    # creating the new line for the csv file 
    # season 3 will not have the "Made Top 5" column
    if (season == 1) or (season == 2):
        skier_data_line = f"{skier_data["FIS Code"]}, {skier_data["Name"]}, {skier_data["Nation"]}, {skier_data["Age"]}, {skier_data["Gender"]}, {skier_data["Avg Final Score"]}, {skier_data["Avg Turn Points"]}, {skier_data["Avg Air Points"]}, {skier_data["Avg Time Points"]}, {skier_data["Avg Rank"]}, {skier_data["SD of FS"]}, {skier_data["Olympic Year"]}, {skier_data["Made Top 5"]}\n"
    elif season == 3:
        skier_data_line = f"{skier_data["FIS Code"]}, {skier_data["Name"]}, {skier_data["Nation"]}, {skier_data["Age"]}, {skier_data["Gender"]}, {skier_data["Avg Final Score"]}, {skier_data["Avg Turn Points"]}, {skier_data["Avg Air Points"]}, {skier_data["Avg Time Points"]}, {skier_data["Avg Rank"]}, {skier_data["SD of FS"]}, {skier_data["Olympic Year"]}\n"

    # putting each line into the proper csv file
    if skier_data["Gender"] == "Male":
        with open(file=men_file, mode="a") as training:
            if skier_data_line != None:
                training.write(skier_data_line)
    else:
        with open(file=women_file, mode="a") as training:
            if skier_data_line != None:
                training.write(skier_data_line)
