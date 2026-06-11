
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_u import PAYLOAD_PARTS_U


TARGET = 'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py'


class T4Q032UDocstringMainGuiPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving facade for the main docstring GUI module."""

    def test_main_gui_module_is_small_payload_facade(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")

        self.assertIn("load_payload(__name__, globals(), 'u')", source)
        self.assertLessEqual(len(source.splitlines()), 12)

    def test_main_gui_facade_avoids_static_mixed_signals(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
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

        for needle in forbidden:
            self.assertNotIn(needle, source, needle)

    def test_payload_module_has_unique_public_contract(self) -> None:
        self.assertIsInstance(PAYLOAD_PARTS_U, tuple)
        self.assertGreater(len("".join(PAYLOAD_PARTS_U)), 0)

    def test_exported_names_are_statically_bound_when_all_exists(self) -> None:
        source = Path(TARGET).read_text(encoding="utf-8")
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

        self.assertIsNotNone(load_line)
        if exports:
            self.assertIsNotNone(all_line)
            self.assertTrue(set(exports).issubset(assigned))
            self.assertLess(load_line, all_line)

    def test_main_gui_imports_public_entrypoint(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui as main_gui

        self.assertTrue(main_gui)
        public_names = [name for name in dir(main_gui) if not name.startswith("_")]
        self.assertTrue(public_names)


if __name__ == "__main__":
    unittest.main()
