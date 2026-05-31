import pandas as pd

def build_match_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values("date")

    # Very simple starter features
    df["goal_diff"] = df["home_score"].fillna(0) - df["away_score"].fillna(0)
    df["total_goals"] = df["home_score"].fillna(0) + df["away_score"].fillna(0)

    # Rolling averages by home team
    df["home_team_avg_scored_last5"] = (
        df.groupby("home_team")["home_score"]
        .transform(lambda s: s.shift(1).rolling(5, min_periods=1).mean())
    )

    df["home_team_avg_conceded_last5"] = (
        df.groupby("home_team")["away_score"]
        .transform(lambda s: s.shift(1).rolling(5, min_periods=1).mean())
    )

    df["away_team_avg_scored_last5"] = (
        df.groupby("away_team")["away_score"]
        .transform(lambda s: s.shift(1).rolling(5, min_periods=1).mean())
    )

    df["away_team_avg_conceded_last5"] = (
        df.groupby("away_team")["home_score"]
        .transform(lambda s: s.shift(1).rolling(5, min_periods=1).mean())
    )

    return df