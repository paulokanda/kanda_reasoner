"""Regression tests for the canonical reasoner_engine AI bridge box."""

from __future__ import annotations

import importlib
from pathlib import Path
import unittest

import kanda_reasoner_app.reasoner_engine.ai_bridge
import kanda_reasoner_app.reasoner_engine.ai_bridge_help.bridge_signals
import kanda_reasoner_app.reasoner_engine.ai_bridge_help.deterministic_answers
import kanda_reasoner_app.reasoner_engine.ai_bridge_help.focus_snippets
import kanda_reasoner_app.reasoner_engine.ai_bridge_help.grounding_checks
import kanda_reasoner_app.reasoner_engine.ai_bridge_help.prompt_extraction
import kanda_reasoner_app.reasoner_engine.ai_bridge_help.prompt_modes

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"


class ReasonerEngineAiBridgeCanonicalMigrationTests(unittest.TestCase):
    def test_canonical_ai_bridge_implementation_files_exist(self) -> None:
        self.assertTrue((CANONICAL_DIR / "ai_bridge.py").is_file())
        self.assertTrue((CANONICAL_DIR / "ai_bridge_help.json").is_file())
        self.assertTrue((CANONICAL_DIR / "ai_bridge_validate_manifests.py").is_file())
        self.assertTrue((CANONICAL_DIR / "ai_bridge_help" / "__init__.py").is_file())
        self.assertTrue((CANONICAL_DIR / "ai_bridge_help" / "bridge_signals.py").is_file())
        self.assertTrue((CANONICAL_DIR / "ai_bridge_help" / "deterministic_answers.py").is_file())

    def test_legacy_ai_bridge_remains_available_during_migration(self) -> None:
        self.assertTrue((LEGACY_DIR / "ai_bridge.py").is_file())
        self.assertTrue((LEGACY_DIR / "ai_bridge_help" / "bridge_signals.py").is_file())

    def test_canonical_and_legacy_ai_bridge_imports_resolve(self) -> None:
        canonical = importlib.import_module("kanda_reasoner_app.reasoner_engine.ai_bridge")
        legacy = importlib.import_module("kanda_reasoner_app.project_reasoner_v10.ai_bridge")
        self.assertEqual(canonical.__name__, "kanda_reasoner_app.reasoner_engine.ai_bridge")
        self.assertEqual(legacy.__name__, "kanda_reasoner_app.project_reasoner_v10.ai_bridge")
        self.assertTrue(hasattr(canonical, "LocalAIReasoner"))
        self.assertTrue(hasattr(legacy, "LocalAIReasoner"))

    def test_canonical_ai_bridge_uses_reasoner_engine_imports(self) -> None:
        source = (CANONICAL_DIR / "ai_bridge.py").read_text(encoding="utf-8")
        self.assertIn("kanda_reasoner_app.reasoner_engine.ai_bridge_help", source)
        self.assertIn("kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models", source)
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10.ai_bridge_help", source)

    def test_canonical_ai_bridge_helpers_import_through_public_contracts(self) -> None:
        module_names = [
            "bridge_signals",
            "deterministic_answer_core",
            "deterministic_answer_core_parts",
            "deterministic_answer_parts",
            "deterministic_answers",
            "focus_snippets",
            "grounding_checks",
            "prompt_extraction",
            "prompt_modes",
        ]
        for module_name in module_names:
            with self.subTest(module_name=module_name):
                imported = importlib.import_module(
                    "kanda_reasoner_app.reasoner_engine.ai_bridge_help." + module_name
                )
                self.assertTrue(hasattr(imported, "__all__"))


if __name__ == "__main__":
    unittest.main()
