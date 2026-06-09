import subprocess
import os

PROJECT_DIR = os.getcwd()

ANALYSIS_SYSTEM_PROMPT = """
You are in ANALYSIS MODE.

Rules:
- You MUST NOT modify any files.
- You MUST NOT propose diffs or edits.
- You MUST NOT use tools that modify code.
- Only read and explain code.
- Be concise and direct.
- If the user asks for changes, explain what would change but do NOT apply them.

If you detect an instruction that requires editing, refuse and explain what would be done instead.
"""

def run_aider(prompt: str) -> str:
    full_prompt = f"{ANALYSIS_SYSTEM_PROMPT}\n\nUSER REQUEST:\n{prompt}"

    proc = subprocess.Popen(
        [
            "aider",
            "--yes",
            "--read-only",
            "--no-show-model-warnings",
            "--model",
            "ollama/qwen3:8b",
            "--message",
            full_prompt,
        ],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    output = []

    for line in proc.stdout:
        output.append(line)

    proc.wait()

    return "".join(output)