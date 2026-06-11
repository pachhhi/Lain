from tools.run_lain import run_lain
from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".html",
    ".css",
    ".sh",
}

MAX_FILES = 25
MAX_FILE_BYTES = 50_000
MAX_CONTENT_CHARS = 20_000


def _is_allowed_file(path: Path) -> bool:
    return path.suffix.lower() in ALLOWED_EXTENSIONS


def _read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return f"[ERROR leyendo archivo: {exc}]"


def _build_directory_prompt(path: Path, question: str) -> str:
    files = [
        p for p in sorted(path.rglob("*"))
        if p.is_file() and _is_allowed_file(p)
    ]

    if not files:
        file_list = "No se encontraron archivos permitidos en el directorio."
    else:
        file_list = "\n".join(
            f"- {p.relative_to(path)}"
            for p in files[:MAX_FILES]
        )
        if len(files) > MAX_FILES:
            file_list += f"\n- ... y {len(files) - MAX_FILES} archivos más"

    prompt_parts = [
        f"DIRECTORY: {path}",
        "FILES:",
        file_list,
        "",
        "CONTENTS:",
    ]

    for p in files[:MAX_FILES]:
        rel = p.relative_to(path)
        size = p.stat().st_size

        if size > MAX_FILE_BYTES:
            content = f"[SKIPPED: archivo demasiado grande ({size} bytes)]"
        else:
            content = _read_file_safe(p)
            if len(content) > MAX_CONTENT_CHARS:
                content = content[:MAX_CONTENT_CHARS] + "\n...[TRUNCATED]"

        prompt_parts.append(f"FILE: {rel}\n{content}\n")

    if len(files) > MAX_FILES:
        prompt_parts.append(
            f"[... se omitieron {len(files) - MAX_FILES} archivos adicionales ...]"
        )

    prompt_parts.append(
        "QUESTION:"
    )
    prompt_parts.append(
        question if question else "Explain what this directory contains and how its files relate to each other."
    )

    return "\n".join(prompt_parts)


def analyze_file(file_path: str, question: str = "") -> str:
    path = Path(file_path).expanduser()

    if not path.exists():
        return f"Archivo no encontrado: {file_path}"

    if path.is_dir():
        prompt = _build_directory_prompt(path, question)
    else:
        if not _is_allowed_file(path):
            return f"Extensión no permitida para análisis: {path.suffix}"

        code = _read_file_safe(path)
        prompt = f"""
FILE: {file_path}

CODE:
{code}

QUESTION:
{question if question else "Explain what this file or directory does."}
"""

    return run_lain(prompt, mode="analyze")
    