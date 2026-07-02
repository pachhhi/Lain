from core.intents.intents import Intent
from core.providers.system import SystemProvider
from core.providers.history import HistoryProvider
from core.providers.memory import MemoryProvider
from core.knowledge.SEL.SEL import SELKnowledgeProvider
from core.providers.rag import RAGProvider

ROUTES = {
    Intent.GREETING: [SystemProvider],
    Intent.CHAT: [SystemProvider, HistoryProvider, RAGProvider],
    Intent.REMEMBER: [SystemProvider, HistoryProvider, MemoryProvider],
}

FEATURE_PROVIDERS = {
    # "sel": [SELKnowledgeProvider],
}

def get_route(intent, mode=None):

    base = ROUTES[intent]

    if mode and mode in FEATURE_PROVIDERS:
        base = FEATURE_PROVIDERS[mode] + base

    return base