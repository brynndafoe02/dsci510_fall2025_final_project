import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import pdfplumber
import os
import glob
import numpy as np
from World_Cup_Results import get_WC_results
from Olympic_Results import get_olympic_results
from Athlete_Data import get_skier_data, make_athlete_data_csv
from Getting_Athlete_Names import getting_athlete_names
from Athlete_URLs import return_athlete_urls
from Getting_WC_URLs import return_wc_urls
from Input_LogR import get_fis_code, pull_data_for_athlete

if __name__ == "__main__":
    
    print("Running tests for Final Project Progress:\n")

    #################################################################

    # WC Results
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
    
    pdf_urls_wc_RLF = return_wc_urls()
    #####
    
    #get_WC_results(pdf_urls_wc_RLF)
    print("Done getting World Cup Results_______________\n")

    #################################################################

    # Olympic Results
    print("Getting Olympic Results_______________")

    #####
    urls_olympics = {
        "M_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/mens-moguls", 
        "W_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/ladies-moguls", 
        "M_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/men-moguls", 
        "W_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/women-moguls"}
    #####
    
    #get_olympic_results(urls_olympics)
    print("Done getting Olympic Results_______________\n")

    #################################################################

    # Athlete Data -> TEST
    print("Getting Athlete Data_______________")
    # need to gather my total list of athletes later, but starting and testing with four URLs first
    urls = ["https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=197224&type=career", "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=182830", "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=170101", "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=174753"]
    # all_skiers = []
    # i = 0
    # for url in urls:
    #     skier_data = get_skier_data(url, i)
    #     all_skiers.append(skier_data)
    #     i+=1
    #make_athlete_data_csv(all_skiers)
    # ^^^ this .py file was actually the first one I made out of the 3
    # so the csv ouput is a separate function,
    # but I plan on condensing it all into one function later
    print("Done getting Athlete Data_______________\n")

    #################################################################

    # Getting top 30 names from all CSV files with no repeats
    # Need to give Athlete Data all the URLs
    print("Getting Athlete NAMES_______________")
    #getting_athlete_names()
    print("Done getting Athlete NAMES_______________\n")

    #################################################################

    # Athlete Data -> REAL
    print("Getting Athlete Data_______________")
    # need to gather my total list of athletes later, but starting and testing with four URLs first
    # urls = return_athlete_urls()
    # all_mogul_skiers = []
    # j = 0
    # for url in urls:
    #     skier_data = get_skier_data(url, j)
    #     all_mogul_skiers.append(skier_data)
    #     j+=1
    # make_athlete_data_csv(all_mogul_skiers)
    # ^^^ this .py file was actually the first one I made out of the 3
    # so the csv ouput is a separate function,
    # but I plan on condensing it all into one function later
    print("Done getting Athlete Data_______________\n")

    #################################################################

    fis_list = get_fis_code()

    skier_data = pull_data_for_athlete("2484937", 1)
    for key, value in skier_data.items():
        print(f"{key} : {value}")
    #print(skier_data)
    
    
    