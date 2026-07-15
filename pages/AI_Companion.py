import streamlit as st
from utils.chat import chat_with_ai

if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

st.title("💬 AI Companion")

st.write(
    "Talk to your mental wellness companion. "
    "It listens, supports, and guides you gently."
)

user_input = st.text_area(
    "How are you feeling today?"
)

if st.button("Send"):

    if user_input.strip():

        with st.spinner("Thinking..."):

            response = chat_with_ai(
                user_input
            )

        st.markdown(
            f"**AI Companion:** {response}"
        )

    else:

        st.warning(
            "Please enter a message."
        )
