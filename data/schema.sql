CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    content TEXT,
    timestamp REAL,
    escalated INTEGER
);