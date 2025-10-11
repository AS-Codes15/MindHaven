import os
import pandas as pd
import sqlite3

DB_PATH = "data/companion.db"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

def init_db():
    """Create journal table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            mood TEXT,
            entry TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(date, mood, entry):
    """Add a new journal entry."""
    init_db()  # Ensure table exists
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO journal (date, mood, entry) VALUES (?, ?, ?)", (date, mood, entry))
    conn.commit()
    conn.close()

def get_entries():
    """Retrieve all journal entries as a DataFrame."""
    init_db()  # Ensure table exists
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM journal ORDER BY date DESC", conn)
    conn.close()
    return df
