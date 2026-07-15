import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import re

from utils.auth import (
    init_users_table,
    register_user,
    login_user
)

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="MindHaven - Mental Health Companion",
    layout="wide"
)

# ==========================
# DATABASE INIT
# ==========================

init_users_table()

# ==========================
# SESSION STATE
# ==========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================
# LOGIN / REGISTER
# ==========================

if not st.session_state.logged_in:

    st.title("🔐 MindHaven Authentication")

    login_tab, register_tab = st.tabs(
        ["Login", "Register"]
    )

    # LOGIN TAB
    with login_tab:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            name = login_user(
                email,
                password
            )

            if name:

                st.session_state.logged_in = True
                st.session_state.username = name

                st.success("Login successful")
                st.rerun()

            else:

                st.error(
                    "Invalid email or password"
                )

    # REGISTER TAB
    with register_tab:

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm"
        )

        if st.button("Register"):

            if not name.strip():

                st.error("Name required")

            elif not re.match(
                r"[^@]+@[^@]+\.[^@]+",
                email
            ):

                st.error(
                    "Enter a valid email address"
                )

            elif len(password) < 6:

                st.error(
                    "Password must be at least 6 characters"
                )

            elif password != confirm:

                st.error(
                    "Passwords do not match"
                )

            else:

                success = register_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        "Registration successful. Please login."
                    )

                else:

                    st.error(
                        "Email already exists"
                    )

    st.stop()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.success(
    f"Logged in as {st.session_state.username}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()

# ==========================
# GEMINI SETUP
# ==========================

load_dotenv()

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False

API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_AVAILABLE and API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        st.warning(
            "Gemini configuration failed: "
            + str(e)
        )

# ==========================
# PATHS
# ==========================

PROJECT_ROOT = Path(__file__).parent
ASSETS = PROJECT_ROOT / "assets"

# ==========================
# HELPERS
# ==========================

def find_background():

    candidates = [
        "bg.jpg",
        "bg.png",
        "background.jpg",
        "background.png"
    ]

    for c in candidates:

        p = ASSETS / c

        if p.exists():
            return p

    return None


def create_placeholder_bg(
    path,
    size=(1200, 700),
    color=(220, 230, 240)
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    img = Image.new(
        "RGB",
        size,
        color=color
    )

    draw = ImageDraw.Draw(img)

    text = "MindHaven"

    try:
        fnt = ImageFont.load_default()
    except:
        fnt = None

    draw.text(
        (100, 100),
        text,
        fill=(60, 60, 60),
        font=fnt
    )

    img.save(path)

    return path


def call_gemini_simple(prompt):

    if not GEMINI_AVAILABLE or not API_KEY:
        return (
            "Gemini is not configured. "
            "Add GEMINI_API_KEY to .env"
        )

    try:

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {e}"

# ==========================
# HEADER
# ==========================

cols = st.columns([1, 6])

with cols[0]:

    logo_path = ASSETS / "logo.png"

    if logo_path.exists():
        st.image(
            str(logo_path),
            width=80
        )

with cols[1]:

    st.title(
        "🧠 MindHaven - Mental Health Companion"
    )

    st.write(
        "Track moods, write journals, "
        "and receive supportive AI guidance."
    )

# ==========================
# BANNER
# ==========================

bg_path = find_background()

if not bg_path:

    placeholder = ASSETS / "bg.png"

    if not placeholder.exists():
        create_placeholder_bg(
            placeholder
        )

    bg_path = placeholder

try:

    st.image(
      str(bg_path),
      width="stretch"
    )

except Exception as e:

    st.warning(
        "Background load error: "
        + str(e)
    )

# ==========================
# HOME
# ==========================

st.header("💬 Quick Mood Check")

mood = st.selectbox(
    "How are you feeling today?",
    [
        "Great",
        "Good",
        "Okay",
        "Bad",
        "Terrible"
    ]
)

note = st.text_area(
    "Write a short note (optional)"
)

if st.button(
    "Get Gentle Suggestion"
):

    with st.spinner(
        "Generating response..."
    ):

        prompt = f"""
        User feels {mood}.

        Write a short supportive message
        and suggest one healthy activity.
        """

        suggestion = call_gemini_simple(
            prompt
        )

    st.subheader(
        "💡 Suggestion"
    )

    st.write(
        suggestion
    )

# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.write(
    "Use the sidebar to explore "
    "Journal, Mood Tracker, Dashboard "
    "and AI Companion."
)