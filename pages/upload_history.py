import streamlit as st
from src.ingestion.csv_loader import load_uploaded_csv
from src.processing.clean_history import clean_history
from src.utils.validators import check_required_columns
from src.config.schema import HISTORY_REQUIRED_COLUMNS

st.title("📤 Upload History")

uploaded_file = st.file_uploader("Upload your history CSV", type=["csv"])

if uploaded_file is not None:
    df = load_uploaded_csv(uploaded_file)
    df = clean_history(df)

    missing = check_required_columns(df, HISTORY_REQUIRED_COLUMNS)

    if missing:
        st.error(f"Missing required columns: {missing}")
    else:
        st.session_state.history_df = df
        st.success("History uploaded and validated successfully.")
        st.dataframe(df.head(20), use_container_width=True)

if st.session_state.history_df is not None:
    st.markdown("### Current in session")
    st.dataframe(st.session_state.history_df.head(10), use_container_width=True)

from src.ingestion.sample_data_generator import generate_sample_data

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