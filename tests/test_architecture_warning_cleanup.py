"""Focused tests for accepted architecture warning cleanup."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ArchitectureWarningCleanupTests(unittest.TestCase):
    """Verify warning-cleanup owner files keep safe boundaries."""

    def _read_source(self, relative_path: str) -> str:
        path = PROJECT_ROOT / relative_path
        return path.read_text(encoding="utf-8")

    def test_docstring_injection_main_avoids_broad_exception_handlers(self) -> None:
        source = self._read_source("_inject_missing_module_docstrings.py")
        tree = ast.parse(source)
        main_node = next(
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == "main"
        )

        broad_handlers = []
        for node in ast.walk(main_node):
            if not isinstance(node, ast.ExceptHandler):
                continue
            if node.type is None:
                broad_handlers.append("bare")
                continue
            if isinstance(node.type, ast.Name) and node.type.id == "Exception":
                broad_handlers.append("Exception")

        self.assertEqual([], broad_handlers)

    def test_bridge_signals_has_no_direct_qt_import_statement(self) -> None:
        source = self._read_source(
            "kanda_reasoner_app/project_reasoner_v10/ai_bridge_help/bridge_signals.py"
        )
        tree = ast.parse(source)
        imports = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        imported_names = []
        for node in imports:
            if isinstance(node, ast.Import):
                imported_names.extend(alias.name for alias in node.names)
            else:
                imported_names.append(node.module or "")

        self.assertNotIn("PySide6.QtCore", imported_names)
        self.assertNotIn("PySide6.QtWidgets", imported_names)

    def test_architecture_ai_review_gui_imports_qt_lazily(self) -> None:
        source = self._read_source(
            "kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py"
        )
        tree = ast.parse(source)
        imports = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        imported_names = []
        for node in imports:
            if isinstance(node, ast.Import):
                imported_names.extend(alias.name for alias in node.names)
            else:
                imported_names.append(node.module or "")

        self.assertNotIn("PySide6.QtCore", imported_names)
        self.assertNotIn("PySide6.QtWidgets", imported_names)


if __name__ == "__main__":
    unittest.main()
