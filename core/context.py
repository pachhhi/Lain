from pathlib import Path
import json
import re
from datetime import datetime


def _remove_thinking_blocks(text: str) -> str:
    """Remove chain-of-thought blocks from text.
    
    Removes blocks between 'Thinking...' (or 'Thinking..') and '...done thinking.' (or '...done thinking').
    Handles various whitespace and punctuation variants.
    """
    if not isinstance(text, str):
        return text

    pattern = re.compile(
        r"Thinking\.+\s*.*?(?:\.\.\.)?done thinking\.?",
        re.IGNORECASE | re.DOTALL
    )
    result = pattern.sub("", text).strip()
    return result if result else text.strip()


def load_system_prompt():
    return Path("/home/pachhh/Lain/prompts/system.txt") \
        .read_text(encoding="utf-8").strip()


def load_last_messages(limit=5):
    log_dir = Path("/home/pachhh/Lain/logs")

    jsonl_file = (
        log_dir /
        f"{datetime.now():%Y-%m-%d}.jsonl"
    )

    if not jsonl_file.exists():
        return []

    messages = []
    with open(jsonl_file, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            message = json.loads(line)
            if "content" in message and isinstance(message["content"], str):
                message["content"] = _remove_thinking_blocks(message["content"])
            messages.append(message)

    return messages[-limit:]

SESSION_FILE = Path(
    "/home/pachhh/Lain/memory/session.json"
)

def load_session():
    if not SESSION_FILE.exists():
        return {}

    try:
        content = SESSION_FILE.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            return {}

        return json.loads(content)

    except Exception:
        return {}

def save_session(data):
    SESSION_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    SESSION_FILE.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

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