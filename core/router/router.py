from core.intents.intents import Intent
from core.router.classifier import is_greeting, is_remember_request
from core.router.flags import Flags
from core.context.context_object import ContextObject


class RuleRouter:

    def route(self, user_input: str):

        flags = Flags()

        if is_greeting(user_input):
            return ContextObject(
                user_input=str(user_input),  
                intent=Intent.GREETING,
                flags=flags
            )

        if is_remember_request(user_input):
            return ContextObject(
                user_input=str(user_input),   
                intent=Intent.REMEMBER,
                flags=flags
            )

        return ContextObject(
            user_input=str(user_input),  
            intent=Intent.CHAT,
            flags=flags
        )