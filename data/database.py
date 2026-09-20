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

    c.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frustration_score INTEGER,
            summary TEXT,
            raw_chat TEXT,
            timestamp REAL
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


def save_case(frustration_score, summary, messages):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    raw_chat = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in messages
    )

    c.execute("""
        INSERT INTO cases (
            frustration_score,
            summary,
            raw_chat,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        frustration_score,
        summary,
        raw_chat,
        time.time()
    ))

    conn.commit()
    conn.close()


def get_messages():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT role, content
        FROM messages
        ORDER BY id ASC
    """)

    rows = c.fetchall()
    conn.close()

    return [
        {"role": row[0], "content": row[1]}
        for row in rows
    ]


def get_latest_case():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT id, frustration_score, summary, raw_chat, timestamp
        FROM cases
        ORDER BY id DESC
        LIMIT 1
    """)

    row = c.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "frustration": row[1],
        "summary": row[2],
        "raw_chat": row[3],
        "timestamp": row[4]
    }