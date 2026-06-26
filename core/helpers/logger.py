from pathlib import Path
from datetime import datetime
import json


LOG_DIR = Path("/home/pachhh/Lain/logs")


def write_log(role, content):
    LOG_DIR.mkdir(exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")

    log_file = LOG_DIR / f"{date}.log"
    jsonl_file = LOG_DIR / f"{date}.jsonl"

    timestamp = datetime.now().strftime("%H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{role}]\n")
        f.write(content)
        f.write("\n\n")

    with open(jsonl_file, "a", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": timestamp,
                "role": role.lower(),
                "content": content,
            },
            f,
            ensure_ascii=False,
        )
        f.write("\n")