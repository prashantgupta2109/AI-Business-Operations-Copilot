import streamlit as st
from utils.helpers import load_css
from utils.api_client import client
from components.uploader import render_uploader
from components.document_table import render_document_table

st.set_page_config(page_title="Documents — AI Copilot", page_icon="📄", layout="wide")
st.markdown(f"<style>{load_css('assets/styles.css')}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>📄 Document Management</h2>
    <p>Upload and manage the documents in your knowledge base.</p>
</div>
""", unsafe_allow_html=True)

# Upload section
st.subheader("Upload New Document")
render_uploader()

st.divider()

# Existing documents
st.subheader("Indexed Documents")
render_document_table()

st.divider()

# Re-ingest
st.subheader("Rebuild Knowledge Base")
st.caption("Use this if you have manually added or edited files in the knowledge directory.")
if st.button("🔄 Re-ingest All Documents", use_container_width=True):
    with st.spinner("Re-ingesting all documents..."):
        try:
            result = client.reingest()
            st.success(f"✅ {result['message']}")
            st.info(f"Processed {result['documents_processed']} document(s) into {result['total_chunks']} chunks.")
        except Exception as e:
            st.error(f"Re-ingestion failed: {e}")
