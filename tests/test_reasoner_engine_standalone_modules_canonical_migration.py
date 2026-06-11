"""Regression tests for canonical reasoner_engine standalone modules."""

from pathlib import Path
import unittest

import kanda_reasoner_app.reasoner_engine.query_router as canonical_query_router
import kanda_reasoner_app.reasoner_engine.v10_conversation_memory as canonical_v10_conversation_memory
import kanda_reasoner_app.reasoner_engine.v10_intent_detection as canonical_v10_intent_detection
import kanda_reasoner_app.reasoner_engine.v10_model_registry as canonical_v10_model_registry
import kanda_reasoner_app.reasoner_engine.v10_models as canonical_v10_models
import kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models as canonical_v10_qwen_ai_models
import kanda_reasoner_app.reasoner_engine.v10_scoring_config as canonical_v10_scoring_config
import kanda_reasoner_app.project_reasoner_v10.query_router as legacy_query_router
import kanda_reasoner_app.project_reasoner_v10.v10_conversation_memory as legacy_v10_conversation_memory
import kanda_reasoner_app.project_reasoner_v10.v10_intent_detection as legacy_v10_intent_detection
import kanda_reasoner_app.project_reasoner_v10.v10_model_registry as legacy_v10_model_registry
import kanda_reasoner_app.project_reasoner_v10.v10_models as legacy_v10_models
import kanda_reasoner_app.project_reasoner_v10.v10_qwen_ai_models as legacy_v10_qwen_ai_models
import kanda_reasoner_app.project_reasoner_v10.v10_scoring_config as legacy_v10_scoring_config


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"

STANDALONE_MODULES = (
    "query_router",
    "v10_conversation_memory",
    "v10_intent_detection",
    "v10_model_registry",
    "v10_models",
    "v10_qwen_ai_models",
    "v10_scoring_config",
)

CANONICAL_MODULES = (
    canonical_query_router,
    canonical_v10_conversation_memory,
    canonical_v10_intent_detection,
    canonical_v10_model_registry,
    canonical_v10_models,
    canonical_v10_qwen_ai_models,
    canonical_v10_scoring_config,
)

LEGACY_MODULES = (
    legacy_query_router,
    legacy_v10_conversation_memory,
    legacy_v10_intent_detection,
    legacy_v10_model_registry,
    legacy_v10_models,
    legacy_v10_qwen_ai_models,
    legacy_v10_scoring_config,
)


class ReasonerEngineStandaloneModulesCanonicalMigrationTests(unittest.TestCase):
    """Validate the standalone module migration gate."""

    def test_canonical_standalone_files_exist(self):
        for module_name in STANDALONE_MODULES:
            canonical_path = CANONICAL_ROOT / f"{module_name}.py"
            with self.subTest(module=module_name):
                self.assertTrue(canonical_path.exists(), canonical_path)

    def test_legacy_standalone_files_remain_available(self):
        for module_name in STANDALONE_MODULES:
            legacy_path = LEGACY_ROOT / f"{module_name}.py"
            with self.subTest(module=module_name):
                self.assertTrue(legacy_path.exists(), legacy_path)

    def test_canonical_imports_resolve_from_reasoner_engine(self):
        for module in CANONICAL_MODULES:
            with self.subTest(module=module.__name__):
                self.assertIn("kanda_reasoner_app.reasoner_engine", module.__name__)
                self.assertIn("reasoner_engine", str(Path(module.__file__)))

    def test_legacy_imports_remain_available_during_migration(self):
        for module in LEGACY_MODULES:
            with self.subTest(module=module.__name__):
                self.assertIn("kanda_reasoner_app.project_reasoner_v10", module.__name__)
                self.assertIn("project_reasoner_v10", str(Path(module.__file__)))

    def test_canonical_files_do_not_use_legacy_package_imports(self):
        forbidden_markers = (
            "ask_ai_project_reasoner.project_reasoner_v10",
            "kanda_reasoner_app.project_reasoner_v10",
            "kanda_reasoner_app/project_reasoner_v10",
            "kanda_reasoner_app\\project_reasoner_v10",
        )
        for module_name in STANDALONE_MODULES:
            canonical_path = CANONICAL_ROOT / f"{module_name}.py"
            text = canonical_path.read_text(encoding="utf-8")
            with self.subTest(module=module_name):
                for marker in forbidden_markers:
                    self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()
