from app.config.settings import settings


def chunk_document(content: str, filename: str) -> list[dict]:
    """
    Split a document into overlapping text chunks.
    Returns a list of dicts: {text, filename, chunk_index}
    """
    size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP
    chunks = []
    start = 0

    while start < len(content):
        text = content[start : start + size].strip()
        if text:
            chunks.append({
                "text": text,
                "filename": filename,
                "chunk_index": len(chunks),
            })
        start += size - overlap

    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chunk all documents and return a flat list of all chunks."""
    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_document(doc["content"], doc["filename"])
        all_chunks.extend(doc_chunks)
    return all_chunks
