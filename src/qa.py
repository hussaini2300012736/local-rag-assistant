from src.foundry_client import get_chat_client
from src.retrieve import get_top_chunks

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about Formula 1 "
    "using ONLY the provided context. If the answer is not in the context, "
    "say 'I don't have that information in my documents.' Mention which "
    "source document you used, e.g. '(source: doc5.txt)'."
)


def build_prompt(query, chunks):
    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['content']}" for c in chunks
    )
    return f"Context:\n{context}\n\nQuestion: {query}"


def answer_query(query, top_k=3):
    chunks = get_top_chunks(query, top_k=top_k)
    if not chunks:
        return "I don't have that information in my documents.", []

    prompt = build_prompt(query, chunks)
    client = get_chat_client()
    response = client.complete_chat([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ])
    answer = response.choices[0].message.content
    return answer, chunks


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "What is RAG?"
    answer, chunks = answer_query(query)
    print("Q:", query)
    print("A:", answer)
