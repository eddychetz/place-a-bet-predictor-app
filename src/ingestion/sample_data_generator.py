import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# -----------------------------
# Sample data pools
# -----------------------------
leagues = ["EPL", "LaLiga", "SerieA", "Bundesliga"]
teams = {
    "EPL": ["Arsenal", "Chelsea", "Liverpool", "Man City", "Spurs"],
    "LaLiga": ["Barcelona", "Real Madrid", "Sevilla", "Valencia"],
    "SerieA": ["Juventus", "AC Milan", "Inter", "Napoli"],
    "Bundesliga": ["Bayern", "Dortmund", "Leipzig", "Leverkusen"],
}

results = ["win", "loss"]


# -----------------------------
# Generator function
# -----------------------------
def generate_sample_data(n_rows=50):
    data = []

    start_date = datetime(2026, 1, 1)

    for i in range(n_rows):
        league = random.choice(leagues)
        home_team, away_team = random.sample(teams[league], 2)

        # selection = randomly either home or away team
        selection = random.choice([home_team, away_team])

        # generate odds (realistic range)
        odds = round(np.random.uniform(1.3, 3.5), 2)

        # generate stake
        stake = random.randint(10, 200)

        # assume 50% win probability biased by odds
        prob_win = 1 / odds
        result = "win" if random.random() < prob_win else "loss"

        row = {
            "date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "league": league,
            "home_team": home_team,
            "away_team": away_team,
            "selection": selection,
            "odds": odds,
            "stake": stake,
            "result": result,
        }

        data.append(row)

    return pd.DataFrame(data)


# -----------------------------
# Generate dataset
# -----------------------------
df = generate_sample_data(n_rows=100)

# Preview
print(df.head())

# Save to CSV
df.to_csv("sample_betting_history.csv", index=False)
