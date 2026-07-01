from core.llm.ollama import OllamaLLM
from core.llm.client import LLMClient
from config import MODEL

provider = OllamaLLM(MODEL)
llm = LLMClient(provider)


def run_llm(prompt: str) -> str:

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    return llm.generate(messages)