"""
Cleaning pipeline for business survival rates data.

"""


from pathlib import Path
import pandas as pd

# Load

def load_business_survival_rates(path: str | Path) -> pd.DataFrame:
    """
    Load raw business survival rates dataset.
    """
    return pd.read_csv(path)

# Clean

def clean_business_survival_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare business survival rates data.

    Steps:
    - standardise column names
    - drop completely empty rows
    - convert numeric-looking columns to numeric
    - drop rows missing key fields (year / survival-related columns)
    """
    df = df.copy()

    # Standardise column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Drop completely empty rows
    df = df.dropna(how="all")

    # Convert likely numeric columns
    numeric_cols = [
        col for col in df.columns
        if any(keyword in col for keyword in ["year", "rate", "percent"])
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows missing key values
    key_cols = [c for c in df.columns if "year" in c or "survival" in c]
    if key_cols:
        df = df.dropna(subset=key_cols)

    # Sort chronologically if year exists
    if "year" in df.columns:
        df = df.sort_values("year")

    return df.reset_index(drop=True)


# -----------------------------
# Save
# -----------------------------

def save_clean_business_survival_rates(
    df: pd.DataFrame,
    output_path: str | Path
) -> None:
    """
    Save cleaned survival rates dataset.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

# Run as script

if __name__ == "__main__":
    # Project root = folder above src/
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw_path = PROJECT_ROOT / "data" / "raw" / "business_survival_rates.csv"
    clean_path = PROJECT_ROOT / "data" / "processed" / "business_survival_rates_clean.csv"

    print("PROJECT ROOT:", PROJECT_ROOT)
    print("RAW PATH:", raw_path)

    raw_df = load_business_survival_rates(raw_path)
    clean_df = clean_business_survival_rates(raw_df)
    save_clean_business_survival_rates(clean_df, clean_path)

    print("Saved cleaned data to:", clean_path)
