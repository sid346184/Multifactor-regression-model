import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Read JSON
df = pd.read_json("outputs/factor_contributions.json")
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Get factor columns dynamically (exclude 'const' and 'Predicted_Return' if present)
exclude_cols = ['const', 'Predicted_Return']
factors = [c for c in df.columns if c not in exclude_cols]

os.makedirs("outputs", exist_ok=True)

# -----------------------------
# 1. Line Chart (per day contributions)
# -----------------------------
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

# -----------------------------
# 2. Stacked Area Chart
# -----------------------------
plt.figure(figsize=(12,6))
df[factors].plot.area(alpha=0.6, figsize=(12,6), stacked=False)
plt.title("Daily Factor Contributions - Area Chart (Unstacked)")
plt.ylabel("Contribution")
plt.xlabel("Date")
plt.tight_layout()
plt.savefig("outputs/factor_contributions_area_unstacked.png")
plt.close()


# -----------------------------
# 3. Bar Chart of Average Contributions
# -----------------------------
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

print("All visualizations saved in outputs/ folder!")
