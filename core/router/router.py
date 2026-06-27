
from core.intents.intents import Intent
from core.router.classifier import is_greeting, is_remember_request


class RuleRouter:
    def route(self, prompt: str) -> Intent:
        p = prompt.lower().strip()

        if is_greeting(p):
            return Intent.GREETING

        if is_remember_request(p):
            return Intent.MEMORY

        return Intent.CHAT