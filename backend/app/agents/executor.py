import time

from app.agents.base import BaseAgent
from app.services.llm_service import call_llm

_SYSTEM_PROMPT = """\
You are a professional business operations assistant.
Answer the user's question based ONLY on the context provided below.
If the context does not contain enough information, say so clearly and briefly.
Be concise, accurate, and professional. Use bullet points or numbered lists where appropriate.
"""


class ExecutorAgent(BaseAgent):
    name = "Executor"

    def run(self, query: str, chunks: list[dict]) -> dict:
        """
        Generate an answer to the query using retrieved chunks as context.
        Returns: {answer: str, timing: float}
        """
        start = time.time()

        # Build the context block from retrieved chunks
        context_parts = [
            f"[Source: {c['filename']}]\n{c['text']}" for c in chunks
        ]
        context = "\n\n".join(context_parts)

        prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        answer = call_llm(prompt, system_prompt=_SYSTEM_PROMPT)

        return {"answer": answer, "timing": round(time.time() - start, 2)}
