import os
import pandas as pd
import sqlite3
from datetime import datetime

DB_PATH = "data/companion.db"

os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        mood TEXT,
        entry TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_entry(username, date, mood, entry):
    init_db()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO journal
        (username, date, mood, entry, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        date,
        mood,
        entry,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def get_entries(username):
    init_db()

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM journal WHERE username=? ORDER BY created_at DESC",
        conn,
        params=(username,)
    )

    conn.close()

    return df