"Focused tests for GUI tab specs after project_reasoner_v10 deletion."

from __future__ import annotations

import importlib
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GUI_SPEC_FILES = (
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "tool_specs.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "tab_specs.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "gui_support.py",
    PROJECT_ROOT / "reasoner_tools_gui.py",
)

RETIRED_MAIN_WINDOW_CANDIDATES = (
    "kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window",
    "ask_ai_project_reasoner.project_reasoner_v10.ai_reasoner_main_window",
)

CANONICAL_MAIN_WINDOW = "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"


class GuiTabSpecsAfterProjectReasonerV10DeletionRepairTests(unittest.TestCase):
    def test_project_reasoner_v10_folder_is_absent(self):
        retired_dir = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"
        self.assertFalse(retired_dir.exists(), str(retired_dir))

    def test_canonical_main_window_imports(self):
        module = importlib.import_module(CANONICAL_MAIN_WINDOW)
        self.assertIsNotNone(module)

    def test_gui_spec_files_do_not_reference_retired_main_window_candidate(self):
        offenders = []

        for path in GUI_SPEC_FILES:
            if not path.exists():
                continue

            text = path.read_text(encoding="utf-8", errors="replace")
            for retired_candidate in RETIRED_MAIN_WINDOW_CANDIDATES:
                if retired_candidate in text:
                    offenders.append(str(path.relative_to(PROJECT_ROOT)))

        self.assertEqual([], sorted(set(offenders)))

    def test_gui_spec_files_do_not_reference_top_level_main_window_candidate(self):
        offenders = []

        for path in GUI_SPEC_FILES:
            if not path.exists():
                continue

            text = path.read_text(encoding="utf-8", errors="replace")
            if '"ai_reasoner_main_window"' in text or "'ai_reasoner_main_window'" in text:
                offenders.append(str(path.relative_to(PROJECT_ROOT)))

        self.assertEqual([], sorted(set(offenders)))

    def test_gui_spec_files_prefer_canonical_main_window_candidate(self):
        combined = ""

        for path in GUI_SPEC_FILES:
            if path.exists():
                combined += path.read_text(encoding="utf-8", errors="replace")

        self.assertIn(CANONICAL_MAIN_WINDOW, combined)

    def test_gui_support_first_imports_canonical_main_window(self):
        support_module = importlib.import_module(
            "kanda_reasoner_app.reasoner_tools_gui_shell.gui_support"
        )
        first_imported_module = getattr(support_module, "_first_imported_module")
        module = first_imported_module([CANONICAL_MAIN_WINDOW])
        self.assertEqual(CANONICAL_MAIN_WINDOW, module.__name__)


if __name__ == "__main__":
    unittest.main()
