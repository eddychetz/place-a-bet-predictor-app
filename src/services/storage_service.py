from src.utils.io import save_csv, save_parquet

def persist_outputs(df, base_name, target_format="csv"):
    if target_format == "csv":
        save_csv(df, f"data/exports/{base_name}.csv")
    else:
        save_parquet(df, f"data/exports/{base_name}.parquet")