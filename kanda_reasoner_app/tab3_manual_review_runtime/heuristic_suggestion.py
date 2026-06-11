# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Suggest deterministic AST-aware manual-review docstrings.
# EXPORTS       : _suggest_manual_review_heuristic
# DEPENDS ON    : none
# REFACTOR DATE : 2026-06-01
# ------------------------------------------------------
"""Suggest deterministic AST-aware manual-review docstrings."""

from __future__ import annotations

import ast



def _suggest_manual_review_heuristic(location: dict, module_text: str) -> str:
    """Return one deterministic AST-aware docstring suggestion."""
    node = _node_at_line(module_text, int(location.get("line", 1) or 1))
    if isinstance(node, ast.ClassDef):
        return _wrap("Represent " + _words(node.name) + " behavior.")
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return _wrap(_function_sentence(node))
    target = str(location.get("target_name", "") or "").strip()
    if target and target != "<module>":
        return _wrap("Support " + _words(target) + " behavior.")
    return _wrap("Provide module-level support for this component.")


def _node_at_line(module_text: str, line_number: int) -> ast.AST | None:
    """Return the smallest function/class node containing a line."""
    try:
        tree = ast.parse(module_text)
    except SyntaxError:
        return None
    candidates: list[ast.AST] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        start = int(getattr(node, "lineno", 0) or 0)
        end = int(getattr(node, "end_lineno", start) or start)
        if start <= line_number <= end:
            candidates.append(node)
    candidates.sort(key=lambda item: int(getattr(item, "end_lineno", 0)) - int(getattr(item, "lineno", 0)))
    return candidates[0] if candidates else None


def _function_sentence(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Return a conservative sentence for a function node."""
    name = _words(node.name)
    if node.name.startswith(("get_", "read_", "load_", "find_", "build_", "format_")):
        return "Return " + name + "."
    if node.name.startswith(("set_", "save_", "write_", "apply_", "update_")):
        return "Update " + name + "."
    if node.name.startswith(("validate_", "check_", "is_", "has_")):
        return "Return whether " + name + "."
    return "Support " + name + " behavior."


def _words(name: str) -> str:
    """Return human-readable words for an identifier."""
    text = str(name or "target").strip("_").replace("_", " ").replace("-", " ")
    return " ".join(text.split()) or "target"


def _wrap(sentence: str) -> str:
    """Return a triple-quoted one-line docstring."""
    return (chr(34) * 3) + sentence.strip() + (chr(34) * 3)
