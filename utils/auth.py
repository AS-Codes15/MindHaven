import sqlite3
import bcrypt

DB_PATH = "data/companion.db"

def init_users_table():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT,
       email TEXT UNIQUE,
       password_hash TEXT
    )
    """)

    conn.commit()
    conn.close()


def register_user(name, email, password):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    try:

        cur.execute(
            """
            INSERT INTO users
            (name,email,password_hash)
            VALUES (?,?,?)
            """,
            (
                name,
                email,
                password_hash
            )
        )

        conn.commit()

        print("USER SAVED SUCCESSFULLY")

        return True

    except Exception as e:

        print("REGISTER ERROR:", e)

        return False

    finally:

        conn.close()


def login_user(email, password):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT password_hash, name
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cur.fetchone()

    conn.close()

    if not user:
        return None

    if bcrypt.checkpw(
        password.encode(),
        user[0].encode()
    ):
        return user[1]

    return None