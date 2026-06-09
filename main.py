from pathlib import Path
from datetime import datetime
import json
import os
import shutil

from ollama import chat

from config import (
    MODEL,
    ASSISTANT_NAME,
    USER_NAME,
)

from tools.run_lain import run_lain
from tools.aider_tool import run_aider
from tools.analyze import analyze_file

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
        memory_file,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    facts = data.get("facts", [])

    if not facts:
        return ""

    return (
        "\n\nInformación conocida del usuario:\n"
        + "\n".join(
            f"- {fact}"
            for fact in facts
        )
    )


def write_log(role, content):
    log_dir = Path(
        "/home/pachhh/Lain/logs"
    )

    log_dir.mkdir(
        exist_ok=True
    )

    logfile = (
        log_dir
        / f"{datetime.now():%Y-%m-%d}.log"
    )

    timestamp = datetime.now().strftime(
        "%H:%M:%S"
    )

    with open(
        logfile,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(
            f"[{timestamp}] [{role}]\n"
        )

        f.write(content)
        f.write("\n\n")

#
def read_file(filepath):
    path = Path(filepath).expanduser()

    if not path.exists():
        raise FileNotFoundError(
            f"Archivo no encontrado: {path}"
        )

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


def backup_file(filepath):
    path = Path(filepath).expanduser()

    backup_path = Path(
        str(path) + ".bak"
    )

    shutil.copy2(
        path,
        backup_path
    )

    return backup_path

def main():
    # system_prompt = (
    #     load_system_prompt()
    #     + load_memory()
    # )

    # messages = [
    #     {
    #         "role": "system",
    #         "content": system_prompt
    #     }
    # ]

    print(
        f"[{ASSISTANT_NAME} v1]"
    )

    print(
        "Escribí 'exit' para salir.\n"
    )

    while True:
        user_input = input("> ")

        if user_input.lower() == "exit":
            print("Adiós!")
            break

        elif user_input.startswith("/analyze "):
            parts = user_input[len("/analyze "):].strip().split(" ", 1)

            file_path = parts[0]
            question = parts[1] if len(parts) > 1 else ""

            result = analyze_file(file_path, question)

            continue

        elif user_input.startswith("/aider "):
            
            continue

        run_lain(user_input)


if __name__ == "__main__":
    main()
