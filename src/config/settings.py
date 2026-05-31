from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    football_data_api_key: str = os.getenv("FOOTBALL_DATA_API_KEY", "")
    odds_api_key: str = os.getenv("ODDS_API_KEY", "")
    app_env: str = os.getenv("APP_ENV", "dev")
    data_dir: str = "data"
    raw_dir: str = "data/raw"
    processed_dir: str = "data/processed"
    features_dir: str = "data/features"
    exports_dir: str = "data/exports"
    model_path: str = "models/match_outcome_model.joblib"

settings = Settings()