# project-path: kanda_reasoner_app/source_hygiene/_shadow_audit_ast.py
"""AST public-surface extraction and statement classification helpers.

Private helpers for the shadow conflict audit. These functions only depend on
the standard-library ``ast`` module and never import the ``shadow_audit`` facade,
keeping the dependency direction one-way (facade -> this helper).
"""

from __future__ import annotations

import ast


def _collect_public_symbols(module: ast.Module) -> set[str]:
    """Support collect public symbols behavior.
    
    Parameters
    ----------
    module : ast.Module
        The module value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    symbols: set[str] = set()
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                symbols.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                symbols.update(_public_names_from_target(target))
        elif isinstance(node, ast.AnnAssign):
            symbols.update(_public_names_from_target(node.target))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                if not name.startswith("_"):
                    symbols.add(name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                name = alias.asname or alias.name
                if not name.startswith("_"):
                    symbols.add(name)
    symbols.discard("__all__")
    return symbols


def _collect_explicit_all(module: ast.Module) -> tuple[tuple[str, ...], bool]:
    """Support collect explicit all behavior.
    
    Parameters
    ----------
    module : ast.Module
        The module value.
    
    Returns
    -------
    tuple[tuple[str, ...], bool]
        The tuple of values.
    """
    
    names: list[str] = []
    found_dynamic = False
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        extracted = _literal_string_sequence(node.value)
        if extracted is None:
            found_dynamic = True
        else:
            names.extend(extracted)
    return tuple(names), found_dynamic


def _literal_string_sequence(node: ast.AST) -> tuple[str, ...] | None:
    """Support literal string sequence behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    tuple[str, ...] | None
        The tuple of values.
    """
    
    if not isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return None
    values: list[str] = []
    for item in node.elts:
        if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
            return None
        values.append(item.value)
    return tuple(values)


def _public_names_from_target(target: ast.AST) -> set[str]:
    """Support public names from target behavior.
    
    Parameters
    ----------
    target : ast.AST
        The target value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    names: set[str] = set()
    if isinstance(target, ast.Name):
        if not target.id.startswith("_"):
            names.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for item in target.elts:
            names.update(_public_names_from_target(item))
    return names


def _is_runtime_statement(node: ast.AST) -> bool:
    """Support is runtime statement behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if isinstance(node, ast.Expr):
        return not _is_module_docstring(node)
    if isinstance(node, ast.Assign):
        if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            return False
        return True
    if isinstance(node, ast.AnnAssign):
        return not (isinstance(node.target, ast.Name) and node.target.id == "__all__")
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return False
    return isinstance(node, (ast.For, ast.While, ast.If, ast.Try, ast.With, ast.Call))


def _is_module_docstring(node: ast.AST) -> bool:
    """Support is module docstring behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _is_type_checking_import(node: ast.AST) -> bool:
    """Support is type checking import behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return False
