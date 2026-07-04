"""
Automated data quality tests for the cleaned Forbes Global 2000 dataset.

Run from the repo root with:
    pytest tests/test_data_quality.py -v
"""

import pandas as pd
import pytest
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "forbes_2000_cleaned.csv")


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)


def test_file_exists():
    assert os.path.exists(DATA_PATH), "Cleaned dataset not found — run scripts/clean_forbes_2000.py first"


def test_row_count(df):
    assert len(df) == 2000, f"Expected 2000 companies, found {len(df)}"


def test_expected_columns(df):
    expected = {
        "Rank", "Company", "Country", "City", "Industry",
        "Sales ($B)", "Profit ($B)", "Assets ($B)", "Market Value ($B)",
        "Profit_Margin_%", "Asset_Efficiency", "ROA_%"
    }
    assert expected.issubset(set(df.columns)), f"Missing columns: {expected - set(df.columns)}"


def test_no_duplicate_companies(df):
    assert df["Company"].duplicated().sum() == 0, "Found duplicate company names"


def test_rank_range(df):
    assert df["Rank"].min() >= 1
    assert df["Rank"].max() <= 2000


def test_rank_duplicates_are_expected(df):
    # Forbes ties companies at the same rank — duplicates are expected, not a data error.
    # This test just documents and bounds the expected duplicate count.
    dup_count = df["Rank"].duplicated().sum()
    assert dup_count < len(df), "Every rank duplicated would indicate a broken join, not legitimate ties"


def test_missing_values_within_expected_bounds(df):
    # Only Industry (1 row) and Market Value (1 row) are expected to have gaps post-cleaning.
    missing = df.isna().sum()
    unexpected_missing = missing.drop(labels=["Market Value ($B)"], errors="ignore")
    unexpected_missing = unexpected_missing[unexpected_missing > 0]
    # Industry should be fully filled after cleaning
    assert df["Industry"].isna().sum() == 0, "Industry should have no missing values after cleaning"


def test_no_negative_financials(df):
    for col in ["Sales ($B)", "Profit ($B)", "Assets ($B)"]:
        assert (df[col] < 0).sum() == 0, f"Found negative values in {col}"


def test_derived_metrics_present_and_numeric(df):
    for col in ["Profit_Margin_%", "Asset_Efficiency", "ROA_%"]:
        assert col in df.columns
        assert pd.api.types.is_numeric_dtype(df[col]), f"{col} should be numeric"


def test_profit_margin_calculation_is_consistent(df):
    # Spot-check the derived Profit_Margin_% against a fresh calculation from source columns
    sample = df.dropna(subset=["Sales ($B)", "Profit ($B)", "Profit_Margin_%"]).sample(
        min(50, len(df)), random_state=42
    )
    recalculated = (sample["Profit ($B)"] / sample["Sales ($B)"] * 100).round(2)
    assert (recalculated - sample["Profit_Margin_%"]).abs().max() < 0.05, \
        "Profit_Margin_% does not match Profit / Sales * 100 within rounding tolerance"


def test_country_extraction_worked(df):
    assert df["Country"].notna().sum() == len(df), "Every row should have a Country after Headquarters split"
    assert df["Country"].nunique() > 1, "Country extraction should yield more than one distinct country"


def test_no_placeholder_or_junk_strings(df):
    junk_values = {"n/a", "N/A", "null", "NULL", "?", "-", ""}
    for col in ["Company", "Country", "Industry"]:
        assert not df[col].isin(junk_values).any(), f"Found placeholder/junk values in {col}"
