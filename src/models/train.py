import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.config.settings import settings

FEATURE_COLUMNS = [
    "home_team_avg_scored_last5",
    "home_team_avg_conceded_last5",
    "away_team_avg_scored_last5",
    "away_team_avg_conceded_last5",
]

def train_match_model(df):
    model_df = df.dropna(subset=FEATURE_COLUMNS + ["target"]).copy()

    X = model_df[FEATURE_COLUMNS]
    y = model_df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    report = classification_report(y_test, preds, output_dict=False)

    joblib.dump(model, settings.model_path)
    return model, report