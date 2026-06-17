import ast
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

ALLOWED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".html",
    ".css",
    ".sh",
}

IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "logs",
    "memory",
    ".aider.tags.cache.v4",
    ".aider.chat.history.md",
}

PROJECT_TREE_FILE = Path("/home/pachhh/Lain/memory/project_tree.json")
PROJECT_INDEX_FILE = Path("/home/pachhh/Lain/memory/project_index.json")


def normalize_project(project: str | Path) -> Path:
    path = Path(project).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Proyecto no encontrado: {project}")
    return path.resolve()


def is_allowed_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS


def project_files(project: str | Path):
    project = normalize_project(project)
    for path in sorted(project.rglob("*")):
        # Skip ignored directories
        try:
            rel = path.relative_to(project)
        except Exception:
            continue
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue

        if is_allowed_file(path):
            yield path


def build_project_tree(project: str | Path, include_size: bool = True) -> Dict:
    project = normalize_project(project)
    tree = {
        "type": "directory",
        "name": project.name,
        "path": str(project),
        "children": [],
    }
    nodes = {(): tree}

    def _ensure_dir_node(parts):
        node_key = ()
        for part in parts:
            node_key = node_key + (part,)
            if node_key not in nodes:
                parent = nodes[node_key[:-1]]
                node = {
                    "type": "directory",
                    "name": part,
                    "path": str(Path(*node_key)),
                    "children": [],
                }
                parent["children"].append(node)
                nodes[node_key] = node
        return nodes[node_key]

    for path in sorted(project.rglob("*")):
        rel = path.relative_to(project)
        parts = rel.parts
        if any(part in IGNORED_DIRS for part in parts):
            continue
        if path.is_dir():
            _ensure_dir_node(parts)
            continue

        if not is_allowed_file(path):
            continue

        parent = _ensure_dir_node(parts[:-1])
        file_entry = {
            "type": "file",
            "name": parts[-1],
            "path": str(rel),
        }
        if include_size:
            try:
                file_entry["size"] = path.stat().st_size
            except Exception:
                file_entry["size"] = None
        parent["children"].append(file_entry)

    return tree


def _short_desc_from_python(path: Path) -> Optional[str]:
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
        mod = ast.parse(src)
    except Exception:
        return None

    # Prefer module docstring
    doc = ast.get_docstring(mod)
    if doc:
        first = doc.strip().splitlines()[0]
        return first
    # Otherwise try to get first function/class docstring
    for node in mod.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            d = ast.get_docstring(node)
            if d:
                return d.strip().splitlines()[0]

    return None


def build_project_index(project: str | Path) -> Dict[str, Any]:
    project = normalize_project(project)
    index: Dict[str, Any] = {"files": {}, "symbols": {}}

    for path in project_files(project):
        rel = str(path.relative_to(project))
        entry: Dict[str, Any] = {"path": rel, "symbols": [], "short_desc": None}

        if path.suffix == ".py":
            try:
                src = path.read_text(encoding="utf-8", errors="ignore")
                mod = ast.parse(src)
                entry["short_desc"] = ast.get_docstring(mod) and ast.get_docstring(mod).splitlines()[0]

                for node in mod.body:
                    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                        name = node.name
                        desc = ast.get_docstring(node) or None
                        sym = {"name": name, "type": "function", "lineno": node.lineno, "desc": (desc.splitlines()[0] if desc else None)}
                        entry["symbols"].append(sym)
                        index["symbols"].setdefault(name, []).append({"path": rel, "type": "function", "lineno": node.lineno, "desc": sym["desc"]})
                    elif isinstance(node, ast.ClassDef):
                        name = node.name
                        desc = ast.get_docstring(node) or None
                        sym = {"name": name, "type": "class", "lineno": node.lineno, "desc": (desc.splitlines()[0] if desc else None)}
                        entry["symbols"].append(sym)
                        index["symbols"].setdefault(name, []).append({"path": rel, "type": "class", "lineno": node.lineno, "desc": sym["desc"]})
            except Exception:
                entry["short_desc"] = entry.get("short_desc") or None
        else:
            # For non-python files try to get a short description from the first non-empty line
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("#") or line.startswith("//") or line.startswith("/*"):
                        entry["short_desc"] = line.lstrip("#/ ").strip()
                        break
                    entry["short_desc"] = line
                    break
            except Exception:
                entry["short_desc"] = None

        index["files"][rel] = entry

    # persist index
    save_project_index(index)
    return index


