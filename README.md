# ⚽ Place-a-Bet Predictor App

A Streamlit-based AI application for:

- Football match forecasting
- Betting history analysis
- Feature engineering + machine learning

## 🚀 Features

- Upload betting history CSV
- Generate sample data
- Build match features
- Train ML model
- Predict match outcomes

## 🧪 Tech Stack

- Python
- Streamlit
- Pandas / Scikit-learn
- APIs (football-data, Understat)

## ▶️ Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Setup

### 1. Create virtual environment

- `python -m venv .venv`

### 2. Activate environment

Windows:

- `.venv\Scripts\activate`

Mac/Linux:

- `source .venv/bin/activate`

### 3. Install requirements

- `pip install -r requirements.txt`

### 4. Create .env

- Copy `.env` to `.env` and add your API keys.

### 5. Run app

- `streamlit run app.py`

---

The application will have three capabilities:

### 1. Match intelligence

- historical fixtures
- team form
- goals / xG / streaks
- probability forecasts for outcomes

### 2. User history analysis

- import/export past betting history as CSV
- analyze stake patterns, win/loss trends, favorite leagues/teams
- evaluate whether historical choices correlate with model probabilities

### 3. Simulation / education

- let a user test “what-if” scenarios
- compare model confidence vs actual match results
- visualize confidence, uncertainty and drift

## PROJECT PLAN

## Data sources

For structured football data, use APIs and documented libraries instead of fragile account scraping:

- `football-data.org` documents access to football data such as matches, standings, teams, squads, and related entities.
- `Understat` Python libraries expose expected-goals style data and related football statistics.
- `Odds APIs` provide bookmaker odds and markets through structured API responses rather than HTML scraping.

## Project Architecture

┌────────────────────────────────────────────────────────────┐
│                                                        Streamlit Front End                                                                   │
│                               Upload CSV | Explore Data | Forecast | Explain | Monitor                                 │
└────────────────────────────────────────────────────────────┘
                                                                  │
                                                                 ▼
┌────────────────────────────────────────────────────────────┐
│                                                 Application Layer                                                                             │
│                       Orchestration | Validation | Feature Service | Inference                                            │
└────────────────────────────────────────────────────────────┘
                                                                 │
                        ┌───────────────┼────────────────┬────────────────┐
                       ▼                                      ▼                                       ▼                                        ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Data Ingestion                 │ │ Feature Store                   │ │ Model Service                 │ │ Monitoring                        │
│ APIs / CSV                       │ │ engineered vars               │ │ train / infer                       │ │ drift / scores                    │
└────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
                     │                                          │                                                 │                                │
                    ▼                                         ▼                                               ▼                               ▼
┌────────────────────────────────────────────────────────────┐
│                                                     Storage / Persistence                                                                  │
│                                Raw data | Clean data | Predictions | Logs | Model files                                  │
└────────────────────────────────────────────────────────────┘

## Data ingestion design

### A. Football data ingestion

#### Recommended approach

- Pull fixtures, results, standings, and team data from football-data.org. The documentation explicitly describes competitions, seasons, matches, teams, and standings.
- Pull advanced metrics such as xG using an Understat Python wrapper/library. The Understat docs and packages explicitly expose player, team, league, and match-related football data.
- If you want market context, consume odds data via an API, not via bookmaker account scraping. The Odds API documents bookmaker odds and betting markets in JSON.

## User Betting History Ingestion

Recommended approach

Let the user upload CSV files exported from a tracker or export tool.
If the user has no export, support a manual schema template:

- date
- event
- league
- selection
- stake
- odds
- result
- return

This is more robust than scraping a logged-in site and easier to maintain.

## Feature engineering architecture

### A. Match-level features

- Build a feature service that computes:

#### Team performance

- recent wins / draws / losses
- goals scored/conceded in last N matches
- home vs away strength
- clean sheets
- goal difference trend

#### Advanced metrics

- xG for / xG against
- xG difference trend
- shot quality proxies
- finishing vs expected performance gap

#### Schedule / context

- days since last match
- competition strength
  league position
- match importance proxy

### Market context (optional)

If you legally consume odds API data:

- opening odds
- closing odds
- implied probability
- odds movement

#### B. User history features

If a user uploads history:

- average stake
  -preferred leagues
- preferred teams
- historical hit rate by market type
- return distribution
- variance of outcomes

#### C. Explainability features

Prepare derived values for UI explanations:

- feature contribution table
- probability confidence bucket
- calibration bucket
- error category

## Model layer

- Recommended modelling strategy

### Model 1 — Baseline classifier

#### Predict

- `Home Win`
- `Draw`
- `Away Win`

Use:

Logistic Regression
Random Forest
XGBoost / LightGBM (if available in your environment)

Model 2 — Goals model
Predict:

expected home goals
expected away goals

Use:

Poisson regression
Gradient boosting regression

Model 3 — Confidence calibration
After modelling, calibrate probabilities:

isotonic calibration
Platt scaling

Model 4 — Performance tracker
A scoring layer that compares:

model probability
actual result
historical user behaviour

## Evaluation metrics

### For classification

- log loss
- Brier score
- accuracy
- F1 (secondary)

### For goals

- MAE
- RMSE

#### For confidence

- calibration curve
- reliability by bucket

My recommendation: start with a simple baseline and prove value before adding complex deep learning.

## Inference architecture

Prediction flow
When a user selects a fixture:

- fetch latest team data
- fetch or compute engineered features
- align feature schema with training schema
- load best model
- generate probabilities
- run explanation layer
- save prediction + timestamp to log store
  d display result in Streamlit

## Project Structure

place-a-bet-predictor/
│
├── app.py
├── pages/
│   ├── home.py
│   ├── upload_history.py
│   ├── data_explorer.py
│   ├── forecast.py
│   └── model_evaluation.py
│
├── src/
│   ├── config/
│   │   ├── settings.py
│   │   └── schema.py
│   ├── ingestion/
│   │   ├── football_data_client.py
│   │   ├── understat_client.py
│   │   ├── odds_client.py
│   │   └── csv_loader.py
│   ├── processing/
│   │   ├── clean_matches.py
│   │   ├── clean_history.py
│   │   └── standardise.py
│   ├── features/
│   │   ├── match_features.py
│   │   ├── team_form.py
│   │   └── user_features.py
│   ├── models/
│   │   ├── train.py
│   │   ├── predict.py
│   │   ├── evaluate.py
│   │   └── explain.py
│   ├── services/
│   │   ├── inference_service.py
│   │   └── storage_service.py
│   └── utils/
│       ├── dates.py
│       ├── io.py
│       └── validators.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── features/
│   └── exports/
│
├── models/
├── tests/
├── requirements.txt
└── README.md

---

### 🚀 OPTIONAL — Deploy your Streamlit app

Once it's on GitHub:

👉 Use Streamlit Cloud

- Connect [GitHub]() account
- Select repo + branch
- Click **Deploy** 【2-a90bb6】

---

## Best workflow going forward

Every time you update your code:

```bash
git add .
git commit -m "Added OCR feature"
git push