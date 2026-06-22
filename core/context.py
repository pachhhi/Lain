from pathlib import Path
import json
import re
from datetime import datetime
from core.manager import ContextManager
from core.providers.system import SystemProvider

SESSION_FILE = Path("/home/pachhh/Lain/memory/session.json")

#CREO QUE LOAD_SESSION NO SE ESTA LLAMANDO EN NINGUN LADO

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
