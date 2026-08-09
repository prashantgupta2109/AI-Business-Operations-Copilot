import streamlit as st
from utils.api_client import client


def render_document_table():
    """Render the list of indexed documents with delete buttons."""
    try:
        docs = client.list_documents()
    except Exception as e:
        st.error(f"Could not load document list: {e}")
        return

    if not docs:
        st.info("No documents indexed yet. Upload some files above.")
        return

    st.markdown(f"**{len(docs)} document(s) indexed**")

    for doc in docs:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"📄 `{doc['filename']}`")
        with col2:
            st.caption(f"{doc['chunks']} chunks")
        with col3:
            if st.button("🗑️", key=f"del_{doc['filename']}", help=f"Delete {doc['filename']}"):
                try:
                    with st.spinner("Deleting and rebuilding index..."):
                        client.delete_document(doc["filename"])
                    st.success(f"Deleted '{doc['filename']}'")
                    st.rerun()
                except Exception as e:
                    st.error(f"Delete failed: {e}")
