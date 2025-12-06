import pandas as pd
import os
import glob

def load_athlete_bio_data():
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")
    cleaned_folder = os.path.join(data_directory, "cleaned")
    athlete_bio_data_file = os.path.join(cleaned_folder, "AthleteData.csv")
    return pd.read_csv(athlete_bio_data_file)

def load_world_cup_data():
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")
    cleaned_folder = os.path.join(data_directory, "cleaned")
    world_cup_folder = os.path.join(cleaned_folder, "M_2020_2")
    world_cup_files = glob.glob(os.path.join(world_cup_folder, "*.csv"))
    first_world_cup_csv = world_cup_files[0]
    return pd.read_csv(first_world_cup_csv)

def load_olympic_data():
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")
    cleaned_folder = os.path.join(data_directory, "cleaned")
    olympic_results_folder = os.path.join(cleaned_folder, "olympic_results")
    olympic_results_files = glob.glob(os.path.join(olympic_results_folder, "*.csv"))
    first_olymp_results_csv = olympic_results_files[0]
    return pd.read_csv(first_olymp_results_csv)