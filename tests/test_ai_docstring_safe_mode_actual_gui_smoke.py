
from __future__ import annotations

import ast
import importlib
from pathlib import Path
import unittest


TARGET_GUI = (
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
    "insert_missing_docstrings_gui.py"
)
MARKER = "T4Q024_SAFE_MODE_ACTUAL_TAB3_WIRING"
CHECKLIST = "tests/manual_safe_mode_gui_smoke_checklist.txt"


class SafeModeActualGuiSmokeSupportTests(unittest.TestCase):
    """Validate actual Tab 3 Safe Mode GUI wiring support."""

    def test_actual_gui_source_contains_single_safe_mode_wiring_marker(self) -> None:
        root = self._project_root()
        target = root / TARGET_GUI

        self.assertTrue(target.exists(), f"Missing target GUI file: {target}")
        source = target.read_text(encoding="utf-8")

        self.assertEqual(1, source.count(MARKER))
        self.assertIn("install_safe_mode_actual_tab3_wiring(self)", source)
        self.assertIn("_safe_mode_actual_tab3_wiring_result", source)

    def test_actual_gui_wiring_call_is_inside_class_init(self) -> None:
        root = self._project_root()
        target = root / TARGET_GUI
        tree = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))

        found = False
        for class_node in [node for node in tree.body if isinstance(node, ast.ClassDef)]:
            class_name = class_node.name.lower()
            if not any(token in class_name for token in ("window", "gui", "docstring")):
                continue

            for item in class_node.body:
                if not isinstance(item, ast.FunctionDef) or item.name != "__init__":
                    continue

                if self._init_contains_safe_mode_install(item):
                    found = True

        self.assertTrue(found, "Safe Mode install call was not found inside a GUI __init__.")

    def test_actual_gui_module_import_smoke(self) -> None:
        try:
            importlib.import_module(
                "kanda_reasoner_app.insert_missing_docstrings_gui."
                "insert_missing_docstrings_gui"
            )
        except ImportError as exc:
            if "PySide6" in str(exc):
                self.skipTest("PySide6 is unavailable in this Python environment.")
            raise

    def test_manual_smoke_checklist_exists(self) -> None:
        root = self._project_root()
        checklist = root / CHECKLIST

        self.assertTrue(checklist.exists(), f"Missing checklist: {checklist}")

        content = checklist.read_text(encoding="utf-8")
        self.assertIn("Safe Mode", content)
        self.assertIn("Tab 3", content)
        self.assertIn("existing controls", content)
        self.assertIn("No traceback", content)

    def _init_contains_safe_mode_install(self, init_node: ast.FunctionDef) -> bool:
        has_import = False
        has_result_assignment = False

        for node in ast.walk(init_node):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module.endswith("guided_folder_mode.actual_tab3_wiring"):
                    imported_names = {alias.name for alias in node.names}
                    if "install_safe_mode_actual_tab3_wiring" in imported_names:
                        has_import = True

            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and target.attr == "_safe_mode_actual_tab3_wiring_result"
                    ):
                        has_result_assignment = True

        return has_import and has_result_assignment

    def _project_root(self) -> Path:
        return Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    unittest.main()
