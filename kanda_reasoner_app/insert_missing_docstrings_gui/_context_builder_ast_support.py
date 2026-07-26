# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/_context_builder_ast_support.py
"""Pure AST and metadata support for docstring context construction."""

from __future__ import annotations

__all__: list[str] = []

import ast
import textwrap
from typing import Any

from .context_builder_help.inference_private_impl import (
    _dedupe_texts,
    _raise_type_name,
    _walk_without_nested_symbols,
)


def _safe_unparse(node: ast.AST | None) -> str:
    """Support safe unparse behavior.
    
    Parameters
    ----------
    node : ast.AST | None
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def _decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[str]:
    """Support decorator names behavior.
    
    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
        The syntax tree node.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    names: list[str] = []
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name):
            names.append(dec.id)
        elif isinstance(dec, ast.Attribute):
            names.append(dec.attr)
        else:
            text = _safe_unparse(dec)
            if text:
                names.append(text)
    return names


def _extract_imports(tree: ast.Module, *, limit: int = 10) -> list[str]:
    """Support extract imports behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    lines: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            rendered = _safe_unparse(node)
            if rendered:
                lines.append(rendered)
            if len(lines) >= limit:
                break
        elif not isinstance(node, (ast.Expr, ast.Assign, ast.AnnAssign)):
            break
    return lines


def _extract_source_lines(node: ast.AST, file_lines: list[str], *, limit: int = 80) -> list[str]:
    """Support extract source lines behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    file_lines : list[str]
        The file lines value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    try:
        lineno = node.lineno
    except AttributeError:
        lineno = 1
    try:
        end_lineno = node.end_lineno
    except AttributeError:
        end_lineno = lineno
    raw = file_lines[lineno - 1 : end_lineno]
    dedented = textwrap.dedent("\n".join(raw)).splitlines()
    if len(dedented) > limit:
        return dedented[:limit] + ["# ... truncated for prompt ..."]
    return dedented


def _extract_sibling_docstrings(parent_body: list[ast.stmt], current_node: ast.AST, *, limit: int = 3) -> list[str]:
    """Support extract sibling docstrings behavior.
    
    Parameters
    ----------
    parent_body : list[ast.stmt]
        The parent body value.
    current_node : ast.AST
        The current node value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    docs: list[str] = []
    for sibling in parent_body:
        if sibling is current_node:
            continue
        if isinstance(sibling, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(sibling, clean=False)
            if doc:
                docs.append(doc.strip())
            if len(docs) >= limit:
                break
    return docs


def _extract_raises_types(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Support extract raises types behavior.
    
    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        The syntax tree node.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    result: list[str] = []
    for inner in _walk_without_nested_symbols(node):
        if not isinstance(inner, ast.Raise) or inner.exc is None:
            continue
        name = _raise_type_name(inner.exc)
        if name:
            result.append(name)
    return _dedupe_texts(result)


def _find_parent_class(tree: ast.Module, node: ast.AST) -> ast.ClassDef | None:
    """Support find parent class behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    ast.ClassDef | None
        The class def result.
    """
    
    for parent in ast.walk(tree):
        if isinstance(parent, ast.ClassDef) and node in parent.body:
            return parent
    return None


def _collect_overload_siblings(parent_body: list[ast.stmt], name: str, current_node: ast.AST) -> list[str]:
    """Support collect overload siblings behavior.
    
    Parameters
    ----------
    parent_body : list[ast.stmt]
        The parent body value.
    name : str
        The name value.
    current_node : ast.AST
        The current node value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    results: list[str] = []
    for sibling in parent_body:
        if sibling is current_node:
            continue
        if isinstance(sibling, (ast.FunctionDef, ast.AsyncFunctionDef)) and sibling.name == name:
            decs = _decorator_names(sibling)
            if "overload" not in decs:
                continue
            prefix = "async def" if isinstance(sibling, ast.AsyncFunctionDef) else "def"
            try:
                args_text = ast.unparse(sibling.args)
                if not args_text.startswith("("):
                    args_text = f"({args_text})"
            except Exception:
                args_text = "(...)"
            return_text = ""
            if sibling.returns is not None:
                ret = _safe_unparse(sibling.returns)
                if ret:
                    return_text = f" -> {ret}"
            results.append(f"{prefix} {sibling.name}{args_text}{return_text}")
    return results


def _module_summary_block(module_summary: Any | None) -> str:
    """Support module summary block behavior.
    
    Parameters
    ----------
    module_summary : Any | None
        The module summary value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if module_summary is None:
        return ""
    try:
        return module_summary.context_block
    except AttributeError:
        return ""


