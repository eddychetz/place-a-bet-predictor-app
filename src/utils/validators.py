def check_required_columns(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    return missing