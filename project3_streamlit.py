import streamlit as st
import pandas as pd
st.set_page_config(page_title="Recruitment Analytics", layout="wide")
st.title("🎓 Recruitment & Placement Analytics Dashboard")

st.markdown("---")
@st.cache_data
def load_data():
    # Replace with your actual file pathway if different
    data = pd.read_csv(r"C:\Users\jagat\Downloads\cleaned_data.csv")
    
    # Quick text standardization to prevent casing bugs in metric calculations
    for col in data.select_dtypes(include=["object"]).columns:
        data[col] = data[col].astype(str).str.strip().str.title()
    return data

df = load_data()
total_candidates = len(df)
placed_count = len(df[df["status"] == "Placed"])
placement_rate = (placed_count / total_candidates) * 100 if total_candidates > 0 else 0

matched_df = df[df["job_role_match"] == "Matched"]
if len(matched_df) > 0:
    accepted_count = len(matched_df[df["status"] == "Placed"])
    job_acceptance_rate = (accepted_count / len(matched_df)) * 100
    
    # Offer Dropout: Matched for the role but ultimately Not Placed
    dropout_count = len(matched_df[df["status"] == "Not Placed"])
    offer_dropout_rate = (dropout_count / len(matched_df)) * 100
else:
    job_acceptance_rate = 0.0
    offer_dropout_rate = 0.0

# Row 2 Math
# Calculates the combined benchmark across all three interview rounds
df["overall_interview_score"] = df[["technical_score", "aptitude_score", "communication_score"]].mean(axis=1)
avg_interview_score = df["overall_interview_score"].mean()
avg_skills_match = df["skills_match_percentage"].mean()

# High-Risk Criteria: Candidate has a long employment gap (>12 mos) OR a history of layoffs
high_risk_condition = (df["employment_gap_months"] > 12) | (df["layoff_history"] == "Yes")
high_risk_count = len(df[high_risk_condition])
high_risk_percentage = (high_risk_count / total_candidates) * 100 if total_candidates > 0 else 0
st.subheader("Key Recruitment Metrics")
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1:
    st.metric(label="👥 Total Candidates", value=f"{total_candidates:,}")

with row1_col2:
    st.metric(label="📈 Placement Rate", value=f"{placement_rate:.1f}%")
with row1_col3:
    st.metric(label="🤝 Job Acceptance Rate", value=f"{job_acceptance_rate:.1f}%")
    
with row1_col4:
    st.metric(label="🚨 Offer Dropout Rate", value=f"{offer_dropout_rate:.1f}%")

st.markdown(" ") # Creates structural white space between rows
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.metric(label="🎯 Avg Interview Score", value=f"{avg_interview_score:.1f} / 100")

with row2_col2:
    st.metric(label="⚡ Avg Skills Match", value=f"{avg_skills_match:.1f}%")

with row2_col3:
    st.metric(label="⚠️ High-Risk Candidates", value=f"{high_risk_percentage:.1f}%")

st.markdown("---")