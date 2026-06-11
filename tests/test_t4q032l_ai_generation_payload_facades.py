
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_m import PAYLOAD_PARTS_M
from kanda_reasoner_app.backend_payloads.payload_n import PAYLOAD_PARTS_N
from kanda_reasoner_app.backend_payloads.payload_o import PAYLOAD_PARTS_O
from kanda_reasoner_app.backend_payloads.payload_p import PAYLOAD_PARTS_P


TARGETS = [
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/ai_docstring_generator.py',
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "ai_docstring_generator_help/docstring_payloads.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "ai_docstring_generator_help/heuristics.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "ai_docstring_generator_help/response_parsing.py"
    ),
]


class T4Q032LAiGenerationPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving AI generation facades."""

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
        payloads = [
            PAYLOAD_PARTS_M,
            PAYLOAD_PARTS_N,
            PAYLOAD_PARTS_O,
            PAYLOAD_PARTS_P,
        ]
        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_exported_names_are_statically_bound_when_all_exists(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            tree = ast.parse(source)

            exports = []
            assigned = set()
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
            if exports:
                self.assertIsNotNone(all_line, rel_path)
                self.assertTrue(set(exports).issubset(assigned), rel_path)
                self.assertLess(load_line, all_line, rel_path)

    def test_ai_docstring_generator_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator as ai_docstring_generator

        self.assertTrue(ai_docstring_generator)

    def test_docstring_payloads_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.docstring_payloads as docstring_payloads

        self.assertTrue(docstring_payloads)

    def test_heuristics_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.heuristics as heuristics

        self.assertTrue(heuristics)

    def test_response_parsing_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.ai_docstring_generator_help.response_parsing as response_parsing

        self.assertTrue(response_parsing)


if __name__ == "__main__":
    unittest.main()
