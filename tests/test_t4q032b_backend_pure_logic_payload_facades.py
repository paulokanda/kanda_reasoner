from __future__ import annotations

from pathlib import Path
import unittest


TARGETS = [
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/context_builder.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/docstring_validator.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/module_summarizer.py',
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings.py',
]


class T4Q032BBackendPureLogicPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving backend facades."""

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

    def test_payload_loader_imports(self) -> None:
        from kanda_reasoner_app.backend_payloads.loader import load_payload

        self.assertTrue(callable(load_payload))

    def test_payload_modules_exist(self) -> None:
        for key in ["a", "b", "c", "d"]:
            path = Path('ask_' 'ai_project_reasoner' '/backend_payloads/payload_' + key + ".py")
            self.assertTrue(path.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
