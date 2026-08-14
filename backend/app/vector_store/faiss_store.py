import json
from pathlib import Path
import numpy as np
from app.config.settings import settings

_EMBEDDINGS_FILE = "embeddings.npy"
_CHUNKS_FILE = "chunks.json"


class FAISSStore:
    """
    A pure NumPy-based drop-in replacement for the FAISS vector store.
    Bypasses Windows Application Control DLL blocking by using standard NumPy array math.
    """

    def __init__(self):
        self.embeddings: np.ndarray | None = None
        self.chunks: list[dict] = []  # [{text, filename, chunk_index}, ...]

    def build(self, chunks: list[dict], embeddings: np.ndarray) -> None:
        """Build the vector index from chunks and their embeddings."""
        self.chunks = chunks
        self.embeddings = embeddings.astype(np.float32)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> list[dict]:
        """Return the top-k most similar chunks with relevance scores using L2 distance."""
        if self.embeddings is None or len(self.embeddings) == 0:
            return []

        # query_embedding comes in as shape (1, 384) or (384,)
        # Reshape query to match embeddings dimensions
        query = query_embedding.astype(np.float32).reshape(1, -1)

        # Calculate L2 distance squared (equivalent to faiss.IndexFlatL2)
        # (embeddings - query)^2 summed across the columns (384 dimensions)
        diff = self.embeddings - query
        distances = np.sum(diff ** 2, axis=1)

        # Sort indices by distance (ascending - closest first)
        indices = np.argsort(distances)

        k = min(k, len(self.chunks))
        results = []
        for idx in indices[:k]:
            chunk = self.chunks[idx].copy()
            dist = float(distances[idx])
            # Normalize distance to a 0-1 confidence score
            chunk["score"] = round(float(1 / (1 + dist)), 4)
            results.append(chunk)

        return results

    def save(self) -> None:
        """Persist the index and chunk metadata to disk."""
        index_dir = Path(settings.FAISS_INDEX_DIR)
        index_dir.mkdir(exist_ok=True)
        
        # Save embeddings as a binary numpy array file
        if self.embeddings is not None:
            np.save(str(index_dir / _EMBEDDINGS_FILE), self.embeddings)
            
        # Save chunk metadata as JSON
        (index_dir / _CHUNKS_FILE).write_text(
            json.dumps(self.chunks, indent=2, ensure_ascii=False)
        )

    def load(self) -> bool:
        """Load the index and chunk metadata from disk. Returns True if successful."""
        index_dir = Path(settings.FAISS_INDEX_DIR)
        embeddings_path = index_dir / _EMBEDDINGS_FILE
        chunks_path = index_dir / _CHUNKS_FILE

        if not embeddings_path.exists() or not chunks_path.exists():
            return False

        try:
            self.embeddings = np.load(str(embeddings_path))
            self.chunks = json.loads(chunks_path.read_text())
            return True
        except Exception as e:
            print(f"Failed to load vector store: {e}")
            return False

    def total_chunks(self) -> int:
        return len(self.chunks)

    def document_names(self) -> list[str]:
        return list(set(c["filename"] for c in self.chunks))


# Global singleton used across the application
store = FAISSStore()
