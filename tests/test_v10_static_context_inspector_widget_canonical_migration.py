"""Focused tests for canonical v10 static context inspector widget migration."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class V10StaticContextInspectorWidgetCanonicalMigrationTests(unittest.TestCase):
    """Validate the canonical static context inspector widget migration."""

    def test_canonical_inspector_widget_file_exists(self):
        path = Path(
            "kanda_reasoner_app/reasoner_engine/"
            "v10_static_context_inspector_widget.py"
        )
        self.assertTrue(path.exists(), str(path))

    def test_canonical_inspector_widget_source_prefers_reasoner_engine(self):
        path = Path(
            "kanda_reasoner_app/reasoner_engine/"
            "v10_static_context_inspector_widget.py"
        )
        text = path.read_text(encoding="utf-8", errors="replace")
        self.assertNotIn("ask_ai_project_reasoner.project_reasoner_v10", text)
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10", text)

    def test_canonical_inspector_widget_imports(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine."
            "v10_static_context_inspector_widget"
        )
        self.assertIsNotNone(module)

    def test_canonical_static_context_dialog_imports_after_widget(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.v10_static_context_dialog"
        )
        self.assertIsNotNone(module)


if __name__ == "__main__":
    unittest.main()
