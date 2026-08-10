# project-path: tests/test_collector_runtime_scenarios_normalization_manifest_contract.py
"""Focused ownership contract for collector runtime-scenario normalization helpers."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import kanda_reasoner_app.reasoner_context_collector.collector_runtime_scenarios_help.normalization as normalization

EXPECTED_NORMALIZATION_HELPERS = [
    "_safe_text",
    "_safe_lower",
    "_safe_int",
    "_read_json",
    "_normalize_path_text",
]


def test_collector_runtime_scenarios_normalization_manifest_contract() -> None:
    """Keep the manifest-owned normalization helper explicitly test-reachable."""
    module_path = Path(normalization.__file__).resolve()
    manifest_path = module_path.parent.parent / "collector_runtime_scenarios_help.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["helpers"]["normalization.py"] == EXPECTED_NORMALIZATION_HELPERS

    tree = ast.parse(
        module_path.read_text(encoding="utf-8"),
        filename=str(module_path),
    )
    defined_functions = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert set(EXPECTED_NORMALIZATION_HELPERS).issubset(defined_functions)


if __name__ == "__main__":
    test_collector_runtime_scenarios_normalization_manifest_contract()
    print("NORMALIZATION_MANIFEST_CONTRACT_TEST: PASS")
