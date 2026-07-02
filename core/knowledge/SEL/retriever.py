import numpy as np
from core.embeddings.engine import EmbeddingEngine

engine = EmbeddingEngine()


def cosine(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search(query: str, index, k=5):
    q_emb = engine.embed(query)

    scored = []

    for item in index:
        score = cosine(q_emb, item["embedding"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in scored[:k]]