import streamlit as st
from src.qa import answer_query

st.set_page_config(page_title="F1 RAG Assistant", page_icon="🏁", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #15151E;
        color: #FFFFFF;
    }
    h1 {
        color: #E10600;
        font-weight: 800;
        letter-spacing: -1px;
    }
    .header-bar {
        background: repeating-linear-gradient(
            45deg, #E10600, #E10600 10px, #1a1a1a 10px, #1a1a1a 20px
        );
        height: 6px;
        border-radius: 3px;
        margin-bottom: 20px;
    }
    .chat-bubble-user {
        background-color: #E10600;
        color: white;
        padding: 10px 16px;
        border-radius: 12px;
        margin: 8px 0;
        display: inline-block;
        max-width: 85%;
    }
    .chat-bubble-assistant {
        background-color: #1F1F2B;
        color: white;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #E10600;
    }
    .source-tag {
        display: inline-block;
        background-color: #2A2A38;
        color: #E10600;
        border-radius: 6px;
        padding: 2px 8px;
        margin: 2px 4px 2px 0;
        font-size: 0.8em;
        font-family: monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏁 F1 RAG Assistant")
st.markdown('<div class="header-bar"></div>', unsafe_allow_html=True)
st.caption("Answers grounded in a local F1 knowledge base — runs entirely offline via Foundry Local.")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask a question about F1:", key="query_input")

if st.button("Ask") and query:
    with st.spinner("Checking the data..."):
        answer, chunks = answer_query(query)
    st.session_state.history.append({"query": query, "answer": answer, "chunks": chunks})

# Show conversation history, most recent first
for turn in reversed(st.session_state.history):
    st.markdown(f'<div class="chat-bubble-user">🧑 {turn["query"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble-assistant">🏎️ {turn["answer"]}</div>', unsafe_allow_html=True)

    if turn["chunks"]:
        tags = "".join(
            f'<span class="source-tag">{c["source"]} ({c["score"]:.2f})</span>'
            for c in turn["chunks"]
        )
        st.markdown(tags, unsafe_allow_html=True)
    st.markdown("---")

if st.session_state.history and st.button("Clear conversation"):
    st.session_state.history = []
    st.rerun()

with st.sidebar:
    st.markdown("### 📋 Knowledge Base")
    st.caption("This assistant only knows what's in these documents:")
    docs = [
        "doc1.txt — F1 basics",
        "doc2.txt — Power units & tyres (general)",
        "doc3.txt — Teams & cost cap",
        "doc4.txt — 2026 chassis & active aero",
        "doc5.txt — 2026 power unit changes",
        "doc6.txt — 2026 grid & engine suppliers",
        "doc7.txt — 2026 cost cap & calendar",
        "doc8.txt — 2026 tyre compounds",
        "doc9.txt — 2026 qualifying & scoring",
    ]
    for d in docs:
        st.markdown(f"- {d}")
