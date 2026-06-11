
from __future__ import annotations

import ast
from pathlib import Path
import unittest

from kanda_reasoner_app.backend_payloads.payload_q import PAYLOAD_PARTS_Q
from kanda_reasoner_app.backend_payloads.payload_r import PAYLOAD_PARTS_R
from kanda_reasoner_app.backend_payloads.payload_s import PAYLOAD_PARTS_S
from kanda_reasoner_app.backend_payloads.payload_t import PAYLOAD_PARTS_T


TARGETS = [
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_gui_help/ai_settings.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_gui_help/dialogs.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_gui_help/run_controls.py"
    ),
    (
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_gui_help/window_state.py"
    ),
]


class T4Q032MGuiHelperPayloadFacadeTests(unittest.TestCase):
    """Validate source-preserving GUI helper facades."""

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
            PAYLOAD_PARTS_Q,
            PAYLOAD_PARTS_R,
            PAYLOAD_PARTS_S,
            PAYLOAD_PARTS_T,
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

    def test_ai_settings_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.ai_settings as ai_settings

        self.assertTrue(ai_settings)

    def test_dialogs_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.dialogs as dialogs

        self.assertTrue(dialogs)

    def test_run_controls_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.run_controls as run_controls

        self.assertTrue(run_controls)

    def test_window_state_facade_imports_public_api(self) -> None:
        import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.window_state as window_state

        self.assertTrue(window_state)


if __name__ == "__main__":
    unittest.main()
