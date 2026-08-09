import json
from pathlib import Path

import faiss
import numpy as np

from app.config.settings import settings

_INDEX_FILE = "index.bin"
_CHUNKS_FILE = "chunks.json"


class FAISSStore:
    """Manages a FAISS vector index and its associated text chunks."""

    def __init__(self):
        self.index: faiss.Index | None = None
        self.chunks: list[dict] = []  # [{text, filename, chunk_index}, ...]

    def build(self, chunks: list[dict], embeddings: np.ndarray) -> None:
        """Build the FAISS index from chunks and their embeddings."""
        self.chunks = chunks
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype(np.float32))

    def search(self, query_embedding: np.ndarray, k: int = 5) -> list[dict]:
        """Return the top-k most similar chunks with relevance scores."""
        if self.index is None or self.index.ntotal == 0:
            return []

        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding.astype(np.float32), k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= 0:
                chunk = self.chunks[idx].copy()
                # Normalize distance to a 0-1 confidence score
                chunk["score"] = round(float(1 / (1 + dist)), 4)
                results.append(chunk)

        return results

    def save(self) -> None:
        """Persist the FAISS index and chunk metadata to disk."""
        index_dir = Path(settings.FAISS_INDEX_DIR)
        index_dir.mkdir(exist_ok=True)
        faiss.write_index(self.index, str(index_dir / _INDEX_FILE))
        (index_dir / _CHUNKS_FILE).write_text(
            json.dumps(self.chunks, indent=2, ensure_ascii=False)
        )

    def load(self) -> bool:
        """Load the index and chunk metadata from disk. Returns True if successful."""
        index_dir = Path(settings.FAISS_INDEX_DIR)
        index_path = index_dir / _INDEX_FILE
        chunks_path = index_dir / _CHUNKS_FILE

        if not index_path.exists() or not chunks_path.exists():
            return False

        try:
            self.index = faiss.read_index(str(index_path))
            self.chunks = json.loads(chunks_path.read_text())
            return True
        except Exception as e:
            print(f"Failed to load FAISS index: {e}")
            return False

    def total_chunks(self) -> int:
        return len(self.chunks)

    def document_names(self) -> list[str]:
        return list(set(c["filename"] for c in self.chunks))


# Global singleton used across the application
store = FAISSStore()
