import pandas as pd
import os
import glob
from src.load_data import load_athlete_bio_data, load_world_cup_data, load_olympic_data

if __name__ == "__main__":
    # checking if it:
        # is an appropriate data structure 
        # is not empty
        # has the columns specified and needed for the logistic regression model
    
    athlete_bio_df = load_athlete_bio_data()
    if not isinstance(athlete_bio_df, pd.DataFrame):
        raise TypeError("File is not a DataFrame.")
    if athlete_bio_df.empty:
        raise ValueError("File is empty.")
    expected_columns = {"Name", " FIS Code", " Birthdate", " Birth Year", " Age", " Gender"}
    if not expected_columns.issubset(athlete_bio_df.columns):
        raise ValueError("Missing columns in file.")
    print("Successful: Athlete Data Load")

    world_cup_df = load_world_cup_data()
    if not isinstance(world_cup_df, pd.DataFrame):
        raise TypeError("File is not a DataFrame.")
    if world_cup_df.empty:
        raise ValueError("File is empty.")
    expected_columns = {"Rank", " FIS Code", " Name", " Nation", " Birth Year", " Final Score", " Time Points", " Air Points", " Turn Points"}
    if not expected_columns.issubset(world_cup_df.columns):
        raise ValueError("Missing columns in file.")
    print("Successful: World Cup Data Load")

    olympic_df = load_olympic_data()
    if not isinstance(olympic_df, pd.DataFrame):
        raise TypeError("File is not a DataFrame.")
    if olympic_df.empty:
        raise ValueError("File is empty.")
    expected_columns = {"Rank", " FIS Code", " Name", " Country"}
    if not expected_columns.issubset(olympic_df.columns):
        raise ValueError("Missing columns in file.")
    print("Successful: Olympic Data Load")