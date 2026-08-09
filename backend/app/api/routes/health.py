from fastapi import APIRouter
from app.vector_store.faiss_store import store

router = APIRouter(tags=["system"])


@router.get("/health")
def health():
    """System health check: returns index and LLM status."""
    return {
        "status": "healthy",
        "index_ready": store.total_chunks() > 0,
        "total_chunks": store.total_chunks(),
        "documents": store.document_names(),
    }