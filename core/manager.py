from core.providers.system import SystemProvider
from core.providers.memory import MemoryProvider
# from core.providers.history import HistoryProvider

class ContextManager:

    def build(self, prompt, mode):

        context = []

        context.append(
            SystemProvider().get_context()
            # print(SystemProvider().get_context())
        )

        memory = MemoryProvider().get_context()
        context.append(
            memory["text"]
        )

        # context.append(
        #     HistoryProvider().get_context()
        # )

        # context.append(
        #     f"USER:\n{prompt}"
        # )

        print(context)

        return "\n\n".join(
            block for block in context
            if block
        )