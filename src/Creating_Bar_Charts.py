import pandas as pd
import os
import matplotlib.pyplot as plt

# need to access config from root
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)

from config import DATA_FOLDER, COEFFICIENTS_MEN, TESTING_DATA_RANKED_MEN, COEFFICIENTS_WOMEN, TESTING_DATA_RANKED_WOMEN

# sys.path.remove(root)
# # return to running from src

def Ranked_Results_Bar_Chart(gender: str):
    if gender == "men":
        ranked_path = os.path.join(DATA_FOLDER, TESTING_DATA_RANKED_MEN)
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
        plt.title("Men's Singles Moguls: Ranked by Probability")
        plt.xlim(0,.7)
        plt.grid(axis='x', linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.show()