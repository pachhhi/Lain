from pathlib import Path


PROMPT_DIR = "/home/pachhh/Lain/prompts"

def load_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip()

class SystemProvider:

    def get_context(self, user_input=None, flags=None, mode=None):
        with open("prompts/system.txt") as f:
            return {
                "role": "system",
                "content": f.read()
            }