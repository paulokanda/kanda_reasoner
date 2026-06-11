"""Focused protection for canonical v10_static_context_dialog migration."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path

import kanda_reasoner_app.reasoner_engine.v10_static_context_dialog as canonical_static_context_dialog


class V10StaticContextDialogCanonicalMigrationTests(unittest.TestCase):
    def test_canonical_static_context_dialog_file_exists(self):
        path = Path("kanda_reasoner_app/reasoner_engine/v10_static_context_dialog.py")
        self.assertTrue(path.exists(), str(path))

    def test_canonical_static_context_dialog_imports(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.v10_static_context_dialog"
        )
        self.assertIs(module, canonical_static_context_dialog)

    def test_canonical_static_context_dialog_source_avoids_retired_paths(self):
        path = Path("kanda_reasoner_app/reasoner_engine/v10_static_context_dialog.py")
        text = path.read_text(encoding="utf-8", errors="replace")
        self.assertNotIn("ask_ai_project_reasoner.project_reasoner_v10", text)
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10", text)

    def test_static_context_controller_can_import_after_dialog_migration(self):
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.static_context_controller"
        )
        self.assertIsNotNone(module)


if __name__ == "__main__":
    unittest.main()
