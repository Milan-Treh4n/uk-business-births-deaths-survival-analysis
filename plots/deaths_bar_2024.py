import matplotlib.pyplot as plt
import pandas as pd
import pathlib as path

# Load the data
PROJECT_ROOT = path.Path(__file__).resolve().parents[1]

df = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "uk_business_deaths_2024_clean.csv"
)

df = df.sort_values("Number of Business Deaths (2024)", ascending=False)

# Remove non-regional entries
df = df.iloc[4:]

# Create a horizontal bar chart with top 15 regions
df = df.head(15)
plt.figure(figsize=(10, 8))
plt.barh(df["Geography Name"], df["Number of Business Deaths (2024)"], color='skyblue')
plt.xlabel("Number of Business Deaths (2024)")
plt.title("Business Deaths by Region in the UK (2024)")
plt.tight_layout()

# Save the plot
plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)

plt.savefig(plots / "business_deaths_top_regions_2024.png", dpi=300)
plt.show()