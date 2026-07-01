from pathlib import Path

from core.helpers.history_helpers import load_last_messages

class HistoryProvider:

    def get_context(self, prompt=None, flags=None):
        history = load_last_messages(limit=5)

        return "\n".join(
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in history
            if msg["role"] == "user"
        )