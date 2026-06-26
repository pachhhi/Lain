#llamar a run_llm (se puede upgradear ejemplos: aislar ollama, metricas, tokens, etc.), NO tiene contexto ni nada, es el modelo de Lain, mas no Lain.

import subprocess
from config import MODEL

def run_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        capture_output=True,
        text=True,
    )

    return result.stdout