from pathlib import Path
import hashlib
import json

BASE_DIR = Path("/home/pachhh/Lain/memory/sessions")


def get_session_path():
    cwd = str(Path.cwd())
    session_id = hashlib.md5(cwd.encode()).hexdigest()
    return BASE_DIR / f"{session_id}.json"


def load_session():
    path = get_session_path()

    if not path.exists():
        return {
            "current_project": str(Path.cwd()),
            "current_file": None
        }

    try:
        content = path.read_text(encoding="utf-8").strip()

        if not content:
            return {
                "current_project": str(Path.cwd()),
                "current_file": None
            }

        return json.loads(content)

    except Exception:
        return {
            "current_project": str(Path.cwd()),
            "current_file": None
        }


def save_session(data):
    path = get_session_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )