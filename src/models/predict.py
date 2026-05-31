import joblib
import pandas as pd
from src.config.settings import settings
from src.models.train import FEATURE_COLUMNS

def load_model():
    return joblib.load(settings.model_path)

def predict_match(features_df: pd.DataFrame):
    model = load_model()
    X = features_df[FEATURE_COLUMNS]
    probs = model.predict_proba(X)
    classes = model.classes_

    out = features_df.copy()
    for idx, cls in enumerate(classes):
        out[f"prob_{cls}"] = probs[:, idx]

    out["predicted_outcome"] = model.predict(X)
    return out