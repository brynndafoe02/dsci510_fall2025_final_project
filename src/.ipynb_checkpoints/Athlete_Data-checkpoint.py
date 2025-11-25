import requests
from bs4 import BeautifulSoup
import csv
import os

def get_skier_data(url, i):
    first_name = None
    last_name = None
    full_athlete_name = None
    fis_code = None
    birthdate = None
    age = None
    gender = None
    
    print(f"     Skier {i}")
                
    headers = {
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://www.fis-ski.com/DB/general/athletes.html",
        "Upgrade-Insecure-Requests": "1"}
 # pretending to be a browser or else I get an error

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        print("Timed out. Skipping: ", url)
        return None
    except requests.exceptions.RequestException as e:
        print("Request error. Skipping: ", url, "\n   Error:", e)
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

 # Going to the URL page and looking at 'Show Page Source' I can see where the data I want is held 
        # so I can search for it properly in the following code
    first_name_data = soup.find("h1", class_="athlete-profile__name")
    if first_name_data:
        first_name_contents = first_name_data.contents
        first_name = first_name_contents[0].strip()
        # Looks like <h1 class="athlete-profile__name"> in source
            # h1 -> tag
            # athlete-profile__name -> class
    last_name_data = soup.find("span", class_="athlete-profile__lastname")
        # <h1 class="athlete-profile__name"> Cooper <span class="athlete-profile__lastname">WOODS</span>
    if last_name_data:
        last_name = last_name_data.text.strip()
    if first_name and last_name:
        full_athlete_name = f"{first_name} {last_name}"

    ############ Going to condense this later into it's own function

    # want 1) FIS Code, 2) Birthdate, 3) Age, and 4) Gender
        # could get Nation here, but Nation will be captured in WC .py program
    
        # 1) <li class="profile-info__entry profile-info__entry_visible_xs" id="FIS Code"> <span class="profile-info__field">FIS Code</span> <span class="profile-info__value">2532161</span>
    
    li_fis_code = soup.find("li", id="FIS Code")
    if li_fis_code:
        fis_code_data = li_fis_code.find("span", class_="profile-info__value")
        fis_code = fis_code_data.text.strip()
    else:
        fis_code = None
    
        # 2) <li class="profile-info__entry profile-info__entry_visible_xs" id="Birthdate"> <span class="profile-info__field">Birthdate</span> <span class="profile-info__value hidden-xs">07-09-2000</span> <span class="profile-info__value hidden-sm-up">2000</span> </li>

    li_birthdate = soup.find("li", id="Birthdate")
    if li_birthdate:
        birthdate_data = li_birthdate.find("span", class_="profile-info__value")
        birthdate = birthdate_data.text.strip()
    else:
        birthdate = None

        # 3) <li class="profile-info__entry" id="Age"> <span class="profile-info__field">Age</span> <span class="profile-info__value">25</span> </li>

    li_age = soup.find("li", id="Age")
    if li_age:
        age_data = li_age.find("span", class_="profile-info__value")
        age = age_data.text.strip()
    else:
        age = None

        # 4) </li> <li class="profile-info__entry" id="Gender"> <span class="profile-info__field">Gender</span> <span class="profile-info__value">Male</span> </li>

    li_gender = soup.find("li", id="Gender")
    if li_gender:
        gender_data = li_gender.find("span", class_="profile-info__value")
        gender = gender_data.text.strip()
    else:
        gender = None

    ############
    
    return {
        "Name": full_athlete_name,
        "FIS Code": fis_code,
        "Birthdate": birthdate,
        "Age": age,
        "Gender": gender
    }

def make_athlete_data_csv(all_skiers : list):
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")

    csv_file_name = os.path.join(data_directory, "Athlete_Data.csv")

    with open(file=csv_file_name, mode='w') as f:
        column_names = "Name, FIS Code, Birthdate, Birth Year, Age, Gender\n"
        f.write(column_names)
        for skier in all_skiers:
            name = skier['Name'] if skier['Name'] else "None"
            fis_code = skier['FIS Code'] if skier['FIS Code'] else "None"
            birthdate = skier['Birthdate'] if skier['Birthdate'] else "None"
            birth_year = birthdate[-4:] if (birthdate and (len(birthdate) >= 4)) else "None"
            age = skier['Age'] if skier['Age'] else "None"
            gender = skier['Gender'] if skier['Gender'] else "None"
            new_line = f"{name}, {fis_code}, {birthdate}, {birth_year}, {age}, {gender}\n"
            f.write(new_line)

