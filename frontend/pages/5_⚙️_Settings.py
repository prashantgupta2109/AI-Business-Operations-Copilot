import streamlit as st
from utils.helpers import load_css
from utils.api_client import client
from utils.constants import BACKEND_URL

st.set_page_config(page_title="Settings — AI Copilot", page_icon="⚙️", layout="wide")
st.markdown(f"<style>{load_css('assets/styles.css')}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>⚙️ Settings</h2>
    <p>View system configuration and connection status.</p>
</div>
""", unsafe_allow_html=True)

# --- Backend Connection ---
st.subheader("🔗 Backend Connection")
health = client.health()
is_online = health.get("status") == "healthy"

st.markdown(f"**Backend URL:** `{BACKEND_URL}`")
if is_online:
    st.success("✅ Backend is reachable.")
else:
    st.error("❌ Backend is not reachable. Make sure the FastAPI server is running.")
    st.code("cd backend && uvicorn app.main:app --reload --port 8000", language="bash")

st.divider()

# --- System Info ---
st.subheader("📋 System Info")
col1, col2 = st.columns(2)
with col1:
    st.markdown("| Setting | Value |")
    st.markdown("|---------|-------|")
    st.markdown("| LLM | Llama 3 (Ollama) |")
    st.markdown("| Embedding Model | all-MiniLM-L6-v2 |")
    st.markdown("| Vector Store | FAISS (IndexFlatL2) |")
    st.markdown("| Framework | FastAPI + Streamlit |")
with col2:
    st.markdown("| Metric | Value |")
    st.markdown("|--------|-------|")
    total_chunks = health.get("total_chunks", 0)
    docs = health.get("documents", [])
    st.markdown(f"| Indexed Chunks | {total_chunks} |")
    st.markdown(f"| Indexed Documents | {len(docs)} |")
    st.markdown(f"| Knowledge Base Status | {'Ready ✅' if total_chunks > 0 else 'Empty ⚠️'} |")
    st.markdown(f"| Agent Pipeline | 4 agents |")

st.divider()

# --- How to Run ---
st.subheader("🚀 How to Start the System")
st.code("""
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Start the backend (runs on http://localhost:8000)
uvicorn app.main:app --reload

# 3. In a new terminal, install frontend dependencies
cd frontend
pip install -r requirements.txt

# 4. Start the frontend (runs on http://localhost:8501)
streamlit run app.py
""", language="bash")
