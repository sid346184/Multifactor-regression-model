import pandas as pd

# Load data
index = pd.read_csv("data/index_returns.csv", parse_dates=['Date'], index_col='Date')
factors = pd.read_csv("data/factors.csv", parse_dates=['Date'], index_col='Date')

# Align data on dates
data = index.join(factors, how='inner')

# Optional: fill missing values
data.fillna(0, inplace=True)

# Save aligned data
data.to_csv("data/aligned_data.csv")
print("Aligned data ready:")
print(data.head())
