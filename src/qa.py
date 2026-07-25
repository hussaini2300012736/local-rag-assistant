import time
from src.foundry_client import get_chat_client
from src.retrieve import get_top_chunks

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about Formula 1 "
    "using ONLY the provided context. If the answer is not in the context, "
    "say 'I don't have that information in my documents.' Mention which "
    "source document you used, e.g. '(source: doc5.txt)'."
)


def build_prompt(query, chunks):
    context = "\n\n".join(f"[Source: {c['source']}]\n{c['content']}" for c in chunks)
    return f"Context:\n{context}\n\nQuestion: {query}"


def answer_query(query, top_k=3):
    t0 = time.time()
    chunks = get_top_chunks(query, top_k=top_k)
    print(f"[TIMING] retrieval total: {time.time() - t0:.2f}s")

    if not chunks:
        return "I don't have that information in my documents.", []

    prompt = build_prompt(query, chunks)

    t1 = time.time()
    client = get_chat_client()
    print(f"[TIMING] get_chat_client: {time.time() - t1:.2f}s")

    t2 = time.time()
    response = client.complete_chat([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ])
    print(f"[TIMING] complete_chat (actual generation): {time.time() - t2:.2f}s")

    answer = response.choices[0].message.content
    return answer, chunks
