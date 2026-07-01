from core.knowledge.SEL.index import SELIndex

class SELKnowledgeProvider:

    def __init__(self):
        self.index = SELIndex()

    def get_context(self, user_input, flags):

        if not flags or flags.mode != "sel":
            return None

        results = self.index.search(user_input)

        # 🔥 FALLBACK IMPORTANTE
        if not results:
            return {
                "role": "system",
                "content": self.base_context()
            }

        return {
            "role": "system",
            "content": self.format(results)
        }

#     def base_context(self):
#         return """
# SEL MODE ACTIVE:

# You interpret reality through the lens of Serial Experiments Lain.

# Core principles:
# - reality is layered (physical / digital / perceptual)
# - identity is fragmented across systems
# - The Wired represents interconnected consciousness
# """