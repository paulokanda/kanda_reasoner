# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/ast_safety.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : AST guard helpers that permit only docstring changes
# EXPORTS       : docstring_free_ast_dump, validate_docstring_only_change
# DEPENDS ON    : source_io.py
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""AST guard helpers that permit only docstring changes."""

from __future__ import annotations

import ast
import copy
from pathlib import Path

from .source_io import parse_source

__all__ = [
    "docstring_free_ast_dump",
    "validate_docstring_only_change",
]


def _body_without_leading_docstring(body: list[ast.stmt]) -> list[ast.stmt]:
    """Return a body with its leading docstring expression removed."""
    if not body:
        return body

    first = body[0]
    if (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return body[1:]

    return body

def _strip_docstring_nodes(node: ast.AST) -> None:
    """Remove module, class, and function docstring nodes in-place."""
    if isinstance(
        node,
        (
            ast.Module,
            ast.ClassDef,
            ast.FunctionDef,
            ast.AsyncFunctionDef,
        ),
    ):
        node.body = _body_without_leading_docstring(node.body)

    for child in ast.iter_child_nodes(node):
        _strip_docstring_nodes(child)

def docstring_free_ast_dump(source: str, path: Path) -> str:
    """Return an AST dump with all docstring expression nodes removed."""
    tree = parse_source(source, path)
    tree_copy = copy.deepcopy(tree)
    _strip_docstring_nodes(tree_copy)
    return ast.dump(tree_copy, include_attributes=False)

def validate_docstring_only_change(
    original: str,
    desired: str,
    path: Path,
) -> str:
    """Return an empty string when only docstring/comment text changed."""
    try:
        original_dump = docstring_free_ast_dump(original, path)
        desired_dump = docstring_free_ast_dump(desired, path)
    except SyntaxError as exc:
        return f"syntax validation failed: {exc}"
    except Exception as exc:
        return f"AST validation failed: {type(exc).__name__}: {exc}"

    if original_dump != desired_dump:
        return "non-docstring AST changed after insertion"

    return ""
