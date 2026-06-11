"""PA040C tests for heuristic helper manifest export contract."""

from __future__ import annotations

import ast
import json
from pathlib import Path

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


def test_heuristic_docstrings_exports_match_manifest_contract() -> None:
    assert sorted(heuristic_docstrings.__all__) == sorted(_EXPECTED_EXPORTS)

    for export_name in _EXPECTED_EXPORTS:
        assert hasattr(heuristic_docstrings, export_name), export_name


def test_heuristic_docstrings_manifest_lists_exported_names() -> None:
    manifest_path = Path(
        'ask_' 'ai_project_reasoner'
        "/insert_missing_docstrings_gui"
        "/insert_missing_docstrings_help.json"
    )
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_exports = data["helpers"]["heuristic_docstrings.py"]["exports"]

    assert sorted(manifest_exports) == sorted(_EXPECTED_EXPORTS)


def test_payload_facade_still_generates_neutral_text() -> None:
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
    test_heuristic_docstrings_exports_match_manifest_contract()
    test_heuristic_docstrings_manifest_lists_exported_names()
    test_payload_facade_still_generates_neutral_text()
    print("PA040C heuristic manifest contract tests passed.")
