import streamlit as st


def metric_card(label: str, value: str, sub: str = "", col=None):
    """Render a styled metric card."""
    html = (
        f"<div class='metric-card'>"
        f"  <div class='metric-label'>{label}</div>"
        f"  <div class='metric-value'>{value}</div>"
        f"  {'<div class=\"metric-sub\">' + sub + '</div>' if sub else ''}"
        f"</div>"
    )
    target = col if col else st
    target.markdown(html, unsafe_allow_html=True)
