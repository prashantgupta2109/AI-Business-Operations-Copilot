import time

from app.agents.base import BaseAgent

# Phrases that indicate the LLM failed to produce a useful answer
_FAILURE_PHRASES = [
    "cannot connect",
    "error:",
    "i don't know",
    "i do not know",
    "no information",
    "not enough information",
    "context does not",
    "context provided does not",
]


class ReviewerAgent(BaseAgent):
    name = "Reviewer"

    def run(self, answer: str, chunks: list[dict]) -> dict:
        """
        Assess the quality of the executor's answer.
        Returns: {final_answer: str, confidence: float, timing: float}
        """
        start = time.time()

        if not chunks:
            confidence = 0.1
        else:
            # Average chunk relevance score as base confidence
            avg_score = sum(c.get("score", 0) for c in chunks) / len(chunks)
            confidence = round(min(avg_score * 1.3, 0.98), 2)

        # Penalise if answer shows signs of failure
        answer_lower = answer.lower()
        if any(phrase in answer_lower for phrase in _FAILURE_PHRASES):
            confidence = max(round(confidence - 0.3, 2), 0.05)

        return {
            "final_answer": answer,
            "confidence": confidence,
            "timing": round(time.time() - start, 2),
        }
