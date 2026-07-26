"""Regression tests for Refactor Report help-button wiring."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_tools_gui_shell.gui_support import _format_help_catalog_text
from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS


HELP_CATALOG = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_help" / "refactor_report.json"


class RefactorReportHelpButtonTests(unittest.TestCase):
    def test_tool_spec_registers_help_catalog(self) -> None:
        spec = next(item for item in TOOLS if item.tab_id == "refactor_report")

        self.assertEqual(spec.step_title, "Refactor Report")
        self.assertEqual(spec.help_catalog, "refactor_report.json")

    def test_help_catalog_exists_and_formats_useful_text(self) -> None:
        payload = json.loads(HELP_CATALOG.read_text(encoding="utf-8"))
        formatted = _format_help_catalog_text(HELP_CATALOG)

        self.assertEqual(payload["tab"], "Refactor Report")
        self.assertIn("Refactor Report", formatted)
        self.assertIn("Mode A", formatted)
        self.assertIn("Compile State Vector", formatted)
        self.assertIn("Save Bundle Now", formatted)
        self.assertGreaterEqual(len(payload["display_lines"]), 6)
        self.assertGreaterEqual(len(payload["errors"]), 6)


if __name__ == "__main__":
    unittest.main()
