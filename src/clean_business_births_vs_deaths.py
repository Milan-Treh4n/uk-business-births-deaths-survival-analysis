"""
Clean business_birth_death_rates.csv into a tidy Year / Birth / Death % table.
"""

from pathlib import Path
import pandas as pd


def load_raw(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def detect_year_and_rate_columns(df: pd.DataFrame) -> tuple[str, str, str]:
    numeric = df.apply(pd.to_numeric, errors="coerce")

    # --- year column ---
    year_candidates = []
    for col in df.columns:
        col_series = numeric[col]
        n_year_like = col_series.between(2000, 2100).sum()
        year_candidates.append((col, n_year_like))

    year_col = max(year_candidates, key=lambda x: x[1])[0]

    # --- rate columns (0–100) ---
    rate_candidates = []
    for col in df.columns:
        if col == year_col:
            continue
        col_series = numeric[col]
        n_rate_like = col_series.between(0, 100).sum()
        if n_rate_like >= 3:  # needs to look like a real column
            rate_candidates.append((col, n_rate_like))

    # sort best first
    rate_candidates.sort(key=lambda x: x[1], reverse=True)

    if len(rate_candidates) < 2:
        raise ValueError("Could not find two rate-like columns in the file.")

    # try to use names to decide births vs deaths
    births_col = None
    deaths_col = None
    for col, _ in rate_candidates:
        name = col.lower()
        if "birth" in name and births_col is None:
            births_col = col
        elif "death" in name and deaths_col is None:
            deaths_col = col

    # if still missing, fall back to the top 2
    if births_col is None:
        births_col = rate_candidates[0][0]
    if deaths_col is None:
        # pick the best candidate that isn't the births column
        deaths_col = next(col for col, _ in rate_candidates if col != births_col)

    return year_col, births_col, deaths_col


def clean_business_birth_death_rates(df: pd.DataFrame) -> pd.DataFrame:
    year_col, births_col, deaths_col = detect_year_and_rate_columns(df)

    numeric = df.apply(pd.to_numeric, errors="coerce")

    year_series = numeric[year_col]
    births_series = numeric[births_col]
    deaths_series = numeric[deaths_col]

    mask = (
        year_series.between(2000, 2100)
        & births_series.notna()
        & deaths_series.notna()
    )

    cleaned = pd.DataFrame(
        {
            "Year": year_series[mask].astype(int),
            "Birth Rate (%)": births_series[mask],
            "Death Rate (%)": deaths_series[mask],
        }
    ).reset_index(drop=True)

    # sort by year just in case
    cleaned = cleaned.sort_values("Year").reset_index(drop=True)
    return cleaned


def save_clean(df: pd.DataFrame, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    raw_path = PROJECT_ROOT / "data" / "raw" / "business_birth_death_rates.csv"
    out_path = PROJECT_ROOT / "data" / "processed" / "business_birth_death_rates_clean.csv"

    raw_df = load_raw(raw_path)
    clean_df = clean_business_birth_death_rates(raw_df)
    save_clean(clean_df, out_path)

    print(f"Saved cleaned file to: {out_path}")
    print(clean_df)
