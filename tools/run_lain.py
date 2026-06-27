

from core.context import build_context
from tools.llm_tool import run_llm
from core.router.router import RuleRouter
from core.router.route import  get_route


def run_lain(prompt, debug=True):

    router = RuleRouter()

    intent = router.route(prompt)
    providers = get_route(intent)
    # print(providers)

    context = build_context(prompt, providers, debug)
    # print("=" * 50)
    # print(context)
    # print("=" * 50)
    response = run_llm(context)

    return response