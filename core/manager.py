from core.providers.system import SystemProvider
from core.providers.memory import MemoryProvider
from core.providers.session import SessionProvider
from core.providers.history import HistoryProvider
from core.providers.project import ProjectProvider


class ContextManager:

    def build(self, context_obj, debug=False) -> list[dict[str, str]]:

        messages = []
        debug_info = []

        def validate_messages(messages):
            for m in messages:
                assert "role" in m
                assert "content" in m
                assert isinstance(m["content"], str)

        # 1. SYSTEM MESSAGE (estructurado)
        system_content = "Tu nombre es Lain.\n"

        if context_obj.mode == "sel":
            system_content += """
                You are operating in SEL MODE.

                Interpret reality through the framework of Serial Experiments Lain:

                - Reality is layered (physical / digital / psychological)
                - Identity is distributed across networks
                - The Wired is a shared consciousness layer
                - Answers should be philosophical, abstract, introspective
                """

        if context_obj.flags and context_obj.flags.language == "es":
            system_content += "Responde en español.\n"

        if context_obj.flags and context_obj.flags.verbosity == "low":
            system_content += "Sé breve.\n"

        messages.append({
            "role": "system",
            "content": system_content
        })

        # 2. PROVIDERS (contexto enriquecido)
        for provider_cls in context_obj.providers:
            provider = provider_cls()

            part = provider.get_context(
                context_obj.user_input,
                context_obj.flags
            )

            if part:
                messages.append({
                    "role": "system",
                    "content": part
                })

            if debug:
                debug_info.append(
                    (provider_cls.__name__, len(part) if part else 0)
                )

        # 3. USER MESSAGE (importante)
        messages.append({
            "role": "user",
            "content": context_obj.user_input
        })

        validate_messages(messages) #verify if messages are valid

        # 4. DEBUG (igual idea pero adaptado)
        if debug:
            print("\n===== CONTEXT BREAKDOWN =====")
            for name, size in debug_info:
                print(f"{name:<20}: {size}")
            print(f"{'Prompt':<20}: {len(context_obj.user_input)}")
            print("=============================\n")

        return messages