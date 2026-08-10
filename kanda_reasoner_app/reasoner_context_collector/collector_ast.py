# project-path: kanda_reasoner_app/reasoner_context_collector/collector_ast.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any
from .collector_docstrings import build_docstring_summary
from .collector_utils import safe_read_text
from .collector_ast_helpers_private import (
    _get_docstring,
    _extract_comments_and_strings,
    _name_from_node,
    _get_line_end,
    _get_decorator_names,
    _build_function_record,
)

from .collector_warnings import parse_python_source_with_warnings


def parse_python_file(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Parse the python file.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    tuple[dict[str, Any] | None, str | None]
        The tuple of values.
    """
    
    try:
        source = safe_read_text(path)
        tree, parse_warning_error, parse_warnings = parse_python_source_with_warnings(source)
        if parse_warning_error is not None or tree is None:
            return None, parse_warning_error
    except Exception as exc:
        return None, str(exc)

    comments, strings = _extract_comments_and_strings(source, tree)

    module_docstring = _get_docstring(tree)
    imports: list[str] = []
    classes: list[dict[str, Any]] = []
    functions: list[dict[str, Any]] = []

    function_types = (ast.FunctionDef, ast.AsyncFunctionDef)

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            imports.append(module_name)

        elif isinstance(node, function_types):

            functions.append(_build_function_record(node, node.name))

        elif isinstance(node, ast.ClassDef):
            methods: list[dict[str, Any]] = []
            bases = [_name_from_node(base) for base in node.bases]
            class_docstring = _get_docstring(node)

            for item in node.body:
                if isinstance(item, function_types):
                    methods.append(
                        _build_function_record(
                            item,
                            node.name + "." + item.name,
                            parent_symbol=node.name,
                        )
                    )

            classes.append(
                {
                    "name": node.name,
                    "qualname": node.name,
                    "lineno": getattr(node, "lineno", None),
                    "line_end": _get_line_end(node),
                    "symbol_kind": "class",
                    "parent_symbol": "",
                    "decorator_names": _get_decorator_names(node),
                    "docstring": class_docstring,
                    "docstring_summary": build_docstring_summary(class_docstring),
                    "bases": bases,
                    "methods": methods,
                }
            )

    payload = {
        "module_docstring": module_docstring,
        "module_docstring_summary": build_docstring_summary(module_docstring),
        "imports": sorted(set(filter(None, imports))),
        "classes": classes,
        "functions": functions,
        "comments": comments,
        "strings": strings,
        "parse_warnings": parse_warnings,
        "source": source,
    }
    return payload, None
