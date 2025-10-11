import streamlit as st
import datetime
from utils.db import add_entry, get_entries

st.title("📝 Journal")

# --- Input Section ---
date = st.date_input("Date", datetime.date.today())
mood = st.selectbox("Mood", ["😊 Happy", "😐 Neutral", "😔 Sad", "😡 Angry"])
entry = st.text_area("Write your thoughts...")

if st.button("Save"):
    if entry.strip():  # Ensure user entered something
        add_entry(str(date), mood, entry)
        st.success("Entry saved successfully!")
    else:
        st.warning("Please write something before saving.")

# --- Display Previous Entries ---
entries = get_entries()

st.subheader("Previous Entries")
if not entries.empty:
    st.dataframe(entries.rename(columns={"date": "Date", "mood": "Mood", "entry": "Entry"}))
else:
    st.info("No journal entries yet. Start by adding one above!")
