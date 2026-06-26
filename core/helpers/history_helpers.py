from pathlib import Path
from datetime import datetime
import json 

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
            messages.append(message)

    return messages[-limit:]

SESSION_FILE = Path(
    "/home/pachhh/Lain/memory/session.json"
)