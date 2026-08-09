import streamlit as st

# Safe retrieval of BACKEND_URL.
# If running locally (no secrets file), it will catch the error and fall back to localhost.
try:
    BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")
except Exception:
    BACKEND_URL = "http://localhost:8000"

# Agent pipeline metadata
AGENTS = [
    {"name": "Planner",    "icon": "🧠", "desc": "Breaks query into actionable steps",         "color": "#818cf8"},
    {"name": "Researcher", "icon": "🔍", "desc": "Retrieves relevant document chunks",          "color": "#34d399"},
    {"name": "Executor",   "icon": "⚙️", "desc": "Generates answer from context",               "color": "#fb923c"},
    {"name": "Reviewer",   "icon": "✅", "desc": "Validates quality and confidence",            "color": "#a78bfa"},
]
