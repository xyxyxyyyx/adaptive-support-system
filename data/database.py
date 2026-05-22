import sqlite3
import time

DB_NAME = "chat.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            timestamp REAL,
            escalated INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def save_message(role, content, escalated=0):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO messages (role, content, timestamp, escalated)
        VALUES (?, ?, ?, ?)
    """, (role, content, time.time(), escalated))

    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT role, content FROM messages ORDER BY id ASC")
    rows = c.fetchall()

    conn.close()

    return [{"role": r[0], "content": r[1]} for r in rows]