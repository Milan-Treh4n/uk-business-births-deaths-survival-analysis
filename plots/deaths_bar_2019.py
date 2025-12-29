import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Define the path to 2019 deaths data CSV file
PROJECT_ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "uk_business_deaths_2019_clean.csv"
)

df = df.sort_values("Number of Business Deaths (2019)", ascending=False)

# remove first 4 non-regional entries
df = df.iloc[4:]

# Create a horizontal bar chart with top 15 regions
df = df.head(15)
plt.figure(figsize=(10, 8))
plt.barh(df["Geography Name"], df["Number of Business Deaths (2019)"], color='skyblue')
plt.xlabel("Number of Business Deaths (2019)")
plt.title("Business Deaths by Region in the UK (2019)")
plt.tight_layout()

# Save the plot
plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)

plt.savefig(plots / "business_deaths_top_regions_2019.png", dpi=300)
plt.show()