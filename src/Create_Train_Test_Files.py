import os
import csv

def creating_train_test_files():
    # just creating all the files so that they are ready
    
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")

    men_training_file_name = "Training_Data_Men.csv"
    men_training_file = os.path.join(data_directory, men_training_file_name)
    
    with open(file=men_training_file, mode="w") as training:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year, Made Top 5\n"
        training.write(column_names)

    men_testing_file_name = "Testing_Data_Men.csv"
    men_testing_file = os.path.join(data_directory, men_testing_file_name)
    
    with open(file=men_testing_file, mode="w") as testing:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year\n"
        testing.write(column_names)

    women_training_file_name = "Training_Data_Women.csv"
    women_training_file = os.path.join(data_directory, women_training_file_name)
    
    with open(file=women_training_file, mode="w") as training:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year, Made Top 5\n"
        training.write(column_names)

    women_testing_file_name = "Testing_Data_Women.csv"
    women_testing_file = os.path.join(data_directory, women_testing_file_name)
    
    with open(file=women_testing_file, mode="w") as testing:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year\n"
        testing.write(column_names)