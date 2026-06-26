from core.providers.system import SystemProvider
from core.providers.memory import MemoryProvider
from core.providers.session import SessionProvider
from core.providers.history import HistoryProvider
from core.providers.project import ProjectProvider


class ContextManager:
    def __init__(self):
        self.providers = [
            SystemProvider(),
            MemoryProvider(),
            SessionProvider(),
            # ProjectProvider(),
            HistoryProvider(),
        ]

    def build(self, prompt):
        context = []

        for provider in self.providers:
            part = provider.get_context(prompt)

            if part:
                context.append(part)

        context.append(f"USER:\n{prompt}")

        return "\n\n".join(context)