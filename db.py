import sqlite3
from datetime import datetime

def create_table():
    conn = sqlite3.connect("quiz_responses.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER,
            answers TEXT,
            submitted_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_response(username, score, answers):
    conn = sqlite3.connect("quiz_responses.db")
    c = conn.cursor()
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answers_str = ";".join(answers)
    c.execute('''
        INSERT INTO user_responses (username, score, answers, submitted_at)
        VALUES (?, ?, ?, ?)
    ''', (username, score, answers_str, submitted_at))
    conn.commit()
    conn.close()

def fetch_all_responses():
    conn = sqlite3.connect("quiz_responses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM user_responses")
    rows = c.fetchall()
    conn.close()
    return rows
