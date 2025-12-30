import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

deaths_2019 = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "uk_business_deaths_2019_clean.csv"
)
deaths_2024 = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "uk_business_deaths_2024_clean.csv"
)
# Exclude top 4 non-regions
d19 = deaths_2019.sort_values("Number of Business Deaths (2019)", ascending=False).iloc[4:]
d24 = deaths_2024.sort_values("Number of Business Deaths (2024)", ascending=False).iloc[4:]

# Merge datasets on Geography Name
merged = d19[["Geography Name", "Number of Business Deaths (2019)"]].merge(
    d24[["Geography Name", "Number of Business Deaths (2024)"]],
    on="Geography Name",
    how="inner",
)

merged["Total"] = (
    merged["Number of Business Deaths (2019)"] + merged["Number of Business Deaths (2024)"]
)
merged = merged.sort_values("Total", ascending=False).head(15)

regions = merged["Geography Name"]
deaths19 = merged["Number of Business Deaths (2019)"]
deaths24 = merged["Number of Business Deaths (2024)"]

# Configure Plot
x = np.arange(len(regions))
width = 0.4

plt.figure(figsize=(12, 6))
plt.bar(x - width / 2, deaths19, width, label="2019", alpha=0.7, color='darkblue')
plt.bar(x + width / 2, deaths24, width, label="2024", alpha=0.7, color='skyblue')

plt.title("Business Deaths by Region – 2019 vs 2024 (Top 15 Regions)")
plt.xlabel("Region")
plt.ylabel("Number of Business Deaths")
plt.xticks(x, regions, rotation=45, ha="right")
plt.legend()
plt.tight_layout()

# Save Plot
plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)
out_path = plots / "business_deaths_2019_2024_comparison.png"
plt.savefig(out_path, dpi=300)
plt.show()

