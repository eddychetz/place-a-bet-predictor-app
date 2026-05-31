import streamlit as st
import plotly.express as px
from src.ingestion.football_data_client import FootballDataClient
from src.processing.standardise_matches import standardise_matches
from src.ingestion.sample_data_generator import generate_sample_data

st.title("📊 Data Explorer")

competition_code = st.text_input("Competition code", value="PL")

if st.button("Load competition matches"):
    client = FootballDataClient()
    df = client.get_competition_matches(competition_code=competition_code)
    df = standardise_matches(df)
    st.session_state.matches_df = df
    st.success("Matches loaded into session.")

if st.button("Generate sample data"):
    df = generate_sample_data(100)
    st.session_state.history_df = df
    st.success("Sample data generated!")
    st.dataframe(df.head())

    missing = check_required_columns(df, HISTORY_REQUIRED_COLUMNS)

    if missing:
        st.error(f"Missing required columns: {missing}")
    else:
        st.session_state.history_df = df
        st.success("History uploaded and validated successfully.")
        st.dataframe(df.head(20), use_container_width=True)

if st.session_state.matches_df is not None:
    df = st.session_state.matches_df
    st.dataframe(df.head(20), use_container_width=True)

    if "competition" in df.columns:
        fig = px.histogram(df, x="competition", title="Competition distribution")
        st.plotly_chart(fig, use_container_width=True)

    if {"home_score", "away_score"}.issubset(df.columns):
        df["total_goals"] = df["home_score"].fillna(0) + df["away_score"].fillna(0)
        fig2 = px.histogram(df, x="total_goals", title="Total goals distribution")
        st.plotly_chart(fig2, use_container_width=True)