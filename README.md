# Mental Health Companion

A comprehensive **Streamlit app** to support mental well-being.  
Designed for students facing stress, anxiety, or loneliness, it offers mood tracking, journaling, and an AI-powered companion that provides empathetic suggestions and relaxation tips.

---

## Features

1. **Dashboard**
   - Overview of mental wellness journey.
   - Displays mood history and journal entries.

2. **Journal**
   - Track daily thoughts and moods.
   - Add, view, and organize personal journal entries.

3. **Mood Tracker**
   - Visualize mood trends over time.
   - Interactive graphs powered by Plotly.

4. **AI Companion Chatbot**
   - Powered by **Gemini 2.5** (Google Generative AI).
   - Provides empathetic, motivational responses based on user input.

5. **Exercises / Relaxation**
   - Play meditation or relaxation audio tracks.
   - Encourages mindfulness and stress relief.


## Quick Start (Windows PowerShell)

1. **Create & activate virtual environment**  
python -m venv venv
.\venv\Scripts\activate

2. **Install dependencies**
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

3. **Set up environment variables**
GEMINI_API_KEY=YOUR_REAL_KEY_HERE

4. **Run the app**
python -m streamlit run app.py




