"""Final compatibility audit aligned with planned legacy-root deletion.

This audit is intentionally transitional. It verifies that canonical
reasoner_engine imports are healthy, that current legacy compatibility
imports still work before deletion, and that tests no longer require the
legacy engine file to contain the full source implementation.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path


class ReasonerEngineFinalCompatibilityAuditTests(unittest.TestCase):
    """Read-only audit for the final reasoner_engine migration phase."""

    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    FINAL_DELETE_TARGETS = (
        "ask_ai_project_reasoner",
        "kanda_reasoner_app/project_reasoner_v10",
    )

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

    RUNTIME_REFERENCE_FILES = (
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

    def test_final_delete_targets_are_documented(self) -> None:
        """The audit records the user's requested final deletion targets."""
        self.assertIn("ask_ai_project_reasoner", self.FINAL_DELETE_TARGETS)
        self.assertIn(
            "kanda_reasoner_app/project_reasoner_v10",
            self.FINAL_DELETE_TARGETS,
        )

    def test_canonical_reasoner_engine_modules_import(self) -> None:
        """All migrated canonical engine modules must import successfully."""
        for module_name in self.CANONICAL_MODULES:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                self.assertIsNotNone(module)

    def test_canonical_main_window_artifacts_exist(self) -> None:
        """The canonical GUI module and helper manifest contract must exist."""
        required_paths = (
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py",
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help",
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help.json",
            "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_validate_manifests.py",
        )

        for relative_path in required_paths:
            with self.subTest(relative_path=relative_path):
                path = self.PROJECT_ROOT / relative_path
                self.assertTrue(path.exists(), str(path))

    def test_canonical_main_window_manifest_validator_passes(self) -> None:
        """The canonical main window manifest validator must return success."""
        validator = (
            self.PROJECT_ROOT
            / "kanda_reasoner_app"
            / "reasoner_engine"
            / "ai_reasoner_main_window_validate_manifests.py"
        )
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=str(self.PROJECT_ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_transitional_legacy_imports_remain_available_before_deletion(self) -> None:
        """Legacy roots may be facades now, but must import until deleted."""
        legacy_modules = (
            "ask_ai_project_reasoner",
            "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window",
        )

        for module_name in legacy_modules:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                self.assertIsNotNone(module)

    def test_legacy_main_window_no_longer_needs_real_source_body(self) -> None:
        """A compatibility facade is acceptable before final deletion."""
        path = (
            self.PROJECT_ROOT
            / "kanda_reasoner_app"
            / "project_reasoner_v10"
            / "ai_reasoner_main_window.py"
        )
        self.assertTrue(path.exists(), str(path))
        text = path.read_text(encoding="utf-8", errors="replace")
        self.assertTrue(
            "JsonProjectReasonerV10" in text or "load_payload" in text,
            "legacy main_window must be either real source or a compatibility facade",
        )

    def test_runtime_files_do_not_hard_pin_gui_to_legacy_engine(self) -> None:
        """Runtime entry files should not hard-pin the GUI to legacy paths."""
        forbidden_tokens = (
            "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window",
            "ask_ai_project_reasoner.project_reasoner_v10.ai_reasoner_main_window",
        )

        for relative_path in self.RUNTIME_REFERENCE_FILES:
            path = self.PROJECT_ROOT / relative_path
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in forbidden_tokens:
                with self.subTest(relative_path=relative_path, token=token):
                    self.assertNotIn(token, text)

    def test_gui_shell_still_imports(self) -> None:
        """The GUI shell entry point should still import without side effects."""
        module = importlib.import_module("reasoner_tools_gui")
        self.assertIsNotNone(module)


if __name__ == "__main__":
    unittest.main()
