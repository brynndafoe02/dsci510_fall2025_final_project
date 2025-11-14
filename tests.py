import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import pdfplumber
import os
from World_Cup_Results import get_WC_results
from Olympic_Results import get_olympic_results
from Athlete_Data import get_skier_data, make_athlete_data_csv

if __name__ == "__main__":
    
    print("Running tests for Final Project Progress:\n")

    #################################################################

    # WC Results
    print("Getting World Cup Results_______________")
    # Will be grouping my urls together by ski season. Testing my dictionary on 3 of them
    # Will change "Group 1" and such later to something like "2017 Season"
    pdf_urls = {"Group 1": ["https://medias1.fis-ski.com/pdf/2025/FS/8105/2025FS8105RLF.pdf"], "Group 2": ["https://medias2.fis-ski.com/pdf/2025/FS/8237/2025FS8237RLF.pdf", "https://medias4.fis-ski.com/pdf/2025/FS/8254/2025FS8254RLF.pdf"]}
    get_WC_results(pdf_urls)
    print("Done getting World Cup Results_______________\n")

    #################################################################

    # Olympic Results
    print("Getting Olympic Results_______________")
    # just testing with 2 URLs for now
    urls = ["https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/men-moguls", "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/mens-moguls"]
    get_olympic_results(urls)
    print("Done getting Olympic Results_______________\n")

    #################################################################

    # Athlete Data 
    print("Getting Athlete Data_______________")
    # need to gather my total list of athletes later, but starting and testing with four URLs first
    urls = ["https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=197224&type=career", "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=182830", "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=170101", "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=174753"]
    all_skiers = []
    for url in urls:
        skier_data = get_skier_data(url)
        all_skiers.append(skier_data)
    make_athlete_data_csv(all_skiers)
    # ^^^ this .py file was actually the first one I made out of the 3
    # so the csv ouput is a separate function,
    # but I plan on condensing it all into one function later
    print("Done getting Athlete Data_______________\n")

    #################################################################