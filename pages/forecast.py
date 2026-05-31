import streamlit as st
from src.features.match_features import build_match_features
from src.models.train import train_match_model
from src.services.inference_service import run_inference

st.title("🔮 Forecast")

if st.session_state.matches_df is None:
    st.warning("Please load match data first in the Data Explorer page.")
    st.stop()

matches_df = st.session_state.matches_df

if st.button("Build features"):
    feature_df = build_match_features(matches_df)
    st.session_state.feature_df = feature_df
    st.success("Features built.")
    st.dataframe(feature_df.head(20), use_container_width=True)

if "feature_df" in st.session_state and st.button("Train baseline model"):
    model, report = train_match_model(st.session_state.feature_df)
    st.session_state.training_report = report
    st.success("Model trained and saved.")
    st.text(report)

if "feature_df" in st.session_state and st.button("Run predictions"):
    preds = run_inference(st.session_state.feature_df.dropna())
    st.session_state.predictions_df = preds
    st.success("Predictions generated.")
    st.dataframe(preds.head(20), use_container_width=True)