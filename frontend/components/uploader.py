import streamlit as st
from utils.api_client import client


def render_uploader():
    """File upload widget that sends files to the backend."""
    st.markdown(
        "<div class='info-box'>Upload <strong>.txt</strong> documents "
        "(SOPs, policies, reports) to expand the knowledge base.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("")

    uploaded = st.file_uploader(
        "Choose a .txt file",
        type=["txt"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

    if uploaded is not None:
        if st.button("📤 Upload & Ingest", type="primary", use_container_width=True):
            with st.spinner(f"Uploading '{uploaded.name}' and rebuilding knowledge base..."):
                try:
                    result = client.upload_document(uploaded.read(), uploaded.name)
                    st.success(f"✅ {result['message']}")
                    st.info(
                        f"Knowledge base now has {result['total_chunks']} chunks "
                        f"from {result['documents_processed']} document(s)."
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"Upload failed: {e}")
