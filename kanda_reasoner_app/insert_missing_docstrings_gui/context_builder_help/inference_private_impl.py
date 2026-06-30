# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/context_builder_help/inference_private_impl.py
"""Private AST inference helpers for docstring context building."""

# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/context_builder.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/context_builder_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/context_builder_help/
# PURPOSE       : Private AST inference helpers for docstring context building
# EXPORTS       : none
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-30
# ------------------------------------------------------
from __future__ import annotations

import ast


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
        return ast.unparse(node).strip()
    except Exception:
        return ""


def _dedupe_texts(values: list[str]) -> list[str]:
    """Support dedupe texts behavior.
    
    Parameters
    ----------
    values : list[str]
        The input values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        output.append(text)
    return output


def _annotation_from_default(default: ast.AST | None) -> str:
    """Support annotation from default behavior.
    
    Parameters
    ----------
    default : ast.AST | None
        The default value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if default is None:
        return ""
    if isinstance(default, ast.Constant):
        value = default.value
        if value is None:
            return "None"
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int) and not isinstance(value, bool):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, str):
            return "str"
        if isinstance(value, bytes):
            return "bytes"
    if isinstance(default, ast.List):
        return "list"
    if isinstance(default, ast.Dict):
        return "dict"
    if isinstance(default, ast.Set):
        return "set"
    if isinstance(default, ast.Tuple):
        return "tuple"
    return ""


def _walk_without_nested_symbols(node: ast.AST) -> list[ast.AST]:
    """Support walk without nested symbols behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    list[ast.AST]
        The list of values.
    """
    
    output: list[ast.AST] = []
    stack = list(ast.iter_child_nodes(node))
    while stack:
        current = stack.pop(0)
        if current is not node and isinstance(
            current,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda),
        ):
            continue
        output.append(current)
        stack[0:0] = list(ast.iter_child_nodes(current))
    return output


def _has_top_level_yield(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Support has top level yield behavior.
    
    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for inner in _walk_without_nested_symbols(node):
        if isinstance(inner, (ast.Yield, ast.YieldFrom)):
            return True
    return False


def _top_level_returns(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.Return]:
    """Support top level returns behavior.
    
    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        The syntax tree node.
    
    Returns
    -------
    list[ast.Return]
        The list of values.
    """
    
    returns: list[ast.Return] = []
    for inner in _walk_without_nested_symbols(node):
        if isinstance(inner, ast.Return):
            returns.append(inner)
    return returns


def _infer_return_annotation(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Support infer return annotation behavior.
    
    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    if _has_top_level_yield(node):
        if isinstance(node, ast.AsyncFunctionDef):
            return "AsyncIterator[object]"
        return "Iterator[object]"

    returns = _top_level_returns(node)
    if not returns:
        return "None"

    has_value_return = False
    for item in returns:
        if item.value is None:
            continue
        if isinstance(item.value, ast.Constant) and item.value.value is None:
            continue
        has_value_return = True
        break

    if not has_value_return:
        return "None"
    return ""


def _raise_type_name(exc: ast.AST) -> str:
    """Support raise type name behavior.
    
    Parameters
    ----------
    exc : ast.AST
        The exc value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(exc, ast.Call):
        return _safe_unparse(exc.func)
    if isinstance(exc, (ast.Name, ast.Attribute, ast.Subscript)):
        return _safe_unparse(exc)
    return ""

__all__ = []
