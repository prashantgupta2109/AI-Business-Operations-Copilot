import streamlit as st
from utils.helpers import load_css
from utils.api_client import client
from components.chat_window import render_message, render_response_details

st.set_page_config(page_title="Chat — AI Copilot", page_icon="💬", layout="wide")
st.markdown(f"<style>{load_css('assets/styles.css')}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>💬 Chat with your Knowledge Base</h2>
    <p>Ask questions in natural language. The AI will search your documents and answer accurately.</p>
</div>
""", unsafe_allow_html=True)

# Initialise session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {role, content, response?}

# Sidebar controls
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")
    top_k = st.slider("Chunks to retrieve (top-k)", min_value=1, max_value=10, value=5)
    st.divider()
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Render conversation history
for msg in st.session_state.chat_history:
    render_message(msg["role"], msg["content"])
    if msg["role"] == "assistant" and "response" in msg:
        render_response_details(msg["response"])

# Chat input
if query := st.chat_input("Ask anything about your company data..."):
    # Show user message immediately
    render_message("user", query)
    st.session_state.chat_history.append({"role": "user", "content": query})

    # Call backend
    with st.spinner("🤖 Running agent pipeline..."):
        try:
            response = client.chat(query=query, top_k=top_k)
            answer = response.get("answer", "No answer returned.")

            render_message("assistant", answer)
            render_response_details(response)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
                "response": response,
            })
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            render_message("assistant", error_msg)
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
