import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/Womens_Testing_Data_Ranked.csv")
df.columns = df.columns.str.strip()

df_sorted = df.sort_values('predicted_prob_top5', ascending=False).head(10)
df_sorted = df_sorted.iloc[::-1]

colors = ['#b5e2ff' if i < 5 else '#45b6fe' for i in range(len(df_sorted))]

plt.rcParams['font.size'] = 10

plt.figure(figsize=(8,12))
plt.barh(df_sorted['Name'], df_sorted['predicted_prob_top5'], color=colors)

plt.xlabel('Predicted Probability')
plt.ylabel('Skier')
plt.title("Women's Singles Moguls: Top 10 Ranked by Probability")
plt.xlim(0,.9)
plt.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
