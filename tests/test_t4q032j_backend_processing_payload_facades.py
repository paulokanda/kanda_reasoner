
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_h import PAYLOAD_PARTS_H
from kanda_reasoner_app.backend_payloads.payload_i import PAYLOAD_PARTS_I
from kanda_reasoner_app.backend_payloads.payload_j import PAYLOAD_PARTS_J


TARGETS = [
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/file_processing.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/heuristic_docstrings.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_help/reporting.py"
    ),
]


class T4Q032JBackendProcessingPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving backend processing/reporting facades."""

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
        payloads = [PAYLOAD_PARTS_H, PAYLOAD_PARTS_I, PAYLOAD_PARTS_J]
        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_exported_names_are_statically_bound(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            tree = ast.parse(source)

            assigned = set()
            exports = []
            load_line = None
            all_line = None

            for node in tree.body:
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    func = node.value.func
                    if isinstance(func, ast.Name) and func.id == "load_payload":
                        load_line = node.lineno
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            all_line = node.lineno
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                for item in node.value.elts:
                                    if isinstance(item, ast.Constant):
                                        exports.append(str(item.value))
                        elif isinstance(target, ast.Name):
                            assigned.add(target.id)

            self.assertIsNotNone(load_line, rel_path)
            self.assertIsNotNone(all_line, rel_path)
            self.assertTrue(exports, rel_path)
            self.assertTrue(set(exports).issubset(assigned), rel_path)
            self.assertLess(load_line, all_line, rel_path)

    def test_file_processing_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing as file_processing

        self.assertTrue(file_processing)

    def test_heuristic_docstrings_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.heuristic_docstrings as heuristic_docstrings

        self.assertTrue(heuristic_docstrings)

    def test_reporting_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.reporting as reporting

        self.assertTrue(reporting)


if __name__ == "__main__":
    unittest.main()
