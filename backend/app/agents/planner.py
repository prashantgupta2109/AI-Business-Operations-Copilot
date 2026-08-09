import time

from app.agents.base import BaseAgent
from app.services.llm_service import call_llm

_SYSTEM_PROMPT = """\
You are a planning assistant for a business operations AI.
Your job is to break a user's question into 2-4 clear, actionable steps needed to answer it.
Rules:
- Return ONLY a numbered list (1. 2. 3. ...)
- Each step should be a short, clear action (under 15 words)
- Do NOT include any explanation, preamble, or conclusion
"""


class PlannerAgent(BaseAgent):
    name = "Planner"

    def run(self, query: str) -> dict:
        """
        Break a user query into a list of steps.
        Returns: {steps: list[str], timing: float}
        """
        start = time.time()

        prompt = f'Question: "{query}"\n\nList the steps to answer this:'
        raw_output = call_llm(prompt, system_prompt=_SYSTEM_PROMPT)

        # Detect LLM failure responses — use fallback silently
        error_indicators = ["cannot connect", "llm error", "llm returned", "no response", "error:"]
        if any(indicator in raw_output.lower() for indicator in error_indicators):
            raw_output = ""  # treat as empty so fallback kicks in

        # Parse numbered lines from LLM output
        steps = []
        for line in raw_output.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            # Strip leading number, dot, dash, parenthesis
            cleaned = line.lstrip("0123456789.-) ").strip()
            if cleaned and len(cleaned) > 5:  # skip very short/garbage lines
                steps.append(cleaned)

        # Fallback if LLM output couldn't be parsed
        if not steps:
            steps = [
                f"Search knowledge base for: {query[:60]}",
                "Identify the most relevant facts from retrieved documents",
                "Formulate a clear and accurate answer",
            ]

        return {"steps": steps, "timing": round(time.time() - start, 2)}
