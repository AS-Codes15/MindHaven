import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import get_entries

st.title("📊 Mood Tracker")

data = get_entries()
if len(data) > 0:
    # Convert date column to datetime
    data["date"] = pd.to_datetime(data["date"])

    # Map moods to scores for plotting
    mood_map = {"😊 Happy": 5, "😐 Neutral": 3, "😔 Sad": 2, "😡 Angry": 1}
    data["mood_score"] = data["mood"].map(mood_map)

    fig = px.bar(data, x="date", y="mood_score", text="mood",
                 title="Mood over Time", labels={"mood_score": "Mood Score"})
    st.plotly_chart(fig)
else:
    st.info("No mood data yet. Add journal entries to start tracking!")
