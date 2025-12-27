"""
Cleaning pipeline for UK Business Births 2019 dataset.

"""

from pathlib import Path
import pandas as pd


def load_births_2019(path: str | Path) -> pd.DataFrame:
    """Load raw UK business births 2019 dataset."""
    return pd.read_csv(path)


def clean_births_2019(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare UK business births 2019 data."""
    df = df.copy()

    # Drop fully empty rows
    df = df.dropna(how="all")

    # Keep only first 3 useful columns (code, region, value)
    df = df.iloc[:, :3]

    # Remove metadata / header rows where first cell is NaN or the word 'Code'
    df = df[df.iloc[:, 0].notna()]
    df.columns = ["code", "region", "births_2019"]
    df = df[df["code"] != "Code"]
    df = df[df["region"].notna()]

    # Clean numeric formatting
    df["births_2019"] = (
        df["births_2019"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(":", "", regex=False)
        .str.strip()
    )
    df["births_2019"] = pd.to_numeric(df["births_2019"], errors="coerce")

    # Drop rows with no numeric value
    df = df.dropna(subset=["births_2019"]).reset_index(drop=True)

    # Professional column titles
    df = df.rename(
        columns={
            "code": "Geography Code",
            "region": "Geography Name",
            "births_2019": "Number of Business Births (2019)",
        }
    )

    return df


def save_births_2019(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw = PROJECT_ROOT / "data" / "raw" / "uk_business_births.csv"
    out = PROJECT_ROOT / "data" / "processed" / "uk_business_births_2019_clean.csv"

    print("PROJECT ROOT:", PROJECT_ROOT)
    print("RAW PATH:", raw)

    raw_df = load_births_2019(raw)
    clean_df = clean_births_2019(raw_df)
    save_births_2019(clean_df, out)

    print("Saved cleaned data to:", out)

