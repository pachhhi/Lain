

from core.context import build_context
from tools.llm_tool import run_llm
from core.providers.system import SystemProvider
from core.providers.memory import MemoryProvider
from core.providers.session import SessionProvider
from core.providers.project import ProjectProvider
from core.providers.history import HistoryProvider


def run_lain(prompt, debug=True):

    context = build_context(prompt)
    response = run_llm(context)
    print(context)


    #DEBUG
    system = SystemProvider().get_context()
    memory = MemoryProvider().get_context()
    session = SessionProvider().get_context()
    history = HistoryProvider().get_context()
    
    if debug:
        print("\n===== CONTEXT BREAKDOWN =====")
        print("system:", len(system))
        print("memory:", len(memory))
        print("session:", len(session))
        # print("project:", len(project))
        print("history:", len(history))
        print("prompt:", len(prompt))
        print("total:", len(context))
        print("=============================\n")

    return response