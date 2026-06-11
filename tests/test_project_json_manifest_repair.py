"""Focused regression test for repaired JSON manifests."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

JSON_PATHS = (
    "workflow_manifest.json",
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/box_manifest.json",
    "kanda_reasoner_app/daily_rfctr_report/daily_refactor_report_help.json",
    "kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help.json",
    "kanda_reasoner_app/insert_missing_docstrings_gui/context_builder_help.json",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json",
    "kanda_reasoner_app/json_splitter/json_splitter_8_help.json",
    "kanda_reasoner_app/json_splitter/json_splitter_split_reassemble_validation_help.json",
    "kanda_reasoner_app/manage_architecture/manage_architecture_gui_help.json",
    "kanda_reasoner_app/manage_architecture/manage_architecture_help.json",
    "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help.json",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help.json",
    "kanda_reasoner_app/reasoner_context_collector/collector_main_help.json",
    "kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap_help.json",
    "kanda_reasoner_app/reasoner_context_collector/collector_runtime_scenarios_help.json",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help.json",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help.json",
    "kanda_reasoner_app/reasoner_engine/ai_bridge_help.json",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help.json",
    "kanda_reasoner_app/reasoner_engine/help_index_help.json",
    "kanda_reasoner_app/reasoner_engine/index_loader_help.json",
    "kanda_reasoner_app/reasoner_engine/project_profile_help.json",
    "kanda_reasoner_app/reasoner_engine/prompt_builder_help.json",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help.json",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval_help.json",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/snippet_retrieval_help.json",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help.json",
    "kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab_help.json",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help.json",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help.json",
)


class ProjectJsonManifestRepairTests(unittest.TestCase):
    """Ensure repaired helper manifests and workflow manifest parse as JSON."""

    def test_repaired_json_manifests_are_nonempty_and_parseable(self) -> None:
        for rel_path in JSON_PATHS:
            with self.subTest(path=rel_path):
                path = PROJECT_ROOT / rel_path
                text = path.read_text(encoding="utf-8-sig")
                self.assertTrue(text.strip(), rel_path)
                parsed = json.loads(text)
                self.assertIsInstance(parsed, dict)


if __name__ == "__main__":
    unittest.main()
