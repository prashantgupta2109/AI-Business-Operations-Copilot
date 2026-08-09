import numpy as np
from sentence_transformers import SentenceTransformer
from app.config.settings import settings

# Lazily loaded singleton to avoid loading on import
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"   Loading embedding model: {settings.EMBEDDING_MODEL}...")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed(texts: list[str]) -> np.ndarray:
    """Convert a list of texts to embedding vectors."""
    model = _get_model()
    return model.encode(texts, show_progress_bar=False)
