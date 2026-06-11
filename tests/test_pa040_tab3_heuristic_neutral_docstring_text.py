"""PA040 tests for neutral heuristic docstring text."""

from __future__ import annotations

import ast
from pathlib import Path

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help import (
    heuristic_docstrings,
)


def _first_function(source: str) -> ast.FunctionDef | ast.AsyncFunctionDef:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return node
    raise AssertionError("No function node found")


def test_build_function_docstring_removes_todo_and_double_spaces() -> None:
    node = _first_function(
        "def build_runner(name: str, retries: int = 2) -> PipelineRunner:\n"
        "    return PipelineRunner(name=name, retries=retries)\n"
    )

    docstring = heuristic_docstrings.build_function_docstring(node)

    assert "TODO" not in docstring
    assert "Build  runner" not in docstring
    assert "Build a runner." in docstring
    assert "name : str" in docstring
    assert "The runner name." in docstring
    assert "retries : int, optional" in docstring
    assert "The retry count." in docstring
    assert "PipelineRunner" in docstring
    assert "A pipeline runner instance." in docstring


def test_build_function_docstring_uses_common_parameter_descriptions() -> None:
    node = _first_function(
        "def read_header_value(raw: str, path: Path) -> str:\n"
        "    return raw.strip()\n"
    )

    docstring = heuristic_docstrings.build_function_docstring(node)

    assert "TODO" not in docstring
    assert "Return the header value." in docstring
    assert "The raw input value." in docstring
    assert "The file or folder path." in docstring
    assert "The string result." in docstring


def test_build_module_docstring_stays_neutral() -> None:
    docstring = heuristic_docstrings.build_module_docstring(
        Path("app/main.py"),
        "app.main",
        ast.parse("from __future__ import annotations\n"),
        Path("."),
        None,
    )

    assert docstring == '"""Utilities and definitions for main."""'
    assert "TODO" not in docstring


if __name__ == "__main__":
    test_build_function_docstring_removes_todo_and_double_spaces()
    test_build_function_docstring_uses_common_parameter_descriptions()
    test_build_module_docstring_stays_neutral()
    print("PA040 Tab 3 heuristic neutral docstring text tests passed.")
