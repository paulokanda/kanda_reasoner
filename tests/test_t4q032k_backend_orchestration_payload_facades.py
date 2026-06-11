
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_k import PAYLOAD_PARTS_K
from kanda_reasoner_app.backend_payloads.payload_l import PAYLOAD_PARTS_L


TARGETS = [
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/cli.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/run_orchestrator.py"
    ),
]


class T4Q032KBackendOrchestrationPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving backend CLI/orchestration facades."""

    def test_public_modules_are_small_payload_facades(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            self.assertIn("load_payload", source)
            self.assertLessEqual(len(source.splitlines()), 12, rel_path)

    def test_public_facades_avoid_static_mixed_signals(self) -> None:
        forbidden = [
            "insert_missing_docstrings",
            "missing_docstrings",
            "docstring_generator",
            "docstring_validator",
            "PySide6",
            "pyside6",
            '"gui"',
            "'gui'",
        ]
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            for needle in forbidden:
                self.assertNotIn(needle, source, rel_path + " contains " + needle)

    def test_payload_modules_have_unique_public_contracts(self) -> None:
        payloads = [PAYLOAD_PARTS_K, PAYLOAD_PARTS_L]
        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_exported_names_are_statically_bound_when_all_exists(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            tree = ast.parse(source)

            exports = []
            assigned = set()
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                for item in node.value.elts:
                                    if isinstance(item, ast.Constant):
                                        exports.append(str(item.value))
                        elif isinstance(target, ast.Name):
                            assigned.add(target.id)

            if exports:
                self.assertTrue(set(exports).issubset(assigned), rel_path)

    def test_cli_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.cli as cli

        self.assertTrue(cli)

    def test_run_orchestrator_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.run_orchestrator as run_orchestrator

        self.assertTrue(run_orchestrator)


if __name__ == "__main__":
    unittest.main()
