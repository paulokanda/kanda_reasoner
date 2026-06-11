"""Read-only deletion-readiness audit for project_reasoner_v10.

This audit supports the final target of deleting the transitional legacy
engine folder after all runtime dependencies have been moved to
kanda_reasoner_app.reasoner_engine.
"""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ENGINE = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_ENGINE = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"
TOP_LEVEL_LEGACY = PROJECT_ROOT / "ask_ai_project_reasoner"

CANONICAL_MODULES = (
    "kanda_reasoner_app.reasoner_engine.ai_bridge",
    "kanda_reasoner_app.reasoner_engine.help_index",
    "kanda_reasoner_app.reasoner_engine.index_loader",
    "kanda_reasoner_app.reasoner_engine.project_profile",
    "kanda_reasoner_app.reasoner_engine.prompt_builder",
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever",
    "kanda_reasoner_app.reasoner_engine.query_router",
    "kanda_reasoner_app.reasoner_engine.v10_conversation_memory",
    "kanda_reasoner_app.reasoner_engine.v10_intent_detection",
    "kanda_reasoner_app.reasoner_engine.v10_model_registry",
    "kanda_reasoner_app.reasoner_engine.v10_models",
    "kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models",
    "kanda_reasoner_app.reasoner_engine.v10_scoring_config",
    "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window",
)

RUNTIME_FILES = (
    "reasoner_tools_gui.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/gui_support.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/tab_specs.py",
    "kanda_reasoner_app/reasoner_context_collector/runner.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner.py",
    "kanda_reasoner_app/manage_architecture/ai_review/adapter.py",
    "kanda_reasoner_app/manage_workflows/ai_review/adapter.py",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_reader_ai_contract_detectors.py",
)

LEGACY_RUNTIME_PATTERNS = (
    "kanda_reasoner_app.project_reasoner_v10.",
    "ask_ai_project_reasoner.project_reasoner_v10.",
    "kanda_reasoner_app/project_reasoner_v10",
    "kanda_reasoner_app\\project_reasoner_v10",
    "ask_ai_project_reasoner/project_reasoner_v10",
    "ask_ai_project_reasoner\\project_reasoner_v10",
)

EXPECTED_DELETE_TARGETS = (
    "ask_ai_project_reasoner",
    "kanda_reasoner_app/project_reasoner_v10",
)


class ProjectReasonerV10DeletionReadinessAuditTests(unittest.TestCase):
    """Read-only audit before deleting project_reasoner_v10."""

    def test_final_delete_targets_are_recorded(self):
        self.assertIn("ask_ai_project_reasoner", EXPECTED_DELETE_TARGETS)
        self.assertIn("kanda_reasoner_app/project_reasoner_v10", EXPECTED_DELETE_TARGETS)

    def test_canonical_reasoner_engine_modules_import(self):
        for module_name in CANONICAL_MODULES:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                self.assertIsNotNone(module)

    def test_canonical_engine_manifest_artifacts_are_present(self):
        expected = (
            CANONICAL_ENGINE / "ai_reasoner_main_window.py",
            CANONICAL_ENGINE / "ai_reasoner_main_window_help.json",
            CANONICAL_ENGINE / "ai_reasoner_main_window_validate_manifests.py",
            CANONICAL_ENGINE / "ai_reasoner_main_window_help",
        )
        for path in expected:
            with self.subTest(path=str(path)):
                self.assertTrue(path.exists(), str(path))

    def test_transitional_legacy_roots_still_exist_before_deletion(self):
        self.assertTrue(LEGACY_ENGINE.exists(), str(LEGACY_ENGINE))
        self.assertTrue(TOP_LEVEL_LEGACY.exists(), str(TOP_LEVEL_LEGACY))

    def test_transitional_legacy_imports_still_work_before_deletion(self):
        legacy_modules = (
            "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window",
            "ask_ai_project_reasoner",
        )
        for module_name in legacy_modules:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                self.assertIsNotNone(module)

    def test_runtime_entry_files_do_not_pin_to_project_reasoner_v10(self):
        offenders = []
        for relative_path in RUNTIME_FILES:
            path = PROJECT_ROOT / relative_path
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in LEGACY_RUNTIME_PATTERNS:
                if pattern in text:
                    offenders.append(f"{relative_path}: {pattern}")
        self.assertEqual([], offenders)

    def test_canonical_main_window_manifest_validator_passes(self):
        validator = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_validate_manifests"
        )
        validate = getattr(validator, "main", None)
        if callable(validate):
            result = validate()
            self.assertIn(result, (None, 0))


if __name__ == "__main__":
    unittest.main()
