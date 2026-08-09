import streamlit as st

# Check if BACKEND_URL exists in Streamlit Secrets (for cloud deployment),
# otherwise fall back to localhost (for local development).
if "BACKEND_URL" in st.secrets:
    BACKEND_URL = st.secrets["BACKEND_URL"]
else:
    BACKEND_URL = "http://localhost:8000"

# Agent pipeline metadata
AGENTS = [
    {"name": "Planner",    "icon": "🧠", "desc": "Breaks query into actionable steps",         "color": "#818cf8"},
    {"name": "Researcher", "icon": "🔍", "desc": "Retrieves relevant document chunks",          "color": "#34d399"},
    {"name": "Executor",   "icon": "⚙️", "desc": "Generates answer from context",               "color": "#fb923c"},
    {"name": "Reviewer",   "icon": "✅", "desc": "Validates quality and confidence",            "color": "#a78bfa"},
]
