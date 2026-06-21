from pathlib import Path

def load_system_prompt():
    return Path(
        "/home/pachhh/Lain/prompts/system.txt"
    ).read_text(
        encoding="utf-8"
    ).strip()


class SystemProvider:

    def get_context(self):
        return load_system_prompt()