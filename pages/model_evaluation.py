import streamlit as st
import plotly.express as px

st.title("📈 Model Evaluation")

if "training_report" in st.session_state:
    st.markdown("### Classification report")
    st.text(st.session_state.training_report)

if st.session_state.predictions_df is not None:
    preds = st.session_state.predictions_df

    prob_cols = [c for c in preds.columns if c.startswith("prob_")]
    if prob_cols:
        melted = preds[prob_cols].melt(var_name="class", value_name="probability")
        fig = px.box(melted, x="class", y="probability", title="Prediction probability distribution")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(preds.head(20), use_container_width=True)
else:
    st.info("No predictions available yet.")