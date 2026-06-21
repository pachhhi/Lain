import subprocess
import re

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich import box

console = Console()


def clean(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(
        r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])',
        '',
        text
    )
    text = re.sub(r'[⠁-⣿]', '', text)
    return text

def run_llm(prompt: str, model: str = "qwen3:8b") -> str:
    proc = subprocess.Popen(
    ["ollama", "run", model],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    )

    proc.stdin.write(prompt)
    proc.stdin.close()

    full_text = ""
    in_thinking = True

    with Live(
        Panel("", title="Lain", box=box.ASCII),
        refresh_per_second=20,
        console=console
    ) as live:

        for chunk in proc.stdout:
            chunk = clean(chunk)

            full_text += chunk

            text = Text()

            if "...done thinking." in full_text:
                thinking, answer = full_text.split(
                    "...done thinking.",
                    1
                )

                text.append(thinking, style="grey50")
                text.append("\n...done thinking.\n", style="grey50")
                text.append(answer, style="green")

            else:
                text.append(full_text, style="grey50")

            live.update(
                Panel(
                    text,
                    title="Lain",
                    border_style="blue",
                    box=box.ASCII
                )
            )

    proc.wait()
    print(f"Prompt size: {len(prompt):,} chars")

    return full_text