import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
DB = os.path.join(DB_DIR, "events.db")

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def save_event(event, score, level):
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO events(timestamp,event,risk_score,risk_level) VALUES(?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), event, score, level)
    )
    con.commit()
    con.close()

def get_events(limit=30):
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT id,timestamp,event,risk_score,risk_level FROM events "
        "ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    con.close()
    return rows

def clear_events():
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM events")
    con.commit()
    con.close()
