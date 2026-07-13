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

## Knowledge Base Expansion — 2026 Regulation Detail

!! made app.py using streamlit open source framework of python ( it lets to make web applications using only python) to make an f1 dashboard instead of using HTML and CSS and javascript 

Added 2 more docs (doc8, doc9) covering specifics beyond the basics:
- doc8.txt — 2026 tyre changes (5 compounds instead of 6, narrower tyres, rim freedom)
- doc9.txt — qualifying format changes for 11 teams, fastest lap point removal, mirror safety lights

Now 9 total documents in the knowledge base. Tested complex questions — correctly synthesizes across multiple docs with accurate citations.

**Quirk found:** on "is there still X?" yes/no questions, the model sometimes says "I don't have that information" even when the retrieved context directly answers it (e.g. it correctly stated the fastest-lap point was removed, then contradicted itself by saying it didn't know if that's current). Grounding is working — it's not inventing anything — but it can misjudge whether retrieved context actually answers a yes/no question.
**Possible fix:** tighten system prompt to explicitly handle yes/no questions first before elaborating.

## Week 4 — LLM Integration + CLI ✅ Done

- `qa.py` — `answer_query()` combines retrieved chunks + chat model into one real answer
- System prompt: answer only from context, say "I don't know" if not found, cite source
- Interactive CLI loop in `main.py` (`python main.py`, or `python main.py ask "..."` for one-off questions)
- Tested: complex multi-doc questions get correctly combined answers with citations
- Tested: unrelated/unanswerable questions correctly get "I don't have that information"

**Known limitation:** `get_top_chunks()` always returns the closest chunks it can find, even when nothing is actually relevant. So on "I don't know" answers, it still shows retrieved/cited docs that don't really apply (for example asking about a driver's salary still cites F1 cost-cap docs). Not wrong, just slightly misleading.

**Possible fix (Week 5 stretch goal):** add a similarity score threshold — if nothing scores above it, retrieve nothing at all instead of forcing a "best guess" match.

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
