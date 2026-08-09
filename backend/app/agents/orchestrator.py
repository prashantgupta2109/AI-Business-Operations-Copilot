from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearcherAgent
from app.agents.executor import ExecutorAgent
from app.agents.reviewer import ReviewerAgent

# Agent singletons
_planner = PlannerAgent()
_researcher = ResearcherAgent()
_executor = ExecutorAgent()
_reviewer = ReviewerAgent()


def run_pipeline(query: str, top_k: int = 5) -> dict:
    """
    Run the full 4-agent pipeline:
      Planner → Researcher → Executor → Reviewer

    Returns a structured result dict matching the ChatResponse schema.
    """
    print(f"\n[Pipeline] Starting for: '{query[:60]}...'")

    # --- Step 1: Planner ---
    print("[1/4] Planner: Breaking query into steps...")
    plan = _planner.run(query=query)

    # --- Step 2: Researcher ---
    print("[2/4] Researcher: Retrieving relevant documents...")
    research = _researcher.run(query=query, steps=plan["steps"], top_k=top_k)

    # --- Step 3: Executor ---
    print("[3/4] Executor: Generating answer...")
    execution = _executor.run(query=query, chunks=research["chunks"])

    # --- Step 4: Reviewer ---
    print("[4/4] Reviewer: Assessing answer quality...")
    review = _reviewer.run(answer=execution["answer"], chunks=research["chunks"])

    print(f"   Pipeline complete. Confidence: {review['confidence']}\n")

    return {
        "answer": review["final_answer"],
        "plan": plan["steps"],
        "sources": [
            {
                "filename": c["filename"],
                "chunk": c["text"][:250] + "..." if len(c["text"]) > 250 else c["text"],
                "score": c.get("score", 0.0),
            }
            for c in research["chunks"]
        ],
        "confidence": review["confidence"],
        "timing": {
            "planner": plan["timing"],
            "researcher": research["timing"],
            "executor": execution["timing"],
            "reviewer": review["timing"],
        },
    }
