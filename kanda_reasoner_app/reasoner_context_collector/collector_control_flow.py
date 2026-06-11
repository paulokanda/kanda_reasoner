"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import ast
from typing import Any


def _name_from_node(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _name_from_node(node.value)
        return base + "." + node.attr if base else node.attr
    if isinstance(node, ast.Call):
        return _name_from_node(node.func)
    return ""


def _safe_unparse(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        text = ast.unparse(node)
        return " ".join(text.split())
    except Exception:
        return ""


def _append_unique_call(call_name: str, calls: list[str]) -> None:
    if call_name and call_name not in calls:
        calls.append(call_name)


def _collect_calls_in_nodes(nodes: list[ast.stmt]) -> list[str]:
    found: list[str] = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            name = _name_from_node(node.func)
            _append_unique_call(name, found)
            self.generic_visit(node)

    visitor = Visitor()
    for node in nodes:
        visitor.visit(node)
    return found


def _collect_simple_statement_calls(stmt: ast.stmt) -> list[dict[str, Any]]:
    if isinstance(stmt, (ast.If, ast.For, ast.While, ast.Return, ast.Try, ast.With, ast.AsyncWith)):
        return []

    calls: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
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
    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.found = False

        def visit_Call(self, call_node: ast.Call) -> None:
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