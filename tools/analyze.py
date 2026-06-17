from pathlib import Path

from tools.run_lain import run_lain
from tools.project_search import (
    build_project_tree,
    save_project_tree,
    tree_to_text,
)
from core.context import load_session, save_session


def _read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return f"[ERROR leyendo archivo: {exc}]"


def _build_directory_prompt(path: Path, tree: dict, question: str) -> str:
    tree_text = tree_to_text(tree, max_items=200)
    question_text = question if question else "Describe la estructura del proyecto y las partes más importantes."

    return f"""
PROJECT: {path}

ÁRBOL DEL PROYECTO:
{tree_text}

QUESTION:
{question_text}
"""


def analyze_file(file_path: str, question: str = "") -> str:
    path = Path(file_path).expanduser()

    if not path.exists():
        return f"Archivo no encontrado: {file_path}"

    session = load_session()
    session["last_analyze_target"] = str(path)

    if path.is_dir():
        session["current_project"] = str(path)
        session["current_file"] = None
    else:
        session["current_project"] = str(path.parent)
        session["current_file"] = str(path)

    session["current_topic"] = question if question else None
    save_session(session)

    if path.is_dir():
        tree = build_project_tree(path, include_size=True)
        save_project_tree(path, tree)
        prompt = _build_directory_prompt(path, tree, question)
    else:
        code = _read_file_safe(path)
        prompt = f"""
FILE: {path}

CODE:
{code}

QUESTION:
{question if question else 'Explain what this file does.'}
"""

    return run_lain(prompt, mode="analyze")
    