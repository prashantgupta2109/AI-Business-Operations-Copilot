from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Abstract base class for all agents in the pipeline."""

    name: str = "BaseAgent"

    @abstractmethod
    def run(self, **kwargs) -> dict:
        """Execute the agent's task and return a result dict."""
        pass
