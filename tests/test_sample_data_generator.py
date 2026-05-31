import pandas as pd
from src.ingestion.sample_data_generator import generate_sample_data
from src.processing.clean_history import clean_history
from src.utils.validators import check_required_columns
from src.config.schema import HISTORY_REQUIRED_COLUMNS


def test_generate_sample_data_structure():
    df = generate_sample_data(n_rows=50)

    # ✅ Check it's a DataFrame
    assert isinstance(df, pd.DataFrame), "Output is not a DataFrame"

    # ✅ Check number of rows
    assert len(df) == 50, "Incorrect number of rows generated"

    # ✅ Check required columns exist
    for col in HISTORY_REQUIRED_COLUMNS:
        assert col in df.columns, f"Missing column: {col}"


def test_generate_sample_data_types():
    df = generate_sample_data(n_rows=20)

    # ✅ Basic type checks
    assert df["date"].dtype == object, "Date column should be string before cleaning"
    assert pd.api.types.is_numeric_dtype(df["odds"]), "Odds must be numeric"
    assert pd.api.types.is_numeric_dtype(df["stake"]), "Stake must be numeric"


def test_clean_history_pipeline():
    df = generate_sample_data(n_rows=30)
    clean_df = clean_history(df)

    # ✅ Check not empty
    assert not clean_df.empty, "Cleaned dataframe is empty"

    # ✅ Check date conversion
    assert pd.api.types.is_datetime64_any_dtype(
        clean_df["date"]
    ), "Date not converted to datetime"

    # ✅ Check no missing required columns
    missing = check_required_columns(clean_df, HISTORY_REQUIRED_COLUMNS)
    assert not missing, f"Missing columns after cleaning: {missing}"


def test_result_values():
    df = generate_sample_data(n_rows=50)

    valid_results = {"win", "loss"}

    assert set(df["result"].unique()).issubset(
        valid_results
    ), "Invalid result values detected"


def test_basic_statistics():
    df = generate_sample_data(n_rows=100)

    # ✅ Odds should be reasonable
    assert df["odds"].between(1.3, 3.5).all(), "Odds out of expected range"

    # ✅ Stake should be positive
    assert (df["stake"] > 0).all(), "Stake must be positive"

    # ✅ Data variability check
    assert df["league"].nunique() > 1, "Not enough league variability"
