import pandas as pd
import matplotlib.pyplot as plt

coeffs_df = pd.read_csv("../data/Mens_Coefficients.csv")
coeffs_df1 = pd.read_csv("../data/Womens_Coefficients.csv")

coeffs_df['abs_coef'] = coeffs_df['coefficient'].abs()
coeffs_df = coeffs_df.sort_values('abs_coef', ascending=True)

df = pd.read_csv("../data/Womens_Testing_Data_Ranked.csv") 
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
plt.title('Logistic Regression Coefficients: Women\'s Singles Moguls')
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()