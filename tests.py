import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import pdfplumber
import os
import glob
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.World_Cup_Results import get_WC_results
from src.Olympic_Results import get_olympic_results
from src.Athlete_Data import get_skier_data, make_athlete_data_csv
from src.Input_LogR import get_fis_code, pull_data_for_athlete
from src.Logistic_Regression import running_logr_model

if __name__ == "__main__":
    
    print("Running tests for Final Project Progress:\n")

    #################################################################

    # Scraping World Cup Results
    print("Getting World Cup Results_______________")

    #####
    # I found that some of my files are in FRL style (Final Results List)
        # example: https://medias1.fis-ski.com/pdf/2015/FS/8106/2015FS8106FRL.pdf
    # and some in RLF style (Results List Final)
        # example: https://medias1.fis-ski.com/pdf/2017/FS/8271/2017FS8271RLF.pdf
    # my code is currently only set up to parse RLF style because I did not realize there were two types, so I will be manually making the CSV files for the 18 FRL style PDFs because it is a little too late for me now to make code to parse the FRL files
    pdf_urls_wc_FRL = {
        "M_2015_1" : ["https://medias1.fis-ski.com/pdf/2015/FS/8106/2015FS8106FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8335/2015FS8335FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8352/2015FS8352FRL.pdf", "https://medias3.fis-ski.com/pdf/2015/FS/8112/2015FS8112FRL.pdf", "https://medias4.fis-ski.com/pdf/2015/FS/8214/2015FS8214FRL.pdf"], 
        "W_2015_1" : ["https://medias2.fis-ski.com/pdf/2015/FS/8105/2015FS8105FRL.pdf", "https://medias4.fis-ski.com/pdf/2015/FS/8333/2015FS8333FRL.pdf", "https://medias2.fis-ski.com/pdf/2015/FS/8351/2015FS8351FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8111/2015FS8111FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8213/2015FS8213FRL.pdf"],
        "M_2016_1" : ["https://medias1.fis-ski.com/pdf/2016/FS/8091/2016FS8091FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8093/2016FS8093FRL.pdf", "https://medias3.fis-ski.com/pdf/2016/FS/8399/2016FS8399FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8249/2016FS8249FRL.pdf"],
        "W_2016_1" : ["https://medias2.fis-ski.com/pdf/2016/FS/8090/2016FS8090FRL.pdf", "https://medias4.fis-ski.com/pdf/2016/FS/8092/2016FS8092FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8397/2016FS8397FRL.pdf", "https://medias1.fis-ski.com/pdf/2016/FS/8248/2016FS8248FRL.pdf"]}
    # ^^^ these are the urls I manually made csv files for

    get_WC_results() # scrapes the data and creates the csv files
    print("Done getting World Cup Results_______________\n")

    #################################################################

    # Scraping Olympic Results
    print("Getting Olympic Results_______________")

    #####
    urls_olympics = {
        "M_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/mens-moguls", 
        "W_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/ladies-moguls", 
        "M_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/men-moguls", 
        "W_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/women-moguls"}
    #####
    
    get_olympic_results(urls_olympics) # scrapes the data and creates the csv files
    print("Done getting Olympic Results_______________\n")


    #################################################################

    # Scraping Athlete Data
    print("Getting Athlete Data_______________")

    bio_urls = []
    # making a list of the Athlete Biography URLs from the csv file holding them
    with open(file="data/Athlete_URLs.csv", mode="r") as f:
        next(f)
        for url in f:
            bio_urls.append(url.strip())
    
    all_mogul_skiers = []
    j = 0
    # scraping the data
    print("Expecting 369 Skiers:")
    for url in bio_urls:
        skier_data = get_skier_data(url, j)
        all_mogul_skiers.append(skier_data)
        j+=1

    # creating the csv files
    make_athlete_data_csv(all_mogul_skiers)
    
    print("Done getting Athlete Data_______________\n")

    #################################################################

    # Creating the Training and Testing Files
    print("Creating the Training and Testing Files for the Logistic Regression Model_______________")

    fis_list = get_fis_code() # getting a list of all the FIS Codes (the reliable identifiers, compared to names which I noticed on some score sheets are spelled differently sometimes)

    ##### starting all the training / testing files with the column names first 
    men_training_file_name = "data/Training_Data_Men.csv"
    with open(file=men_training_file_name, mode="w") as training:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year, Made Top 5\n"
        training.write(column_names)
    
    men_testing_file_name = "data/Testing_Data_Men.csv"
    with open(file=men_testing_file_name, mode="w") as testing:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year\n"
        testing.write(column_names)

    women_training_file_name = "data/Training_Data_Women.csv"
    with open(file=women_training_file_name, mode="w") as training:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year, Made Top 5\n"
        training.write(column_names)
    
    women_testing_file_name = "data/Testing_Data_Women.csv"
    with open(file=women_testing_file_name, mode="w") as testing:
        column_names = "FIS Code, Name, Nation, Age, Gender, Avg Final Score, Avg Turn Points, Avg Air Points, Avg Time Points, Avg Rank, Standard Deviation FS, Olympic Year\n"
        testing.write(column_names)

    training_data = []
    testing_data = []

    for fis_code in fis_list:
        ################################ splitting data pulls by Olympic cyle. 1 = 2018 (training), 2 = 2022 (training), 3 = 2026 (testing)
        skier_data_1 = pull_data_for_athlete(fis_code, 1)
        if skier_data_1:

            # I need to split this up by gender, but if there is no gender it means the row is most likely not one I want to use so skip
            if skier_data_1["Gender"] == None:
                continue

            # creating the new line for the csv file 
            sd1_line = f"{skier_data_1["FIS Code"]}, {skier_data_1["Name"]}, {skier_data_1["Nation"]}, {skier_data_1["Age"]}, {skier_data_1["Gender"]}, {skier_data_1["Avg Final Score"]}, {skier_data_1["Avg Turn Points"]}, {skier_data_1["Avg Air Points"]}, {skier_data_1["Avg Time Points"]}, {skier_data_1["Avg Rank"]}, {skier_data_1["SD of FS"]}, {skier_data_1["Olympic Year"]}, {skier_data_1["Made Top 5"]}\n"

            # putting each line into the proper csv file
            if skier_data_1["Gender"] == "Male":
                with open(file=men_training_file_name, mode="a") as training:
                    if sd1_line != None:
                        training.write(sd1_line)
            else:
                with open(file=women_training_file_name, mode="a") as training:
                    if sd1_line != None:
                        training.write(sd1_line)
        elif skier_data_1 == None:
            sd1_line = None
        ################################
        skier_data_2 = pull_data_for_athlete(fis_code, 2)
        if skier_data_2:

            if skier_data_2["Gender"] == None:
                continue
            
            sd2_line = f"{skier_data_2["FIS Code"]}, {skier_data_2["Name"]}, {skier_data_2["Nation"]}, {skier_data_2["Age"]}, {skier_data_2["Gender"]}, {skier_data_2["Avg Final Score"]}, {skier_data_2["Avg Turn Points"]}, {skier_data_2["Avg Air Points"]}, {skier_data_2["Avg Time Points"]}, {skier_data_2["Avg Rank"]}, {skier_data_2["SD of FS"]}, {skier_data_2["Olympic Year"]}, {skier_data_2["Made Top 5"]}\n"

            if skier_data_2["Gender"] == "Male":
                with open(file=men_training_file_name, mode="a") as training:
                    if sd2_line != None:
                        training.write(sd2_line)
            else:
                with open(file=women_training_file_name, mode="a") as training:
                    if sd2_line != None:
                        training.write(sd2_line)
        elif skier_data_2 == None:
            sd2_line = None
        ################################
        skier_data_3 = pull_data_for_athlete(fis_code, 3)
        if skier_data_3:

            if skier_data_3["Gender"] == None:
                continue
            
            sd3_line = f"{skier_data_3["FIS Code"]}, {skier_data_3["Name"]}, {skier_data_3["Nation"]}, {skier_data_3["Age"]}, {skier_data_3["Gender"]}, {skier_data_3["Avg Final Score"]}, {skier_data_3["Avg Turn Points"]}, {skier_data_3["Avg Air Points"]}, {skier_data_3["Avg Time Points"]}, {skier_data_3["Avg Rank"]}, {skier_data_3["SD of FS"]}, {skier_data_3["Olympic Year"]}\n"
            if skier_data_3["Gender"] == "Male":
                with open(file=men_testing_file_name, mode="a") as training:
                    if sd3_line != None:
                        training.write(sd3_line)
            else:
                with open(file=women_testing_file_name, mode="a") as training:
                    if sd3_line != None:
                        training.write(sd3_line)
        elif skier_data_3 == None:
            sd3_line = None

    print("Finished creating the Training and Testing Files for the Logistic Regression Model_______________\n")
    
    #################################################################

    # Running the Logistic Regression Model
    print("Running the Logistic Regression Model_______________")

    men_training_file_name = "../data/Training_Data_Men.csv"
    men_testing_file_name = "../data/Testing_Data_Men.csv"
    women_training_file_name = "../data/Training_Data_Women.csv"
    women_testing_file_name = "../data/Testing_Data_Women.csv"
    
    mens_LR_model = "../data/Mens_Testing_Data_Ranked.csv"
    womens_LR_model = "../data/Womens_Testing_Data_Ranked.csv"
    mens_coefficients_file = "../data/Mens_Coefficients.csv"
    womens_coefficients_file = "../data/Womens_Coefficients.csv"
    
    print("Running LR for Men")
    running_logr_model(men_training_file_name, men_testing_file_name, mens_LR_model, mens_coefficients_file)
    print("Running LR for Women")
    running_logr_model(women_training_file_name, women_testing_file_name, womens_LR_model, womens_coefficients_file)

    print("Done running the Logistic Regression Model_______________\n")
    
    