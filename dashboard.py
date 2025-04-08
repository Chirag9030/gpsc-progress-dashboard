import pandas as pd
import streamlit as st
import plotly.express as px

st.title("📊 GPSC Progress Tracker")

# --- Upload Section ---
uploaded_file = st.file_uploader("📂 Upload your Excel file (optional)", type=["xlsx"])
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    st.success("✅ Custom file uploaded!")
else:
    xls = pd.ExcelFile("GPSC_Exam_Tracker_Final.xlsx")
    st.info("ℹ️ Using default file from repo")

# --- Load all sheets ---
data = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

# --- Sidebar ---
st.sidebar.title("📘 Select View")
sheet_name = st.sidebar.selectbox("Choose a Target View:", list(data.keys()))
df = data[sheet_name].copy()

# --- Progress Calculation ---
check_columns = ["Reading Done", "Notes Prepared", "PYQ Done", "Revision Done"]
for col in check_columns:
    df[col] = df[col].astype(str).str.lower().map({"yes": 1, "no": 0})
df["Progress (%)"] = df[check_columns].mean(axis=1) * 100

# --- Dashboard UI ---
st.header(f"🔍 Dashboard: {sheet_name}")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Topics", len(df))
    st.metric("Completed Topics", int((df["Progress (%)"] == 100).sum()))

with col2:
    st.metric("Average Progress", f"{df['Progress (%)'].mean():.2f}%")
    overdue = df[df["Deadline"] < pd.Timestamp.today()]
    st.metric("Overdue Topics", len(overdue))

st.subheader("📚 Progress by Subject")
subject_progress = df.groupby("Subject")["Progress (%)"].mean().reset_index()
fig = px.bar(subject_progress, x="Subject", y="Progress (%)", color="Progress (%)",
             color_continuous_scale="Blues", title="Average Progress by Subject")
st.plotly_chart(fig)

st.subheader("📋 Topic-level Detail")
st.dataframe(df[["Subject", "Topic", "Progress (%)", "Deadline", "Completion Date"] + check_columns])
