"""Focused tests for canonical main window helper manifest artifacts."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


class ReasonerEngineMainWindowManifestContractTests(unittest.TestCase):
    def test_manifest_artifacts_exist(self) -> None:
        root = Path("kanda_reasoner_app/reasoner_engine")
        self.assertTrue((root / "ai_reasoner_main_window_help.json").exists())
        self.assertTrue((root / "ai_reasoner_main_window_validate_manifests.py").exists())

    def test_validator_imports_and_passes(self) -> None:
        validator = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_validate_manifests"
        )
        self.assertEqual(validator.main(), 0)

    def test_manifest_points_to_canonical_paths(self) -> None:
        text = Path(
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help.json"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py", text)
        self.assertIn("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help", text)
        self.assertNotIn("kanda_reasoner_app/project_reasoner_v10/main_window_help", text)


if __name__ == "__main__":
    unittest.main()
