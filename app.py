import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# ENVIRONMENT & GEMINI SETUP
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
        st.warning("⚠️ Gemini library present but failed to configure: " + str(e))

# HELPER FILE PATH SETUP
PROJECT_ROOT = Path(__file__).parent
ASSETS = PROJECT_ROOT / "assets"

def find_background():
    """Return a Path to a background image if available."""
    candidates = ["bg.jpg", "bg.png", "background.jpg", "background.png"]
    for c in candidates:
        p = ASSETS / c
        if p.exists():
            return p
    return None

def create_placeholder_bg(path: Path, size=(1200, 700), color=(220, 230, 240)):
    """Create a simple placeholder background if none exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", size, color=color)
    draw = ImageDraw.Draw(img)
    text = "Placeholder Background"
    try:
        fnt = ImageFont.load_default()
    except Exception:
        fnt = None
    w, h = draw.textsize(text, font=fnt)
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=(60, 60, 60), font=fnt)
    img.save(path)
    return path


# GEMINI TEXT GENERATION CALL
def call_gemini_simple(prompt: str, max_tokens: int = 256):
    """
    Make a short text generation call to Gemini 2.5.
    Compatible with google-generativeai >= 0.8.5.
    """
    if not GEMINI_AVAILABLE or not API_KEY:
        return "⚠️ Gemini is not configured. Add GEMINI_API_KEY to your .env file."

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text
        elif response and hasattr(response, "candidates") and len(response.candidates) > 0:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                return parts[0].text

        return "Sorry, I couldn’t generate a response right now."

    except Exception as e:
        return f"Gemini call failed: {e}"

# STREAMLIT PAGE CONFIG
st.set_page_config(
    page_title="Mental Health Companion",
    layout="wide",
)


# HEADER SECTION
cols = st.columns([1, 6])
with cols[0]:
    logo_path = ASSETS / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=80)
    else:
        st.write("")  # keep layout consistent

with cols[1]:
    st.title("🧠 Mental Health Companion")
    st.write("Track your mood, write journals, and find supportive suggestions powered by AI.")


# BACKGROUND / BANNER
bg_path = find_background()
if not bg_path:
    placeholder = ASSETS / "bg.png"
    if not placeholder.exists():
        create_placeholder_bg(placeholder)
    bg_path = placeholder

try:
    st.image(str(bg_path), width="stretch")
except Exception as e:
    st.warning("⚠️ Could not load background image: " + str(e))


# MAIN APP BODY
st.header("💬 Quick Mood Check")
mood = st.selectbox("How are you feeling today?", ["Great", "Good", "Okay", "Bad", "Terrible"])
note = st.text_area("Write a short note (optional):", height=120)

if st.button("Get Gentle Suggestion"):
    with st.spinner("Generating a supportive message..."):
        prompt = f"Write a short, kind, and supportive message for someone feeling {mood}. Suggest one simple positive activity."
        suggestion = call_gemini_simple(prompt)
    st.subheader("💡 Suggestion")
    st.write(suggestion)


# FOOTER
st.markdown("---")
st.write("Explore your Journal, Exercises, and Community pages from the sidebar.")
