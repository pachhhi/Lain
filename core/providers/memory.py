from pathlib import Path
import json

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

class MemoryProvider:

    def get_context(self):
        text = load_memory()

        return {
            "text": text,
            "chars": len(text),
            "tokens_est": len(text) // 4
        }

    def get_chars(self):
        return len(load_memory())