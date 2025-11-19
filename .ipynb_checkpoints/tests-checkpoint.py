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
    pdf_urls1 = {"Group 1": ["https://medias1.fis-ski.com/pdf/2025/FS/8105/2025FS8105RLF.pdf"], "Group 2": ["https://medias2.fis-ski.com/pdf/2025/FS/8237/2025FS8237RLF.pdf", "https://medias4.fis-ski.com/pdf/2025/FS/8254/2025FS8254RLF.pdf"]}

    #####
    pdf_urls_wc = {
        "M_2015_1" : ["https://medias1.fis-ski.com/pdf/2015/FS/8106/2015FS8106FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8335/2015FS8335FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8352/2015FS8352FRL.pdf", "https://medias3.fis-ski.com/pdf/2015/FS/8112/2015FS8112FRL.pdf", "https://medias4.fis-ski.com/pdf/2015/FS/8214/2015FS8214FRL.pdf"], 
        "W_2015_1" : ["https://medias2.fis-ski.com/pdf/2015/FS/8105/2015FS8105FRL.pdf", "https://medias4.fis-ski.com/pdf/2015/FS/8333/2015FS8333FRL.pdf", "https://medias2.fis-ski.com/pdf/2015/FS/8351/2015FS8351FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8111/2015FS8111FRL.pdf", "https://medias1.fis-ski.com/pdf/2015/FS/8213/2015FS8213FRL.pdf"],
        "M_2016_1" : ["https://medias1.fis-ski.com/pdf/2016/FS/8091/2016FS8091FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8093/2016FS8093FRL.pdf", "https://medias3.fis-ski.com/pdf/2016/FS/8399/2016FS8399FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8249/2016FS8249FRL.pdf"],
        "W_2016_1" : ["https://medias2.fis-ski.com/pdf/2016/FS/8090/2016FS8090FRL.pdf", "https://medias4.fis-ski.com/pdf/2016/FS/8092/2016FS8092FRL.pdf", "https://medias2.fis-ski.com/pdf/2016/FS/8397/2016FS8397FRL.pdf", "https://medias1.fis-ski.com/pdf/2016/FS/8248/2016FS8248FRL.pdf"],
        "M_2017_1" : ["https://medias4.fis-ski.com/pdf/2017/FS/8272/2017FS8272RLF.pdf", "https://medias3.fis-ski.com/pdf/2017/FS/8464/2017FS8464RLF.pdf", "https://medias2.fis-ski.com/pdf/2017/FS/8203/2017FS8203RLF.pdf", "https://medias2.fis-ski.com/pdf/2017/FS/8205/2017FS8205RLF.pdf", "https://medias2.fis-ski.com/pdf/2017/FS/8480/2017FS8480RLF.pdf", "https://medias4.fis-ski.com/pdf/2017/FS/8405/2017FS8405RLF.pdf", "https://medias4.fis-ski.com/pdf/2017/FS/8360/2017FS8360RLF.pdf", "https://medias4.fis-ski.com/pdf/2017/FS/8253/2017FS8253RLF.pdf"],
        "W_2017_1" : ["https://medias1.fis-ski.com/pdf/2017/FS/8271/2017FS8271RLF.pdf", "https://medias1.fis-ski.com/pdf/2017/FS/8463/2017FS8463RLF.pdf", "https://medias1.fis-ski.com/pdf/2017/FS/8202/2017FS8202RLF.pdf", "https://medias3.fis-ski.com/pdf/2017/FS/8204/2017FS8204RLF.pdf", "https://medias3.fis-ski.com/pdf/2017/FS/8479/2017FS8479RLF.pdf", "https://medias1.fis-ski.com/pdf/2017/FS/8404/2017FS8404RLF.pdf", "https://medias4.fis-ski.com/pdf/2017/FS/8359/2017FS8359RLF.pdf", "https://medias2.fis-ski.com/pdf/2017/FS/8252/2017FS8252RLF.pdf"],
        "M_2018_1" : ["https://medias2.fis-ski.com/pdf/2018/FS/8148/2018FS8148RLF.pdf", "https://medias1.fis-ski.com/pdf/2018/FS/8138/2018FS8138RLF.pdf", "https://medias2.fis-ski.com/pdf/2018/FS/8114/2018FS8114RLF.pdf", "https://medias4.fis-ski.com/pdf/2018/FS/8281/2018FS8281RLF.pdf", "https://medias2.fis-ski.com/pdf/2018/FS/8120/2018FS8120RLF.pdf"],
        "W_2018_1" : ["https://medias4.fis-ski.com/pdf/2018/FS/8147/2018FS8147RLF.pdf", "https://medias4.fis-ski.com/pdf/2018/FS/8137/2018FS8137RLF.pdf", "https://medias3.fis-ski.com/pdf/2018/FS/8113/2018FS8113RLF.pdf", "https://medias1.fis-ski.com/pdf/2018/FS/8280/2018FS8280RLF.pdf", "https://medias3.fis-ski.com/pdf/2018/FS/8119/2018FS8119RLF.pdf"],
        "M_2019_2" : ["https://medias1.fis-ski.com/pdf/2019/FS/8500/2019FS8500RLF.pdf", "https://medias3.fis-ski.com/pdf/2019/FS/8474/2019FS8474RLF.pdf", "https://medias1.fis-ski.com/pdf/2019/FS/8418/2019FS8418RLF.pdf", "https://medias3.fis-ski.com/pdf/2019/FS/8316/2019FS8316RLF.pdf", "https://medias3.fis-ski.com/pdf/2019/FS/8428/2019FS8428RLF.pdf", "https://medias1.fis-ski.com/pdf/2019/FS/8090/2019FS8090RLF.pdf"],
        "W_2019_2" : ["https://medias2.fis-ski.com/pdf/2019/FS/8363/2019FS8363RLF.pdf", "https://medias4.fis-ski.com/pdf/2019/FS/8473/2019FS8473RLF.pdf", "https://medias1.fis-ski.com/pdf/2019/FS/8417/2019FS8417RLF.pdf", "https://medias1.fis-ski.com/pdf/2019/FS/8315/2019FS8315RLF.pdf", "https://medias3.fis-ski.com/pdf/2019/FS/8427/2019FS8427RLF.pdf", "https://medias2.fis-ski.com/pdf/2019/FS/8089/2019FS8089RLF.pdf"],
        "M_2020_2" : ["https://medias3.fis-ski.com/pdf/2020/FS/8186/2020FS8186RLF.pdf", "https://medias4.fis-ski.com/pdf/2020/FS/8143/2020FS8143RLF.pdf", "https://medias4.fis-ski.com/pdf/2020/FS/8123/2020FS8123RLF.pdf", "https://medias2.fis-ski.com/pdf/2020/FS/8125/2020FS8125RLF.pdf", "https://medias2.fis-ski.com/pdf/2020/FS/8364/2020FS8364RLF.pdf", "https://medias4.fis-ski.com/pdf/2020/FS/8260/2020FS8260RLF.pdf"],
        "W_2020_2" : ["https://medias1.fis-ski.com/pdf/2020/FS/8185/2020FS8185RLF.pdf", "https://medias1.fis-ski.com/pdf/2020/FS/8142/2020FS8142RLF.pdf", "https://medias4.fis-ski.com/pdf/2020/FS/8122/2020FS8122RLF.pdf", "https://medias2.fis-ski.com/pdf/2020/FS/8124/2020FS8124RLF.pdf", "https://medias1.fis-ski.com/pdf/2020/FS/8363/2020FS8363RLF.pdf", "https://medias1.fis-ski.com/pdf/2020/FS/8259/2020FS8259RLF.pdf"],
        "M_2021_2" : ["https://medias2.fis-ski.com/pdf/2021/FS/8145/2021FS8145RLF.pdf", "https://medias2.fis-ski.com/pdf/2021/FS/8344/2021FS8344RLF.pdf", "https://medias2.fis-ski.com/pdf/2021/FS/8380/2021FS8380RLF.pdf"],
        "W_2021_2" : ["https://medias1.fis-ski.com/pdf/2021/FS/8146/2021FS8146RLF.pdf", "https://medias1.fis-ski.com/pdf/2021/FS/8345/2021FS8345RLF.pdf", "https://medias3.fis-ski.com/pdf/2021/FS/8381/2021FS8381RLF.pdf"],
        "M_2022_2" : ["https://medias2.fis-ski.com/pdf/2022/FS/8611/2022FS8611RLF.pdf", "https://medias2.fis-ski.com/pdf/2022/FS/8435/2022FS8435RLF.pdf", "https://medias4.fis-ski.com/pdf/2022/FS/8206/2022FS8206RLF.pdf", "https://medias2.fis-ski.com/pdf/2022/FS/8160/2022FS8160RLF.pdf", "https://medias3.fis-ski.com/pdf/2022/FS/8505/2022FS8505RLF.pdf"],
        "W_2022_2" : ["https://medias1.fis-ski.com/pdf/2022/FS/8612/2022FS8612RLF.pdf", "https://medias3.fis-ski.com/pdf/2022/FS/8436/2022FS8436RLF.pdf", "https://medias1.fis-ski.com/pdf/2022/FS/8207/2022FS8207RLF.pdf", "https://medias3.fis-ski.com/pdf/2022/FS/8161/2022FS8161RLF.pdf", "https://medias4.fis-ski.com/pdf/2022/FS/8506/2022FS8506RLF.pdf"],
        "M_2023_3" : ["https://medias4.fis-ski.com/pdf/2023/FS/8145/2023FS8145RLF.pdf", "https://medias2.fis-ski.com/pdf/2023/FS/8278/2023FS8278RLF.pdf", "https://medias4.fis-ski.com/pdf/2023/FS/8159/2023FS8159RLF.pdf", "https://medias1.fis-ski.com/pdf/2023/FS/8135/2023FS8135RLF.pdf", "https://medias4.fis-ski.com/pdf/2023/FS/8312/2023FS8312RLF.pdf", "https://medias1.fis-ski.com/pdf/2023/FS/8215/2023FS8215RLF.pdf"],
        "W_2023_3" : ["https://medias1.fis-ski.com/pdf/2023/FS/8146/2023FS8146RLF.pdf", "https://medias3.fis-ski.com/pdf/2023/FS/8279/2023FS8279RLF.pdf", "https://medias2.fis-ski.com/pdf/2023/FS/8160/2023FS8160RLF.pdf", "https://medias4.fis-ski.com/pdf/2023/FS/8136/2023FS8136RLF.pdf", "https://medias4.fis-ski.com/pdf/2023/FS/8313/2023FS8313RLF.pdf", "https://medias1.fis-ski.com/pdf/2023/FS/8216/2023FS8216RLF.pdf"],
        "M_2024_3" : ["https://medias1.fis-ski.com/pdf/2024/FS/8118/2024FS8118RLF.pdf", "https://medias4.fis-ski.com/pdf/2024/FS/8284/2024FS8284RLF.pdf", "https://medias2.fis-ski.com/pdf/2024/FS/8138/2024FS8138RLF.pdf", "https://medias3.fis-ski.com/pdf/2024/FS/8172/2024FS8172RLF.pdf", "https://medias2.fis-ski.com/pdf/2024/FS/8088/2024FS8088RLF.pdf", "https://medias1.fis-ski.com/pdf/2024/FS/8310/2024FS8310RLF.pdf", "https://medias4.fis-ski.com/pdf/2024/FS/8322/2024FS8322RLF.pdf", "https://medias1.fis-ski.com/pdf/2024/FS/8220/2024FS8220RLF.pdf"],
        "W_2024_3" : ["https://medias3.fis-ski.com/pdf/2024/FS/8119/2024FS8119RLF.pdf", "https://medias3.fis-ski.com/pdf/2024/FS/8285/2024FS8285RLF.pdf", "https://medias4.fis-ski.com/pdf/2024/FS/8139/2024FS8139RLF.pdf", "https://medias2.fis-ski.com/pdf/2024/FS/8173/2024FS8173RLF.pdf", "https://medias3.fis-ski.com/pdf/2024/FS/8089/2024FS8089RLF.pdf", "https://medias4.fis-ski.com/pdf/2024/FS/8311/2024FS8311RLF.pdf", "https://medias2.fis-ski.com/pdf/2024/FS/8323/2024FS8323RLF.pdf", "https://medias2.fis-ski.com/pdf/2024/FS/8221/2024FS8221RLF.pdf"],
        "M_2025_3" : ["https://medias1.fis-ski.com/pdf/2025/FS/8105/2025FS8105RLF.pdf", "https://medias4.fis-ski.com/pdf/2025/FS/8237/2025FS8237RLF.pdf", "https://medias3.fis-ski.com/pdf/2025/FS/8127/2025FS8127RLF.pdf", "https://medias3.fis-ski.com/pdf/2025/FS/8254/2025FS8254RLF.pdf", "https://medias3.fis-ski.com/pdf/2025/FS/8070/2025FS8070RLF.pdf", "https://medias1.fis-ski.com/pdf/2025/FS/8258/2025FS8258RLF.pdf", "https://medias4.fis-ski.com/pdf/2025/FS/8098/2025FS8098RLF.pdf", "https://medias3.fis-ski.com/pdf/2025/FS/8171/2025FS8171RLF.pdf", "https://medias1.fis-ski.com/pdf/2025/FS/8165/2025FS8165RLF.pdf"],
        "W_2025_3" : ["https://medias2.fis-ski.com/pdf/2025/FS/8106/2025FS8106RLF.pdf", "https://medias2.fis-ski.com/pdf/2025/FS/8238/2025FS8238RLF.pdf", "https://medias1.fis-ski.com/pdf/2025/FS/8128/2025FS8128RLF.pdf", "https://medias1.fis-ski.com/pdf/2025/FS/8255/2025FS8255RLF.pdf", "https://medias2.fis-ski.com/pdf/2025/FS/8071/2025FS8071RLF.pdf", "https://medias2.fis-ski.com/pdf/2025/FS/8259/2025FS8259RLF.pdf", "https://medias4.fis-ski.com/pdf/2025/FS/8099/2025FS8099RLF.pdf", "https://medias1.fis-ski.com/pdf/2025/FS/8172/2025FS8172RLF.pdf", "https://medias4.fis-ski.com/pdf/2025/FS/8166/2025FS8166RLF.pdf"]}
    #####
    
    get_WC_results(pdf_urls_wc)
    print("Done getting World Cup Results_______________\n")

    #################################################################

    # Olympic Results
    print("Getting Olympic Results_______________")
    # just testing with 2 URLs for now
    urls_olympics1 = ["https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/men-moguls", "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/mens-moguls"]

    #####
    urls_olympics = {
        "M_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/mens-moguls", 
        "W_2018_1" : "https://www.olympics.com/en/olympic-games/pyeongchang-2018/results/freestyle-skiing/ladies-moguls", 
        "M_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/men-moguls", 
        "W_2022_2" : "https://www.olympics.com/en/olympic-games/beijing-2022/results/freestyle-skiing/women-moguls"}
    #####
    
    get_olympic_results(urls_olympics)
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