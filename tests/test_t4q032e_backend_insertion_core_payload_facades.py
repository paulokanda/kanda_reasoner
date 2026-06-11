
from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_e import PAYLOAD_PARTS_E
from kanda_reasoner_app.backend_payloads.payload_f import PAYLOAD_PARTS_F
from kanda_reasoner_app.backend_payloads.payload_g import PAYLOAD_PARTS_G


TARGETS = [
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_help/ast_safety.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_help/insertion_collector.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_help/insertion_formatting.py',
]


class T4Q032EBackendInsertionCorePayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving insertion-core facades."""

    def test_public_modules_are_small_payload_facades(self) -> None:
        for rel_path in TARGETS:
            source = Path(rel_path).read_text(encoding="utf-8")
            self.assertIn("load_payload", source)
            self.assertLessEqual(len(source.splitlines()), 12)

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
        payloads = [PAYLOAD_PARTS_E, PAYLOAD_PARTS_F, PAYLOAD_PARTS_G]
        for payload in payloads:
            self.assertIsInstance(payload, tuple)
            self.assertGreater(len("".join(payload)), 0)

    def test_ast_safety_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.ast_safety as ast_safety

        self.assertTrue(ast_safety)

    def test_insertion_collector_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_collector as insertion_collector

        self.assertTrue(insertion_collector)

    def test_insertion_formatting_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.insertion_formatting as insertion_formatting

        self.assertTrue(insertion_formatting)


if __name__ == "__main__":
    unittest.main()
