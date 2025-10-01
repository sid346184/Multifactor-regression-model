import pandas as pd
import matplotlib.pyplot as plt

# Read JSON
df = pd.read_json("outputs/factor_contributions.json")
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Factors to plot (exclude const if you want)
factors = ['CPI','Interest_Rate','Oil','FX','VIX']

# -----------------------------
# 1️⃣ Line plot of all factors
# -----------------------------
plt.figure(figsize=(14,6))
for factor in factors:
    plt.plot(df.index, df[factor], label=factor, alpha=0.7)
plt.title("Daily Factor Contributions to Index Returns")
plt.ylabel("Contribution")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/line_plot_factor_contributions.png")
plt.show()

# -----------------------------
# 2️⃣ Stacked area plot (absolute values)
# -----------------------------
plt.figure(figsize=(14,6))
df[factors].abs().plot(kind='area', stacked=True, alpha=0.6)
plt.title("Stacked Factor Contributions (Absolute Values)")
plt.ylabel("Contribution")
plt.xlabel("Date")
plt.tight_layout()
plt.savefig("outputs/stacked_area_factor_contributions.png")
plt.show()

# -----------------------------
# 3️⃣ Bar plot of average contributions
# -----------------------------
avg_contrib = df[factors].abs().mean().sort_values(ascending=False)
plt.figure(figsize=(10,5))
avg_contrib.plot(kind='bar', color='skyblue')
plt.title("Average Factor Contributions")
plt.ylabel("Average Absolute Contribution")
plt.xlabel("Factor")
plt.tight_layout()
plt.savefig("outputs/avg_bar_factor_contributions.png")
plt.show()
