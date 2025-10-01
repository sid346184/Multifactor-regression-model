import pandas as pd
import statsmodels.api as sm
import numpy as np
import os

# -----------------------------
# CONFIG
# -----------------------------
DATA_PATH = "data/aligned_data.csv"
OUTPUT_JSON = "outputs/factor_contributions.json"
OUTPUT_COEFF = "outputs/regression_coefficients.csv"
OUTPUT_SUMMARY = "outputs/summary_report.txt"

# -----------------------------
# Load aligned data
# -----------------------------
data = pd.read_csv(DATA_PATH, parse_dates=['Date'], index_col='Date')

# -----------------------------
# Regression setup
# -----------------------------
X = data.drop(columns=['Returns'])
y = data['Returns']
X = sm.add_constant(X)

# Fit OLS model
model = sm.OLS(y, X).fit()
print(model.summary())

# -----------------------------
# Save regression coefficients
# -----------------------------
coefficients = model.params
coefficients.to_csv(OUTPUT_COEFF)

# -----------------------------
# Compute contributions per day
# -----------------------------
contributions = X.multiply(coefficients, axis=1)
contributions['Predicted_Return'] = contributions.sum(axis=1)

# Reset index to include Date column
contributions.reset_index(inplace=True)

# Save machine-readable JSON
os.makedirs("outputs", exist_ok=True)
contributions.to_json(OUTPUT_JSON, orient='records', date_format='iso')
print(f"Factor contributions saved to {OUTPUT_JSON}")

# -----------------------------
# Human-readable summary with dynamic interpretations
# -----------------------------
# Identify top contributing factors (absolute average impact)
factors = [c for c in contributions.columns if c not in ['Date', 'Predicted_Return', 'const']]
avg_contrib = contributions[factors].mean()
top_factors = avg_contrib.abs().sort_values(ascending=False).head(3).index.tolist()

# Dynamic factor interpretations
factor_interpretation = {
    "VIX": "Higher market volatility negatively impacts index returns.",
    "Gold": "Rising gold prices may indicate investor hedging or risk-off behavior, positively affecting returns.",
    "FX": "Currency fluctuations influence export/import-heavy companies, affecting returns.",
    "Oil": "Changes in oil prices affect energy-related sectors and inflation expectations.",
    "CPI": "Higher inflation can impact market sentiment and returns.",
    "Interest_Rate": "Rising rates may increase discounting of future cash flows, affecting index returns."
}

# Generate summary
summary_lines = []
summary_lines.append("### Multi-Factor Attribution Summary\n")

for factor in top_factors:
    direction = "positive" if avg_contrib[factor] > 0 else "negative"
    magnitude = avg_contrib[factor]
    interpretation = factor_interpretation.get(
        factor,
        f"{factor} contributes to index returns based on market/sector dynamics."
    )
    summary_lines.append(
        f"**{factor}** had a {direction} impact on index returns, "
        f"with an average contribution of {magnitude:.5f} per day. {interpretation}"
    )

# Overall explained return
total_explained = contributions[factors].sum(axis=1).mean()
summary_lines.append(f"\nOverall, the model explains an average of {total_explained:.5f} of daily index returns.")

# Save summary report
with open(OUTPUT_SUMMARY, "w") as f:
    f.write("\n".join(summary_lines))

# Print summary to console
print("\n".join(summary_lines))
