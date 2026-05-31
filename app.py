import streamlit as st

st.set_page_config(
    page_title="Football Forecast App",
    page_icon="⚽",
    layout="wide"
)

if "history_df" not in st.session_state:
    st.session_state.history_df = None

if "matches_df" not in st.session_state:
    st.session_state.matches_df = None

if "predictions_df" not in st.session_state:
    st.session_state.predictions_df = None

st.title("⚽ Football Forecast & Performance Analysis")
st.write(
    "Use the sidebar to upload history, explore football data, and generate match forecasts."
)

st.info("Open the pages in the left sidebar to begin.")