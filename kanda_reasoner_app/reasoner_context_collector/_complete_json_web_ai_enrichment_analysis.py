# project-path: kanda_reasoner_app/reasoner_context_collector/_complete_json_web_ai_enrichment_analysis.py
"""Static analysis helpers for complete JSON Web-AI enrichment."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_context_collector.collector_scope import (
    iter_project_python_files,
)


def _read_text(path: Path) -> str:
    """Read UTF-8 text while replacing undecodable bytes."""
    return path.read_text(encoding="utf-8", errors="replace")


def _iter_python_files(project_root: Path, *args: object, **kwargs: object) -> list[Path]:
    """Return project-scoped Python files using the canonical collector scope."""
    del args, kwargs
    return list(iter_project_python_files(project_root))


def _safe_parse(path: Path) -> ast.AST | None:
    """Parse one Python file, returning None for syntax errors."""
    try:
        return ast.parse(_read_text(path), filename=str(path))
    except SyntaxError:
        return None


def _symbol_kind(node: ast.AST) -> str:
    """Return the stable symbol-kind label for an AST definition node."""
    if isinstance(node, ast.ClassDef):
        return "class"
    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"
    if isinstance(node, ast.FunctionDef):
        return "function"
    return "symbol"


def _responsibility_from_path(rel_path: str) -> str:
    """Derive a deterministic high-level responsibility label from a path."""
    lowered = rel_path.lower()
    if "runtime" in lowered:
        return "runtime evidence collection"
    if "collector" in lowered:
        return "static evidence collection"
    if "reasoner_retriever" in lowered or "retrieval" in lowered:
        return "retrieval and evidence selection"
    if "json_splitter" in lowered:
        return "json splitting and reassembly"
    if "manage_architecture" in lowered:
        return "architecture governance"
    if "manage_workflows" in lowered:
        return "workflow governance"
    if "gui" in lowered or "window" in lowered:
        return "gui behavior"
    if "test" in lowered:
        return "test support"
    return "project support"


def _is_main_guard_test(test: ast.AST) -> bool:
    """Return whether an AST test structurally matches a __main__ guard."""
    if not isinstance(test, ast.Compare):
        return False
    if not isinstance(test.left, ast.Name) or test.left.id != "__name__":
        return False
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    if len(test.comparators) != 1:
        return False
    comparator = test.comparators[0]
    return isinstance(comparator, ast.Constant) and comparator.value == "__main__"


def _looks_like_entry_point(tree: ast.AST) -> bool:
    """Return whether a parsed module contains a structural __main__ guard."""
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and _is_main_guard_test(node.test):
            return True
    return False


def _symbol_records(
    project_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    """Build symbol, primary-definition, and entry-point records."""
    symbol_index: list[dict[str, Any]] = []
    primary_definitions: dict[str, Any] = {}
    entry_points: list[dict[str, Any]] = []

    for path in _iter_python_files(project_root):
        rel_path = path.relative_to(project_root).as_posix()
        tree = _safe_parse(path)
        if not isinstance(tree, ast.Module):
            continue
        module_symbols: list[dict[str, Any]] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                record = {
                    "name": node.name,
                    "kind": _symbol_kind(node),
                    "file": rel_path,
                    "line": int(node.lineno or 0),
                }
                module_symbols.append(record)
                primary_definitions.setdefault(node.name, []).append(record)
        if module_symbols:
            symbol_index.append(
                {
                    "file": rel_path,
                    "responsibility": _responsibility_from_path(rel_path),
                    "symbols": module_symbols,
                }
            )
        has_main_function = any(item["name"] == "main" for item in module_symbols)
        has_main_guard = _looks_like_entry_point(tree)
        if has_main_guard or has_main_function:
            entry_points.append(
                {
                    "file": rel_path,
                    "has_main_function": has_main_function,
                    "has_main_guard": has_main_guard,
                }
            )
    return symbol_index, primary_definitions, entry_points


def _file_responsibility_index(
    project_root: Path,
    symbol_index: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build one deterministic responsibility record per Python source file."""
    by_file = {entry["file"]: entry for entry in symbol_index}
    records: list[dict[str, Any]] = []
    for path in _iter_python_files(project_root):
        rel_path = path.relative_to(project_root).as_posix()
        entry = by_file.get(rel_path, {})
        records.append(
            {
                "file": rel_path,
                "responsibility": _responsibility_from_path(rel_path),
                "public_symbols": [
                    item["name"]
                    for item in entry.get("symbols", [])
                    if not item["name"].startswith("_")
                ],
            }
        )
    return records


def _test_protection_index(
    project_root: Path,
    responsibility_index: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build deterministic related-test evidence for each responsibility record."""
    test_files = {
        path.relative_to(project_root).as_posix().lower()
        for path in _iter_python_files(project_root)
        if "test" in path.name.lower()
        or "tests" in [
            part.lower() for part in path.relative_to(project_root).parts
        ]
    }
    records: list[dict[str, Any]] = []
    for item in responsibility_index:
        rel_path = item["file"]
        stem = Path(rel_path).stem.lower()
        related_tests = [test for test in sorted(test_files) if stem in test]
        records.append(
            {
                "file": rel_path,
                "has_related_test": bool(related_tests),
                "related_tests": related_tests[:10],
            }
        )
    return records


def _stable_evidence_index(sections: dict[str, Any]) -> dict[str, Any]:
    """Build deterministic short evidence identifiers for generated sections."""
    evidence: dict[str, Any] = {}
    for section_name, section_value in sorted(sections.items()):
        encoded = json.dumps(section_value, sort_keys=True, default=str)
        evidence_id = hashlib.sha256(
            (section_name + "\n" + encoded).encode("utf-8")
        ).hexdigest()[:16]
        evidence[evidence_id] = {
            "section": section_name,
            "sha256_16": evidence_id,
        }
    return evidence
