import streamlit as st
from utils.helpers import load_css, truncate
from utils.api_client import client

st.set_page_config(page_title="Tools — AI Copilot", page_icon="🛠️", layout="wide")
st.markdown(f"<style>{load_css('assets/styles.css')}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>🛠️ Developer Tools</h2>
    <p>Test the vector search and inspect the knowledge base directly.</p>
</div>
""", unsafe_allow_html=True)

# --- Vector Search Tester ---
st.subheader("🔍 Vector Search Tester")
st.caption("Enter a query to see which document chunks the retriever would select — without running the full LLM pipeline.")

with st.form("search_form"):
    test_query = st.text_input("Search query", placeholder="e.g. What is the leave policy?")
    top_k = st.slider("Number of results (k)", 1, 10, 5)
    submitted = st.form_submit_button("🔍 Search", type="primary")

if submitted and test_query:
    try:
        # Call the chat API but we're only interested in sources here
        # For a pure search, we use a lightweight trick: call chat and show sources only
        with st.spinner("Searching knowledge base..."):
            result = client.chat(query=test_query, top_k=top_k)

        sources = result.get("sources", [])
        st.markdown(f"**Found {len(sources)} relevant chunk(s):**")
        for i, src in enumerate(sources, 1):
            score = src.get("score", 0)
            st.markdown(
                f"<div class='source-card'>"
                f"  <div class='source-filename'>#{i} — 📄 {src['filename']}"
                f"    <span class='source-score'>Score: {score:.3f}</span></div>"
                f"  <div class='source-text'>{src.get('chunk', '')}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"Search failed: {e}")

st.divider()

# --- Knowledge Base Stats ---
st.subheader("📊 Knowledge Base Stats")
try:
    docs = client.list_documents()
    if docs:
        total_chunks = sum(d["chunks"] for d in docs)
        st.markdown(f"**{len(docs)} document(s)** — **{total_chunks} total chunks**")
        for doc in docs:
            pct = doc["chunks"] / total_chunks * 100
            st.markdown(f"- `{doc['filename']}` — {doc['chunks']} chunks ({pct:.1f}%)")
    else:
        st.info("No documents indexed yet.")
except Exception as e:
    st.error(f"Could not fetch stats: {e}")

st.divider()

# --- Re-Ingest Button ---
st.subheader("🔄 Rebuild Index")
if st.button("Re-ingest All Documents", use_container_width=True):
    with st.spinner("Rebuilding knowledge base..."):
        try:
            result = client.reingest()
            st.success(f"Done! {result['total_chunks']} chunks from {result['documents_processed']} documents.")
        except Exception as e:
            st.error(f"Failed: {e}")
