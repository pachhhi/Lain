from core.intents.intents import Intent
from core.providers.system import SystemProvider
from core.providers.history import HistoryProvider
from core.providers.memory import MemoryProvider

ROUTES = {
    Intent.GREETING: [SystemProvider],
    Intent.CHAT: [SystemProvider, HistoryProvider],
    Intent.MEMORY: [SystemProvider, HistoryProvider, MemoryProvider],
}

def get_route(intent):
    return ROUTES[intent]