from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, chat, documents
from app.ingestion.pipeline import run_ingestion
from app.vector_store.faiss_store import store

app = FastAPI(
    title="AI Business Operations Copilot",
    description="Multi-agent RAG system for intelligent business operations.",
    version="1.0.0",
)

# Allow the Streamlit frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(documents.router)


@app.on_event("startup")
def on_startup():
    """Load existing FAISS index on startup, or build one from scratch."""
    loaded = store.load()
    if loaded:
        print(f"\n[Startup] Loaded existing FAISS index ({store.total_chunks()} chunks).")
    else:
        print("\n[Startup] No index found. Running initial ingestion...")
        run_ingestion()


@app.get("/")
def root():
    return {"message": "AI Business Operations Copilot is running. Visit /docs for the API."}