from core.knowledge.SEL.vector_index import SELVectorIndex

class SELKnowledgeProvider:

    def __init__(self):
        self.index = SELVectorIndex()

    def get_context(self, user_input, flags):

        if not flags or flags.mode != "sel":
            return None

        results = self.index.search(user_input)

        if not results:
            return {
                "role": "system",
                "content": self.fallback()
            }

        return {
            "role": "system",
            "content": self.format(results)
        }

    def format(self, results):
        return "SEL KNOWLEDGE:\n\n" + "\n".join(f"- {r}" for r in results)

    def fallback(self):
        return """
SEL MODE ACTIVE:

You interpret reality through SEL lens:
- identity is distributed
- reality is layered
- consciousness emerges from networks
"""