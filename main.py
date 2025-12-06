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
from src.Scraping_World_Cup_Results import get_WC_results
from src.Scraping_Olympic_Results import get_olympic_results
from src.Scraping_Athlete_Data import get_skier_data, make_athlete_data_csv
from src.Input_for_LogR import get_fis_code, pull_data_for_athlete, update_train_test_files
from src.Running_Logistic_Regression import running_logr_model
from src.Create_Train_Test_Files import creating_train_test_files

if __name__ == "__main__":

    base_directory = os.path.dirname(os.path.dirname(__file__))
    
    print("Running Pipeline for Final Project:\n")
    # LINES THAT CALL MY WEB SCRAPING PROGRAMS ARE COMMENTED OUT!!!

    #################################################################

    # Scraping World Cup Results
    print("Getting World Cup Results_______________")

    # I found that some of my files are in FRL style (Final Results List)
        # example: https://medias1.fis-ski.com/pdf/2015/FS/8106/2015FS8106FRL.pdf
    # and some in RLF style (Results List Final)
        # example: https://medias1.fis-ski.com/pdf/2017/FS/8271/2017FS8271RLF.pdf
    
    # my code is only set up to parse RLF style because I did not realize there were two types, so I manually made the CSV files for the FRL style PDFs (and I did not have time to edit my original code to parse FRL style)
    
    pdf_urls_wc_FRL = {
        "M_2015_1" : ["https://medias1.fis-ski.com/pdf/2015/FS/8106/2015FS8106FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8335/2015FS8335FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8352/2015FS8352FRL.pdf", "https://medias3.fis-ski.com/pdf/2015/FS/8112/2015FS8112FRL.pdf", "https://medias4.fis-ski.com/pdf/2015/FS/8214/2015FS8214FRL.pdf"], 
        "W_2015_1" : ["https://medias2.fis-ski.com/pdf/2015/FS/8105/2015FS8105FRL.pdf", "https://medias4.fis-ski.com/pdf/2015/FS/8333/2015FS8333FRL.pdf", "https://medias2.fis-ski.com/pdf/2015/FS/8351/2015FS8351FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8111/2015FS8111FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8213/2015FS8213FRL.pdf"],
        "M_2016_1" : ["https://medias1.fis-ski.com/pdf/2016/FS/8091/2016FS8091FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8093/2016FS8093FRL.pdf", "https://medias3.fis-ski.com/pdf/2016/FS/8399/2016FS8399FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8249/2016FS8249FRL.pdf"],
        "W_2016_1" : ["https://medias2.fis-ski.com/pdf/2016/FS/8090/2016FS8090FRL.pdf", "https://medias4.fis-ski.com/pdf/2016/FS/8092/2016FS8092FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8397/2016FS8397FRL.pdf", "https://medias1.fis-ski.com/pdf/2016/FS/8248/2016FS8248FRL.pdf"]}
    # ^^^ these are the urls I manually made csv files for

    # get_WC_results() # -> scrapes the data and creates the csv files
    print("Done getting World Cup Results_______________\n")

    #################################################################

    # Scraping Olympic Results
    print("Getting Olympic Results_______________")

    urls_olympics = {
        "M_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/mens-moguls", 
        "W_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/ladies-moguls", 
        "M_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/men-moguls", 
        "W_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/women-moguls"}
    
    # get_olympic_results(urls_olympics) # -> scrapes the data and creates the csv files
    print("Done getting Olympic Results_______________\n")

    #################################################################

    # Scraping Athlete Data
    print("Getting Athlete Data_______________")
    # !!! COMMENTED all of this out because none of this is needed since results will use my cleaned files, not raw

    biography_urls = []
    
    # # making a list of the Athlete Biography URLs from the csv file holding them
    # data_directory = os.path.join("data")
    
    # athlete_urls_file_path = os.path.join(data_directory, "Athlete_URLs.csv")
    # with open(file=athlete_urls_file_path, mode="r") as f:
    #     next(f)
    #     for url in f:
    #         biography_urls.append(url.strip())
    
    # all_mogul_skiers = []
    # j = 0
    # # scraping the data
    # print("Expecting 369 Skiers:")
    # for url in biography_urls:
    #     skier_data = get_skier_data(url, j)
    #     all_mogul_skiers.append(skier_data)
    #     j+=1

    # # creating the csv files
    # make_athlete_data_csv(all_mogul_skiers)
    
    print("Done getting Athlete Data_______________\n")

    #################################################################

    # Creating the Training and Testing Files
    # !!! This uses the CLEANED data from the cleaned folder inside data, so this does not use any of the raw data files !!!
    
    print("Creating the Training and Testing Files for the Logistic Regression Model_______________")

    # creating all the training / testing files with the column names
    creating_train_test_files()

    # getting a list of all the FIS Codes (the reliable identifiers, compared to names which I noticed on some score sheets are spelled differently sometimes)
    fis_list = get_fis_code()
    
    training_data = []
    testing_data = []

    for fis_code in fis_list:
        ################################ splitting data pulls by Olympic cyle. 1 = 2018 (training), 2 = 2022 (training), 3 = 2026 (testing)
        
        skier_data_1 = pull_data_for_athlete(fis_code, 1)
        if skier_data_1:
            update_train_test_files(skier_data_1, 1)

        skier_data_2 = pull_data_for_athlete(fis_code, 2)
        if skier_data_2:
            update_train_test_files(skier_data_2, 2)

        skier_data_3 = pull_data_for_athlete(fis_code, 3)
        if skier_data_3:
            update_train_test_files(skier_data_3, 3)

    print("Finished creating the Training and Testing Files for the Logistic Regression Model_______________\n")
    
    #################################################################

    # Running the Logistic Regression Model
    print("Running the Logistic Regression Model_______________")
    
    print("Running LR for Men")
    running_logr_model("men")
    print("Running LR for Women")
    running_logr_model("women")

    print("Done running the Logistic Regression Model_______________\n")
    
    