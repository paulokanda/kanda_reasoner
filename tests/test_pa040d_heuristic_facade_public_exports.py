"""PA040D tests for heuristic facade public exports."""

from __future__ import annotations

import ast

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help import (
    heuristic_docstrings,
)

_EXPECTED_EXPORTS = [
    "function_summary",
    "class_summary",
    "module_summary",
    "build_module_docstring",
    "build_class_docstring",
    "iter_function_parameters",
    "build_function_docstring",
]


def test_facade_public_exports_are_defined() -> None:
    """Public exports should be concrete facade functions."""
    assert sorted(heuristic_docstrings.__all__) == sorted(_EXPECTED_EXPORTS)

    for export_name in _EXPECTED_EXPORTS:
        exported = getattr(heuristic_docstrings, export_name, None)
        assert callable(exported), export_name


def test_facade_exports_generate_neutral_docstring_text() -> None:
    """The facade should preserve PA040 neutral heuristic output."""
    node = ast.parse(
        "def build_runner(name: str, retries: int = 2) -> PipelineRunner:\n"
        "    return PipelineRunner(name=name, retries=retries)\n"
    ).body[0]

    docstring = heuristic_docstrings.build_function_docstring(node)

    assert "TODO" not in docstring
    assert "Build a runner." in docstring
    assert "The runner name." in docstring
    assert "The retry count." in docstring
    assert "A pipeline runner instance." in docstring


if __name__ == "__main__":
    test_facade_public_exports_are_defined()
    test_facade_exports_generate_neutral_docstring_text()
    print("PA040D heuristic facade public export tests passed.")
