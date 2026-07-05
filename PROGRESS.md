# Progress Report — Local RAG Q&A Assistant

Offline F1 Q&A chatbot built with Microsoft Foundry Local, SQLite, and Python. No internet needed at run time.

---

## Week 1 — Setup - Done

- Installed Foundry Local (`brew tap microsoft/foundrylocal && brew install foundrylocal`)
- Verified with `foundry model run phi-3.5-mini`
- Python venv + `requirements.txt` (`foundry-local-sdk`, `openai`)
- `test_hello.py` confirms Python → Foundry Local → model works

**Remember:** current SDK pattern (older tutorials online are outdated):
```python
from foundry_local_sdk import Configuration, FoundryLocalManager
config = Configuration(app_name="rag_project")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("phi-3.5-mini")
model.download()
model.load()
client = model.get_chat_client()
```

---

## Week 2 — Embeddings + SQLite - Done

- Embedding model: `qwen3-embedding-0.6b` (doesn't show in `foundry model list` — CLI display bug — but works fine from Python)
- Confirmed similarity works: "cat sat on mat" vs "feline rested on rug" → 0.75, vs "stock market crashed" → 0.38
- SQLite stores embeddings as JSON text

**Remember:** embedding response is nested — `response.data[0].embedding`, not `response.embedding`

---

## Week 3 — Ingestion + Retrieval Pipeline - Done

- Knowledge base: 7 F1 docs (basics + 2026 season: new power units, active aero, new teams Audi/Cadillac, cost cap changes)
- `chunk_text()` — splits docs into ~100-word passages
- `ingest.py` — chunks → embeds → stores in SQLite (14 chunks)
- `retrieve.py` — `get_top_chunks(query)`, cosine similarity ranking
- Tested with real questions — correct doc ranks #1 every time, clear score gap over others

---

## Week 4 — LLM Integration + CLI - Not started

- [ ] `answer_query()` — combine retrieved chunks + chat model into one real answer
- [ ] System prompt: answer only from context, say "I don't know" if not found, cite source
- [ ] Interactive CLI loop in `main.py`

## Week 5 — Testing - Not started

- [ ] Write test cases (answerable + unanswerable questions)
- [ ] Check response quality and timing

## Week 6 — Documentation & Presentation - Not started

- [ ] Finalize README
- [ ] Clean up code/comments
- [ ] Prepare demo + lessons learned

---

## Environment gotchas (don't forget)

- New terminal → run `source venv/bin/activate` first, every time
- Run scripts as `python -m src.ingest` (not `python src/ingest.py`) to keep it running as a whole package or imports break
- `data/knowledge.db` is gitignored — rebuild anytime with `python -m src.ingest`
