"""Regression tests for canonical reasoner_engine help_index migration."""

from __future__ import annotations

import importlib
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"


class ReasonerEngineHelpIndexCanonicalMigrationTests(unittest.TestCase):
    def test_canonical_help_index_implementation_files_exist(self) -> None:
        self.assertTrue((CANONICAL_DIR / "help_index.py").is_file())
        self.assertTrue((CANONICAL_DIR / "help_index_help.json").is_file())
        self.assertTrue((CANONICAL_DIR / "help_index_validate_manifests.py").is_file())
        self.assertTrue((CANONICAL_DIR / "help_index_help" / "__init__.py").is_file())
        self.assertTrue((CANONICAL_DIR / "help_index_help" / "help_index_data.py").is_file())
        self.assertTrue((CANONICAL_DIR / "help_index_help" / "help_index_raw.py").is_file())
        self.assertTrue(
            (
                CANONICAL_DIR
                / "help_index_help"
                / "help_index_raw_parts"
                / "raw_part_1_private_impl.py"
            ).is_file()
        )

    def test_legacy_help_index_remains_available_during_migration(self) -> None:
        self.assertTrue((LEGACY_DIR / "help_index.py").is_file())
        self.assertTrue((LEGACY_DIR / "help_index_help" / "help_index_data.py").is_file())
        self.assertTrue((LEGACY_DIR / "ai_bridge.py").is_file())

    def test_canonical_and_legacy_help_index_imports_resolve_same_payload(self) -> None:
        canonical = importlib.import_module("kanda_reasoner_app.reasoner_engine.help_index")
        legacy = importlib.import_module("kanda_reasoner_app.project_reasoner_v10.help_index")
        self.assertEqual(canonical.__name__, "kanda_reasoner_app.reasoner_engine.help_index")
        self.assertEqual(legacy.__name__, "kanda_reasoner_app.project_reasoner_v10.help_index")
        self.assertTrue(hasattr(canonical, "HELP_INDEX"))
        self.assertEqual(canonical.HELP_INDEX, legacy.HELP_INDEX)

    def test_canonical_help_index_uses_reasoner_engine_manifest_paths(self) -> None:
        manifest = (CANONICAL_DIR / "help_index_help.json").read_text(encoding="utf-8")
        self.assertIn("kanda_reasoner_app/reasoner_engine/help_index.py", manifest)
        self.assertIn("kanda_reasoner_app/reasoner_engine/help_index_help", manifest)
        self.assertNotIn("kanda_reasoner_app/project_reasoner_v10/help_index.py", manifest)

    def test_canonical_help_index_helpers_import_through_public_contracts(self) -> None:
        module_names = [
            "help_index_data",
            "help_index_normalization",
            "help_index_raw",
            "help_index_raw_parts.raw_part_1_private_impl",
            "help_index_raw_parts.raw_part_2_private_impl",
        ]
        for module_name in module_names:
            with self.subTest(module_name=module_name):
                imported = importlib.import_module(
                    "kanda_reasoner_app.reasoner_engine.help_index_help." + module_name
                )
                self.assertTrue(hasattr(imported, "__all__"))


if __name__ == "__main__":
    unittest.main()
