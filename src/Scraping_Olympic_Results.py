import json
import requests
import re
import csv
import os

# when I do "Show Page Source" I found the data I wanted, but it did not look like HTML
# so when looking it up I found that the area in which I want to pull data from
# is JSON embedded inside, so using json to access it

def get_olympic_results(urls_olympics : dict):
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")
    output_folder = os.path.join(data_directory, "olympic_results")
    
    # Will not make the folder if it exists already
    os.makedirs(output_folder, exist_ok=True)
    
    for olympic_year, url in urls_olympics.items(): # -> {what year + gender : url}
        print(f"Processing: {url}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
            "Connection": "keep-alive"}
        
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
    
        # what the source page shows with the data I want to pull -> *** LOOK AT BOTTOM
        # all the top 30 skiers are in the "standing":[xxx]
        pattern = r'"standing":(\[.*?\])'
        # "standing": -> matching literally
        # () -> grouping to capture entire thing inside "standing":[(xxx)]
        # \[ -> want to match literal [
        # .*? -> any characters
        # \] -> want to match literal ]
        match = re.search(pattern, html)
        if not match:
            print("!!! Pattern not found.")
            continue
        standings_text = match.group(1) # grab first group
    
        data = json.loads(standings_text)
        # if the string is in proper json format:
            # json.loads will turn that string into a parsable python data strucutre
            # in this case it creates a large dictionary 
            # looks like ****** LOOK AT BOTTOM
    
        url_parts = url.split("/")
        last_part = url_parts[-1] # easy file name
        filename = f"{olympic_year}.csv" # making .csv file name
        csv_path = os.path.join(output_folder, filename) # connecting
    
        with open(file=csv_path, mode="w") as f:
            column_names = "Rank, Name, Country\n"
            f.write(column_names)
            for data_part in data:
                # dictionary below in ******
                rank = data_part["rank"]["position"]
                name = data_part["participant"]["displayName"]
                country = data_part["noc"]["code"]
                new_line = f"{rank}, {name}, {country}\n"
                f.write(new_line)
        print("Results Saved")

# ***

# starts with

# "standing":[{"__typename":"ParticipantResult","rank":{"__typename":"Rank","equal":false,"order":1,"position":"1"},"value":{"__typename":"ParticipantResultValue","type":"POINTS","unit":"83.23"},"qualificationMark":null,"medalType":"GOLD","noc":{"__typename":"NOC","code":"SWE","name":"Sweden"},"participant":{"__typename":"Athlete","name":"Walter","surname":"WALLBERG","displayName":"Walter WALLBERG","thumbnail":{"__typename":"Image","urlTemplate":"https://img.olympics.com/images/image/private/{formatInstructions}/primary/yfgpvdc1ocpdr60nd4ca"},"meta":{"__typename":"Meta","url":"https://www.olympics.com/en/athletes/wallberg"},"countryObject":{"__typename":"Country","name":"Sweden","code":"SE","triLetterCode":"SWE"}}}

# ends with

# {"__typename":"NOC","code":"CHN","name":"P. R. China"},"participant":{"__typename":"Athlete","name":"Yang","surname":"ZHAO","displayName":"Yang ZHAO","thumbnail":null,"meta":{"__typename":"Meta","url":"https://www.olympics.com/en/athletes/yang-zhao"},"countryObject":{"__typename":"Country","name":"People's Republic of China","code":"CN","triLetterCode":"CHN"}}}]

# all enwrapped in "standing":[xxx]

# ******

# [{'__typename': 'ParticipantResult', 'rank': {'__typename': 'Rank', 'equal': False, 'order': 1, 'position': '1'}, 'value': {'__typename': 'ParticipantResultValue', 'type': 'POINTS', 'unit': '86.63'}, 'qualificationMark': None, 'medalType': 'GOLD', 'noc': {'__typename': 'NOC', 'code': 'CAN', 'name': 'Canada'}, 'participant': {'__typename': 'Athlete', 'name': 'Mikael', 'surname': 'KINGSBURY', 'displayName': 'Mikael KINGSBURY', 'thumbnail': {'__typename': 'Image', 'urlTemplate': 'https://img.olympics.com/images/image/private/{formatInstructions}/primary/jskr14nlcjwlbhfjooi3'}, 'meta': {'__typename': 'Meta', 'url': 'https://www.olympics.com/en/athletes/mikael-kingsbury'}, 'countryObject': {'__typename': 'Country', 'name': 'Canada', 'code': 'CA', 'triLetterCode': 'CAN'}}}, 

# first item in list ^




