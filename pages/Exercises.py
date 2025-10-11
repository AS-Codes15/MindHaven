import streamlit as st

st.title("🧘 Mindfulness Exercises")

st.write("Take a few minutes to relax and focus on yourself.")

exercise = st.radio("Choose an exercise:", ["Breathing", "Meditation", "Positive Affirmations"])

if exercise == "Breathing":
    st.markdown("Inhale... Exhale... Focus on your breath for 1 minute.")
elif exercise == "Meditation":
    st.audio("assets/meditation.mp3")
else:
    st.markdown("Repeat: *I am calm, I am capable, I am enough.*")

