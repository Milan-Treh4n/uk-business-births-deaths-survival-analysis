import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "uk_business_births_2019_clean.csv"
)

df = df.sort_values("Number of Business Births (2019)", ascending=False)

# remove first 4 non-regional entries
df = df.iloc[4:]

top_n = min(15, len(df))
df = df.head(top_n)

plt.figure(figsize=(10, 6))
plt.barh(df["Geography Name"], df["Number of Business Births (2019)"])
plt.xlabel("Number of Business Births")
plt.ylabel("Region")
plt.title(f"Top {top_n} Regions – Business Births (2019)")
plt.tight_layout()

plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)
plt.savefig(plots / "business_births_top_regions_2019.png", dpi=300)
plt.show()



