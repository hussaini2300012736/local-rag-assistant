import streamlit as st
from src.qa import answer_query

st.set_page_config(page_title="F1 RAG Assistant", page_icon="🏁", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700;900&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0C0C10; color: #F5F5F7; }

    /* Scrolling checkered flag stripe */
    .checker-stripe {
        height: 10px;
        background-image: repeating-linear-gradient(45deg, #F5F5F7 0, #F5F5F7 10px, #0C0C10 10px, #0C0C10 20px);
        background-size: 28px 28px;
        animation: scrollFlag 1.2s linear infinite;
        border-radius: 4px;
        margin-bottom: 4px;
    }
    @keyframes scrollFlag {
        from { background-position: 0 0; }
        to { background-position: 28px 0; }
    }

    .session-strip {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, #E10600 0%, #8B0000 100%);
        padding: 10px 20px;
        border-radius: 4px;
        font-family: 'Titillium Web', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 24px;
    }
    .session-strip .live-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: #F5F5F7;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

    h1 {
        font-family: 'Titillium Web', sans-serif;
        font-weight: 900;
        color: #F5F5F7;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    /* Racing loader — car speeding across a track */
    .track-container {
        position: relative;
        height: 50px;
        background: #1A1A22;
        border-radius: 8px;
        overflow: hidden;
        margin: 16px 0;
        border-bottom: 3px dashed #3A3A44;
    }
    .racing-car {
        position: absolute;
        top: 10px;
        font-size: 28px;
        animation: raceAcross 1.4s linear infinite;
    }
    @keyframes raceAcross {
        from { left: -40px; }
        to { left: 100%; }
    }
    .track-label {
        position: absolute;
        right: 12px;
        top: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75em;
        color: #8E8E96;
    }

    /* Radio transcript cards with slide-in */
    .radio-card {
        background-color: #1A1A22;
        border-left: 3px solid #E10600;
        border-radius: 6px;
        padding: 14px 18px;
        margin: 10px 0;
        animation: slideIn 0.35s ease-out;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-12px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .radio-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72em;
        color: #8E8E96;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }
    .driver-msg .radio-label { color: #E10600; }
    .engineer-msg { border-left-color: #FFB800; }
    .engineer-msg .radio-label { color: #FFB800; }

    .gauge-row {
        display: flex; align-items: center; margin: 6px 0;
        font-family: 'JetBrains Mono', monospace; font-size: 0.78em;
    }
    .gauge-label { width: 110px; color: #8E8E96; }
    .gauge-track {
        flex: 1; height: 8px; background: #2A2A34;
        border-radius: 4px; overflow: hidden; margin: 0 10px;
    }
    .gauge-fill {
        height: 100%;
        background: linear-gradient(90deg, #FFB800, #E10600);
        border-radius: 4px;
        animation: fillBar 0.6s ease-out;
    }
    @keyframes fillBar { from { width: 0%; } }
    .gauge-score { width: 45px; color: #F5F5F7; text-align: right; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []

DOC_COUNT = 9

st.markdown('<div class="checker-stripe"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="session-strip">
        <span><span class="live-dot"></span>LIVE SESSION</span>
        <span>DOCS LOADED: {DOC_COUNT}</span>
        <span>QUESTIONS ASKED: {len(st.session_state.history)}</span>
        <span>ENGINE: FOUNDRY LOCAL</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("🏁 F1 RAG Assistant")
st.caption("Grounded answers from a local F1 knowledge base — no internet required at run time.")

query = st.text_input("Ask a question about F1:", key="query_input")
col1, col2 = st.columns([1, 5])
with col1:
    ask_clicked = st.button("Ask", use_container_width=True)

if ask_clicked and query:
    loader = st.empty()
    loader.markdown(
        """
        <div class="track-container">
            <div class="racing-car">🏎️</div>
            <div class="track-label">PROCESSING...</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    answer, chunks = answer_query(query)
    loader.empty()
    st.session_state.history.append({"query": query, "answer": answer, "chunks": chunks})
    st.rerun()

for turn in reversed(st.session_state.history):
    st.markdown(
        f'<div class="radio-card driver-msg"><div class="radio-label">👩 You</div>{turn["query"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="radio-card engineer-msg"><div class="radio-label">🏎️ Assistant</div>{turn["answer"]}</div>',
        unsafe_allow_html=True,
    )

    if turn["chunks"]:
        gauges = ""
        for c in turn["chunks"]:
            pct = max(0, min(100, int(c["score"] * 100)))
            gauges += f"""
            <div class="gauge-row">
                <div class="gauge-label">{c['source']}</div>
                <div class="gauge-track"><div class="gauge-fill" style="width:{pct}%;"></div></div>
                <div class="gauge-score">{c['score']:.2f}</div>
            </div>
            """
        st.markdown(gauges, unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

if st.session_state.history and st.button("Clear conversation"):
    st.session_state.history = []
    st.rerun()

with st.sidebar:
    st.markdown("### 🔧 Car Setup Sheet")
    st.caption("Knowledge base — what this assistant actually knows")
    docs = [
        ("doc1.txt", "F1 basics"),
        ("doc2.txt", "Power units & tyres (general)"),
        ("doc3.txt", "Teams & cost cap"),
        ("doc4.txt", "2026 chassis & active aero"),
        ("doc5.txt", "2026 power unit changes"),
        ("doc6.txt", "2026 grid & engine suppliers"),
        ("doc7.txt", "2026 cost cap & calendar"),
        ("doc8.txt", "2026 tyre compounds"),
        ("doc9.txt", "2026 qualifying & scoring"),
    ]
    for name, desc in docs:
        st.markdown(f"**{name}**  \n<span style='color:#8E8E96;font-size:0.85em'>{desc}</span>", unsafe_allow_html=True)
