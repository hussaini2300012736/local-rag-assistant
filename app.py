import math
import time
import base64
import streamlit as st
from src.qa import answer_query

st.set_page_config(page_title="F1 RAG Assistant", page_icon="🏁", layout="wide")

DOCS = [
    ("doc1.txt", "F1 basics"),
    ("doc2.txt", "Power units & tyres"),
    ("doc3.txt", "Teams & cost cap"),
    ("doc4.txt", "2026 chassis & aero"),
    ("doc5.txt", "2026 power unit"),
    ("doc6.txt", "2026 grid & engines"),
    ("doc7.txt", "2026 cost cap & calendar"),
    ("doc8.txt", "2026 tyres"),
    ("doc9.txt", "2026 qualifying & scoring"),
]

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700;900&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    color: #F5F5F7;
    background-color: transparent;
}
.checker-stripe {
    height: 8px;
    background-image: repeating-linear-gradient(45deg, #F5F5F7 0, #F5F5F7 10px, #0A0A0E 10px, #0A0A0E 20px);
    background-size: 28px 28px;
    animation: scrollFlag 1.2s linear infinite;
    border-radius: 4px; margin-bottom: 4px;
}
@keyframes scrollFlag { from { background-position: 0 0; } to { background-position: 28px 0; } }
.session-strip {
    display: flex; justify-content: space-between; align-items: center;
    background: linear-gradient(90deg, #E10600 0%, #7A0000 100%);
    padding: 10px 20px; border-radius: 4px;
    font-family: 'Titillium Web', sans-serif; font-weight: 700;
    letter-spacing: 1px; margin-bottom: 20px;
}
.live-dot {
    display: inline-block; width: 8px; height: 8px;
    background: #F5F5F7; border-radius: 50%; margin-right: 8px;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
h1 { font-family: 'Titillium Web', sans-serif; font-weight: 900; letter-spacing: -1px; margin-bottom: 0; }
.panel { background: #14141B; border-radius: 10px; padding: 16px; border: 1px solid #24242E; margin-bottom: 16px; }
.panel-title { font-family: 'JetBrains Mono', monospace; font-size: 0.72em; color: #7C7C88; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; }
.tyre-gauge { display: inline-flex; flex-direction: column; align-items: center; margin: 6px 10px 6px 0; width: 78px; }
.tyre-circle {
    width: 62px; height: 62px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.95em;
    background: conic-gradient(var(--gcolor) calc(var(--pct) * 1%), #24242E 0);
    position: relative;
}
.tyre-circle::after { content: ""; position: absolute; width: 48px; height: 48px; border-radius: 50%; background: #14141B; }
.tyre-circle span { z-index: 1; }
.tyre-label { font-size: 0.68em; color: #7C7C88; margin-top: 4px; text-align: center; }
.radio-card {
    background-color: #14141B; border-left: 3px solid #E10600;
    border-radius: 6px; padding: 14px 18px; margin: 10px 0;
    animation: slideIn 0.35s ease-out;
}
@keyframes slideIn { from { opacity: 0; transform: translateX(-12px); } to { opacity: 1; transform: translateX(0); } }
.radio-label { font-family: 'JetBrains Mono', monospace; font-size: 0.72em; color: #E10600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px; }
.engineer-msg { border-left-color: #FFB800; }
.engineer-msg .radio-label { color: #FFB800; }
.track-container { position: relative; height: 46px; background: #14141B; border-radius: 8px; overflow: hidden; margin: 12px 0; border-bottom: 3px dashed #2A2A34; }
.racing-car { position: absolute; top: 8px; font-size: 26px; animation: raceAcross 1.4s linear infinite; }
@keyframes raceAcross { from { left: -40px; } to { left: 100%; } }
</style>
"""

INTRO_HTML = """
<style>
.intro-wrap {
    height: 80vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: radial-gradient(ellipse at center, #1a0505 0%, #0A0A0E 70%);
    position: relative; overflow: hidden;
}
.speed-line {
    position: absolute; height: 2px; background: linear-gradient(90deg, transparent, rgba(225,6,0,0.7), transparent);
    animation: streak 1.1s linear infinite;
}
.speed-line:nth-child(1) { top: 20%; width: 300px; animation-delay: 0s; }
.speed-line:nth-child(2) { top: 35%; width: 200px; animation-delay: 0.3s; }
.speed-line:nth-child(3) { top: 55%; width: 260px; animation-delay: 0.15s; }
.speed-line:nth-child(4) { top: 70%; width: 180px; animation-delay: 0.5s; }
.speed-line:nth-child(5) { top: 85%; width: 240px; animation-delay: 0.35s; }
@keyframes streak { from { left: -320px; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } to { left: 110%; opacity: 0; } }
.gantry {
    background: linear-gradient(180deg, #1C1C22, #0F0F13);
    border: 2px solid #2A2A34; border-radius: 6px;
    padding: 18px 30px; margin-bottom: 34px; z-index: 2;
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
}
.lights-rig { display: flex; gap: 26px; }
.light {
    width: 54px; height: 54px; border-radius: 50%;
    background: #2A0000; border: 3px solid #3A0000;
    animation: litUp 0.45s ease-in forwards;
}
.light:nth-child(1) { animation-delay: 0.2s; }
.light:nth-child(2) { animation-delay: 0.85s; }
.light:nth-child(3) { animation-delay: 1.5s; }
.light:nth-child(4) { animation-delay: 2.15s; }
.light:nth-child(5) { animation-delay: 2.8s; }
@keyframes litUp {
    from { background: #2A0000; box-shadow: none; }
    to { background: #FF1E00; box-shadow: 0 0 30px 8px rgba(255,30,0,0.9), 0 0 60px 16px rgba(255,30,0,0.4); }
}
.lights-out { animation: goOut 0.3s ease-out forwards; animation-delay: 3.5s; }
@keyframes goOut { to { background: #2A0000; box-shadow: none; } }
.big-text {
    font-family: 'Titillium Web', sans-serif; font-weight: 900;
    font-size: 3.2em; color: #F5F5F7; opacity: 0; text-align: center;
    letter-spacing: 3px; text-shadow: 0 0 30px rgba(255,30,0,0.6);
    transform: scale(0.7);
    animation: zoomIn 0.6s cubic-bezier(0.2, 0.8, 0.3, 1.4) forwards;
    animation-delay: 3.7s; z-index: 2;
}
@keyframes zoomIn { to { opacity: 1; transform: scale(1); } }
.sub-text {
    font-family: 'JetBrains Mono', monospace; font-size: 1em; color: #FFB800;
    letter-spacing: 4px; text-transform: uppercase; opacity: 0;
    margin-top: 14px; animation: fadeUp 0.5s ease-out forwards; animation-delay: 4.5s; z-index: 2;
}
@keyframes fadeUp { from { opacity: 0; transform: translateY(10px);} to { opacity: 1; transform: translateY(0);} }
.mini-checker {
    position: absolute; bottom: 0; left: 0; width: 100%; height: 14px;
    background-image: repeating-linear-gradient(45deg, #F5F5F7 0, #F5F5F7 12px, #0A0A0E 12px, #0A0A0E 24px);
    background-size: 34px 34px;
    animation: scrollFlag 1s linear infinite;
    opacity: 0.85;
}
</style>
<div class="intro-wrap">
    <div class="speed-line"></div>
    <div class="speed-line"></div>
    <div class="speed-line"></div>
    <div class="speed-line"></div>
    <div class="speed-line"></div>
    <div class="gantry">
        <div class="lights-rig">
            <div class="light lights-out"></div>
            <div class="light lights-out"></div>
            <div class="light lights-out"></div>
            <div class="light lights-out"></div>
            <div class="light lights-out"></div>
        </div>
    </div>
    <div class="big-text">LIGHTS OUT</div>
    <div class="sub-text">🏁 F1 RAG Assistant — Session Starting</div>
    <div class="mini-checker"></div>
</div>
"""


@st.cache_data
def get_video_background(path):
    with open(path, "rb") as f:
        video_bytes = f.read()
    b64 = base64.b64encode(video_bytes).decode()
    return f"""
    <style>
    #bg-video {{
        position: fixed;
        top: 0; left: 0;
        min-width: 100%; min-height: 100%;
        object-fit: cover;
        z-index: -1;
        opacity: 0.25;
    }}
    </style>
    <video autoplay muted loop id="bg-video">
        <source src="data:video/mp4;base64,{b64}" type="video/mp4">
    </video>
    """


def gauge_color(score):
    if score >= 0.6:
        return "#00D26A"
    if score >= 0.4:
        return "#FFB800"
    return "#E10600"


def render_gauges(chunks):
    parts = []
    for c in chunks:
        pct = max(0, min(100, int(c["score"] * 100)))
        color = gauge_color(c["score"])
        parts.append(
            f'<div class="tyre-gauge"><div class="tyre-circle" style="--pct:{pct}; --gcolor:{color};">'
            f'<span>{pct}%</span></div><div class="tyre-label">{c["source"]}</div></div>'
        )
    return "".join(parts)


def render_circuit_map(used_sources):
    cx, cy, rx, ry = 150, 90, 120, 65
    node_svgs = []
    path_points = []
    for i, (name, desc) in enumerate(DOCS):
        angle = (i / len(DOCS)) * 2 * math.pi - math.pi / 2
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        path_points.append((x, y))
        active = name in used_sources
        fill = "#E10600" if active else "#2A2A34"
        stroke = "#FFB800" if active else "#3A3A44"
        text_color = "#F5F5F7" if active else "#7C7C88"
        node_svgs.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y+4:.1f}" font-size="9" fill="{text_color}" text-anchor="middle" font-family="JetBrains Mono">{i+1}</text>'
        )
    path_d = " ".join(f"{'M' if i == 0 else 'L'} {x:.1f} {y:.1f}" for i, (x, y) in enumerate(path_points)) + " Z"
    nodes_str = "".join(node_svgs)
    return (
        f'<svg width="100%" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="{path_d}" fill="none" stroke="#24242E" stroke-width="8" stroke-linejoin="round"/>'
        f'{nodes_str}</svg>'
    )


st.markdown(BASE_CSS, unsafe_allow_html=True)
st.markdown(get_video_background("assets/background.mp4"), unsafe_allow_html=True)

if "intro_shown" not in st.session_state:
    st.session_state.intro_shown = False
if "history" not in st.session_state:
    st.session_state.history = []

if not st.session_state.intro_shown:
    st.markdown(INTRO_HTML, unsafe_allow_html=True)
    time.sleep(5.2)
    st.session_state.intro_shown = True
    st.rerun()

st.markdown('<div class="checker-stripe"></div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="session-strip"><span><span class="live-dot"></span>LIVE SESSION</span>'
    f'<span>DOCS LOADED: {len(DOCS)}</span><span>QUESTIONS ASKED: {len(st.session_state.history)}</span>'
    f'<span>ENGINE: FOUNDRY LOCAL</span></div>',
    unsafe_allow_html=True,
)

st.title("🏁 F1 RAG Assistant")
st.caption("Grounded answers from a local F1 knowledge base — no internet required at run time.")

main_col, side_col = st.columns([2.2, 1])

with side_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Knowledge Base Circuit</div>', unsafe_allow_html=True)
    last_sources = set()
    if st.session_state.history:
        last_sources = {c["source"] for c in st.session_state.history[-1]["chunks"]}
    st.markdown(render_circuit_map(last_sources), unsafe_allow_html=True)
    st.caption("Highlighted nodes = documents used in your last answer.")
    for i, (name, desc) in enumerate(DOCS):
        st.markdown(f"<span style='font-family:JetBrains Mono;color:#7C7C88;font-size:0.78em'>{i+1}. {name} — {desc}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("▶ Replay intro"):
        st.session_state.intro_shown = False
        st.rerun()

with main_col:
    query = st.text_input("Ask a question about F1:", key="query_input")
    ask_clicked = st.button("Ask")

    if ask_clicked and query:
        loader = st.empty()
        loader.markdown('<div class="track-container"><div class="racing-car">🏎️</div></div>', unsafe_allow_html=True)
        start = time.time()
        answer, chunks = answer_query(query)
        elapsed = time.time() - start
        loader.empty()
        st.session_state.history.append({"query": query, "answer": answer, "chunks": chunks, "time": elapsed})
        st.rerun()

    for turn in reversed(st.session_state.history):
        st.markdown(f'<div class="radio-card"><div class="radio-label">👩 You</div>{turn["query"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="radio-card engineer-msg"><div class="radio-label">🏎️ Assistant</div>{turn["answer"]}</div>', unsafe_allow_html=True)
        st.caption(f"⏱️ {turn.get('time', 0):.1f}s")
        if turn["chunks"]:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Source Confidence</div>', unsafe_allow_html=True)
            st.markdown(render_gauges(turn["chunks"]), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.history and st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()
