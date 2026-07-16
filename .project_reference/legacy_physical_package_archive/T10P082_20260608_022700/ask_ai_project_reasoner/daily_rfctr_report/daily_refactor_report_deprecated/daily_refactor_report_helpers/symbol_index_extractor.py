"""
Symbol Index Extractor - v1.0
=============================

Deterministic semantic grounding layer.

Extracts top-level symbols:
- Classes
- Functions
- Async functions
- Top-level assignments (constants)

Read-only.
No mutation.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def extract_symbol_index(domain_root: Path, output_path: Path, prefix: str) -> Dict[str, Any]:
    if not domain_root.exists():
        raise ValueError(f"Invalid domain root: {domain_root}")

    py_files = list(domain_root.rglob("*.py"))

    symbols: List[Dict[str, Any]] = []

    for file_path in py_files:
        try:
            source = file_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source)
        except Exception:
            continue

        for node in tree.body:

            # Classes
            if isinstance(node, ast.ClassDef):
                symbols.append({
                    "name": node.name,
                    "type": "class",
                    "module": str(file_path.relative_to(domain_root)),
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", node.lineno),
                })

            # Functions
            elif isinstance(node, ast.FunctionDef):
                symbols.append({
                    "name": node.name,
                    "type": "function",
                    "module": str(file_path.relative_to(domain_root)),
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", node.lineno),
                })

            # Async functions
            elif isinstance(node, ast.AsyncFunctionDef):
                symbols.append({
                    "name": node.name,
                    "type": "async_function",
                    "module": str(file_path.relative_to(domain_root)),
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", node.lineno),
                })

            # Top-level constants (assignments)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        symbols.append({
                            "name": target.id,
                            "type": "constant",
                            "module": str(file_path.relative_to(domain_root)),
                            "line_start": node.lineno,
                            "line_end": getattr(node, "end_lineno", node.lineno),
                        })

    symbol_index = {
        "index_version": "1.0",
        "domain_prefix": prefix,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "symbol_count": len(symbols),
        "symbols": sorted(symbols, key=lambda s: (s["module"], s["name"]))
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(symbol_index, f, indent=4, sort_keys=True)

    return symbol_index