import pandas as pd
import matplotlib.pyplot as plt

# Read JSON
df = pd.read_json("outputs/factor_contributions.json")
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Get factor columns dynamically (exclude 'const' and 'Predicted_Return' if present)
exclude_cols = ['const', 'Predicted_Return']
factors = [c for c in df.columns if c not in exclude_cols]

plt.figure(figsize=(12,6))
for factor in factors:
    plt.plot(df.index, df[factor], label=factor, alpha=0.7)

plt.title("Daily Factor Contributions to Index Returns")
plt.ylabel("Contribution")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()

# Save figure
plt.savefig("outputs/factor_contributions.png")
plt.show()
