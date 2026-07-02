import re

MAX_CHUNK_SIZE = 1200  # caracteres aprox (simple V1)


def split_sections(md_text):
    """
    Divide por headers ## Section
    """
    sections = re.split(r"\n##\s+", md_text)
    
    cleaned = []
    for sec in sections:
        sec = sec.strip()
        if sec:
            cleaned.append(sec)
    
    return cleaned


def split_paragraphs(section):
    """
    Divide por saltos de línea dobles
    """
    return [p.strip() for p in section.split("\n\n") if p.strip()]


def build_chunks(section_text, section_name):
    paragraphs = split_paragraphs(section_text)

    chunks = []
    current = ""

    for p in paragraphs:
        # evitar diálogos sueltos
        if p.startswith('"') and len(p) < 80:
            continue

        if len(current) + len(p) < MAX_CHUNK_SIZE:
            current += " " + p
        else:
            chunks.append({
                "text": current.strip(),
                "section": section_name
            })
            current = p

    if current:
        chunks.append({
            "text": current.strip(),
            "section": section_name
        })

    return chunks


def chunk_md(md_text):
    sections = split_sections(md_text)

    all_chunks = []

    for sec in sections:
        lines = sec.split("\n", 1)

        # primer línea = título de sección
        section_name = lines[0].strip()
        content = lines[1] if len(lines) > 1 else ""

        chunks = build_chunks(content, section_name)
        all_chunks.extend(chunks)

    return all_chunks