from core.manager import ContextManager

def build_context(context_obj, debug=False):

    manager = ContextManager()

    messages = manager.build(context_obj, debug)

    return messages