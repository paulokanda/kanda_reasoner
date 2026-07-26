# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_docstring_inserter.py
"""Preview-only docstring insertion for moved-code refactor artifacts."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
from typing import Any

__all__ = [
    "DocstringInsertion",
    "DocstringInsertionResult",
    "insert_missing_docstrings_for_preview_blocks",
]


@dataclass(frozen=True)
class DocstringInsertion:
    """One deterministic docstring insertion performed in a preview block."""

    symbol: str
    target: str
    kind: str
    provenance: str = "deterministic_template"
    confidence: str = "medium"

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-ready insertion record."""
        return asdict(self)


@dataclass(frozen=True)
class DocstringInsertionResult:
    """Preview block text plus docstring insertion evidence."""

    blocks: dict[str, str]
    insertions: list[DocstringInsertion] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready insertion report."""
        return {
            "blocks": sorted(self.blocks),
            "insertions": [item.to_dict() for item in self.insertions],
            "warnings": list(self.warnings),
            "blockers": list(self.blockers),
        }


def insert_missing_docstrings_for_preview_blocks(
    blocks: dict[str, str],
) -> DocstringInsertionResult:
    """Insert conservative docstrings into moved preview blocks only."""
    updated: dict[str, str] = {}
    insertions: list[DocstringInsertion] = []
    warnings: list[str] = []
    blockers: list[str] = []
    for symbol, text in blocks.items():
        try:
            new_text, symbol_insertions, symbol_warnings = _insert_for_symbol(symbol, text)
        except SyntaxError as exc:
            updated[symbol] = text
            blockers.append(f"DOCSTRING_INSERTION_PARSE_FAILED:{symbol}:{exc}")
            continue
        updated[symbol] = new_text
        insertions.extend(symbol_insertions)
        warnings.extend(symbol_warnings)
    if insertions:
        warnings.append("DETERMINISTIC_DOCSTRINGS_INSERTED_IN_PREVIEW_ONLY")
    return DocstringInsertionResult(
        blocks=updated,
        insertions=insertions,
        warnings=sorted(set(warnings)),
        blockers=sorted(set(blockers)),
    )


def _insert_for_symbol(symbol: str, text: str) -> tuple[str, list[DocstringInsertion], list[str]]:
    """Return one block with missing docstrings inserted."""
    tree = ast.parse(text, type_comments=True)
    lines = text.splitlines()
    insertions: list[tuple[int, list[str], DocstringInsertion]] = []
    warnings: list[str] = []
    top = _first_public_symbol(tree, symbol)
    if top is None:
        warnings.append(f"DOCSTRING_INSERTION_SYMBOL_NOT_FOUND:{symbol}")
        return text, [], warnings
    if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(top) is None:
        insertions.append(_docstring_insert(symbol, symbol, "function", top))
    if isinstance(top, ast.ClassDef):
        if ast.get_docstring(top) is None:
            insertions.append(_docstring_insert(symbol, symbol, "class", top))
        for child in top.body:
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if child.name.startswith("_") or ast.get_docstring(child) is not None:
                continue
            target = f"{symbol}.{child.name}"
            insertions.append(_docstring_insert(symbol, target, "method", child))
    if not insertions:
        return text, [], warnings
    insertion_records: list[DocstringInsertion] = []
    for line_number, doc_lines, record in sorted(insertions, key=lambda item: item[0], reverse=True):
        index = max(0, min(line_number - 1, len(lines)))
        lines[index:index] = doc_lines
        insertion_records.append(record)
    insertion_records.reverse()
    return "\n".join(lines).rstrip() + "\n", insertion_records, warnings


def _first_public_symbol(tree: ast.Module, symbol: str) -> ast.AST | None:
    """Return the top-level function/class node matching a moved symbol."""
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == symbol:
            return node
    return None


def _docstring_insert(
    root_symbol: str,
    target: str,
    kind: str,
    node: ast.AST,
) -> tuple[int, list[str], DocstringInsertion]:
    """Return an insertion tuple for one missing docstring."""
    body = getattr(node, "body", [])
    if not body:
        line_number = getattr(node, "end_lineno", getattr(node, "lineno", 1)) + 1
        indent = _node_indent(node) + "    "
    else:
        first = body[0]
        line_number = getattr(first, "lineno", getattr(node, "lineno", 1) + 1)
        indent = _node_indent(first)
    doc_lines = _docstring_lines(indent, target, kind)
    return (
        line_number,
        doc_lines,
        DocstringInsertion(symbol=root_symbol, target=target, kind=kind),
    )


def _docstring_lines(indent: str, target: str, kind: str) -> list[str]:
    """Return deterministic Google-style-compatible docstring lines."""
    readable_kind = kind.replace("_", " ")
    safe_target = target.replace(chr(34) * 3, "triple_quotes")
    return [
        f'{indent}"""Describe {safe_target}.',
        f"{indent}",
        f"{indent}Generated during preview-only large-file refactor planning for this {readable_kind}.",
        f"{indent}Review wording before treating this as final source documentation.",
        f'{indent}"""',
    ]


def _node_indent(node: ast.AST) -> str:
    """Return indentation based on the node column offset."""
    return " " * int(getattr(node, "col_offset", 0))
