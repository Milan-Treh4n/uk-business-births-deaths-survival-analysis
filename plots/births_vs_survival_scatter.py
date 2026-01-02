import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "business_survival_rates_2019_clean.csv"
)

# Columns from your dataset
region_col = "Region"
one_year_col = "Surviving After 1 Year – Count"
five_year_col = "Surviving After 5 Years – Count"
births_col = "Births of New Enterprises (2019)"

# Keep relevant columns only
df = df[[region_col, births_col, one_year_col, five_year_col]].dropna()

# Remove total row
df = df[df[region_col].str.lower() != "total"]

# Handle duplicated regions (keep first occurrence)
df = df.groupby(region_col, as_index=False).first()

# Select top 10 regions by number of births (most meaningful)
df = df.sort_values(births_col, ascending=False).head(10)

# Plot setup
x = np.arange(len(df))
width = 0.35

plt.figure(figsize=(12, 6))
plt.bar(x - width / 2, df[one_year_col], width, label="Survived 1 Year", color="navy")
plt.bar(x + width / 2, df[five_year_col], width, label="Survived 5 Years", color="skyblue")

plt.xticks(x, df[region_col], rotation=45, ha="right")
plt.ylabel("Number of Businesses")
plt.title("Business Survival: 1-Year vs 5-Year Outcomes (2019 Cohort)")
plt.legend()
plt.tight_layout()

# Save plot
plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)
out_path = plots / "survival_1yr_vs_5yr_2019.png"
plt.savefig(out_path, dpi=300)

# Show locally only
if os.environ.get("CI") != "true":
    plt.show()

print("Saved:", out_path)



