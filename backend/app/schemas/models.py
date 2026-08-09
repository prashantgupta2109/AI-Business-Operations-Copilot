from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5


class Source(BaseModel):
    filename: str
    chunk: str
    score: float


class AgentTiming(BaseModel):
    planner: float
    researcher: float
    executor: float
    reviewer: float


class ChatResponse(BaseModel):
    answer: str
    plan: list[str]
    sources: list[Source]
    confidence: float
    timing: AgentTiming


class DocumentInfo(BaseModel):
    filename: str
    chunks: int


class IngestionResponse(BaseModel):
    message: str
    total_chunks: int
    documents_processed: int
