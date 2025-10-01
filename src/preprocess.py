import pandas as pd

index = pd.read_csv("data/index_returns.csv", parse_dates=['Date'], index_col='Date')
factors = pd.read_csv("data/factors.csv", parse_dates=['Date'], index_col='Date')

data = index.join(factors, how='inner')

data.fillna(0, inplace=True)

data.to_csv("data/aligned_data.csv")
print("Aligned data ready:")
print(data.head())
