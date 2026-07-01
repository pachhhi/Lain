from core.providers.system import SystemProvider
from core.providers.memory import MemoryProvider
from core.providers.session import SessionProvider
from core.providers.history import HistoryProvider
from core.providers.project import ProjectProvider


class ContextManager:

    def build(self, context_obj, debug=False):

        context = []
        debug_info = []

        for provider_cls in context_obj.providers:
            provider = provider_cls()

            part = provider.get_context(
                context_obj.prompt,
                context_obj.flags
            )

            if part:
                context.append(part)

            if debug:
                debug_info.append(
                    (provider_cls.__name__, len(part) if part else 0)
                )

        # SYSTEM dinámico
        system = "Tu nombre es Lain.\n"

        if context_obj.flags.language == "es":
            system += "Responde en español.\n"

        if context_obj.flags.verbosity == "low":
            system += "Sé breve.\n"

        context.insert(0, system)
        context.append(f"USER:\n{context_obj.prompt}")

        response = "\n\n".join(context)

        if debug:
            print("\n===== CONTEXT BREAKDOWN =====")
            for name, size in debug_info:
                print(f"{name:<20}: {size}")
            print(f"{'Prompt':<20}: {len(context_obj.prompt)}")
            print(f"{'Total':<20}: {len(response)}")
            print("=============================\n")

        return response

    