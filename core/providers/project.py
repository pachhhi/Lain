from core.helpers.project_helpers import *
from core.providers.session import SessionProvider
from core.helpers.session_helper import load_session


class ProjectProvider:

    def get_context(self, prompt=None):

        session = load_session()

        current_project = session.get("current_project")
        current_file = session.get("current_file")

        if not current_project:
            return ""

        if not needs_project_context(prompt):
            return ""

        if not load_project_index():
            try:
                build_project_index(current_project)
            except Exception:
                pass

        candidates = _extract_symbol_candidates(prompt)

        exact_defs = []
        missing = []

        for candidate in candidates:
            if has_definition_match(candidate, current_project):
                exact_defs.append(candidate)
            else:
                missing.append(candidate)

        blocks = [
            f"PROYECTO ACTUAL: {current_project}"
        ]

        if exact_defs:
            blocks.append(
                _build_exact_definitions_block(
                    current_project,
                    exact_defs
                )
            )

        if missing:
            blocks.append(
                _build_partial_symbol_context(
                    current_project,
                    missing
                )
            )

        blocks.append(
            _build_relevant_files_block(
                current_project,
                prompt,
                current_file=current_file
            )
        )

        return "\n\n".join(
            block for block in blocks if block
        )