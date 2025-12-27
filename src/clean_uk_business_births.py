"""
Cleaning pipeline for UK business births dataset.

"""

from pathlib import Path
import pandas as pd

# Load

def load_uk_business_births(path: str | Path) -> pd.DataFrame:
    """
    Load raw UK business births dataset.
    """
    return pd.read_csv(path)

# Clean

def clean_uk_business_births(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare UK business births data.
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
        if any(keyword in col for keyword in ["year", "birth", "count", "total"])
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows missing birth data
    key_cols = [c for c in df.columns if "birth" in c]
    if key_cols:
        df = df.dropna(subset=key_cols)

    # Remove invalid year values
    if "year" in df.columns:
        df = df[df["year"] > 0]

    return df.reset_index(drop=True)
# Save

def save_clean_uk_business_births(
    df: pd.DataFrame,
    output_path: str | Path
) -> None:
    """
    Save cleaned births dataset.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

# Run as script

if __name__ == "__main__":
    # Project root = folder above src/
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw_path = PROJECT_ROOT / "data" / "raw" / "uk_business_births.csv"
    clean_path = PROJECT_ROOT / "data" / "processed" / "uk_business_births_clean.csv"

    print("PROJECT ROOT:", PROJECT_ROOT)
    print("RAW PATH:", raw_path)

    raw_df = load_uk_business_births(raw_path)
    clean_df = clean_uk_business_births(raw_df)
    save_clean_uk_business_births(clean_df, clean_path)

    print("Saved cleaned data to:", clean_path)
