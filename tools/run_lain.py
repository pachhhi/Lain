import re
from pathlib import Path
import json


from tools.llm_tool import run_llm
from tools.project_search import (
    find_file,
    load_project_tree,
    normalize_project,
    search_symbol,
    search_text,
    tree_to_text,
    build_project_index,
    load_project_index,
    has_definition_match,
)
from core.context import (
    load_system_prompt,
    load_memory,
    load_session,
    load_last_messages,
)

from core.providers.system import load_system_prompt
from core.manager import ContextManager

MAX_RELEVANT_FILES = 5
MAX_FILE_CHARS = 4000
MAX_FILE_PROMPT_CHARS = 12000
COMMON_STOPWORDS = {
    "qué",
    "que",
    "como",
    "cómo",
    "dónde",
    "donde",
    "se",
    "usa",
    "usar",
    "tiene",
    "hace",
    "hacer",
    "revisa",
    "revisar",
    "esta",
    "está",
    "mostrame",
    "mostrar",
    "mostrarme",
    "archivo",
    "archivos",
    "funcion",
    "función",
    "clase",
    "módulo",
    "modulo",
    "proyecto",
    "actual",
    "anterior",
    "ruta",
    "me",
    "puede",
    "por",
    "favor",
    "explica",
    "explicar",
    "tema",
    "donde",
    "cual",
    "cuales",
    "usar",
    "informacion",
    "información",
}


def _read_file_safe(path: Path, max_chars: int = None) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return f"[ERROR leyendo archivo: {exc}]"

    if max_chars and len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]"

    return text


