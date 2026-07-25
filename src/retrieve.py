import math

from src import db
from src.foundry_client import get_embedding_client, embed


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)


def get_top_chunks(query, client=None, top_k=3):
    client = client or get_embedding_client()
    conn = db.get_connection()
    all_chunks = db.fetch_all_chunks(conn)
    conn.close()

    if not all_chunks:
        return []

    query_vec = embed(client, query)
    scored = [
        (cosine_similarity(query_vec, c["embedding"]), c)
        for c in all_chunks
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"score": s, **c} for s, c in scored[:top_k]]

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "What tyres do F1 cars use?"
    results = get_top_chunks(query)
    print(f"Query: {query}\n")
    for r in results:
        print(f"[{r['score']:.3f}] {r['source']}: {r['content'][:100]}...")
        print()
