import sys

from src.ingest import ingest_documents
from src.qa import answer_query


def interactive_loop():
    print("F1 RAG Assistant — type 'exit' to quit.\n")
    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        answer, chunks = answer_query(query)
        print(f"\nAssistant: {answer}")
        sources = ", ".join(sorted({c["source"] for c in chunks}))
        print(f"(retrieved from: {sources})\n" if sources else "\n")


def main():
    args = sys.argv[1:]

    if args and args[0] == "ingest":
        ingest_documents()
        return

    if args and args[0] == "ask":
        query = " ".join(args[1:])
        answer, chunks = answer_query(query)
        print("Q:", query)
        print("A:", answer)
        return

    interactive_loop()


if __name__ == "__main__":
    main()
