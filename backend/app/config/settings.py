from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM (Ollama)
    OLLAMA_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3"

    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Paths (relative to backend/ directory)
    KNOWLEDGE_DIR: str = "knowledge"
    FAISS_INDEX_DIR: str = "faiss_index"

    # Retrieval
    TOP_K: int = 5
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    # App
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
