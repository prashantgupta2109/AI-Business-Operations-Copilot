import requests
from utils.constants import BACKEND_URL


class APIClient:
    """Thin wrapper around the backend REST API."""

    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url

    def health(self) -> dict:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=5)
            return r.json()
        except Exception:
            return {"status": "offline", "index_ready": False, "total_chunks": 0, "documents": []}

    def chat(self, query: str, top_k: int = 5) -> dict:
        r = requests.post(
            f"{self.base_url}/chat/",
            json={"query": query, "top_k": top_k},
            timeout=180,  # LLM can be slow
        )
        r.raise_for_status()
        return r.json()

    def list_documents(self) -> list:
        r = requests.get(f"{self.base_url}/documents/list", timeout=10)
        r.raise_for_status()
        return r.json()

    def upload_document(self, file_bytes: bytes, filename: str) -> dict:
        r = requests.post(
            f"{self.base_url}/documents/upload",
            files={"file": (filename, file_bytes, "text/plain")},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def delete_document(self, filename: str) -> dict:
        r = requests.delete(f"{self.base_url}/documents/{filename}", timeout=30)
        r.raise_for_status()
        return r.json()

    def reingest(self) -> dict:
        r = requests.post(f"{self.base_url}/documents/reingest", timeout=120)
        r.raise_for_status()
        return r.json()


# Global client instance used across all pages
client = APIClient()
