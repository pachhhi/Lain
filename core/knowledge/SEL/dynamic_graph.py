import numpy as np
from core.embeddings.engine import EmbeddingEngine
from core.knowledge.SEL.node import ConceptNode


class SELDynamicGraph:

    def __init__(self):
        self.embedder = EmbeddingEngine()
        self.nodes = {}

    # ---------------------------
    # MAIN ENTRY
    # ---------------------------
    def ingest(self, text: str):
        emb = self.embedder.embed(text)

        best_node = self._find_best_node(emb)

        if best_node and best_node[1] > 0.75:
            node = self.nodes[best_node[0]]
            node.count += 1
            created = False
        else:
            node = ConceptNode(text, emb)
            self.nodes[text] = node
            created = True

        self._update_edges(node)

        # 🔥 TELEMETRÍA SIMPLE
        print("\n[SEL GRAPH UPDATE]")
        print(f"input: {text}")
        print(f"nodes: {len(self.nodes)}")
        print(f"created: {created}")
        print("--------------------\n")

    # ---------------------------
    # SEARCH
    # ---------------------------
    def query(self, text: str, top_k=5):
        emb = self.embedder.embed(text)

        scored = []

        for node in self.nodes.values():
            score = self._cos(emb, node.embedding)
            scored.append((score, node))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [n.text for _, n in scored[:top_k]]

    # ---------------------------
    # GRAPH BUILDING
    # ---------------------------
    def _update_edges(self, node):
        for other in self.nodes.values():

            if other.text == node.text:
                continue

            sim = self._cos(node.embedding, other.embedding)

            if sim > 0.4:
                node.edges[other.text] = sim
                other.edges[node.text] = sim

    # ---------------------------
    # UTILS
    # ---------------------------
    def _find_best_node(self, emb):
        best = None
        best_score = 0

        for text, node in self.nodes.items():
            score = self._cos(emb, node.embedding)

            if score > best_score:
                best = text
                best_score = score

        if best is None:
            return None

        return best, best_score

    def _cos(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# DEBUGGING ---------------------
    def debug_state(self):
        print("\n===== SEL GRAPH STATE =====")
        print(f"NODES: {len(self.nodes)}")

        for text, node in self.nodes.items():
            print(f"\nNODE: {text}")
            print(f"  count: {node.count}")
            print(f"  edges: {len(node.edges)}")

            for e, w in node.edges.items():
                print(f"    -> {e} ({w:.2f})")

        print("===========================\n")