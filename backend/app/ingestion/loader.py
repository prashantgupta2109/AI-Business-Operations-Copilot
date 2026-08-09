from pathlib import Path
from app.config.settings import settings


def load_documents() -> list[dict]:
    """
    Load all .txt files from the knowledge directory.
    Returns a list of dicts: {filename, content, size_bytes}
    """
    knowledge_dir = Path(settings.KNOWLEDGE_DIR)

    if not knowledge_dir.exists():
        print(f"Knowledge directory '{knowledge_dir}' does not exist.")
        return []

    documents = []
    for file_path in sorted(knowledge_dir.glob("*.txt")):
        try:
            content = file_path.read_text(encoding="utf-8")
            documents.append({
                "filename": file_path.name,
                "content": content,
                "size_bytes": file_path.stat().st_size,
            })
            print(f"  Loaded: {file_path.name} ({file_path.stat().st_size} bytes)")
        except Exception as e:
            print(f"  Failed to load {file_path.name}: {e}")

    return documents
