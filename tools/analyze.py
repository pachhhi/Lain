from tools.run_lain import run_lain
from pathlib import Path

def analyze_file(file_path: str, question: str = "") -> str:
    path = Path(file_path).expanduser()

    if not path.exists():
        return f"Archivo no encontrado: {file_path}"

    code = path.read_text(encoding="utf-8", errors="ignore")

    prompt = f"""
FILE: {file_path}

CODE:
{code}

QUESTION:
{question if question else "Explain what this file does."}
"""

    return run_lain(prompt, mode="analyze", typing=True)