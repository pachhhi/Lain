from core.manager import ContextManager

def build_context(prompt, providers, debug):
    manager = ContextManager()
    return manager.build(prompt, providers, debug)