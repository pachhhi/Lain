from tools.llm_tool import run_llm
from core.context import load_system_prompt, load_memory
from tools.llm_tool import run_llm

def build_context(prompt, mode="chat"):
    system = load_system_prompt()
    memory = load_memory()

    return f"""
{system}

{memory}

MODE: {mode}

USER:
{prompt}
"""

def run_lain(prompt, mode="chat", typing=True):
    full_prompt = build_context(prompt, mode)
    return run_llm(full_prompt, typing=typing)