import streamlit as st
from utils.api_client import client


def render_sidebar():
    """Render the navigation sidebar with system health indicators."""
    with st.sidebar:
        st.markdown("""<div style='text-align:center; padding:1rem 0 0.5rem'>
            <span style='font-size:2.5rem'>🤖</span>
            <h2 style='margin:0.3rem 0 0; color:#e2e8f0; font-size:1.1rem'>AI Copilot</h2>
            <p style='color:#64748b; font-size:0.8rem; margin:0'>Business Operations</p>
        </div>""", unsafe_allow_html=True)

        st.divider()

        # Live system health
        health = client.health()
        is_online = health.get("status") == "healthy"
        is_ready  = health.get("index_ready", False)
        chunks    = health.get("total_chunks", 0)

        st.markdown("**System Status**")
        status_color = "#22c55e" if is_online else "#ef4444"
        status_text  = "Online" if is_online else "Offline"
        st.markdown(f"<span style='color:{status_color}'>● {status_text}</span>", unsafe_allow_html=True)

        st.markdown("**Knowledge Base**")
        kb_color = "#22c55e" if is_ready else "#f59e0b"
        kb_text  = f"{chunks} chunks indexed" if is_ready else "Not ready"
        st.markdown(f"<span style='color:{kb_color}'>● {kb_text}</span>", unsafe_allow_html=True)

        st.divider()
        st.caption("Navigate using the pages in the sidebar above.")
