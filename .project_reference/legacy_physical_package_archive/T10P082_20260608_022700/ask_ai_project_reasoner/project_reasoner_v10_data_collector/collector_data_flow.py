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
    if isinstance(node, ast.Subscript):
        return _name_from_node(node.value)
    if isinstance(node, ast.Call):
        return _name_from_node(node.func)
    return ""


def _safe_unparse(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return " ".join(ast.unparse(node).split())
    except Exception:
        return ""


def _append_unique(value: str, items: list[str]) -> None:
    if value and value not in items:
        items.append(value)


def _extract_reads_from_expr(node: ast.AST | None) -> list[str]:
    reads: list[str] = []

    if node is None:
        return reads

    class Visitor(ast.NodeVisitor):
        def visit_Name(self, name_node: ast.Name) -> None:
            _append_unique(name_node.id, reads)

        def visit_Attribute(self, attr_node: ast.Attribute) -> None:
            name = _name_from_node(attr_node)
            _append_unique(name, reads)
            self.generic_visit(attr_node.value)

    Visitor().visit(node)
    return reads


def _extract_write_targets(target_node: ast.AST) -> list[str]:
    targets: list[str] = []

    class Visitor(ast.NodeVisitor):
        def visit_Name(self, name_node: ast.Name) -> None:
            _append_unique(name_node.id, targets)

        def visit_Attribute(self, attr_node: ast.Attribute) -> None:
            name = _name_from_node(attr_node)
            _append_unique(name, targets)
            self.generic_visit(attr_node.value)

        def visit_Tuple(self, tuple_node: ast.Tuple) -> None:
            for elt in tuple_node.elts:
                self.visit(elt)

        def visit_List(self, list_node: ast.List) -> None:
            for elt in list_node.elts:
                self.visit(elt)

        def visit_Subscript(self, sub_node: ast.Subscript) -> None:
            name = _name_from_node(sub_node)
            if name:
                _append_unique(name, targets)
            self.generic_visit(sub_node.value)

    Visitor().visit(target_node)
    return targets


def _record_dependency(
    dependencies: list[dict[str, Any]],
    target: str,
    sources: list[str],
    line: int | None,
    expr: str,
) -> None:
    if not target:
        return
    dependencies.append(
        {
            "target": target,
            "sources": sources,
            "line": line,
            "expr": expr,
        }
    )


def build_data_flow(function_node: ast.AST) -> dict[str, Any]:
    reads: list[str] = []
    writes: list[str] = []
    return_reads: list[str] = []
    dependencies: list[dict[str, Any]] = []
    module_writes: list[str] = []
    attribute_writes: list[str] = []

    for stmt in ast.walk(function_node):
        if isinstance(stmt, ast.Assign):
            sources = _extract_reads_from_expr(stmt.value)
            for source in sources:
                _append_unique(source, reads)

            for target_node in stmt.targets:
                targets = _extract_write_targets(target_node)
                for target in targets:
                    _append_unique(target, writes)
                    if "." in target:
                        _append_unique(target, attribute_writes)
                    else:
                        _append_unique(target, module_writes)
                    _record_dependency(
                        dependencies,
                        target,
                        sources,
                        getattr(stmt, "lineno", None),
                        _safe_unparse(stmt.value),
                    )

        elif isinstance(stmt, ast.AnnAssign):
            sources = _extract_reads_from_expr(stmt.value)
            for source in sources:
                _append_unique(source, reads)

            targets = _extract_write_targets(stmt.target)
            for target in targets:
                _append_unique(target, writes)
                if "." in target:
                    _append_unique(target, attribute_writes)
                else:
                    _append_unique(target, module_writes)
                _record_dependency(
                    dependencies,
                    target,
                    sources,
                    getattr(stmt, "lineno", None),
                    _safe_unparse(stmt.value),
                )

        elif isinstance(stmt, ast.AugAssign):
            sources = _extract_reads_from_expr(stmt.value)
            targets = _extract_write_targets(stmt.target)

            dependency_sources: list[str] = []
            for source in sources:
                _append_unique(source, reads)
                _append_unique(source, dependency_sources)

            for target in targets:
                _append_unique(target, reads)
                _append_unique(target, writes)
                _append_unique(target, dependency_sources)
                if "." in target:
                    _append_unique(target, attribute_writes)
                else:
                    _append_unique(target, module_writes)
                _record_dependency(
                    dependencies,
                    target,
                    dependency_sources,
                    getattr(stmt, "lineno", None),
                    _safe_unparse(stmt.value),
                )

        elif isinstance(stmt, ast.Return):
            sources = _extract_reads_from_expr(stmt.value)
            for source in sources:
                _append_unique(source, reads)
                _append_unique(source, return_reads)

    return {
        "reads": reads,
        "writes": writes,
        "return_reads": return_reads,
        "attribute_writes": attribute_writes,
        "module_writes": module_writes,
        "dependencies": dependencies,
    }