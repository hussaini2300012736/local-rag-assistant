import sqlite3
import json

conn = sqlite3.connect("test.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        embedding TEXT
    )
""")

# Fake embedding just to test storage/retrieval mechanics
sample_vector = [0.1, 0.2, 0.3]
conn.execute(
    "INSERT INTO chunks (content, embedding) VALUES (?, ?)",
    ("This is a test sentence.", json.dumps(sample_vector))
)
conn.commit()

rows = conn.execute("SELECT id, content, embedding FROM chunks").fetchall()
for row in rows:
    id, content, embedding_json = row
    embedding = json.loads(embedding_json)
    print(f"id={id}, content='{content}', embedding={embedding}")

conn.close()
