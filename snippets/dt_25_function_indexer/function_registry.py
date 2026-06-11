import ast
from pathlib import Path
from typing import Dict, List


class FunctionRecord:
    def __init__(self, name: str, module: str, source: str, doc: str = ""):
        self.name = name
        self.module = module
        self.source = source
        self.doc = doc

    def __repr__(self):
        return f"<Function {self.name} in {self.module}>"

def extract_functions_from_file(file_path: Path) -> List[FunctionRecord]:
    text = file_path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    source_lines = text.splitlines()
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_lines = source_lines[node.lineno - 1: node.end_lineno]
            docstring = ast.get_docstring(node) or ""
            functions.append(FunctionRecord(
                name=node.name,
                module=str(file_path),
                source="\n".join(func_lines),
                doc=docstring
            ))

    return functions

def index_project_functions(base_path: Path) -> Dict[str, FunctionRecord]:
    registry = {}
    for path in base_path.rglob("*.py"):
        if "venv" in path.parts or "site-packages" in path.parts:
            continue
        print(f"🔍 Scanning file: {path}")
        try:
            for record in extract_functions_from_file(path):
                key = f"{record.module}::{record.name}"
                registry[key] = record
        except SyntaxError:
            print(f"⚠️ Skipped (syntax error): {path}")
    return registry
