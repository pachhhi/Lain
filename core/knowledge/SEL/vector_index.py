from core.embeddings.engine import EmbeddingEngine
import numpy as np

class SELVectorIndex:

    def __init__(self):
        self.embedder = EmbeddingEngine()
        self.data = []

        self._load_base_concepts()

    def _load_base_concepts(self):
        concepts = [
            "The Wired is a distributed consciousness network.",
            "Identity is fragmented across physical and digital layers.",
            "Reality is subjective and perception-based.",
            "Lain exists across multiple states of consciousness.",
            "The boundary between human and machine is blurred."
        ]

        for c in concepts:
            self.add(c)

    def add(self, text: str):
        emb = self.embedder.embed(text)

        self.data.append({
            "text": text,
            "embedding": emb
        })

    def search(self, query: str, k=3):
        q_emb = self.embedder.embed(query)

        scored = []

        for item in self.data:
            score = self._cosine(q_emb, item["embedding"])
            scored.append((score, item["text"]))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [t for _, t in scored[:k]]

    def _cosine(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))