from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.config.settings import settings
from app.ingestion.pipeline import run_ingestion
from app.vector_store.faiss_store import store

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/list")
def list_documents():
    """List all indexed documents with their chunk counts."""
    if not store.chunks:
        return []

    file_chunk_counts: dict[str, int] = {}
    for chunk in store.chunks:
        fname = chunk["filename"]
        file_chunk_counts[fname] = file_chunk_counts.get(fname, 0) + 1

    return [{"filename": k, "chunks": v} for k, v in sorted(file_chunk_counts.items())]


@router.post("/upload")
async def upload_document(file: UploadFile):
    """Upload a .txt document and add it to the knowledge base."""
    if not file.filename or not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported.")

    knowledge_dir = Path(settings.KNOWLEDGE_DIR)
    knowledge_dir.mkdir(exist_ok=True)

    dest_path = knowledge_dir / file.filename
    content = await file.read()
    dest_path.write_bytes(content)
    print(f"Uploaded: {file.filename}")

    result = run_ingestion()
    return {
        "message": f"'{file.filename}' uploaded and knowledge base rebuilt.",
        "total_chunks": result["chunks"],
        "documents_processed": result["documents"],
    }


@router.post("/reingest")
def reingest():
    """Re-process all documents in the knowledge directory."""
    result = run_ingestion()
    return {
        "message": "Re-ingestion complete.",
        "total_chunks": result["chunks"],
        "documents_processed": result["documents"],
    }


@router.delete("/{filename}")
def delete_document(filename: str):
    """Delete a document from the knowledge base and rebuild the index."""
    file_path = Path(settings.KNOWLEDGE_DIR) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    file_path.unlink()
    print(f"Deleted: {filename}")

    result = run_ingestion()
    return {
        "message": f"'{filename}' deleted and knowledge base rebuilt.",
        "total_chunks": result["chunks"],
        "documents_processed": result["documents"],
    }
