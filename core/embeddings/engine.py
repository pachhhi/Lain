from sentence_transformers import SentenceTransformer

class EmbeddingEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print(">>> LOADING MODEL <<<")
            cls._instance = super().__new__(cls)
            cls._instance.model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._instance

    def embed(self, text):
        return self.model.encode(text, normalize_embeddings=True)