def _extract_symbol_candidates(prompt: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", prompt)
    symbols = []

    for token in tokens:
        lower = token.lower()
        if lower in COMMON_STOPWORDS:
            continue
        if len(token) < 3:
            continue
        if token not in symbols:
            symbols.append(token)

    return symbols


def _project_symbol_candidates(project: str, candidates: list[str]) -> list[str]:
    index = load_project_index()
    if index is None:
        try:
            build_project_index(project)
            index = load_project_index()
        except Exception:
            index = None

    if not index:
        return []

    symbol_names = set(index.get("symbols", {}).keys())
    return [candidate for candidate in candidates if candidate in symbol_names]


def needs_project_context(prompt: str) -> bool:
    if not prompt or not prompt.strip():
        return False

    text = prompt.lower()
    keywords = [
        "build_context",
        "run_lain.py",
        "main.py",
        "funcion",
        "función",
        "archivo",
        "analiza",
        "analizar",
        "revisa",
        "revisar",
        "error",
        "donde esta",
        "donde está",
        "explicame",
        "que hace",
        "busca",
        "codigo",
        "código",
    ]

    return any(keyword in text for keyword in keywords)


def _select_relevant_project_files(project: str, prompt: str, current_file: str | None = None):
    if not project:
        return []

    candidates = _extract_symbol_candidates(prompt)
    selected = []
    seen = set()

    if current_file:
        current_path = Path(current_file)
        if current_path.exists() and current_path not in seen:
            selected.append(current_path)
            seen.add(current_path)

    for candidate in candidates:
        for path in find_file(project, candidate, max_results=MAX_RELEVANT_FILES):
            if path not in seen:
                selected.append(path)
                seen.add(path)
                if len(selected) >= MAX_RELEVANT_FILES:
                    return selected

    for candidate in candidates:
        for path in search_symbol(project, candidate, max_results=MAX_RELEVANT_FILES):
            if path not in seen:
                selected.append(path)
                seen.add(path)
                if len(selected) >= MAX_RELEVANT_FILES:
                    return selected

    if not selected:
        for path in search_text(project, prompt, max_results=MAX_RELEVANT_FILES):
            if path not in seen:
                selected.append(path)
                seen.add(path)
                if len(selected) >= MAX_RELEVANT_FILES:
                    return selected

    return selected[:MAX_RELEVANT_FILES]


def _build_relevant_files_block(project: str, prompt: str, current_file: str | None = None) -> str:
    files = _select_relevant_project_files(project, prompt, current_file=current_file)
    if not files:
        return f"PROYECTO ACTUAL: {project}\n"

    blocks = [f"PROYECTO ACTUAL: {project}", "ARCHIVOS RELEVANTES:"]
    total_chars = 0

    for path in files:
        relative_path = Path(path).relative_to(Path(project))
        content = _read_file_safe(Path(path), max_chars=MAX_FILE_CHARS)
        block = f"\nFILE: {relative_path}\n{content}\n"
        total_chars += len(block)

        if total_chars > MAX_FILE_PROMPT_CHARS:
            blocks.append("...[más archivos relevantes omitidos por límite de tamaño]...")
            break

        blocks.append(block)

    return "\n".join(blocks)


def _read_source_snippet(path: Path, lineno: int, context: int = 3) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as exc:
        return f"[ERROR leyendo archivo para fragmento: {exc}]"

    start = max(0, lineno - 1 - context)
    end = min(len(lines), lineno - 1 + context + 1)
    snippet_lines = []
    for i in range(start, end):
        prefix = ">" if i == lineno - 1 else " "
        snippet_lines.append(f"{prefix} {i + 1}: {lines[i]}")
    return "\n".join(snippet_lines)


def _extract_relevant_snippet(path: Path, query: str, context: int = 2) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as exc:
        return f"[ERROR leyendo archivo para fragmento: {exc}]"

    query_lower = query.lower()
    for index, line in enumerate(lines):
        if query_lower in line.lower():
            start = max(0, index - context)
            end = min(len(lines), index + context + 1)
            snippet_lines = []
            for i in range(start, end):
                prefix = ">" if i == index else " "
                snippet_lines.append(f"{prefix} {i + 1}: {lines[i]}")
            return "\n".join(snippet_lines)

    return ""


def _build_exact_definitions_block(project: str, candidates: list[str]) -> str:
    index = load_project_index()
    if not index:
        return ""

    blocks = []
    for candidate in candidates:
        entries = index.get("symbols", {}).get(candidate)
        if not entries:
            continue

        blocks.append(f"DEFINICIONES EXACTAS ENCONTRADAS PARA: {candidate}")
        for entry in entries:
            path = normalize_project(project).joinpath(entry["path"])
            blocks.append(f"FILE: {entry['path']}")
            blocks.append(f"TIPO: {entry['type']} LINEA: {entry['lineno']}")
            if entry.get("desc"):
                blocks.append(f"DESCRIPCIÓN: {entry['desc']}")
            blocks.append(_read_source_snippet(path, entry["lineno"]))
            blocks.append("")

    return "\n".join(blocks).strip()


def _build_partial_symbol_context(project: str, missing: list[str]) -> str:
    blocks = []
    for symbol in missing:
        blocks.append(f"INFORMACIÓN PARCIAL PARA: {symbol}")

        found_files = []
        file_hits = find_file(project, symbol, max_results=3)
        if file_hits:
            blocks.append("Archivos relacionados:")
            for path in file_hits:
                rel = Path(path).relative_to(normalize_project(project))
                blocks.append(f"  - {rel}")
                found_files.append(path)

        text_hits = search_text(project, symbol, max_results=3)
        if text_hits:
            if not file_hits:
                blocks.append("Archivos con menciones:")
            for path in text_hits:
                rel = Path(path).relative_to(normalize_project(project))
                if path not in found_files:
                    blocks.append(f"  - {rel}")
                    found_files.append(path)

        if not found_files:
            blocks.append("  - No se encontraron archivos relacionados directamente.")

        for path in found_files[:2]:
            snippet = _extract_relevant_snippet(Path(path), symbol)
            if snippet:
                rel = Path(path).relative_to(normalize_project(project))
                blocks.append(f"FRAGMENTO RELEVANTE EN {rel}:")
                blocks.append(snippet)

        blocks.append("")

    return "\n".join(blocks).strip()



#THIS CONTEXT WILL BE PART FROM CONTEXT.PY
def build_context(prompt, mode="chat"):
    # system = load_system_prompt()
    # memory = load_memory()
    # session = load_session()
    # history = load_last_messages(limit=5)

    manager = ContextManager()

    return manager.build(
        prompt=prompt,
        mode=mode
    )

    session_text = "\n".join(
        f"{k}: {v}"
        for k, v in session.items()
        if v
    )

    history_text = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in history
    )
    
    if len(history_text) > 1500:
        messages_list = [
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in history
        ]
        history_text = ""
        for msg in reversed(messages_list):
            if len(history_text) + len(msg) + 1 <= 1500:
                history_text = msg + "\n" + history_text if history_text else msg
            else:
                break
        history_text = history_text.rstrip()

    project_block = ""
    current_project = session.get("current_project")
    current_file = session.get("current_file")

    if current_project and needs_project_context(prompt):
        print("[PROJECT_CONTEXT] enabled")
        # Ensure there's an index available for faster symbol/file lookups
        if not load_project_index():
            try:
                build_project_index(current_project)
            except Exception:
                pass

        candidates = _extract_symbol_candidates(prompt)
        exact_defs = []
        missing = []
        if candidates:
            for candidate in candidates:
                if has_definition_match(candidate, current_project):
                    exact_defs.append(candidate)
                else:
                    missing.append(candidate)

        definition_block = _build_exact_definitions_block(current_project, exact_defs) if exact_defs else ""
        partial_block = _build_partial_symbol_context(current_project, missing) if missing else ""
        info_block = ""
        if missing:
            info_block = (
                f"[INFO] No se encontró una definición exacta para: {', '.join(missing)}. "
                "Respondiendo con el contexto disponible."
            )

        relevant_files_block = _build_relevant_files_block(
            current_project,
            prompt,
            current_file=current_file,
        )

        project_parts = [f"PROYECTO ACTUAL: {current_project}"]
        if info_block:
            project_parts.append(info_block)
        if definition_block:
            project_parts.append(definition_block)
        if partial_block:
            project_parts.append(partial_block)
        project_parts.append(relevant_files_block)

        project_block = "\n\n".join(part for part in project_parts if part)
    else:
        print("[PROJECT_CONTEXT] disabled")
        project_block = ""
        if not current_project and session_text:
            project_block = f"ESTADO ACTUAL:\n{session_text}\n"

    return f"""
{system}

{memory}

ESTADO ACTUAL:

{session_text}

{project_block}

CONVERSACIÓN RECIENTE:

{history_text}

MODO:
{mode}

MENSAJE ACTUAL DEL USUARIO:

{prompt}
"""


def run_lain(prompt, mode="chat", typing=False):
    full_prompt = build_context(prompt, mode)

    Path("/tmp/lain_prompt.txt").write_text(
        full_prompt,
        encoding="utf-8"
    )

    memory = load_memory()
    session = load_session()
    history = load_last_messages(limit=5)

    session_text = "\n".join(
        f"{k}: {v}"
        for k, v in session.items()
        if v
    )

    history_text = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in history
    )

    current_project = session.get("current_project")
    current_file = session.get("current_file")

    project_block = ""
    if current_project and needs_project_context(prompt):
        project_block = _build_relevant_files_block(
            current_project,
            prompt,
            current_file=current_file,
        )
    elif session_text:
        project_block = f"ESTADO ACTUAL:\n{session_text}\n"

    print("\n===== PROMPT BREAKDOWN =====")
    print("memory:", len(memory))
    print("session:", len(session_text))
    print("project:", len(project_block))
    print("history:", len(history_text))
    print("prompt:", len(prompt))
    print("TOTAL:", len(full_prompt))
    print("===========================\n")

    return run_llm(full_prompt)
