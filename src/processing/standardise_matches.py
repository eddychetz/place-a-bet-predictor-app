import pandas as pd
from src.utils.dates import to_datetime_column

def standardise_matches(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df = to_datetime_column(df, "date")

    for col in ["home_score", "away_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Create target label if scores available
    if {"home_score", "away_score"}.issubset(df.columns):
        df["target"] = df.apply(_derive_result, axis=1)

    return df

def _derive_result(row):
    if pd.isna(row["home_score"]) or pd.isna(row["away_score"]):
        return None
    if row["home_score"] > row["away_score"]:
        return "H"
    elif row["home_score"] < row["away_score"]:
        return "A"
    return "D"