from __future__ import annotations

import importlib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ReasonerEngineCanonicalFacadeTests(unittest.TestCase):
    def test_reasoner_engine_facade_resolves_legacy_public_api(self) -> None:
        canonical = importlib.import_module("kanda_reasoner_app.reasoner_engine")
        legacy = importlib.import_module("kanda_reasoner_app.project_reasoner_v10")

        self.assertEqual(canonical.__all__, legacy.__all__)
        self.assertIn("ProjectRetriever", canonical.__all__)

    def test_canonical_submodule_imports_work(self) -> None:
        registry = importlib.import_module("kanda_reasoner_app.reasoner_engine.v10_model_registry")
        models = importlib.import_module("kanda_reasoner_app.reasoner_engine.v10_models")

        self.assertTrue(hasattr(registry, "LocalModelRegistry"))
        self.assertTrue(hasattr(models, "EvidenceItem"))

    def test_legacy_implementation_folder_remains_available_during_migration(self) -> None:
        legacy_dir = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"
        canonical_dir = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"

        self.assertTrue((legacy_dir / "ai_bridge.py").is_file())
        self.assertTrue((canonical_dir / "__init__.py").is_file())
        self.assertTrue((canonical_dir / "__main__.py").is_file())
        self.assertTrue((canonical_dir / "ai_bridge.py").is_file())

    def test_ai_review_adapters_use_canonical_reasoner_engine_path(self) -> None:
        checked_files = [
            PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "ai_review" / "adapter.py",
            PROJECT_ROOT / "kanda_reasoner_app" / "manage_workflows" / "ai_review" / "adapter.py",
        ]

        for path in checked_files:
            text = path.read_text(encoding="utf-8")
            self.assertIn("kanda_reasoner_app.reasoner_engine", text)
            self.assertNotIn("kanda_reasoner_app.project_reasoner_v10", text)
            self.assertNotIn("ask_ai_project_reasoner", text)


if __name__ == "__main__":
    unittest.main()
