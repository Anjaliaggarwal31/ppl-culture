import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("ppl&culture.csv")
    df = df.dropna(subset=["Invited", "Attended"])
    df.columns = df.columns.str.strip().str.title().str.replace(' ', '')
    df.rename(columns={
        "MonthList": "Month", 
        "Topic": "UpdatedTopic"
    }, inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter by:")
trainer = st.sidebar.multiselect("Trainer", sorted(df["Trainer"].unique()))
location = st.sidebar.multiselect("Location", sorted(df["Location"].dropna().unique()))
audience = st.sidebar.multiselect("Target Audience", sorted(df["TargetAudience"].dropna().unique()))
month = st.sidebar.multiselect("Month", sorted(df["Month"].dropna().unique()))

# Apply filters
filtered_df = df.copy()
if trainer:
    filtered_df = filtered_df[filtered_df["Trainer"].isin(trainer)]
if location:
    filtered_df = filtered_df[filtered_df["Location"].isin(location)]
if audience:
    filtered_df = filtered_df[filtered_df["TargetAudience"].isin(audience)]
if month:
    filtered_df = filtered_df[filtered_df["Month"].isin(month)]

# Summary Table
summary = filtered_df.groupby("UpdatedTopic")[["Invited", "Attended"]].sum().reset_index()
summary = summary.sort_values("Attended", ascending=False)
st.subheader("Learning Summary Table")
st.dataframe(summary)

# Bar Chart
st.subheader("Invited vs Attended")
fig = px.bar(summary, x="UpdatedTopic", y=["Invited", "Attended"], barmode="group")
fig.update_layout(xaxis_title="Topic", yaxis_title="Count", xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)
