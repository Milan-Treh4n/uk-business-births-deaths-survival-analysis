import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path

# Project root (this file lives in /plots)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load dataset that already contains percentages
df = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "business_birth_death_rates_clean.csv"
)

# Assume structure: [Year, Births %, Deaths %]
years = df.iloc[:, 0]
births_pct = df.iloc[:, 1]
deaths_pct = df.iloc[:, 2]

# ---- Plot ----
plt.figure(figsize=(10, 6))

plt.plot(years, births_pct, marker="o", linewidth=3,
         color="navy", label="Business Birth Rate")
plt.plot(years, deaths_pct, marker="o", linewidth=3,
         color="skyblue", label="Business Death Rate")

plt.title("UK Business Birth & Death Rates (2019–2024)")
plt.xlabel("Year")
plt.ylabel("Rate (%)")

# Nice percentage formatting on y-axis
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1f}%"))

plt.grid(True, linestyle="--", alpha=0.5)
plt.xticks(years)  # show each year on x-axis
plt.legend()
plt.tight_layout()

# ---- Save ----
plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)
out_path = plots / "uk_business_birth_death_rates_2019_2024.png"
plt.savefig(out_path, dpi=300)
plt.show()

print("Saved plot to:", out_path)


