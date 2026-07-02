import json
from pathlib import Path
from core.embeddings.engine import EmbeddingEngine
from core.knowledge.SEL.chunker import chunk_md

engine = EmbeddingEngine()

OUTPUT_PATH = Path("data/index.json")


def load_md(path):
    full_path = Path("core/knowledge/wiki/") / path
    return full_path.read_text(encoding="utf-8")


def build():
    index = []  # 👈 SIEMPRE primero

    md_files = [
        "layer01.md",
        # "layer02.md"
    ]

    for file in md_files:
        text = load_md(file)
        chunks = chunk_md(text)

        for i, c in enumerate(chunks):
            emb = engine.embed(c["text"])

            index.append({
                "id": f"{file}_{i}",
                "text": c["text"],
                "section": c["section"],
                "source": file,
                "embedding": emb.tolist()
            })

    # 👇 asegurar carpeta
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Built index with {len(index)} chunks")


if __name__ == "__main__":
    build()