import pandas as pd
from src.utils.dates import to_datetime_column

def clean_history(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df = to_datetime_column(df, "date")

    numeric_cols = ["odds", "stake"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "result" in df.columns:
        df["result"] = df["result"].astype(str).str.strip().str.lower()

    return df