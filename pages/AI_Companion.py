import streamlit as st
from utils.chat import chat_with_ai

st.title("💬 AI Companion")
st.write("Talk to your mental wellness companion. It listens, supports, and guides you gently.")

user_input = st.text_area("How are you feeling today?")

if st.button("Send"):
    with st.spinner("Thinking..."):
        response = chat_with_ai(user_input)
        st.markdown(f"**AI Companion:** {response}")

