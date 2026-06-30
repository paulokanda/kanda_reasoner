# project-path: kanda_reasoner_app/reasoner_context_collector/collector_control_flow.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import ast
from typing import Any


def _name_from_node(node: ast.AST) -> str:
    """Support name from node behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _name_from_node(node.value)
        return base + "." + node.attr if base else node.attr
    if isinstance(node, ast.Call):
        return _name_from_node(node.func)
    return ""


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
        text = ast.unparse(node)
        return " ".join(text.split())
    except Exception:
        return ""


def _append_unique_call(call_name: str, calls: list[str]) -> None:
    """Support append unique call behavior.
    
    Parameters
    ----------
    call_name : str
        The call name value.
    calls : list[str]
        The calls value.
    """
    
    if call_name and call_name not in calls:
        calls.append(call_name)


def _collect_calls_in_nodes(nodes: list[ast.stmt]) -> list[str]:
    """Support collect calls in nodes behavior.
    
    Parameters
    ----------
    nodes : list[ast.stmt]
        The nodes value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    found: list[str] = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            """Support visit call behavior.
            
            Parameters
            ----------
            node : ast.Call
                The syntax tree node.
            """
            
            name = _name_from_node(node.func)
            _append_unique_call(name, found)
            self.generic_visit(node)

    visitor = Visitor()
    for node in nodes:
        visitor.visit(node)
    return found


def _collect_simple_statement_calls(stmt: ast.stmt) -> list[dict[str, Any]]:
    """Support collect simple statement calls behavior.
    
    Parameters
    ----------
    stmt : ast.stmt
        The stmt value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    if isinstance(stmt, (ast.If, ast.For, ast.While, ast.Return, ast.Try, ast.With, ast.AsyncWith)):
        return []

    calls: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            """Support visit call behavior.
            
            Parameters
            ----------
            node : ast.Call
                The syntax tree node.
            """
            
            call_name = _name_from_node(node.func)
            if call_name:
                calls.append(
                    {
                        "type": "call",
                        "name": call_name,
                        "line": getattr(node, "lineno", None),
                    }
                )
            self.generic_visit(node)

    Visitor().visit(stmt)
    return calls


def _has_recursion_hint(function_name: str, node: ast.AST) -> bool:
    """Support has recursion hint behavior.
    
    Parameters
    ----------
    function_name : str
        The function name value.
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            """Support init behavior.
            """
            
            self.found = False

        def visit_Call(self, call_node: ast.Call) -> None:
            """Support visit call behavior.
            
            Parameters
            ----------
            call_node : ast.Call
                The call node value.
            """
            
            call_name = _name_from_node(call_node.func)
            if call_name == function_name or call_name.endswith("." + function_name):
                self.found = True
                return
            self.generic_visit(call_node)

    visitor = Visitor()
    visitor.visit(node)
    return visitor.found


def _walk_statements(
    body: list[ast.stmt],
    sequence: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    loops: list[dict[str, Any]],
    returns: list[dict[str, Any]],
    calls: list[str],
) -> None:
    """Support walk statements behavior.
    
    Parameters
    ----------
    body : list[ast.stmt]
        The body value.
    sequence : list[dict[str, Any]]
        The sequence value.
    branches : list[dict[str, Any]]
        The branches value.
    loops : list[dict[str, Any]]
        The loops value.
    returns : list[dict[str, Any]]
        The returns value.
    calls : list[str]
        The calls value.
    """
    
    for stmt in body:
        if isinstance(stmt, ast.If):
            sequence.append(
                {
                    "type": "if",
                    "line": getattr(stmt, "lineno", None),
                }
            )

            body_calls = _collect_calls_in_nodes(stmt.body)
            orelse_calls = _collect_calls_in_nodes(stmt.orelse)

            for name in body_calls:
                _append_unique_call(name, calls)
            for name in orelse_calls:
                _append_unique_call(name, calls)

            branches.append(
                {
                    "line": getattr(stmt, "lineno", None),
                    "has_else": bool(stmt.orelse),
                    "test": _safe_unparse(stmt.test),
                    "body_calls": body_calls,
                    "orelse_calls": orelse_calls,
                }
            )

            _walk_statements(stmt.body, sequence, branches, loops, returns, calls)

            if stmt.orelse:
                else_line = getattr(stmt.orelse[0], "lineno", getattr(stmt, "lineno", None))
                sequence.append(
                    {
                        "type": "else",
                        "line": else_line,
                    }
                )
                _walk_statements(stmt.orelse, sequence, branches, loops, returns, calls)

            continue

        if isinstance(stmt, ast.For):
            sequence.append(
                {
                    "type": "for",
                    "line": getattr(stmt, "lineno", None),
                }
            )

            body_calls = _collect_calls_in_nodes(stmt.body)
            for name in body_calls:
                _append_unique_call(name, calls)

            loops.append(
                {
                    "type": "for",
                    "line": getattr(stmt, "lineno", None),
                    "target": _safe_unparse(stmt.target),
                    "iter": _safe_unparse(stmt.iter),
                    "body_calls": body_calls,
                }
            )

            _walk_statements(stmt.body, sequence, branches, loops, returns, calls)

            if stmt.orelse:
                _walk_statements(stmt.orelse, sequence, branches, loops, returns, calls)

            continue

        if isinstance(stmt, ast.While):
            sequence.append(
                {
                    "type": "while",
                    "line": getattr(stmt, "lineno", None),
                }
            )

            body_calls = _collect_calls_in_nodes(stmt.body)
            for name in body_calls:
                _append_unique_call(name, calls)

            loops.append(
                {
                    "type": "while",
                    "line": getattr(stmt, "lineno", None),
                    "test": _safe_unparse(stmt.test),
                    "body_calls": body_calls,
                }
            )

            _walk_statements(stmt.body, sequence, branches, loops, returns, calls)

            if stmt.orelse:
                _walk_statements(stmt.orelse, sequence, branches, loops, returns, calls)

            continue

        if isinstance(stmt, ast.Return):
            line = getattr(stmt, "lineno", None)
            sequence.append(
                {
                    "type": "return",
                    "line": line,
                }
            )
            returns.append({"line": line})

            value_calls = _collect_calls_in_nodes([stmt])
            for name in value_calls:
                _append_unique_call(name, calls)
                sequence.append(
                    {
                        "type": "call",
                        "name": name,
                        "line": line,
                    }
                )
            continue

        simple_calls = _collect_simple_statement_calls(stmt)
        for item in simple_calls:
            sequence.append(item)
            _append_unique_call(item["name"], calls)


def build_control_flow(function_node: ast.AST, function_name: str) -> dict[str, Any]:
    """Build a control flow.
    
    Parameters
    ----------
    function_node : ast.AST
        The function node value.
    function_name : str
        The function name value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    body = getattr(function_node, "body", [])
    sequence: list[dict[str, Any]] = []
    branches: list[dict[str, Any]] = []
    loops: list[dict[str, Any]] = []
    returns: list[dict[str, Any]] = []
    calls: list[str] = []

    if isinstance(body, list):
        _walk_statements(body, sequence, branches, loops, returns, calls)

    return {
        "sequence": sequence,
        "branches": branches,
        "loops": loops,
        "returns": returns,
        "calls": calls,
        "recursion_hint": _has_recursion_hint(function_name, function_node),
    }
