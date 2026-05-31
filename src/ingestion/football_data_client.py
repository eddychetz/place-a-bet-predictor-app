import requests
import pandas as pd
from src.config.settings import settings

BASE_URL = "https://api.football-data.org/v4"

class FootballDataClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.football_data_api_key
        self.headers = {"X-Auth-Token": self.api_key} if self.api_key else {}

    def get_competition_matches(self, competition_code="PL"):
        url = f"{BASE_URL}/competitions/{competition_code}/matches"
        r = requests.get(url, headers=self.headers, timeout=30)
        r.raise_for_status()
        data = r.json()

        matches = data.get("matches", [])
        records = []
        for m in matches:
            records.append({
                "date": m.get("utcDate"),
                "competition": m.get("competition", {}).get("name"),
                "status": m.get("status"),
                "home_team": m.get("homeTeam", {}).get("name"),
                "away_team": m.get("awayTeam", {}).get("name"),
                "home_score": m.get("score", {}).get("fullTime", {}).get("home"),
                "away_score": m.get("score", {}).get("fullTime", {}).get("away"),
            })
        return pd.DataFrame(records)