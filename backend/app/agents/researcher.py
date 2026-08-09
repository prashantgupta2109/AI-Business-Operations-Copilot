import time

from app.agents.base import BaseAgent
from app.retriever.retriever import retrieve


class ResearcherAgent(BaseAgent):
    name = "Researcher"

    def run(self, query: str, steps: list[str], top_k: int = 5) -> dict:
        """
        Retrieve relevant document chunks for the query and first plan steps.
        Returns: {chunks: list[dict], sources: list[str], timing: float}
        """
        start = time.time()

        # Retrieve chunks for the main query
        chunks = retrieve(query, k=top_k)
        seen = {c["text"] for c in chunks}

        # Also retrieve for first 2 plan steps to broaden context
        for step in steps[:2]:
            for chunk in retrieve(step, k=2):
                if chunk["text"] not in seen:
                    chunks.append(chunk)
                    seen.add(chunk["text"])

        # Sort all results by relevance score (highest first) and keep top_k
        chunks.sort(key=lambda c: c.get("score", 0), reverse=True)
        chunks = chunks[:top_k]

        sources = list(set(c["filename"] for c in chunks))

        return {
            "chunks": chunks,
            "sources": sources,
            "timing": round(time.time() - start, 2),
        }
