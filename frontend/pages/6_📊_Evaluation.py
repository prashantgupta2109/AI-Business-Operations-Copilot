import streamlit as st
from utils.helpers import load_css, confidence_label, total_pipeline_time

st.set_page_config(page_title="Evaluation — AI Copilot", page_icon="📊", layout="wide")
st.markdown(f"<style>{load_css('assets/styles.css')}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>📊 Evaluation Dashboard</h2>
    <p>Review the performance of past queries and agent responses.</p>
</div>
""", unsafe_allow_html=True)

# Collect all assistant responses from session state
responses = []
if "chat_history" in st.session_state:
    for msg in st.session_state.chat_history:
        if msg.get("role") == "assistant" and "response" in msg:
            responses.append(msg["response"])

if not responses:
    st.info("No queries yet. Ask some questions in the 💬 Chat page first.")
else:
    # Summary metrics
    avg_confidence = sum(r.get("confidence", 0) for r in responses) / len(responses)
    avg_time = sum(total_pipeline_time(r.get("timing", {})) for r in responses) / len(responses)
    total_sources = sum(len(r.get("sources", [])) for r in responses)

    label, color = confidence_label(avg_confidence)
    col1, col2, col3 = st.columns(3)

    for col, lbl, val, sub in [
        (col1, "Queries Run",      str(len(responses)),          "total this session"),
        (col2, "Avg Confidence",   f"{avg_confidence:.0%}",      f"Overall: {label}"),
        (col3, "Avg Pipeline Time", f"{avg_time:.1f}s",           "per query"),
    ]:
        col.markdown(
            f"<div class='metric-card'>"
            f"  <div class='metric-label'>{lbl}</div>"
            f"  <div class='metric-value'>{val}</div>"
            f"  <div class='metric-sub'>{sub}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # Per-query breakdown
    st.subheader("Query History")
    chat_history = st.session_state.get("chat_history", [])
    q_idx = 0
    for msg in chat_history:
        if msg.get("role") == "user":
            q_idx += 1
            # Find the corresponding assistant response
            pass  # handled below

    pairs = []
    i = 0
    while i < len(chat_history):
        if chat_history[i]["role"] == "user":
            user_msg = chat_history[i]
            if i + 1 < len(chat_history) and chat_history[i + 1]["role"] == "assistant":
                asst_msg = chat_history[i + 1]
                pairs.append((user_msg, asst_msg))
                i += 2
                continue
        i += 1

    for idx, (user_msg, asst_msg) in enumerate(pairs, 1):
        resp = asst_msg.get("response", {})
        conf = resp.get("confidence", 0)
        lbl, col_color = confidence_label(conf)
        timing = resp.get("timing", {})
        total_t = total_pipeline_time(timing)
        sources = resp.get("sources", [])

        with st.expander(f"Query #{idx}: {user_msg['content'][:70]}...", expanded=False):
            st.markdown(f"**Question:** {user_msg['content']}")
            st.markdown(f"**Answer:** {asst_msg['content'][:300]}..." if len(asst_msg['content']) > 300 else f"**Answer:** {asst_msg['content']}")
            st.markdown(
                f"**Confidence:** <span class='badge' style='background:{col_color}22;color:{col_color};border:1px solid {col_color}44'>{lbl} ({conf:.0%})</span> &nbsp;"
                f"**Pipeline time:** `{total_t}s` &nbsp;"
                f"**Sources used:** {len(sources)}",
                unsafe_allow_html=True,
            )
