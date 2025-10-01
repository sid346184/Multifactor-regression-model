import pandas as pd
import statsmodels.api as sm
import numpy as np

# Load aligned data
data = pd.read_csv("data/aligned_data.csv", parse_dates=['Date'], index_col='Date')

# Regression setup
X = data.drop(columns=['Returns'])
y = data['Returns']
X = sm.add_constant(X)

# Fit model
model = sm.OLS(y, X).fit()
print(model.summary())

# Save regression coefficients
coefficients = model.params
coefficients.to_csv("outputs/regression_coefficients.csv")

# Compute contributions per day
contributions = X.multiply(coefficients, axis=1)
contributions['Predicted_Return'] = contributions.sum(axis=1)

# Reset index so 'Date' is a column
contributions.reset_index(inplace=True)

# Save machine-readable JSON
contributions.to_json("outputs/factor_contributions.json", orient='records', date_format='iso')
print("Factor contributions saved to outputs/factor_contributions.json")

# --- Human-readable summary with economic intuition ---
factor_intuition = {
    'CPI': 'Inflation changes can affect purchasing power and stock valuations',
    'Interest_Rate': 'Rate changes affect borrowing costs and company valuations',
    'Oil': 'Changes in oil prices affect energy and industrial sectors',
    'FX': 'Currency fluctuations influence export/import-heavy companies',
    'VIX': 'Higher market volatility negatively impacts returns'
}

factors = [c for c in contributions.columns if c not in ['Date', 'Predicted_Return', 'const']]
avg_contrib = contributions[factors].mean()

# Sort by absolute impact
top_factors = avg_contrib.abs().sort_values(ascending=False).head(3).index.tolist()

summary_lines = ["### Multi-Factor Attribution Summary\n"]

for factor in top_factors:
    direction = "positive" if avg_contrib[factor] > 0 else "negative"
    magnitude = avg_contrib[factor]
    intuition = factor_intuition.get(factor, "")
    summary_lines.append(
        f"**{factor}** had a {direction} impact on index returns, "
        f"with an average contribution of {magnitude:.5f} per day. {intuition}"
    )

# Optional: overall explained return
total_explained = contributions[factors].sum(axis=1).mean()
summary_lines.append(f"\nOverall, the model explains an average of {total_explained:.5f} of daily index returns.")

# Save summary report
with open("outputs/summary_report.txt", "w") as f:
    f.write("\n".join(summary_lines))

# Print summary to console
print("\n".join(summary_lines))
