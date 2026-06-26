from core.manager import ContextManager

def build_context(prompt):
    manager = ContextManager()
    return manager.build(prompt)