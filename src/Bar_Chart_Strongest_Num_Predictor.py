import pandas as pd
import matplotlib.pyplot as plt

df_women = pd.read_csv("../data/Womens_Testing_Data_Ranked.csv")
df_women.columns = df_women.columns.str.strip()

df_women_top10_prob = df_women.sort_values('predicted_prob_top5', ascending=False).head(10)

names_order = df_women_top10_prob['Name'].tolist()

df_women_top10_rank = df_women[df_women['Name'].isin(names_order)].copy()

df_women_top10_rank['Name'] = pd.Categorical(df_women_top10_rank['Name'], categories=names_order[::-1], ordered=True)
df_women_top10_rank = df_women_top10_rank.sort_values('Name')

plt.rcParams['font.size'] = 12

plt.figure(figsize=(8,6))
# Blue for Strongest Num Predictor
plt.barh(df_women_top10_rank['Name'], df_women_top10_rank['Avg Time Points'], color='#48cae4')
# Purple for Avg Final Score
#plt.barh(df_women_top10_rank['Name'], df_women_top10_rank['Avg Final Score'], color='#C3B1E1')

plt.xlabel('Average Time Points')
plt.ylabel('Skier')
plt.title("Women's Singles Moguls: Top 10 Average Time Points")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.xlim(12, 20)
plt.tight_layout()
plt.show()
