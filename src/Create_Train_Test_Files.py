import os
import csv
import sys

# need to access config from root
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)

from config import DATA_FOLDER, FINAL_TRAINING_FILE_MEN, FINAL_TESTING_FILE_MEN, FINAL_TRAINING_FILE_WOMEN, FINAL_TESTING_FILE_WOMEN

sys.path.remove(root)
# return to running from src

def creating_train_test_files():
    # just creating all the files so that they are ready
    
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, DATA_FOLDER)

    men_training_file = os.path.join(data_directory, FINAL_TRAINING_FILE_MEN)
    
    with open(file=men_training_file, mode="w") as training:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year, Made Top 5\n"
        training.write(column_names)

    men_testing_file = os.path.join(data_directory, FINAL_TESTING_FILE_MEN)
    
    with open(file=men_testing_file, mode="w") as testing:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year\n"
        testing.write(column_names)

    women_training_file = os.path.join(data_directory, FINAL_TRAINING_FILE_WOMEN)
    
    with open(file=women_training_file, mode="w") as training:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year, Made Top 5\n"
        training.write(column_names)

    women_testing_file = os.path.join(data_directory, FINAL_TESTING_FILE_WOMEN)
    
    with open(file=women_testing_file, mode="w") as testing:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year\n"
        testing.write(column_names)