from core.knowledge.SEL.dynamic_graph import SELDynamicGraph


class SELKnowledgeProvider:

    def __init__(self):
        self.graph = SELDynamicGraph()

    def get_context(self, user_input, flags=None, mode=None):

        if mode != "sel":
            return None

        self.graph.ingest(user_input)
        concepts = self.graph.query(user_input)

        content = self.format(concepts)

        # 🔥 GARANTÍA ABSOLUTA
        if not content or not isinstance(content, str):
            content = "SEL WIRED:\n(no data available)"

        return {
            "role": "system",
            "content": content
        }

    def format(self, concepts):
        if not concepts:
            return "SEL WIRED:\n(no concepts)"

        return "SEL WIRED:\n\n" + "\n".join(
            f"- {str(c)}"
            for c in concepts
        )