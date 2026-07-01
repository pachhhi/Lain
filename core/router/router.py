from core.intents.intents import Intent
from core.router.classifier import is_greeting, is_remember_request
from core.router.flags import Flags
from core.context.context_object import ContextObject


class RuleRouter:

    def route(self, prompt: str):

        p = prompt.lower().strip()

        flags = Flags()

        if is_greeting(p):
            return ContextObject(
                prompt=prompt,
                intent=Intent.GREETING,
                flags=flags
            )

        if is_remember_request(p):
            return ContextObject(
                prompt=prompt,
                intent=Intent.REMEMBER,
                flags=flags
            )

        return ContextObject(
            prompt=prompt,
            intent=Intent.CHAT,
            flags=flags
        )