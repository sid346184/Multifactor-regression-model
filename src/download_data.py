import yfinance as yf
import pandas as pd

# -----------------------
# Parameters
# -----------------------
start_date = "2020-01-01"
end_date = "2025-01-01"
index_symbol = "^GSPC"  # S&P 500 (change to ^NSEI for NIFTY 50)

# Factor symbols
factor_symbols = {
    "Oil": "CL=F",          # Crude Oil
    "FX": "EURUSD=X",       # USD/EUR exchange rate
    "VIX": "^VIX"           # Volatility Index
}

# -----------------------
# Download index data
# -----------------------
print("Downloading index data...")
index_data = yf.download(index_symbol, start=start_date, end=end_date, auto_adjust=True)
index_returns = index_data['Close'].pct_change().dropna()
index_returns = pd.DataFrame(index_returns)
index_returns.columns = ['Returns']

# Save index_returns.csv
index_returns.to_csv("data/index_returns.csv", index_label='Date')
print("Index returns saved to data/index_returns.csv")

# -----------------------
# Download factor data
# -----------------------
factor_data = pd.DataFrame()

for name, symbol in factor_symbols.items():
    print(f"Downloading factor: {name} ({symbol})")
    df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)
    # df is now a single-index DataFrame, 'Close' is already adjusted
    factor_data[name] = df['Close'].pct_change()

# -----------------------
# Add CPI and Interest Rate manually
# -----------------------
dates = factor_data.index
factor_data['CPI'] = 0.001 + 0.0001 * pd.Series(range(len(dates)), index=dates)
factor_data['Interest_Rate'] = 0.002 + 0.00005 * pd.Series(range(len(dates)), index=dates)

# Reorder columns
factor_data = factor_data[['CPI', 'Interest_Rate', 'Oil', 'FX', 'VIX']]

# Drop rows with missing values
factor_data = factor_data.dropna()

# Save factors.csv
factor_data.to_csv("data/factors.csv", index_label='Date')
print("Factors saved to data/factors.csv")

# -----------------------
# Align index and factors
# -----------------------
aligned_data = index_returns.join(factor_data, how='inner')
aligned_data.to_csv("data/aligned_data.csv", index_label='Date')
print("Aligned data saved to data/aligned_data.csv")

print("\n✅ Data download and preprocessing complete!")
