import streamlit as st

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()
    
import pandas as pd
import plotly.express as px
from utils.db import get_entries  

st.title("🏠 Dashboard")
st.write("Here’s an overview of your mental wellness journey.")

try:
    username = st.session_state["username"]
    df = get_entries(st.session_state.username)
    if not df.empty:
        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # Recent journal entries
        st.subheader("Recent Journal Entries")
        st.dataframe(df.sort_values("date", ascending=False))

        # Mood summary
        st.subheader("Mood Summary")
        mood_counts = df["mood"].value_counts()
        st.bar_chart(mood_counts)

        # Total entries
        st.subheader("Total Entries")
        st.metric("Entries Recorded", len(df))

        # Mood trend over time
        st.subheader("Mood Trend Over Time")
        # Convert moods to numeric scale for charting
        mood_scale = {
            "😊 Happy": 5,
            "😐 Neutral": 3,
            "😔 Sad": 2,
            "😡 Angry": 1
        }
        df["mood_score"] = df["mood"].map(mood_scale)
        fig = px.line(df, x="date", y="mood_score", title="Mood Trend Over Time", markers=True)
        fig.update_layout(yaxis=dict(tickvals=[1,2,3,4,5],
                                     ticktext=["😡 Angry","😔 Sad","😐 Neutral","🙂 Good","😊 Happy"]))
        st.plotly_chart(fig)

    else:
        st.info("No journal entries yet. Start journaling to see progress here!")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")
