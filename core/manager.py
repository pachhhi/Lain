from core.providers.system import SystemProvider
from core.providers.memory import MemoryProvider
from core.providers.session import SessionProvider
from core.providers.history import HistoryProvider
from core.providers.project import ProjectProvider


class ContextManager:

    def build(self, prompt, providers, debug=False):

        context = []
        debug_info = []

        for provider_cls in providers:
            provider = provider_cls()

            part = provider.get_context(prompt)

            if part:
                context.append(part)

            if debug:
                debug_info.append(
                    (provider_cls.__name__, len(part) if part else 0)
                )

        context.append(f"USER:\n{prompt}")

        final_context = "\n\n".join(context)

        if debug:
            print("\n===== CONTEXT BREAKDOWN =====")

            for name, size in debug_info:
                print(f"{name:<20}: {size}")

            print(f"{'Prompt':<20}: {len(prompt)}")
            print(f"{'Total':<20}: {len(final_context)}")
            print("=============================\n")

        return final_context

    