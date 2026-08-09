from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_documents
from app.embeddings.embedder import embed
from app.vector_store.faiss_store import store


def run_ingestion() -> dict:
    """
    Full ingestion pipeline: Load -> Chunk -> Embed -> Store.
    Returns counts of documents processed and chunks created.
    """
    print("\n[Step 1] Loading documents...")
    documents = load_documents()
    if not documents:
        print("  WARNING: No documents found. Add .txt files to the knowledge/ directory.")
        return {"documents": 0, "chunks": 0}
    print(f"  OK: Loaded {len(documents)} document(s).")

    print("[Step 2] Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"  OK: Created {len(chunks)} chunks.")

    print("[Step 3] Generating embeddings...")
    texts = [c["text"] for c in chunks]
    embeddings = embed(texts)
    print(f"  OK: Generated {len(embeddings)} embeddings.")

    print("[Step 4] Building and saving FAISS index...")
    store.build(chunks, embeddings)
    store.save()
    print("  OK: FAISS index saved.\n")

    return {"documents": len(documents), "chunks": len(chunks)}
