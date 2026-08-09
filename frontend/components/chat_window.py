import streamlit as st
from utils.helpers import confidence_label, truncate, total_pipeline_time


def render_message(role: str, content: str):
    """Render a single chat message bubble."""
    if role == "user":
        st.markdown(
            f"<div class='chat-label' style='text-align:right'>You</div>"
            f"<div class='chat-user'>{content}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div class='chat-label'>🤖 Copilot</div>"
            f"<div class='chat-assistant'>{content}</div>",
            unsafe_allow_html=True,
        )


def render_response_details(response: dict):
    """Render the plan steps, sources, and confidence for an agent response."""
    confidence = response.get("confidence", 0)
    label, color = confidence_label(confidence)
    timing = response.get("timing", {})

    # Confidence + timing row
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"<span class='badge' style='background:{color}22;color:{color};border:1px solid {color}55'>"
            f"Confidence: {label} ({confidence:.0%})</span>",
            unsafe_allow_html=True,
        )
    with col2:
        st.caption(f"⏱ Pipeline: {total_pipeline_time(timing)}s total")

    # Plan steps
    plan = response.get("plan", [])
    if plan:
        with st.expander("🧠 Agent Plan", expanded=False):
            for i, step in enumerate(plan, 1):
                st.markdown(
                    f"<div class='plan-step'>"
                    f"  <div class='plan-num'>{i}</div>"
                    f"  <div class='plan-text'>{step}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # Sources
    sources = response.get("sources", [])
    if sources:
        with st.expander(f"📚 Sources ({len(sources)})", expanded=False):
            for src in sources:
                score = src.get("score", 0)
                preview = truncate(src.get("chunk", ""), 200)
                st.markdown(
                    f"<div class='source-card'>"
                    f"  <div class='source-filename'>📄 {src['filename']}"
                    f"    <span class='source-score'>Score: {score:.2f}</span>"
                    f"  </div>"
                    f"  <div class='source-text'>{preview}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
