from ollama import Client
from core.llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(self, model: str):
        self.client = Client()
        self.model = model

    def generate(self, messages):

        response = self.client.chat(
            model=self.model,
            messages=messages,
        )

        return response["message"]["content"]