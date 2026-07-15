import streamlit as st

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

import datetime
from utils.db import add_entry, get_entries

username = st.session_state["username"]

st.title("📝 Journal")

date = st.date_input("Date", datetime.date.today())

mood = st.selectbox(
    "Mood",
    ["😊 Happy", "😐 Neutral", "😔 Sad", "😡 Angry"]
)

entry = st.text_area("Write your thoughts...")

if st.button("Save"):

    if entry.strip():

        add_entry(
            username,
            str(date),
            mood,
            entry
        )

        st.success("Entry saved successfully!")

    else:
        st.warning("Please write something.")

entries = get_entries(username)

st.subheader("Previous Entries")

if not entries.empty:

    st.dataframe(entries)

    csv = entries.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 Download Journal as CSV",
        data=csv,
        file_name=f"{username}_journal.csv",
        mime="text/csv"
    )

else:
    st.info("No entries found.")