import streamlit as st
from src.qa import answer_query

st.set_page_config(page_title="F1 RAG Assistant", page_icon="🏁", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: #15151E; color: white; }
    h1 { color: #E10600; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏁 F1 RAG Assistant")
st.caption("Answers grounded in local F1 documents — no internet required.")

query = st.text_input("Ask a question about F1:")

if query:
    with st.spinner("Checking the data..."):
        answer, chunks = answer_query(query)
    st.markdown("### Answer")
    st.write(answer)

    if chunks:
        with st.expander("Sources used"):
            for c in chunks:
                st.markdown(f"**{c['source']}** (score: {c['score']:.3f})")
                st.caption(c["content"][:200] + "...")
