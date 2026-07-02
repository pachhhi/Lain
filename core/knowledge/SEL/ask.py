# core/knowledge/SEL/ask.py
import json
from core.retriever import search

INDEX_PATH = "data/index.json"


def load_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


index = load_index()


def ask(query: str):
    results = search(query, index)

    print("\n===== CONTEXT =====\n")

    for r in results:
        print(f"[{r['section']}] {r['text']}\n")

    return results