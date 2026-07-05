from pathlib import Path

from src import db
from src.foundry_client import get_embedding_client, embed

DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "docs"


def chunk_text(text, max_words=100):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current, current_len = [], [], 0

    for p in paragraphs:
        words = len(p.split())
        if current and current_len + words > max_words:
            chunks.append(" ".join(current))
            current, current_len = [], 0
        current.append(p)
        current_len += words

    if current:
        chunks.append(" ".join(current))
    return chunks


def ingest_documents():
    client = get_embedding_client()
    conn = db.get_connection()
    db.init_db(conn)
    db.clear_chunks(conn)

    total = 0
    for path in sorted(DOCS_DIR.glob("*.txt")):
        text = path.read_text()
        chunks = chunk_text(text)
        for chunk in chunks:
            vector = embed(client, chunk)
            db.insert_chunk(conn, source=path.name, content=chunk, embedding=vector)
            total += 1
        print(f"Ingested {len(chunks)} chunk(s) from {path.name}")

    conn.close()
    print(f"Done. {total} chunks stored in {db.DB_PATH}")


if __name__ == "__main__":
    ingest_documents()
