from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Abstract base class for LLM providers.
    Concrete implementations must implement async generate(prompt, **kwargs) -> str
    """

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Send a prompt to the model and return the raw text response.
        """
        raise NotImplementedError
