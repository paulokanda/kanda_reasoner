# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Docstring payload formatting and insertion helpers
# EXPORTS       : module_path_comment, build_module_header_payload, indentation_for_body, wrap_docstring_lines, render_docstring_body, payload_with_optional_uncertainty, module_insert_index, has_inline_body, is_overload_function, apply_insertions_to_text
# DEPENDS ON    : project_exclusion_rules.py
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Docstring payload formatting and insertion helpers."""

from __future__ import annotations

import ast
from pathlib import Path

from .project_exclusion_rules import normalize_rel_path

__all__ = [
    "module_path_comment",
    "build_module_header_payload",
    "indentation_for_body",
    "wrap_docstring_lines",
    "render_docstring_body",
    "payload_with_optional_uncertainty",
    "module_insert_index",
    "has_inline_body",
    "is_overload_function",
    "apply_insertions_to_text",
]


def module_path_comment(root: Path, path: Path) -> str:
    """Return the canonical file path comment for a module header."""
    return "# " + normalize_rel_path(root, path)

def _line_matches_module_path_comment(line: str, root: Path, path: Path) -> bool:
    """Return whether a line already contains the canonical file path comment."""
    return line.strip() == module_path_comment(root, path)

def build_module_header_payload(
    root: Path,
    path: Path,
    lines: list[str],
    insert_index: int,
    module_docstring: str,
    uncertain_comment: str | None = None,
) -> list[str]:
    """Build the canonical module header payload for a missing docstring."""
    payload: list[str] = []

    payload.append(module_docstring)
    if uncertain_comment:
        payload.append(uncertain_comment)
    payload.append("")
    return payload

def indentation_for_body(node: ast.AST, first_stmt: ast.stmt | None) -> str:
    """Handle indentation for body.
    
    Parameters
    ----------
    node : ast.AST
        TODO: describe node.
    first_stmt : ast.stmt | None
        TODO: describe first_stmt.
    
    Returns
    -------
    str
        TODO: describe the return value.
    """
    
    if first_stmt is not None:
        return " " * first_stmt.col_offset
    col = getattr(node, "col_offset", 0)
    return " " * (col + 4)

def wrap_docstring_lines(docstring: str, indent: str) -> list[str]:
    """Handle wrap docstring lines.
    
    Parameters
    ----------
    docstring : str
        TODO: describe docstring.
    indent : str
        TODO: describe indent.
    
    Returns
    -------
    list[str]
        TODO: describe the return value.
    """
    
    raw_lines = docstring.splitlines()
    return [indent + line if line else indent for line in raw_lines]

def render_docstring_body(body: str) -> str:
    """Render  docstring body.
    
    Parameters
    ----------
    body : str
        TODO: describe body.
    
    Returns
    -------
    str
        TODO: describe the return value.
    """
    
    body = body.strip("\n")
    if "\n" in body:
        return f'"""{body}\n"""'
    return f'"""{body}"""'

def payload_with_optional_uncertainty(
    docstring: str,
    indent: str,
    uncertain_comment: str | None = None,
) -> list[str]:
    """Handle payload with optional uncertainty.
    
    Parameters
    ----------
    docstring : str
        TODO: describe docstring.
    indent : str
        TODO: describe indent.
    uncertain_comment : str | None, optional
        TODO: describe uncertain_comment.
    
    Returns
    -------
    list[str]
        TODO: describe the return value.
    """
    
    payload = wrap_docstring_lines(docstring, indent)
    if uncertain_comment:
        payload.append(indent + uncertain_comment)
    payload.append(indent)
    return payload

def module_insert_index(lines: list[str]) -> int:
    """Handle module insert index.
    
    Parameters
    ----------
    lines : list[str]
        TODO: describe lines.
    
    Returns
    -------
    int
        TODO: describe the return value.
    """
    
    idx = 0
    if idx < len(lines) and lines[idx].startswith("#!"):
        idx += 1
    if idx < len(lines) and "coding" in lines[idx]:
        idx += 1
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    return idx

def has_inline_body(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return whether inline body.
    
    Parameters
    ----------
    node : ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
        TODO: describe node.
    
    Returns
    -------
    bool
        TODO: describe the return value.
    """
    
    if not node.body:
        return False
    first_stmt = node.body[0]
    return first_stmt.lineno == node.lineno

def is_overload_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return whether overload function.
    
    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        TODO: describe node.
    
    Returns
    -------
    bool
        TODO: describe the return value.
    """
    
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name) and dec.id == "overload":
            return True
        if isinstance(dec, ast.Attribute) and dec.attr == "overload":
            return True
    return False

def apply_insertions_to_text(text: str, insertions: list[tuple[int, list[str]]]) -> str:
    """Apply  insertions to text.
    
    Parameters
    ----------
    text : str
        TODO: describe text.
    insertions : list[tuple[int, list[str]]]
        TODO: describe insertions.
    
    Returns
    -------
    str
        TODO: describe the return value.
    """
    
    if not insertions:
        return text
    lines = text.splitlines()
    trailing_newline = text.endswith("\n")

    for index, payload in insertions:
        lines[index:index] = payload

    result = "\n".join(lines)
    if trailing_newline or insertions:
        result += "\n"
    return result
