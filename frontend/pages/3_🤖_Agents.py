import streamlit as st
from utils.helpers import load_css, confidence_label, total_pipeline_time
from utils.constants import AGENTS

st.set_page_config(page_title="Agents — AI Copilot", page_icon="🤖", layout="wide")
st.markdown(f"<style>{load_css('assets/styles.css')}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>🤖 Multi-Agent Pipeline</h2>
    <p>See how the 4 AI agents collaborate to process each query.</p>
</div>
""", unsafe_allow_html=True)

# Agent overview cards
st.subheader("The 4-Agent System")
cols = st.columns(4)
for col, agent in zip(cols, AGENTS):
    col.markdown(
        f"<div class='agent-card' style='flex-direction:column;align-items:flex-start;border-color:{agent['color']}33'>"
        f"  <div style='font-size:2rem'>{agent['icon']}</div>"
        f"  <div class='agent-name' style='color:{agent['color']}'>{agent['name']}</div>"
        f"  <div class='agent-desc'>{agent['desc']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.divider()

# Pipeline diagram
st.subheader("Pipeline Flow")
st.code("""
User Query
    │
    ▼
[🧠 Planner]    →  Breaks query into 2-4 steps
    │
    ▼
[🔍 Researcher] →  Retrieves top-k relevant document chunks (FAISS + Embeddings)
    │
    ▼
[⚙️  Executor]  →  Sends context + query to Llama 3, generates answer
    │
    ▼
[✅ Reviewer]   →  Scores confidence based on retrieved evidence
    │
    ▼
Final Answer + Sources + Confidence
""", language="text")

st.divider()

# Last run stats
st.subheader("Last Run Stats")
if "chat_history" in st.session_state:
    # Find the last assistant message with timing info
    last_response = None
    for msg in reversed(st.session_state.chat_history):
        if msg.get("role") == "assistant" and "response" in msg:
            last_response = msg["response"]
            break

    if last_response:
        timing = last_response.get("timing", {})
        confidence = last_response.get("confidence", 0)
        plan = last_response.get("plan", [])
        label, color = confidence_label(confidence)

        # Timing per agent
        for agent in AGENTS:
            agent_name_lower = agent["name"].lower()
            t = timing.get(agent_name_lower, 0.0)
            st.markdown(
                f"<div class='agent-card'>"
                f"  <div class='agent-icon'>{agent['icon']}</div>"
                f"  <div><div class='agent-name'>{agent['name']}</div><div class='agent-desc'>{agent['desc']}</div></div>"
                f"  <div class='agent-time'>{t}s</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        total = total_pipeline_time(timing)
        st.markdown(f"**Total pipeline time:** `{total}s`  |  **Confidence:** "
                    f"<span class='badge' style='background:{color}22;color:{color};border:1px solid {color}44'>{label} ({confidence:.0%})</span>",
                    unsafe_allow_html=True)

        if plan:
            st.markdown("**Plan steps from last query:**")
            for i, step in enumerate(plan, 1):
                st.markdown(
                    f"<div class='plan-step'><div class='plan-num'>{i}</div><div class='plan-text'>{step}</div></div>",
                    unsafe_allow_html=True,
                )
    else:
        st.info("No queries run yet. Head to the 💬 Chat page to ask a question.")
else:
    st.info("No queries run yet. Head to the 💬 Chat page to ask a question.")