def save_project_index(index: Dict[str, Any]) -> None:
    PROJECT_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_project_index() -> Optional[Dict[str, Any]]:
    if not PROJECT_INDEX_FILE.exists():
        return None
    try:
        return json.loads(PROJECT_INDEX_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def tree_to_text(tree: Dict, max_items: int = 200) -> str:
    lines: List[str] = []

    def walk(node: Dict, prefix: str = ""):
        if len(lines) >= max_items:
            return
        if node["type"] == "directory":
            if prefix:
                lines.append(f"{prefix}{node['name']}/")
            else:
                lines.append(f"{node['name']}/")
            for child in sorted(node.get("children", []), key=lambda x: (x["type"] != "directory", x["name"])):
                walk(child, prefix + "  ")
        else:
            size = node.get("size")
            suffix = f" ({size} bytes)" if size is not None else ""
            lines.append(f"{prefix}{node['name']}{suffix}")

    walk(tree)
    if len(lines) >= max_items:
        lines = lines[:max_items] + ["... (tree truncated)"]
    return "\n".join(lines)


def save_project_tree(project: str | Path, tree: Dict) -> None:
    PROJECT_TREE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_TREE_FILE.write_text(
        json.dumps(tree, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def load_project_tree() -> Optional[Dict]:
    if not PROJECT_TREE_FILE.exists():
        return None
    try:
        return json.loads(PROJECT_TREE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_file(project: str | Path, filename: str, max_results: int = 5):
    project = normalize_project(project)
    target = filename.strip().strip("/\\")
    results = []

    exact_matches = []
    partial_matches = []

    # Try index first
    index = load_project_index()
    if index:
        # exact file path or name
        for rel, info in index.get("files", {}).items():
            name = Path(rel).name
            if name == target or rel == target:
                results.append(project.joinpath(rel))
                if len(results) >= max_results:
                    return results[:max_results]
        for rel, info in index.get("files", {}).items():
            name = Path(rel).name
            if target.lower() in name.lower() or target.lower() in rel.lower():
                results.append(project.joinpath(rel))
                if len(results) >= max_results:
                    return results[:max_results]

    for path in project_files(project):
        rel = str(path.relative_to(project))
        name = path.name
        if name == target or rel == target:
            exact_matches.append(path)
        elif target.lower() in name.lower() or target.lower() in rel.lower():
            partial_matches.append(path)

    results.extend(exact_matches[:max_results])
    if len(results) < max_results:
        results.extend(partial_matches[: max_results - len(results)])

    return results


def has_definition_match(symbol: str, project: str | Path) -> bool:
    project = normalize_project(project)
    if not symbol or len(symbol.strip()) < 2:
        return False

    symbol = symbol.strip()
    index = load_project_index()
    if index and index.get("symbols", {}).get(symbol):
        return True

    def_pattern_py = re.compile(rf"^\s*(def|class)\s+{re.escape(symbol)}\b", re.MULTILINE)
    def_pattern_js = re.compile(rf"\b(export\s+function|function)\s+{re.escape(symbol)}\b")
    scanned = 0
    MAX_SCAN = 200
    files_iter = (project.joinpath(rel) for rel in index.get("files", {}).keys()) if index else project_files(project)

    for path in files_iter:
        if scanned >= MAX_SCAN:
            break
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if def_pattern_py.search(text) or def_pattern_js.search(text):
            return True

    return False


def search_symbol(project: str | Path, symbol: str, max_results: int = 5):
    project = normalize_project(project)
    if not symbol or len(symbol.strip()) < 2:
        return []

    symbol = symbol.strip()
    DEBUG = bool(os.environ.get("PROJECT_SEARCH_DEBUG"))

    scores: Dict[Path, Dict[str, object]] = {}

    def record(path: Path, score: int, kind: str):
        prev = scores.get(path)
        if not prev or score > prev["score"]:
            scores[path] = {"score": score, "kind": kind}

    index = load_project_index()

    if index:
        for m in index.get("symbols", {}).get(symbol, []):
            p = project.joinpath(m["path"]) if isinstance(m["path"], str) else project.joinpath(str(m["path"]))
            record(p, 3, "index-definition")

        if scores:
            results = sorted(scores.items(), key=lambda kv: (-kv[1]["score"], str(kv[0])))
            matched = [p for p, meta in results][:max_results]
            if DEBUG:
                print(f"[DEBUG search_symbol] symbol={symbol} matched={[(str(p), meta['kind'], meta['score']) for p, meta in results]}")
            return matched

    def_pattern_py = re.compile(rf"^\s*(def|class)\s+{re.escape(symbol)}\b", re.MULTILINE)
    def_pattern_js = re.compile(rf"\b(export\s+function|function)\s+{re.escape(symbol)}\b")
    import_pattern = re.compile(rf"\b(import|from|require)\b.*\b{re.escape(symbol)}\b")
    call_pattern = re.compile(rf"\b{re.escape(symbol)}\s*\(")
    mention_pattern = re.compile(rf"\b{re.escape(symbol)}\b", re.IGNORECASE)

    scanned = 0
    MAX_SCAN = 200
    files_iter = (project.joinpath(rel) for rel in index.get("files", {}).keys()) if index else project_files(project)

    for path in files_iter:
        if scanned >= MAX_SCAN:
            break
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if def_pattern_py.search(text) or def_pattern_js.search(text):
            record(path, 3, "definition")
            continue

        if DEBUG:
            if import_pattern.search(text):
                record(path, 2, "import")
                continue
            if call_pattern.search(text):
                record(path, 1, "usage")
                continue
            if mention_pattern.search(text):
                record(path, 1, "mention")
                continue
            if Path(path).stem == symbol:
                record(path, 1, "filename-exact")

    items = sorted(scores.items(), key=lambda kv: (-kv[1]["score"], str(kv[0])))

    if not any(meta["score"] >= 3 for p, meta in items):
        if DEBUG:
            print(f"[DEBUG search_symbol] symbol={symbol} no definition-match found")
            for p, meta in items:
                print(f"  {p} -> {meta['kind']} (score={meta['score']})")
            return [p for p, meta in items][:max_results]
        return []

    results = [p for p, meta in items if meta["score"] >= 3][:max_results]

    if DEBUG:
        print(f"[DEBUG search_symbol] symbol={symbol}")
        for p, meta in items:
            print(f"  {p} -> {meta['kind']} (score={meta['score']})")

    return results


def search_text(project: str | Path, text: str, max_results: int = 5):
    project = normalize_project(project)
    query = text.strip().lower()
    if not query:
        return []

    results = []
    for path in project_files(project):
        if len(results) >= max_results:
            break
        content = path.read_text(encoding="utf-8", errors="ignore")
        if query in content.lower():
            results.append(path)

    return results[:max_results]
