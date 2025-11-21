import requests
from bs4 import BeautifulSoup
import csv

# need to gather my total list of athletes later, but starting and testing with four URLs first
# urls = [
#     "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=197224&type=career",
#     "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=182830",
#     "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=170101",
#     "https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=FS&competitorid=174753"
# ]

def get_skier_data(url):
    headers = {"User-Agent": "SkierData/Moguls"} # pretending to be a browser or else I get an error
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

 # Going to the URL page and looking at 'Show Page Source' I can see where the data I want is held 
        # so I can search for it properly in the following code
    first_name_data = soup.find("h1", class_="athlete-profile__name")
    first_name_contents = first_name_data.contents
    first_name = first_name_contents[0].strip()
        # Looks like <h1 class="athlete-profile__name"> in source
            # h1 -> tag
            # athlete-profile__name -> class
    last_name_data = soup.find("span", class_="athlete-profile__lastname")
        # <h1 class="athlete-profile__name"> Cooper <span class="athlete-profile__lastname">WOODS</span>
    last_name = last_name_data.text.strip()

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

    
# all_skiers = []
# for url in urls:
#     skier_data = get_skier_data(url)
#     all_skiers.append(skier_data)

def make_athlete_data_csv(all_skiers : list):
    csv_file_name = "AthleteData.csv"
    with open(file=csv_file_name, mode='w') as f:
        column_names = "Name, FIS Code, Birthdate, Birth Year, Age, Gender\n"
        f.write(column_names)
        for skier in all_skiers:
            name = skier['Name']
            fis_code = skier['FIS Code']
            birthdate = skier['Birthdate']
            birth_year = birthdate[-4:]
            age = skier['Age']
            gender = skier['Gender']
            new_line = f"{name}, {fis_code}, {birthdate}, {birth_year}, {age}, {gender}\n"
            f.write(new_line)

