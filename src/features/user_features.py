import pandas as pd

def build_user_history_features(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {}

    summary = {
        "total_rows": len(df),
        "avg_stake": float(df["stake"].mean()) if "stake" in df.columns else None,
        "avg_odds": float(df["odds"].mean()) if "odds" in df.columns else None,
        "top_league": (
            df["league"].mode().iloc[0] if "league" in df.columns and not df["league"].mode().empty else None
        ),
    }

    if "result" in df.columns:
        win_rate = (df["result"] == "win").mean()
        summary["win_rate"] = float(win_rate)

    return summary