DSCI 510 Final Project

Ranking mogul skiers in men's singles moguls and women's singles moguls (separately) based on the probability of that skier making the top 5 at the 2026 Olympics using logistic regression. The model also captures the coefficients of features to see what features may be most influential in predicting a top 5 outcome at the Olympics.

Data Sources:
| Data Source | Description | Approach | Size |
|---------|----------|----------|----------|
| FIS World Cup Singles Moguls Results | Results from World Cup events from the 2015 season to the 2025 season. Collected: Rank, FIS Code, Name, Nation, Birth Year, Final Score (out of 100), Time Points (out of 20), Air Points (out of 20), and Turn Points (out of 60). | Used pdfplumber to scrape the data since the score sheets were only available via downloadable pdf files. | Raw: 4678. Cleaned: 3342 |
| Olympic Singles Moguls Resuls | Results from the 2018 Pyeongchang Olympics and 2022 Beijing Olympics. Collected: Rank, Name, and Country. | Used json and regular expression to web scrape the data due to the data being in a json embedded portion of the html. | Raw: 120. Cleaned: 118 (ended up reducing the scope of my project, so ended up with less data in this category than originally expected)|
| FIS Athlete Biographies | Data from the each athlete’s biography page on the FIS website. Collected: Name, FIS Code, Birth Year, Age, and Gender. | Used BeautifulSoup to web scrape the data. | Raw: 370. Cleaned 370 |

Analysis:
I used Logistic Regression in my model to obtain the probability of a skier making the top 5 at the upcoming Olympics and the coefficients of the features to see which ones have the most influence over performance at the Olympics. I used Logistic Regression because the variable I was looking for ("Make Top 5") is binary (which is what LogR is designed for), it provides me the probabilties and the coefficients I wanted, and also this model is interpretable. Another model I was considering was a Decision Tree, but for this project I wanted to obtain the feature coefficients which Decision Trees do not provide. 
Missing and categorial values could also be easily handled in LogR, using One Hot Encoding and Simple Imputer to convert categorical features to binary and replace missing data with means (respectively). The model produced the probabilties for each athlete making the top 5, I was able to rank these athletes in descending order using the probabilities, and it produced the feature coefficients.
Minor issues with the model: if two variables are highly correlated, then something called multicollinearity occurs. This can lead to coefficients of features to be unstable. What I noticed for my own code is that certain relationships between a feature and the outcome that I expected to be negative/positive ended up being flipped. The magnitudes seem to be correct, it is just the signs of certain coefficients that seem to be incorrect.

Summary of Results:
My model produced the probabilites of the skiers making the top 5 and the coefficients of the features. 
For the probabilities: I found that the results are promising, with a few outcomes that differed slightly from what I expected. For men, the 5 athletes with the strongest probabilites of making the top 5 are: Osuke Nakahara (~70%), Mikael Kingsbury (~45%), Walter Wallberg (~20%), Ikuma Horishima (~18%), and Nick Page (~10%). The rest of the athlets have probabilties of ~2-3% or less. Mikael, Walter, Ikuma, and Nick are expected as they, for the past two Olympic cycles, have consistently made top 5. As for Osuke Nakahara, while manually cleaning my data I did not notice this name pop up nearly as much in the top 5 (and even top 10). My first thought is that this may be a fluke, but it is also possible that the model captured a pattern that is not apparent to me. As for women, the 5 athletes with the strongest probabilities are: Anri Kawamura (85%), Jakara Anthony (~70%), Perrine Laffont (~60%), Elizabeth Lemley (~22%), and Olivia Giaccio (~15%). The rest of the athletes have probabilities of ~14% and less. The results for women were similar for men in that Jakara, Perrine, Elizabeth, and Olivia consistently make top 5, whereas Anri consistently makes top 10-15, with a few competitions in which she wins 1st. Again, it seems like it might be a fluke, but the model may have picked up a pattern in the data. One skier who I expected to be a lot higher is Jaelin Kauf. She has the 9th strongest probability of making top 5. For the past Olympic cycle and this upcoming cycle she has consistently been getting 1st and 2nd place, so I wonder why her probability for making top 5 at this upcoming Olympics is not higher (currently, she is the frontrunner to finish first at the upcoming Olympics). 
For the coefficients: As stated before, some of the signs on the coefficients are unexpected, but the magnitudes of the coefficients seem to be correct to me. For men, the strongest numeric predictor is average Time Points. It shows up as a negative relationship in the results, even though more time points should increase the probability of getting into the top 5 (so it should be a positive relationship). The magnitude seems to be correct, though. For men at this elite level, their performance is very similar to one another. Most of the time, it comes down to how fast their run is. A prime example of this is the 2022 Olympics. Mikael Kingsbury and Walter Wallberg had nearly identical runs, Walter in fact getting slightly less points than Mikael, but Walter won first because he got 2 extra time points compared to Mikael. Timing for men makes all the difference, so Time Points being the strongest numeric predictor for men makes sense. As for women, the strongest numeric predictor is average Rank. The coefficient for this feature is negative, which does make sense because the lower the average rank (1st, 2nd, 3rd, etc.) the higher the probability should be of making top 5. This also seems to be correct after noticing certain patterns in scores while cleaning the code. Female mogul skiers scores seemed to be a lot more inconsistent compared to men. Their scores jumped around a lot more. I noticed that rankings depended more on relative performance than the actual score. A score that is low in a certain competition may still result in a high placement if the other skiers also performed poorly. Therefore, the ability to perform better than others rather than acheive a higher score resulted in lower rankings, which explains why average rank shows up as the strongest numeric predictor for women. 

