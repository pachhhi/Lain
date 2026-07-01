from pathlib import Path


PROMPT_DIR = "/home/pachhh/Lain/prompts"

def load_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip()

class SystemProvider:

    def get_context(self, prompt=None, flags=None):
        parts = [
            load_file(f"{PROMPT_DIR}/system.txt"),
        ]

        return "\n\n".join(parts)