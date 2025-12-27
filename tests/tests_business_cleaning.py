import pandas as pd

from src.clean_business_survival_rates import clean_business_survival_rates
from src.clean_uk_business_births import clean_uk_business_births
from src.clean_uk_business_deaths import clean_uk_business_deaths


# ---------- Business survival rates ----------

def test_survival_cleaning_standardises_columns_and_numeric():
    df = pd.DataFrame({
        " Year ": ["2020"],
        "Survival Rate": ["95"]
    })

    cleaned = clean_business_survival_rates(df)

    # column names are cleaned
    assert "year" in cleaned.columns
    assert "survival_rate" in cleaned.columns

    # values converted to numeric
    assert cleaned["year"].dtype.kind in "if"
    assert cleaned["survival_rate"].dtype.kind in "if"


def test_survival_cleaning_drops_empty_rows():
    df = pd.DataFrame({
        "Year": [2020, None],
        "Survival Rate": [90, None]
    })

    cleaned = clean_business_survival_rates(df)

    # second row is completely empty and should be dropped
    assert len(cleaned) == 1


# ---------- UK business births ----------

def test_births_cleaning_converts_births_to_numeric_and_drops_missing():
    df = pd.DataFrame({
        "Year": ["2020", "2021"],
        "Births": ["100", None]
    })

    cleaned = clean_uk_business_births(df)

    # births column should be numeric
    assert cleaned["births"].dtype.kind in "if"

    # row with missing births should be removed
    assert len(cleaned) == 1
    assert cleaned["year"].iloc[0] == 2020


def test_births_cleaning_removes_invalid_years():
    df = pd.DataFrame({
        "Year": [-1, 2020],
        "Births": [50, 100]
    })

    cleaned = clean_uk_business_births(df)

    # negative year should be removed
    assert (cleaned["year"] > 0).all()
    assert 2020 in cleaned["year"].values


# ---------- UK business deaths ----------

def test_deaths_cleaning_converts_deaths_to_numeric_and_drops_missing():
    df = pd.DataFrame({
        "Year": ["2020", "2021"],
        "Deaths": ["80", None]
    })

    cleaned = clean_uk_business_deaths(df)

    # deaths column should be numeric
    assert cleaned["deaths"].dtype.kind in "if"

    # row with missing deaths should be removed
    assert len(cleaned) == 1
    assert cleaned["year"].iloc[0] == 2020


def test_deaths_cleaning_removes_invalid_years():
    df = pd.DataFrame({
        "Year": [0, 2022],
        "Deaths": [10, 20]
    })

    cleaned = clean_uk_business_deaths(df)

    # year 0 should be removed
    assert (cleaned["year"] > 0).all()
    assert 2022 in cleaned["year"].values
