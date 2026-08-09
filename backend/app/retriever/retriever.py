from app.embeddings.embedder import embed
from app.vector_store.faiss_store import store
from app.config.settings import settings


def retrieve(query: str, k: int | None = None) -> list[dict]:
    """
    Retrieve the top-k most relevant chunks for a given query.
    Returns a list of chunk dicts with an added 'score' field.
    """
    k = k or settings.TOP_K
    query_embedding = embed([query])
    return store.search(query_embedding, k=k)
