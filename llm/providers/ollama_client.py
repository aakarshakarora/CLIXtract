import ollama

from llm.base_client import LLMClient


class OllamaClient(LLMClient):
    def __init__(self, model: str, temperature: float):
        self.client = ollama.Client()
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str, **kwargs) -> str:
        # Synchronous call
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "top_p": 1,
            },
        )
        return response.response  # access the text
