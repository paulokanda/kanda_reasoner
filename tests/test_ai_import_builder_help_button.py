"""Regression tests for AI Import Builder GUI-tab deprecation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HELP_CATALOG = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_help" / "ai_import_builder.json"
TOOL_SPECS_PATH = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "tool_specs.py"
WINDOW_PATCHES_PATH = (
    ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "main_window_help"
    / "window_tool_patches.py"
)


class AiImportBuilderDeprecationTests(unittest.TestCase):
    def test_tool_spec_no_longer_registers_ai_import_builder(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        labels = [spec.step_title for spec in TOOLS]
        tab_ids = [spec.tab_id for spec in TOOLS]
        help_catalogs = [spec.help_catalog for spec in TOOLS]

        self.assertNotIn("AI Import Builder", labels)
        self.assertNotIn("ai_import_builder", tab_ids)
        self.assertNotIn("ai_import_builder.json", help_catalogs)

    def test_deprecated_help_catalog_is_not_active(self) -> None:
        self.assertFalse(HELP_CATALOG.exists())

    def test_shell_no_longer_patches_dedicated_splitter_tab(self) -> None:
        text = WINDOW_PATCHES_PATH.read_text(encoding="utf-8")

        self.assertNotIn("_patch_splitter_widget", text)
        self.assertNotIn("_start_split_via_wrapper", text)
        self.assertNotIn("_apply_project_root_to_splitter", text)
        self.assertNotIn("_splitter_widget", text)

    def test_json_splitter_package_is_not_deleted_as_shared_code(self) -> None:
        """The GUI tab is deprecated without deleting shared splitter modules."""

        text = TOOL_SPECS_PATH.read_text(encoding="utf-8")
        self.assertNotIn('step_title="AI Import Builder"', text)

        splitter_package = ROOT / "kanda_reasoner_app" / "json_splitter"
        self.assertTrue(splitter_package.is_dir())
        self.assertTrue((splitter_package / "json_splitter_8.py").is_file())


if __name__ == "__main__":
    unittest.main()
