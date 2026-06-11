# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Symbol naming, public API, and module identifier helpers
# EXPORTS       : to_module_id, split_words, prettify_name, expr_to_text, extract_public_symbols, extract_internal_import_modules
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Symbol naming, public API, and module identifier helpers."""

from __future__ import annotations

import ast
import re
from pathlib import Path

__all__ = [
    "to_module_id",
    "split_words",
    "prettify_name",
    "expr_to_text",
    "extract_public_symbols",
    "extract_internal_import_modules",
]


def to_module_id(root: Path, path: Path) -> str:
    """Handle to module id.
    
    Parameters
    ----------
    root : Path
        TODO: describe root.
    path : Path
        TODO: describe path.
    
    Returns
    -------
    str
        TODO: describe the return value.
    """
    
    rel = path.relative_to(root)
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)

def split_words(name: str) -> list[str]:
    """Handle split words.
    
    Parameters
    ----------
    name : str
        TODO: describe name.
    
    Returns
    -------
    list[str]
        TODO: describe the return value.
    """
    
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name.replace("_", " "))
    return [w for w in text.split() if w]

def prettify_name(name: str) -> str:
    """Handle prettify name.
    
    Parameters
    ----------
    name : str
        TODO: describe name.
    
    Returns
    -------
    str
        TODO: describe the return value.
    """
    
    return " ".join(split_words(name)).strip().lower()

def expr_to_text(expr: ast.expr | None) -> str:
    """Handle expr to text.
    
    Parameters
    ----------
    expr : ast.expr | None
        TODO: describe expr.
    
    Returns
    -------
    str
        TODO: describe the return value.
    """
    
    if expr is None:
        return "object"
    try:
        return ast.unparse(expr)
    except Exception:
        return "object"

def extract_public_symbols(tree: ast.Module) -> list[str]:
    """Extract  public symbols.
    
    Parameters
    ----------
    tree : ast.Module
        TODO: describe tree.
    
    Returns
    -------
    list[str]
        TODO: describe the return value.
    """
    
    explicit_all: list[str] | None = None
    fallback_public: list[str] = []

    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                fallback_public.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    explicit = []
                    if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                        ok = True
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                explicit.append(elt.value)
                            else:
                                ok = False
                                break
                        if ok:
                            explicit_all = explicit

    return sorted(set(explicit_all if explicit_all is not None else fallback_public))

def extract_internal_import_modules(tree: ast.Module) -> list[str]:
    """Extract  internal import modules.
    
    Parameters
    ----------
    tree : ast.Module
        TODO: describe tree.
    
    Returns
    -------
    list[str]
        TODO: describe the return value.
    """
    
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name.split(".")[-1] + ".py")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.append(node.module.split(".")[-1] + ".py")
    return sorted(set(modules))
