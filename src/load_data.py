import pandas as pd
import os
import glob
import sys

# need to access config from root
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)

from config import DATA_FOLDER, CLEANED_FOLDER, CLEANED_ATHLETE_DATA, CLEANED_OLYMPIC_RESULTS, EXAMPLE_WC_FOLDER

sys.path.remove(root)
# return to running from src

def load_athlete_bio_data():
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, DATA_FOLDER)
    cleaned_folder = os.path.join(data_directory, CLEANED_FOLDER)
    athlete_bio_data_file = os.path.join(cleaned_folder, CLEANED_ATHLETE_DATA)
    return pd.read_csv(athlete_bio_data_file)

def load_world_cup_data():
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, DATA_FOLDER)
    cleaned_folder = os.path.join(data_directory, CLEANED_FOLDER)
    world_cup_folder = os.path.join(cleaned_folder, EXAMPLE_WC_FOLDER)
    world_cup_files = glob.glob(os.path.join(world_cup_folder, "*.csv"))
    first_world_cup_csv = world_cup_files[0]
    return pd.read_csv(first_world_cup_csv)

def load_olympic_data():
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, DATA_FOLDER)
    cleaned_folder = os.path.join(data_directory, CLEANED_FOLDER)
    olympic_results_folder = os.path.join(cleaned_folder, CLEANED_OLYMPIC_RESULTS)
    olympic_results_files = glob.glob(os.path.join(olympic_results_folder, "*.csv"))
    first_olymp_results_csv = olympic_results_files[0]
    return pd.read_csv(first_olymp_results_csv)