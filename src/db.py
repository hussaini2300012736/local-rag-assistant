import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    """)
    conn.commit()


def clear_chunks(conn):
    conn.execute("DELETE FROM chunks")
    conn.commit()


def insert_chunk(conn, source, content, embedding):
    conn.execute(
        "INSERT INTO chunks (source, content, embedding) VALUES (?, ?, ?)",
        (source, content, json.dumps(embedding)),
    )
    conn.commit()


def fetch_all_chunks(conn):
    rows = conn.execute("SELECT id, source, content, embedding FROM chunks").fetchall()
    return [
        {"id": r[0], "source": r[1], "content": r[2], "embedding": json.loads(r[3])}
        for r in rows
    ]
