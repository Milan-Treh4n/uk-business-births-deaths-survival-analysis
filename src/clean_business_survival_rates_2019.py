"""
Cleaning pipeline for Business Survival by Region (2019 cohort).

"""

from pathlib import Path
import pandas as pd


def load_survival_2019(path: str | Path) -> pd.DataFrame:
    """Load raw survival table for 2019 cohort."""
    return pd.read_csv(path)


def clean_survival_2019(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and structure the 2019 regional survival table."""
    df = df.copy()

    # Drop fully empty rows
    df = df.dropna(how="all")

    # The first few rows are metadata:
    # 0: long title
    # 1: "This worksheet contains one table"
    # 2: "Units: ..."
    # 3: "2019"
    #
    # Data starts after that, so drop first 4 rows.
    df = df.iloc[4:, :]

    # Keep first 6 columns (region + 5 numeric columns)
    df = df.iloc[:, :6]

    # Rename columns to temporary technical names
    df.columns = [
        "region",
        "births_2019",
        "survive_1yr_count",
        "survive_1yr_rate",
        "survive_5yr_count",
        "survive_5yr_rate",
    ]

    # Drop any remaining non-region rows
    df = df[df["region"].notna()]

    # Clean numeric formatting for all numeric columns
    numeric_cols = [
        "births_2019",
        "survive_1yr_count",
        "survive_1yr_rate",
        "survive_5yr_count",
        "survive_5yr_rate",
    ]

    for col in numeric_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(":", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with no births (safety)
    df = df.dropna(subset=["births_2019"]).reset_index(drop=True)

    # Professional, readable titles
    df = df.rename(
        columns={
            "region": "Region",
            "births_2019": "Births of New Enterprises (2019)",
            "survive_1yr_count": "Surviving After 1 Year – Count",
            "survive_1yr_rate": "1-Year Survival Rate (2019 Cohort, %)",
            "survive_5yr_count": "Surviving After 5 Years – Count",
            "survive_5yr_rate": "5-Year Survival Rate (2019 Cohort, %)",
        }
    )

    return df


def save_survival_2019(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw = PROJECT_ROOT / "data" / "raw" / "business_survival_rates.csv"
    out = PROJECT_ROOT / "data" / "processed" / "business_survival_rates_2019_clean.csv"

    print("PROJECT ROOT:", PROJECT_ROOT)
    print("RAW PATH:", raw)

    raw_df = load_survival_2019(raw)
    clean_df = clean_survival_2019(raw_df)
    save_survival_2019(clean_df, out)

    print("Saved cleaned data to:", out)

