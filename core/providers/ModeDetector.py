class ModeDetector:

    def detect(self, text: str):

        text = text.strip().lower()

        if text.startswith("/sel"):
            return "sel"

        if text.startswith("/debug"):
            return "debug"

        return "chat"


    def strip_mode(self, text: str):
        if text.startswith("/sel"):
            return text.replace("/sel", "", 1).strip()

        if text.startswith("/debug"):
            return text.replace("/debug", "", 1).strip()

        return text