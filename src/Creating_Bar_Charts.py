import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# need to access config from root
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)

from config import DATA_FOLDER, COEFFICIENTS_MEN, TESTING_DATA_RANKED_MEN, COEFFICIENTS_WOMEN, TESTING_DATA_RANKED_WOMEN

sys.path.remove(root)
# return to running from src

################################################################

def Ranked_Results_Bar_Chart(ranked_path, gender: str):
    ranked_df = pd.read_csv(ranked_path)

    ranked_df.columns = ranked_df.columns.str.strip()

    df_sorted = ranked_df.sort_values('predicted_prob_top5', ascending=False).head(10)
    # df_sorted = ranked_df.sort_values('predicted_prob_top5', ascending=False)
        # IF WANT TO SEE ALL ATHLETES, USE THIS LINE ^^^ INSTEAD!
    df_sorted = df_sorted.iloc[::-1]

    colors = ['#b5e2ff' if i < 5 else '#45b6fe' for i in range(len(df_sorted))]

    plt.rcParams['font.size'] = 10

    plt.figure(figsize=(8,12))
    plt.barh(df_sorted['Name'], df_sorted['predicted_prob_top5'], color=colors)

    plt.xlabel('Predicted Probability')
    plt.ylabel('Skier')
    if gender == "men":
        plt.title("Men's Singles Moguls: Ranked by Probability")
        plt.xlim(0,.7)
    if gender == "women":
        plt.title("Women's Singles Moguls: Ranked by Probability")
        plt.xlim(0,.9)
    plt.grid(axis='x', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

def Ranked_Results_Bar_Chart_Setup(gender: str):
    if gender == "men":
        ranked_path = os.path.join(DATA_FOLDER, TESTING_DATA_RANKED_MEN)
        Ranked_Results_Bar_Chart(ranked_path, gender)
    elif gender == "women":
        ranked_path = os.path.join(DATA_FOLDER, TESTING_DATA_RANKED_WOMEN)
        Ranked_Results_Bar_Chart(ranked_path, gender)

################################################################

def Coefficients_Bar_Chart(coeffs_path, gender: str):
    coeffs_df = pd.read_csv(coeffs_path)
    
    coeffs_df['abs_coef'] = coeffs_df['coefficient'].abs()
    coeffs_df = coeffs_df.sort_values('abs_coef', ascending=True)

    if gender == "men":
        testing_data_ranked = TESTING_DATA_RANKED_MEN
    elif gender == "women":
        testing_data_ranked = TESTING_DATA_RANKED_WOMEN
    ranked_path = os.path.join(DATA_FOLDER, testing_data_ranked)
    df = pd.read_csv(ranked_path) 
    df.columns = df.columns.str.strip() 
    
    print("\n")
    print(df[['Avg Final Score', 'Avg Time Points']].corr())
    print("\n")
    print(df[['Avg Final Score', 'Avg Turn Points']].corr())
    print("\n")
    print(df[['Avg Final Score', 'Avg Air Points']].corr())
    print("\n")
    print(df[['Avg Final Score', 'Avg Rank']].corr())
    print("\n")
    
    plt.figure(figsize=(8,6))
    
    plt.barh(coeffs_df['feature'], coeffs_df['coefficient'], color=['red' if x < 0 else 'green' for x in coeffs_df['coefficient']])
    
    plt.xlabel('Coefficient Value')
    if gender == "men":
        plt.title('Logistic Regression Coefficients: Men\'s Singles Moguls')
    elif gender == "women":
        plt.title('Logistic Regression Coefficients: Women\'s Singles Moguls')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

def Coefficients_Bar_Chart_Setup(gender: str):
    if gender == "men":
        coeffs_path = os.path.join(DATA_FOLDER, COEFFICIENTS_MEN)
        Coefficients_Bar_Chart(coeffs_path, gender)
    if gender == "women":
        coeffs_path = os.path.join(DATA_FOLDER, COEFFICIENTS_WOMEN)
        Coefficients_Bar_Chart(coeffs_path, gender)

################################################################

def Strongest_Numeric_Predictor_Bar_Chart(ranked_path, gender: str):
    df_pred = pd.read_csv(ranked_path)
    
    df_pred.columns = df_pred.columns.str.strip()
    
    df_pred_top10_prob = df_pred.sort_values('predicted_prob_top5', ascending=False).head(10)
    
    names_order = df_pred_top10_prob['Name'].tolist()
    
    df_pred_top10_rank = df_pred[df_pred['Name'].isin(names_order)].copy()
    
    df_pred_top10_rank['Name'] = pd.Categorical(df_pred_top10_rank['Name'], categories=names_order[::-1], ordered=True)
    df_pred_top10_rank = df_pred_top10_rank.sort_values('Name')
    
    plt.rcParams['font.size'] = 12
    
    plt.figure(figsize=(8,6))

    if gender == "men":
        plt.barh(df_pred_top10_rank['Name'], df_pred_top10_rank['Avg Time Points'], color='#48cae4')
    elif gender == "women":
        plt.barh(df_pred_top10_rank['Name'], df_pred_top10_rank['Avg Rank'], color='#48cae4')

    if gender == "men":
        plt.xlabel('Average Time Points')
        plt.title("Men's Singles Moguls: Top 10 Average Time Points (Strongest Numeric Predictor)")
        plt.xlim(12, 18)
    elif gender == "women":
        plt.xlabel('Average Rank')
        plt.title("Women's Singles Moguls: Top 10 Average Rank (Strongest Numeric Predictor)")
        plt.xlim(0, 10.5)
    plt.ylabel('Skier')
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def Strongest_Numeric_Predictor_Bar_Chart_Setup(gender: str):
    if gender == "men":
        ranked_path = os.path.join(DATA_FOLDER, TESTING_DATA_RANKED_MEN)
        Strongest_Numeric_Predictor_Bar_Chart(ranked_path, gender)
    elif gender == "women":
        ranked_path = os.path.join(DATA_FOLDER, TESTING_DATA_RANKED_WOMEN)
        Strongest_Numeric_Predictor_Bar_Chart(ranked_path, gender)

################################################################

def Strongest_Intuitive_Predictor_Bar_Chart(ranked_path, gender: str):
    df_pred = pd.read_csv(ranked_path)
    
    df_pred.columns = df_pred.columns.str.strip()
    
    df_pred_top10_prob = df_pred.sort_values('predicted_prob_top5', ascending=False).head(10)
    
    names_order = df_pred_top10_prob['Name'].tolist()
    
    df_pred_top10_rank = df_pred[df_pred['Name'].isin(names_order)].copy()
    
    df_pred_top10_rank['Name'] = pd.Categorical(df_pred_top10_rank['Name'], categories=names_order[::-1], ordered=True)
    df_pred_top10_rank = df_pred_top10_rank.sort_values('Name')
    
    plt.rcParams['font.size'] = 12
    
    plt.figure(figsize=(8,6))
    
    plt.barh(df_pred_top10_rank['Name'], df_pred_top10_rank['Avg Final Score'], color='#C3B1E1')
    
    plt.xlabel('Average Final Score')
    plt.ylabel('Skier')
    if gender == "men":
        plt.title("Men's Singles Moguls: Top 10 Average Final Score (Intuitive Predictor)")
    elif gender == "women":
        plt.title("Women's Singles Moguls: Top 10 Average Final Score (Intuitive Predictor)")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.xlim(0, 85)
    plt.tight_layout()
    plt.show()
    
def Strongest_Intuitive_Predictor_Bar_Chart_Setup(gender: str):
    if gender == "men":
        ranked_path = os.path.join(DATA_FOLDER, TESTING_DATA_RANKED_MEN)
        Strongest_Intuitive_Predictor_Bar_Chart(ranked_path, gender)
    elif gender == "women":
        ranked_path = os.path.join(DATA_FOLDER, TESTING_DATA_RANKED_WOMEN)
        Strongest_Intuitive_Predictor_Bar_Chart(ranked_path, gender)

    