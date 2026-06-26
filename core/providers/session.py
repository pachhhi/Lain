from core.helpers.session_helper import load_session
import json

class SessionProvider:

    def get_context(self, prompt=None):
        session = load_session()

        current_project = session.get("current_project")
        current_file = session.get("current_file")

        return f"SESSION:\nproject={current_project}\nfile={current_file}" if current_project else ""