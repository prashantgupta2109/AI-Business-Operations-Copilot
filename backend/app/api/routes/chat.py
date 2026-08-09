from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.models import ChatRequest, ChatResponse
from app.agents.orchestrator import run_pipeline
from app.vector_store.faiss_store import store
import traceback

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
def chat(request: ChatRequest):
    """Process a user query through the 4-agent RAG pipeline."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if store.total_chunks() == 0:
        raise HTTPException(
            status_code=503,
            detail="Knowledge base is empty. Please upload documents first.",
        )

    try:
        result = run_pipeline(query=request.query, top_k=request.top_k)
        return result
    except Exception as e:
        # Print full traceback to backend terminal for debugging
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(e)}"
        )