Files:
- data/.gitkeep
    - I placed .gitkeep in my data folder because I originally had it so that all files in "data" were hidden, and therefore the entire data folder was hidden, but in "How to Run" below I will need whoever is running my program to download my cleaned data and place it into the data folder, so I wanted to make sure the data folder would appear in my repo for easy placement of my data. 
- main.py
    - My pipeline for my project. It goes through scraping to obtaining results. The lines in which the scraping occurs are commented out so that it is just the results section that runs when calling main.py.
- tests.py
    - Verifying that my data loads with examples of each type of data (Olympic results, World Cup results, and athlete biography data) I gathered for my project. It loads DataFrames from my cleaned data, not raw data. 
- results.ipynb
    - Shows bar charts of my results.
- config.py
    - Holds all my universal variables used by my programs.
- .env.example
    - Presents my variables with no values.
- .gitignore
    - Says what files should be ignored in my repo.
- requirements.txt 
    - Shows the external Python libraries my project needs.
- Create_Train_Test_Files.py
    - My program that sets up the training and testing csv files to be used by my logistic regression model with the column headers.
- Creating_Bar_Charts.py
    - My program that creates all the visual results, used in results.ipynb.
- Input_for_LogR.py
    - My program that, from my cleaned data files, pulls all the data I want to provide to the logistic regression model (calculating averages and standard deviations of scores where needed) and populating this data into the appropriate testing or training files.
- Load_Data.py
    - My program that creates DataFrames for one example of each type of data I collected (Olympic results, World Cup results, and athlete biography data).
- Running_Logistic_Regression.py
    - My program that sets up and runs the logistic regression model and outputs the results into the proper files. 
- Scraping_Athlete_Data.py
    - My program that scrapes the data from each url in the csv file of athlete biography urls and outputs the data into the proper files.
- Scraping_Olympic_Results.py
    - My program that scrapes the data from each url of olympic results urls and outputs the data into the proper files.
- Scraping_World_Cup_Results.py
    - My program that scrapes the data from each url in the csv file of world cup results urls and outputs the data into the proper files.

How to Run:
- Clone repository:
	- git clone https://github.com/brynndafoe02/dsci510_fall2025_final_project
	- cd dsci510_fall2025_final_project
- Download my required data:
    - Download my required datasets from: https://drive.google.com/drive/folders/1WluH0J5-ip4HF8yI6-hqPdBQH6iOHz5d?usp=share_link 
    - Place "cleaned", "Athlete_URLs.csv", and "World_Cup_URLs.csv" into data folder so that it looks like this:
        - dsci510_fall2025_final_project/
            - data/
                - cleaned
                - Athlete_URLs.csv
                - World_Cup_URLs.csv
- Set up environment:
	- conda create -n dsci510_fp 
	- conda activate dsci510_fp 
	- pip install -r requirements.txt
- Run tests:
	- python tests.py
- Run pipeline:
    - python main.py
        - main.py is already configured to run with settings / paths. As long as my data from the Google Drive link is place in the data folder, running "python main.py" will produce results.

Environment:
- Python 3.11 or higher (I am using 3.12.5)
- Conda environment
- Dependencies in 'requirements.txt'
