from core.llm.ollama import OllamaLLM
from core.llm.client import LLMClient
from config import MODEL

def run_llm(model, messages):
    llm = LLMFactory.create(model)
    return llm.generate(messages)