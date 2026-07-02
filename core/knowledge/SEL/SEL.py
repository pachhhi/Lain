from core.knowledge.SEL.dynamic_graph import SELDynamicGraph


class SELKnowledgeProvider:

    def __init__(self):
        self.graph = SELDynamicGraph()

    def get_context(self, user_input, flags=None, mode=None):
        concepts = self.graph.query(user_input)

        if not concepts:
            return None

        content = self.format(concepts)

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