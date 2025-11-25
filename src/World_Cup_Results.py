import requests
import pdfplumber
# for this data source I could only access the data via the provided PDFs,
# so using pdfplumber to extract the data
import csv
import os
from collections import defaultdict

def get_WC_results():
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, "data")

    pdf_folder = os.path.join(data_directory, "FIS_scoresheet_pdfs")
    os.makedirs(pdf_folder, exist_ok=True)
    # Since I will be making folders of my data I am using os to make directories
    # Making a directory for the pdf files scraped or else all the pdf files just populate
    # in the directory I am working in and makes it messy
    # If folder already exists it will not make a new folder

    pdf_urls = defaultdict(list)

    with open(file="../data/World_Cup_URLs.csv", mode="r") as f:
        csv_read = csv.DictReader(f)
        for row in csv_read:
            pdf_urls[row["event"]].append(row["url"])

    pdf_urls = dict(pdf_urls)
    
    for ski_season in pdf_urls:
        for url in pdf_urls[ski_season]:
            pdf_split = url.split("/")
            pdf_name = pdf_split[-1] # just naming it what ever the end of the URL is since that part is unique (and also shows what ski season it is for *2025FS8105RLF.pdf* -> 2025 ski season
            pdf_path = os.path.join(pdf_folder, pdf_name)
            # creating path where pdf will go 
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Connection": "keep-alive"}
            url_contents = requests.get(url, headers=headers, timeout=10)
            with open(file=pdf_path, mode="wb") as f:
                # using "wb" because "w" is used for things like CSV files or text,
                # but PDFs are binary files and may not be extracted correctly using just "w"
                f.write(url_contents.content) # put content of that pdf to a file
            print(f"Downloaded {pdf_name}") # using for testing, will take out later
    
            extracted_data = []
            with pdfplumber.open(pdf_path) as pdf:
                # pdfplumber has page instances / .page property
                for page in pdf.pages:
                    text = page.extract_text() # returns a string
                    if text == '': # if nothing, skip this page
                        continue
                        
                    lines = text.split("\n") # splits text into lines
                    lines_merged = []
    
                    for aline in lines: # will rename 'aline' later to something better
                        one_line = aline.strip() # will rename 'one_line' later to something better
                        if one_line == '': # if nothing, skip
                            continue
                        # *** Below
                        split_words = one_line.split() # split into list of words
                        if split_words[0].isdigit() == True:
                            # *** the first instance where the first word is a digit is the start of the competitor data, so going to look for this data below 
                            lines_merged.append(one_line)
                        else:
                            if len(lines_merged) != 0: # doing this so we don't get an index error in the next line
                                # attach to last skier in merged lines because it is a continuation of their scores
                                last_line = lines_merged[-1]
                                new_line = last_line + " " + one_line
                                lines_merged[-1] = new_line
                            # merging lines because as shown in ***, I want data on the first line with the competitor's name and the third line, because the third line has the final points for each area of points without all the deductions and stuff
                        
                    for bline in lines_merged: # will rename 'bline' later to something better
                        words = bline.split()
    
                        # rank0, bib1, fis_code2, last_name3, first_name4, nation5, birth_year6, scores7
                        if len(words) >= 7:
                            rank = words[0]
                            fis_code = words[2]
                            last_name = words[3]
                            first_name = words[4]
                            nation = words[5]
                            birth_year = words[6]
                        else:
                            continue # skip, because it means it does have the data I want
    
                        full_name = f"{first_name} {last_name}"
    
                        other_values = []
                        if len(words) >= 8:
                            for word in words[7:]:
                                other_values.append(word)
                        # gathering the rest of the scores, will filter out for the scores I care about in the csv part
    
                        extracted_data.append([rank, fis_code, full_name, nation, birth_year] + other_values)

            season_directory = os.path.join(data_directory, ski_season)
            os.makedirs(season_directory, exist_ok=True)
    
            csv_name = pdf_name.replace(".pdf", ".csv") # easy name, might change later
            csv_path = os.path.join(season_directory, csv_name) # connect
            with open(file=csv_path, mode="w", encoding="utf-8") as f:
                # opened pdf file above in binary mode, so here when using regular "w" I need to use encoding or else I get errors
                column_names = "Rank, FIS Code, Name, Nation, Birth Year, Final Score, Time Points, Air Points, Turn Points\n"
                # I started with "Other" columns just to see what would print and went back in later to name the columns
                f.write(column_names)
                for row in extracted_data:
                    if len(row) < 33:
                        # a "good" line has 33 values, anything else is not good
                        continue
                    else:
                        #              R          FIS       N         Nat        BY        FS        TiP         AP        TuP
                        new_line = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[18]}, {row[30]}, {row[31]}, {row[32]}\n" 
                        f.write(new_line)
    
            print(f"Saved {len(extracted_data)} rows to {csv_path}") # used for testing, will delete later

# ***
# first lines look like this
    # FIS FREESTYLE SKI WORLD CUP 2025
    # Results Overall
    # MO
    # Men's Moguls
    # WATERVILLE (USA)
    # FRI 24 JAN 2025 Start Time: 15:05
    # Number of Competitors: 60, Number of NSAs: 16
    # Time Air Turns
    # Rank Bib Co F d IS e Name N C S od A e YB Run Seconds Time J6 J7 Jump DD Total B D J1 J2 J3 J4 J5 Total Sc R o u r n e Tie
    # Points
    # Final 2
    # 1 1 2484937 KINGSBURY Mikael CAN 1992 23.07 16.95 9.4 9.2 bF 0.88 B: 17.6 17.5 17.4 17.3 17.9 52.5 84.95 -> First Line
    # 8.5 8.5 10op 1.05 D: -0.7 -0.5 -0.4 -0.3 -1.0 -1.6 -> Second Line
    # 16.95 17.10 50.9 -> Third Line
    # 2 8 2533462 PAGE Nick USA 2002 23.21 16.76 8.3 8.6 10op 1.05 B: 17.5 17.4 17.0 17.1 17.0 51.5 83.55
