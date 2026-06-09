from pathlib import Path
import json

def load_system_prompt():
    return Path("/home/pachhh/Lain/prompts/system.txt") \
        .read_text(encoding="utf-8").strip()


def load_memory():
    memory_file = Path("/home/pachhh/Lain/memory/memory.json")

    if not memory_file.exists():
        return ""

    data = json.loads(memory_file.read_text(encoding="utf-8"))
    facts = data.get("facts", [])

    if not facts:
        return ""

    return (
        "\n\nInformación conocida del usuario:\n"
        + "\n".join(f"- {f}" for f in facts)
    )