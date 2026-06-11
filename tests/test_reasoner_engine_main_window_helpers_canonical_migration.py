"""Focused tests for canonical main window helper migration."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class ReasonerEngineMainWindowHelpersCanonicalMigrationTests(unittest.TestCase):
    def test_canonical_helper_folder_exists(self):
        root = Path('kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help')
        self.assertTrue(root.exists(), str(root))

    def test_legacy_gui_window_still_imports(self):
        module = importlib.import_module('kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window')
        self.assertIsNotNone(module)

    def test_canonical_helper_package_imports(self):
        module = importlib.import_module('kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help')
        self.assertIsNotNone(module)


if __name__ == '__main__':
    unittest.main()