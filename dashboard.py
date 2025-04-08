
import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    file_path = "GPSC_Exam_Tracker_Final.xlsx"
    xls = pd.ExcelFile(file_path)
    sheets = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
    return sheets

data = load_data()

st.sidebar.title("Target View")
sheet_name = st.sidebar.selectbox("Choose a Target View:", list(data.keys()))
df = data[sheet_name].copy()

st.title(f"📊 Progress Dashboard - {sheet_name}")

check_columns = ["Reading Done", "Notes Prepared", "PYQ Done", "Revision Done"]
for col in check_columns:
    df[col] = df[col].str.lower().map({"yes": 1, "no": 0})

df["Progress (%)"] = df[check_columns].mean(axis=1) * 100

st.subheader("Overall Progress")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Topics", len(df))
    st.metric("Completed Topics", int((df["Progress (%)"] == 100).sum()))

with col2:
    st.metric("Average Progress", f"{df['Progress (%)'].mean():.2f}%")
    overdue = df[df["Deadline"] < pd.Timestamp.today()]
    st.metric("Overdue Topics", len(overdue))

st.subheader("Progress by Subject")
subject_progress = df.groupby("Subject")["Progress (%)"].mean().reset_index()
fig = px.bar(subject_progress, x="Subject", y="Progress (%)", color="Progress (%)",
             color_continuous_scale="Blues", title="Average Progress by Subject")
st.plotly_chart(fig)

st.subheader("Detailed Topic Progress")
st.dataframe(df[["Subject", "Topic", "Progress (%)", "Deadline", "Completion Date"] + check_columns])
