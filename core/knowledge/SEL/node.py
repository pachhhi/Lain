class ConceptNode:

    def __init__(self, text, embedding):
        self.text = text
        self.embedding = embedding
        self.edges = {}  # {node_text: weight}
        self.count = 1   # cuántas veces apareció