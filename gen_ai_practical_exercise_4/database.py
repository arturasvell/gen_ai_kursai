import sqlite3
from datetime import datetime

DATABASE_NAME = "ingestion_log.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_log_entry(topic: str, collection_name: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ingestion_log (topic, collection_name) VALUES (?, ?)
    """, (topic, collection_name))
    conn.commit()
    conn.close()

def get_log_entries(limit: int = 100):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingestion_log ORDER BY creation_date DESC LIMIT ?", (limit,))
    entries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return entries
