"""Focused tests for canonical GUI-facing main window migration."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class ReasonerEngineMainWindowGuiCanonicalMigrationTests(unittest.TestCase):
    """Protect the canonical GUI-facing main window migration."""

    def test_canonical_and_legacy_main_window_files_exist(self):
        canonical_path = Path("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py")
        legacy_path = Path("kanda_reasoner_app/project_reasoner_v10/ai_reasoner_main_window.py")
        self.assertTrue(canonical_path.exists(), str(canonical_path))
        self.assertTrue(legacy_path.exists(), str(legacy_path))

    def test_canonical_and_legacy_main_window_imports_resolve(self):
        canonical = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
        )
        legacy = importlib.import_module(
            "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window"
        )
        self.assertIsNotNone(canonical)
        self.assertIsNotNone(legacy)

    def test_canonical_helpers_and_manifest_artifacts_import(self):
        helpers = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help"
        )
        validator = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_validate_manifests"
        )
        self.assertIsNotNone(helpers)
        self.assertIsNotNone(validator)

    def test_canonical_source_prefers_reasoner_engine_paths(self):
        canonical_path = Path("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py")
        text = canonical_path.read_text(encoding="utf-8")
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10", text)
        self.assertNotIn("ask_ai_project_reasoner.project_reasoner_v10", text)
        self.assertNotIn("kanda_reasoner_app/project_reasoner_v10", text)
        self.assertNotIn("kanda_reasoner_app\\project_reasoner_v10", text)

    def test_legacy_file_remains_real_during_migration(self):
        legacy_path = Path("kanda_reasoner_app/project_reasoner_v10/ai_reasoner_main_window.py")
        text = legacy_path.read_text(encoding="utf-8")
        self.assertGreater(len(text), 100)


if __name__ == "__main__":
    unittest.main()
