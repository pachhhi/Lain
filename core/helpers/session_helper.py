# def load_session():
#     if not SESSION_FILE.exists():
#         return {}

#     try:
#         content = SESSION_FILE.read_text(
#             encoding="utf-8"
#         ).strip()

#         if not content:
#             return {}
            

#         return json.loads(content)

#     except Exception:
#         return {}