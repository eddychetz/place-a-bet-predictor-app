import streamlit as st
import streamlit as st
from src.ingestion.csv_loader import load_uploaded_csv
from src.processing.clean_history import clean_history
from src.utils.validators import check_required_columns
from src.config.schema import HISTORY_REQUIRED_COLUMNS

# ✅ Import generator
from src.ingestion.sample_data_generator import generate_sample_data

st.title("🏠 Home")
st.write("Welcome to the Football Forecast & Performance Analysis app.")

col1, col2, col3 = st.columns(3)
col1.metric(
    "History uploaded", "Yes" if st.session_state.history_df is not None else "No"
)
col2.metric(
    "Matches loaded", "Yes" if st.session_state.matches_df is not None else "No"
)
col3.metric(
    "Predictions ready", "Yes" if st.session_state.predictions_df is not None else "No"
)

st.markdown("### Suggested flow")
st.markdown("""
1. Upload betting/history CSV  
2. Load football match data  
3. Train baseline model  
4. Run forecasts  
5. Review evaluation results
""")
uploaded_image = st.file_uploader("Upload Bet Slip Image", type=["jpg", "png"])

if uploaded_image:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_image.getbuffer())

    df = process_image("temp.jpg")  # wrap OCR + parsing
    st.dataframe(df)

st.title("📤 Upload History")

uploaded_file = st.file_uploader("Upload your history CSV", type=["csv"])


st.title("📤 Upload History")

# -----------------------------
# CSV Upload
# -----------------------------
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

# -----------------------------
# ✅ ADD THIS SECTION (sample generator)
# -----------------------------
st.markdown("### 🔧 Or use sample data")

st.info("📥 No data? ⚙️ Generate sample betting history to test the app instantly.")

n_rows = st.slider("Number of sample rows", 10, 500, 100)

if st.button("♻️ Generate Sample Data"):
    df = generate_sample_data(n_rows)
    df = clean_history(df)

    st.session_state.history_df = df

    st.success("✅ Sample data generated successfully!")
    st.dataframe(df.head(20), use_container_width=True)


# -----------------------------
# Show current data
# -----------------------------
if st.session_state.history_df is not None:
    st.markdown("### 📊 Current Dataset in Session")
    st.dataframe(st.session_state.history_df.head(10), use_container_width=True)
