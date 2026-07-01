from core.build_context import build_context
from core.router.router import RuleRouter
from core.router.route import get_route
from core.providers.ModeDetector import ModeDetector
from core.context.context_object import ContextObject
from core.llm.factory import LLMFactory
from config import MODEL


def run_lain(prompt, debug=True):

    router = RuleRouter()
    mode_detector = ModeDetector()

    # 1. Detectar modo
    mode = mode_detector.detect(prompt)

    # 2. Limpiar input (quita /sel, /debug, etc)
    clean_prompt = mode_detector.strip_mode(prompt)

    # 3. Router SOLO con input limpio
    routed = router.route(clean_prompt)

    # 4. Construcción explícita del ContextObject (IMPORTANTE)
    context_obj = ContextObject(
        user_input=clean_prompt,
        intent=routed.intent,
        mode=mode,
        flags=routed.flags,
        providers=get_route(routed.intent, mode)
    )

    # 5. Build messages
    messages = build_context(context_obj, debug)

    # 6. LLM runtime
    llm = LLMFactory.create(MODEL)
    response = llm.generate(messages)

    return response