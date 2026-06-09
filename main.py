from pathlib import Path
from datetime import datetime
import json

from ollama import chat

from config import (
    MODEL,
    ASSISTANT_NAME,
    USER_NAME,
)

from tools.aider_tool import run_aider

def load_system_prompt():
    return Path(
        "/home/pachhh/Lain/prompts/system.txt"
    ).read_text(
        encoding="utf-8"
    ).strip()


def load_memory():
    memory_file = Path(
        "/home/pachhh/Lain/memory/memory.json"
    )

    if not memory_file.exists():
        return ""

    with open(
        memory
