from pathlib import Path

from core.helpers.history_helpers import load_last_messages

class HistoryProvider:

    def get_context(self, prompt=None, flags=None, mode=None):
        history = load_last_messages(limit=5)
