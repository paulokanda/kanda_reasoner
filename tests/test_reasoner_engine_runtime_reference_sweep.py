"""Focused tests for the reasoner_engine runtime reference sweep."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

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

LEGACY_ENGINE_REFERENCE_STRINGS = (
    "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window",
    "ask_ai_project_reasoner.project_reasoner_v10.ai_reasoner_main_window",
    "kanda_reasoner_app/project_reasoner_v10/ai_reasoner_main_window",
    "kanda_reasoner_app\\project_reasoner_v10\\ai_reasoner_main_window",
)


class ReasonerEngineRuntimeReferenceSweepTests(unittest.TestCase):
    """Validate that runtime-facing references prefer the canonical engine path."""

    def test_canonical_main_window_and_engine_modules_import(self) -> None:
        modules = (
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window",
            "kanda_reasoner_app.reasoner_engine.reasoner_retriever",
            "kanda_reasoner_app.reasoner_engine.prompt_builder",
            "kanda_reasoner_app.reasoner_engine.index_loader",
        )

        for module_name in modules:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                self.assertIsNotNone(module)

    def test_legacy_packages_remain_available_during_sweep(self) -> None:
        modules = (
            "ask_ai_project_reasoner",
            "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window",
        )

        for module_name in modules:
            with self.subTest(module_name=module_name):
                module = importlib.import_module(module_name)
                self.assertIsNotNone(module)

    def test_runtime_reference_files_do_not_pin_main_window_to_legacy_engine(self) -> None:
        checked_files = []

        for relative_path in RUNTIME_REFERENCE_FILES:
            path = PROJECT_ROOT / relative_path
            if not path.exists():
                continue

            checked_files.append(relative_path)
            text = path.read_text(encoding="utf-8", errors="replace")

            for legacy_string in LEGACY_ENGINE_REFERENCE_STRINGS:
                with self.subTest(path=relative_path, legacy_string=legacy_string):
                    self.assertNotIn(legacy_string, text)

        self.assertGreaterEqual(len(checked_files), 1)

    def test_canonical_main_window_source_prefers_reasoner_engine_paths(self) -> None:
        path = PROJECT_ROOT / "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py"
        self.assertTrue(path.exists(), str(path))

        text = path.read_text(encoding="utf-8", errors="replace")
        self.assertNotIn("kanda_reasoner_app.project_reasoner_v10", text)
        self.assertNotIn("ask_ai_project_reasoner.project_reasoner_v10", text)


if __name__ == "__main__":
    unittest.main()
