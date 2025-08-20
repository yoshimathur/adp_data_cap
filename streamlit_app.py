import streamlit as st
import pandas as pd

st.set_page_config(page_title="Benefits Optimization", layout="wide")
st.title("🧠 Benefits Optimization System")

df = pd.read_csv("../output/merged_clean_data.csv")
st.caption(f"Loaded {len(df):,} rows")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Total Usage by Benefit Type")
    st.bar_chart(df.groupby("BenefitType")["UsageFrequency"].sum())

with col2:
    st.subheader("Avg Satisfaction by Benefit Type")
    if "SatisfactionScore" in df.columns:
        st.line_chart(df.groupby("BenefitType")["SatisfactionScore"].mean())
    else:
        st.info("SatisfactionScore not available in merged data.")

st.subheader("Filter by Demographics")
age_groups = df["AgeGroup"].dropna().unique().tolist() if "AgeGroup" in df.columns else []
dept_groups = df["Department"].dropna().unique().tolist() if "Department" in df.columns else []


age = st.selectbox("Age Group", sorted(age_groups)) if age_groups else None
dept = st.selectbox("Department", sorted(dept_groups)) if dept_groups else None

view = df.copy()
if age is not None:
    view = view[view["AgeGroup"] == age]
if dept is not None:
    view = view[view["Department"] == dept]

st.dataframe(view[["EmployeeID","BenefitType","BenefitSubType","UsageFrequency","SatisfactionScore"]].head(50))

st.subheader("💬 AI Feedback Summaries")
try:
    ai = pd.read_csv("../output/genai_feedback_summary.csv")
    cols = [c for c in ai.columns if c in ("BenefitSubType","FeedbackSummary")]
    st.dataframe(ai[cols])
except Exception:
    st.info("Run genai/feedback_summarizer.py to generate summaries.")