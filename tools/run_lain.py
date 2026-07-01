

from core.build_context import build_context
from tools.llm_tool import run_llm
from core.router.router import RuleRouter
from core.router.route import  get_route
from core.router.flags import Flags


def run_lain(prompt, debug=True):
    router = RuleRouter()

    context_obj = router.route(prompt)

    context_obj.providers = get_route(context_obj.intent)

    context = build_context(context_obj, debug)

    response = run_llm(context)

    return response