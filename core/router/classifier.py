from core.intents.intents import Intent


def is_greeting(prompt: str) -> bool:
    return prompt in {
        "hola",
        "holaa",
        "hola lain",
        "buenas",
        "hey",
    }

def is_remember_request(prompt: str) -> bool:
    p = prompt.lower()

    keywords = [
        "recorda",
        "recuerda",
        "acordate",
        "remember",
        "memoriza",
        "guarda esto",
    ]

    return any(k in p for k in keywords)

class RuleClassifier:

    def classify(self, prompt: str) -> Intent:
        p = prompt.lower().strip()

        if is_greeting(p):
            return Intent.GREETING
        if is_remember_request(p):
            return Intent.MEMORY, Intent


        return Intent.CHAT

