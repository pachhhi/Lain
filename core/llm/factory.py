from core.llm.ollama import OllamaLLM
from core.llm.client import LLMClient

class LLMFactory:
    def create(model):
        provider = OllamaLLM(model)
        return LLMClient(provider)