# project-path: kanda_reasoner_app/reasoner_context_collector/collector_ast_helpers_private.py
"""Private AST extraction helpers for collector_ast."""

from __future__ import annotations

__all__: list[str] = []

import ast
from typing import Any

from .collector_control_flow import build_control_flow
from .collector_data_flow import build_data_flow
from .collector_docstrings import build_docstring_summary
from .collector_utils import compact_whitespace


def _get_docstring(node: ast.AST) -> str:
    """Support get docstring behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    try:
        return ast.get_docstring(node) or ""
    except Exception:
        return ""

def _extract_comments_and_strings(
    source: str,
    tree: ast.AST | None,
) -> tuple[list[str], list[str]]:
    """Support extract comments and strings behavior.
    
    Parameters
    ----------
    source : str
        The source value.
    tree : ast.AST | None
        The parsed syntax tree.
    
    Returns
    -------
    tuple[list[str], list[str]]
        The tuple of values.
    """
    
    comments: list[str] = []
    strings: list[str] = []

    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            comments.append(stripped)

    if tree is not None:
        try:
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = compact_whitespace(node.value)
                    if value:
                        strings.append(value)
        except Exception:
            pass

    return comments, strings

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

def _extract_lambda_target(node: ast.Lambda) -> str:
    """Support extract lambda target behavior.
    
    Parameters
    ----------
    node : ast.Lambda
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    body = node.body

    if isinstance(body, ast.Call):
        return _name_from_node(body.func)

    if isinstance(body, ast.Attribute):
        return _name_from_node(body)

    if isinstance(body, ast.Name):
        return _name_from_node(body)

    return ""

def _extract_partial_target(node: ast.Call) -> str:
    """Support extract partial target behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    func_name = _name_from_node(node.func)
    if func_name != "partial":
        return ""

    if not node.args:
        return ""

    return _name_from_node(node.args[0])

def _extract_connect_target_fields(node: ast.Call) -> dict[str, Any]:
    """Support extract connect target fields behavior.
    
    Parameters
    ----------
    node : ast.Call
        The syntax tree node.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    fields = {
        "target": "",
        "handler_name": "",
        "callable_name": "",
        "lambda_target": "",
        "partial_target": "",
    }

    func_name = _name_from_node(node.func)
    if ".connect" not in func_name and not func_name.endswith("connect"):
        return fields

    if not node.args:
        return fields

    first_arg = node.args[0]

    if isinstance(first_arg, ast.Attribute):
        target = _name_from_node(first_arg)
        fields["target"] = target
        fields["handler_name"] = target
        fields["callable_name"] = target
        return fields

    if isinstance(first_arg, ast.Name):
        target = _name_from_node(first_arg)
        fields["target"] = target
        fields["handler_name"] = target
        fields["callable_name"] = target
        return fields

    if isinstance(first_arg, ast.Lambda):
        target = _extract_lambda_target(first_arg)
        if target:
            fields["target"] = target
            fields["lambda_target"] = target
        return fields

    if isinstance(first_arg, ast.Call):
        partial_target = _extract_partial_target(first_arg)
        if partial_target:
            fields["target"] = partial_target
            fields["partial_target"] = partial_target
            return fields

        callable_target = _name_from_node(first_arg.func)
        if callable_target:
            fields["target"] = callable_target
            fields["callable_name"] = callable_target
            return fields

    return fields

def _extract_calls(body: list[ast.stmt]) -> list[dict[str, Any]]:
    """Support extract calls behavior.
    
    Parameters
    ----------
    body : list[ast.stmt]
        The body value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
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
            call_record = {
                "call_name": call_name,
                "lineno": getattr(node, "lineno", None),
            }

            call_record.update(_extract_connect_target_fields(node))
            calls.append(call_record)
            self.generic_visit(node)

    visitor = Visitor()
    for stmt in body:
        visitor.visit(stmt)
    return calls

def _extract_assignments(body: list[ast.stmt]) -> list[dict[str, Any]]:
    """Support extract assignments behavior.
    
    Parameters
    ----------
    body : list[ast.stmt]
        The body value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    items: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Assign(self, node: ast.Assign) -> None:
            """Support visit assign behavior.
            
            Parameters
            ----------
            node : ast.Assign
                The syntax tree node.
            """
            
            for target in node.targets:
                target_name = _name_from_node(target)
                if target_name:
                    items.append(
                        {
                            "target": target_name,
                            "value_type": type(node.value).__name__,
                            "lineno": getattr(node, "lineno", None),
                        }
                    )
            self.generic_visit(node)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            """Support visit ann assign behavior.
            
            Parameters
            ----------
            node : ast.AnnAssign
                The syntax tree node.
            """
            
            target_name = _name_from_node(node.target)
            if target_name:
                items.append(
                    {
                        "target": target_name,
                        "value_type": type(node.value).__name__ if node.value else "",
                        "lineno": getattr(node, "lineno", None),
                    }
                )
            self.generic_visit(node)

    visitor = Visitor()
    for stmt in body:
        visitor.visit(stmt)
    return items

def _extract_attribute_reads(body: list[ast.stmt]) -> list[dict[str, Any]]:
    """Support extract attribute reads behavior.
    
    Parameters
    ----------
    body : list[ast.stmt]
        The body value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    items: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Attribute(self, node: ast.Attribute) -> None:
            """Support visit attribute behavior.
            
            Parameters
            ----------
            node : ast.Attribute
                The syntax tree node.
            """
            
            name = _name_from_node(node)
            if name:
                items.append(
                    {
                        "attribute": name,
                        "lineno": getattr(node, "lineno", None),
                    }
                )
            self.generic_visit(node)

    visitor = Visitor()
    for stmt in body:
        visitor.visit(stmt)
    return items

def _get_line_end(node: ast.AST) -> int | None:
    """Support get line end behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    int | None
        The integer result.
    """
    
    return getattr(node, "end_lineno", None) or getattr(node, "lineno", None)

def _get_decorator_names(node: ast.AST) -> list[str]:
    """Support get decorator names behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    decorator_list = getattr(node, "decorator_list", []) or []
    names: list[str] = []

    for decorator in decorator_list:
        name = _name_from_node(decorator)
        if name:
            names.append(name)

    return names

def _build_function_record(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    qualname: str,
    parent_symbol: str = "",
) -> dict[str, Any]:
    """Support build function record behavior.
    
    Parameters
    ----------
    node : ast.FunctionDef | ast.AsyncFunctionDef
        The syntax tree node.
    qualname : str
        The qualname value.
    parent_symbol : str, optional
        The optional parent symbol value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    docstring = _get_docstring(node)
    is_async = isinstance(node, ast.AsyncFunctionDef)

    return {
        "name": node.name,
        "qualname": qualname,
        "lineno": getattr(node, "lineno", None),
        "line_end": _get_line_end(node),
        "symbol_kind": "async_function" if is_async else "function",
        "is_async": is_async,
        "parent_symbol": parent_symbol,
        "decorator_names": _get_decorator_names(node),
        "docstring": docstring,
        "docstring_summary": build_docstring_summary(docstring),
        "calls": _extract_calls(node.body),
        "assignments": _extract_assignments(node.body),
        "attribute_reads": _extract_attribute_reads(node.body),
        "control_flow": build_control_flow(node, node.name),
        "data_flow": build_data_flow(node),
    }
