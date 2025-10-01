import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

data = pd.read_csv("data/aligned_data.csv", parse_dates=['Date'], index_col='Date')

X = data.drop(columns=['Returns'])
y = data['Returns']


X_sm = sm.add_constant(X)
ols_model = sm.OLS(y, X_sm).fit()
print("----- OLS Summary -----")
print(ols_model.summary())


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ridge_model = Ridge(alpha=0.01).fit(X_train, y_train)
lasso_model = Lasso(alpha=0.001).fit(X_train, y_train)

# R^2 on test set
ridge_r2 = r2_score(y_test, ridge_model.predict(X_test))
lasso_r2 = r2_score(y_test, lasso_model.predict(X_test))

print(f"\nRidge R^2 on test set: {ridge_r2:.4f}")
print(f"Lasso R^2 on test set: {lasso_r2:.4f}")


coefficients = ols_model.params
coefficients.to_csv("outputs/regression_coefficients.csv")

contributions = X_sm.multiply(coefficients, axis=1)
contributions['Predicted_Return'] = contributions.sum(axis=1)
contributions.reset_index(inplace=True)  # include Date

contributions.to_json("outputs/factor_contributions.json", orient='records', date_format='iso')
print("Factor contributions saved to outputs/factor_contributions.json")


factor_interpretation = {
    "VIX": "Higher market volatility negatively impacts index returns.",
    "Gold": "Rising gold prices may indicate investor hedging or risk-off behavior, positively affecting returns.",
    "FX": "Currency fluctuations influence export/import-heavy companies, affecting returns.",
    "Oil": "Changes in oil prices affect energy-related sectors and inflation expectations.",
    "CPI": "Higher inflation can impact market sentiment and returns.",
    "Interest_Rate": "Rising rates may increase discounting of future cash flows, affecting index returns."
}

factors = [c for c in contributions.columns if c not in ['Date', 'Predicted_Return', 'const']]
avg_contrib = contributions[factors].mean().sort_values(key=abs, ascending=False)
top_factors = avg_contrib.head(3).index.tolist()

summary_lines = ["### Multi-Factor Attribution Summary\n"]
for factor in top_factors:
    direction = "positive" if avg_contrib[factor] > 0 else "negative"
    magnitude = avg_contrib[factor]
    interpretation = factor_interpretation.get(factor, f"{factor} contributes to index returns based on market/sector dynamics.")
    summary_lines.append(
        f"**{factor}** had a {direction} impact on index returns, "
        f"with an average contribution of {magnitude:.5f} per day. {interpretation}"
    )

total_explained = contributions[factors].sum(axis=1).mean()
summary_lines.append(f"\nOverall, the model explains an average of {total_explained:.5f} of daily index returns.")

summary_lines.append(f"\nRidge R^2 on test set: {ridge_r2:.4f}")
summary_lines.append(f"Lasso R^2 on test set: {lasso_r2:.4f}")

with open("outputs/summary_report.txt", "w") as f:
    f.write("\n".join(summary_lines))

print("\n".join(summary_lines))
