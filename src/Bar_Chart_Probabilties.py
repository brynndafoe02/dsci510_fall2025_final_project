import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/Mens_Testing_Data_Ranked.csv")
df.columns = df.columns.str.strip()

df_sorted = df.sort_values('predicted_prob_top5', ascending=False).head(10)
df_sorted = df_sorted.iloc[::-1]

colors = []

for i in range(len(df_sorted)):
    if i == len(df_sorted) - 1:
        colors.append('gold')
    elif i == len(df_sorted) - 2:
        colors.append('silver')
    elif i == len(df_sorted) - 3:
        colors.append('#CD7F32')
    else:
        colors.append('blue')

plt.rcParams['font.size'] = 10

plt.figure(figsize=(8,12))
plt.barh(df_sorted['Name'], df_sorted['predicted_prob_top5'], color=colors)

plt.xlabel('Predicted Probability')
plt.ylabel('Skier')
plt.title("Men's Singles Moguls: Top 10 Ranked by Probability")
plt.xlim(0,.9)
plt.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
