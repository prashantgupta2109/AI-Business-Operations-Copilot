import streamlit as st
from utils.api_client import client
from utils.helpers import load_css

st.set_page_config(
    page_title="AI Business Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
st.markdown(f"<style>{load_css('assets/styles.css')}</style>", unsafe_allow_html=True)

# Hero banner
st.markdown("""
<div class="hero-header">
    <h1>🤖 AI Business Operations Copilot</h1>
    <p>Your intelligent enterprise assistant &mdash; powered by Llama 3 &amp; RAG</p>
</div>
""", unsafe_allow_html=True)

# System health metrics
health = client.health()
is_online = health.get("status") == "healthy"
is_ready  = health.get("index_ready", False)
chunks    = health.get("total_chunks", 0)
docs      = health.get("documents", [])

col1, col2, col3, col4 = st.columns(4)
for col, label, value, sub in [
    (col1, "System Status",    "🟢 Online"   if is_online else "🔴 Offline",  "FastAPI backend"),
    (col2, "Knowledge Base",   "✅ Ready"    if is_ready  else "⚠️ Not Ready", f"{chunks} chunks"),
    (col3, "Documents",        str(len(docs)),                                  "files indexed"),
    (col4, "LLM",              "🦙 Llama 3",                                    "via Ollama"),
]:
    col.markdown(
        f"<div class='metric-card'>"
        f"  <div class='metric-label'>{label}</div>"
        f"  <div class='metric-value'>{value}</div>"
        f"  <div class='metric-sub'>{sub}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

# Quick start guide
st.markdown("---")
st.markdown("### 🚀 Quick Start")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='info-box'><strong>1. Upload Documents 📄</strong><br>Go to the <em>Documents</em> page and upload your company files (.txt). The system indexes them automatically.</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='info-box'><strong>2. Ask Questions 💬</strong><br>Head to the <em>Chat</em> page and ask anything about your company data in plain English.</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='info-box'><strong>3. View Agent Pipeline 🤖</strong><br>The <em>Agents</em> page shows each step: Planner → Researcher → Executor → Reviewer.</div>", unsafe_allow_html=True)

# Architecture overview
st.markdown("---")
st.markdown("### 🏗️ System Architecture")
st.code("""
User Query
    │
    ▼
Streamlit Frontend  ──────►  FastAPI Backend
                                   │
                          Agent Orchestrator
                         ┌──────────┴─────────────┐
                     🧠 Planner         🔍 Researcher
                         │                   │
                     ⚙️ Executor ◄──── FAISS + Embeddings
                         │              (knowledge docs)
                     ✅ Reviewer
                         │
                  Final Answer + Sources + Confidence
""", language="text")

# Backend offline warning
if not is_online:
    st.warning("⚠️ Backend is not reachable. Start it with:\n\n`cd backend && uvicorn app.main:app --reload`", icon="⚠️")
