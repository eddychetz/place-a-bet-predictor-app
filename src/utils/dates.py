import pandas as pd

def to_datetime_column(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], errors="coerce")
    return df