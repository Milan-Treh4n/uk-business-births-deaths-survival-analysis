import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from clean_business_survival_2022 import clean_survival_2022
from clean_uk_business_births_2024 import clean_births_2024
from uk_business_deaths_2024 import clean_deaths_2024


def test_survival2022_cleaning_numeric_and_no_empty_rows():
    df = pd.DataFrame({
        "code": ["X1", None],
        "region": ["North East", None],
        "births_2022": ["10,000", None],
        "one_year_survivals": ["9,520", None],
        "one_year_survival_rate": ["95.2", None],
    })

    cleaned = clean_survival_2022(df)

    assert len(cleaned) == 1
    assert cleaned["Number of Business Births (2022)"].dtype.kind in "if"
    assert cleaned["1-Year Survival Rate (%)"].dtype.kind in "if"


def test_births2024_cleaning_numeric_and_drops_missing():
    df = pd.DataFrame({
        "Code": ["K02000001", None],
        "Region": ["UK", None],
        "Value": ["300,000", None],
    })

    cleaned = clean_births_2024(df)

    assert "Number of Business Births (2024)" in cleaned.columns
    assert cleaned["Number of Business Births (2024)"].dtype.kind in "if"
    assert len(cleaned) == 1


def test_deaths2024_cleaning_numeric_and_drops_missing():
    df = pd.DataFrame({
        "Code": ["K02000001", None],
        "Region": ["UK", None],
        "Value": ["250,000", None],
    })

    cleaned = clean_deaths_2024(df)

    assert "Number of Business Deaths (2024)" in cleaned.columns
    assert cleaned["Number of Business Deaths (2024)"].dtype.kind in "if"
    assert len(cleaned) == 1



