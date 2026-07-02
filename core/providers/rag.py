# core/providers/rag.py
import json
from core.knowledge.SEL.retriever import search

class RAGProvider:

    def __init__(self):
        with open("data/index.json", "r", encoding="utf-8") as f:
            self.index = json.load(f)

    def get_context(self, user_input, flags=None, mode=None):
        results = search(user_input, self.index, k=4)

        if not results:
            return None

        text = "WIKI CONTEXT:\n\n" + "\n".join(
            f"- {r['text']}" for r in results
        )

        return {
            "role": "system",
            "content": text
        }