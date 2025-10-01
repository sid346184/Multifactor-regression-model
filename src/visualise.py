import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_json("outputs/factor_contributions.json")
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

exclude_cols = ['const', 'Predicted_Return']
factors = [c for c in df.columns if c not in exclude_cols]

os.makedirs("outputs", exist_ok=True)


plt.figure(figsize=(12,6))
for factor in factors:
    plt.plot(df.index, df[factor], label=factor, alpha=0.7)

plt.title("Daily Factor Contributions to Index Returns - Line Chart")
plt.ylabel("Contribution")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/factor_contributions_line.png")
plt.close()


avg_contrib = df[factors].mean()
plt.figure(figsize=(10,6))
sns.barplot(x=avg_contrib.index, y=avg_contrib.values, palette="viridis")
plt.title("Average Factor Contribution to Index Returns")
plt.ylabel("Average Contribution")
plt.xlabel("Factors")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/factor_contributions_bar.png")
plt.close()

plt.figure(figsize=(12,6))
sns.heatmap(df[factors].T, cmap="coolwarm", cbar_kws={'label': 'Contribution'})
plt.title("Heatmap of Factor Contributions Over Time")
plt.ylabel("Factors")
plt.xlabel("Date Index")
plt.tight_layout()
plt.savefig("outputs/factor_contributions_heatmap.png")
plt.close()

print("All visualizations saved in outputs/ folder!")
