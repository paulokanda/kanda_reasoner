"""Regression tests for the reasoner_engine index_loader migration gate."""

from __future__ import annotations

import importlib
import pathlib
import unittest


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"

# Direct imports are intentional. They give the architecture validator direct
# test protection evidence for the canonical index_loader owner box.
import kanda_reasoner_app.reasoner_engine.index_loader as canonical_index_loader
import kanda_reasoner_app.reasoner_engine.index_loader_help.index_builders as canonical_index_builders
import kanda_reasoner_app.reasoner_engine.index_loader_help.path_resolution as canonical_path_resolution
import kanda_reasoner_app.reasoner_engine.index_loader_help.section_loading as canonical_section_loading
import kanda_reasoner_app.reasoner_engine.index_loader_help.state_init as canonical_state_init


class ReasonerEngineIndexLoaderCanonicalMigrationTests(unittest.TestCase):
    """Validate canonical index_loader imports and legacy availability."""

    def test_canonical_index_loader_implementation_files_exist(self) -> None:
        expected_files = [
            CANONICAL_DIR / "index_loader.py",
            CANONICAL_DIR / "index_loader_help.json",
            CANONICAL_DIR / "index_loader_help" / "__init__.py",
            CANONICAL_DIR / "index_loader_help" / "index_builders.py",
            CANONICAL_DIR / "index_loader_help" / "path_resolution.py",
            CANONICAL_DIR / "index_loader_help" / "section_loading.py",
            CANONICAL_DIR / "index_loader_help" / "state_init.py",
        ]
        missing = [str(path) for path in expected_files if not path.is_file()]
        self.assertEqual([], missing)

    def test_legacy_index_loader_remains_available_during_migration(self) -> None:
        self.assertTrue((LEGACY_DIR / "index_loader.py").is_file())
        legacy = importlib.import_module("kanda_reasoner_app.project_reasoner_v10.index_loader")
        self.assertTrue(hasattr(legacy, "JsonProjectIndex"))

    def test_canonical_and_legacy_index_loader_imports_resolve(self) -> None:
        legacy = importlib.import_module("kanda_reasoner_app.project_reasoner_v10.index_loader")
        self.assertTrue(hasattr(canonical_index_loader, "JsonProjectIndex"))
        self.assertTrue(hasattr(legacy, "JsonProjectIndex"))

    def test_canonical_index_loader_helpers_import_through_public_contracts(self) -> None:
        self.assertTrue(hasattr(canonical_index_builders, "build_boundary_indexes"))
        self.assertTrue(hasattr(canonical_index_builders, "build_core_file_and_symbol_indexes"))
        self.assertTrue(hasattr(canonical_path_resolution, "resolve_runtime_source_file"))
        self.assertTrue(hasattr(canonical_section_loading, "load_full_sections"))
        self.assertTrue(hasattr(canonical_state_init, "initialize_index_state"))

    def test_canonical_index_loader_uses_reasoner_engine_manifest_paths(self) -> None:
        manifest_path = CANONICAL_DIR / "index_loader_help.json"
        manifest_text = manifest_path.read_text(encoding="utf-8")
        self.assertIn("reasoner_engine", manifest_text)
        self.assertNotIn("project_reasoner_v10/index_loader", manifest_text)
        self.assertNotIn("project_reasoner_v10\\\\index_loader", manifest_text)


if __name__ == "__main__":
    unittest.main()
