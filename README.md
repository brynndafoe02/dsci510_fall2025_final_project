DSCI 510 Final Project, Progress Report

Predicting top 5 mogul skiers for men's singles moguls and women's singles moguls (separately) for the 2026 Olympics using logistic regression.

Current Status:
- My .py files currently pull and process data.
- CSV files are generated as output by the .py files.
- Logistic regression has not been used yet.

Files:
- 'Athlete_Data.py' : pulls athlete data (Name, FIS Code, Birthdate, Birth Year, Age, and Gender) from urls using BeautifulSoup, creates 1 .csv file
- 'Olympic_Results.py' : pulls Olympic results (Rank, Name, Country) from urls using json and regular expressions, creates a folder of .csv files
- 'World_Cup_Results.py' : pulls World Cup results (Rank, FIS Code, Name, Nation, Birth Year, Final Score, Time Points, Air Points, and Turn Points) from urls using pdfplumber, creates a folder for processed .pdf files, and a folder of .csv files for each ski season
- 'tests.py' : tests the code in the .py files
- 'doc/progress_report.pdf' : Progress report.
- 'requirements.txt' : Python dependencies.

How to Run:
- Clone repository:
	- git clone https://github.com/brynndafoe02/dsci510_fall2025_final_project
	- cd dsci510_fall2025_final_project
- Set up environment:
	- conda create -n dsci510_fp 
	- conda activate dsci510_fp 
	- pip install -r requirements.txt
- Run tests:
	- python tests.py

Environment:
- Python 3.11 or higher (I am using 3.12.5)
- Conda environment
- Dependencies in 'requirements.txt'

Future:
- Will create a program that will calculate averages and standard deviations of World Cup scores for each skier over each Olympic cycle (2015 Season - 2018 Season, 2019 Season - 2022 Season) for my training .csv file to give to the logistic regression model.
- Will do the same thing, but for the 2023 Season - 2026 Season for my testing .csv file to give to the logistic regression model.
- Will make the program that will run the logistic regression.