# project-path: tests/test_engineering_diagnostics_wave2w_gui_scale.py
"""Physical and scale contracts for the Wave 2W hierarchy."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATHS = (
    ROOT / "reasoner_tools_gui_engineering_safety_panel.py",
    ROOT / "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
    ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py",
    ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/full_engineering_diagnostics_tab.py",
)


class EngineeringDiagnosticsWave2WGuiScaleTests(unittest.TestCase):
    def test_touched_product_modules_remain_below_500_lines(self) -> None:
        for path in PATHS:
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 500)

    def test_full_diagnostics_has_one_executor_and_one_submission(self) -> None:
        text = PATHS[-1].read_text(encoding="utf-8")
        self.assertEqual(text.count("ThreadPoolExecutor(max_workers=1)"), 1)
        self.assertEqual(text.count("executor.submit("), 1)

    def test_workspace_does_not_create_a_second_store_or_database(self) -> None:
        joined = "\n".join(path.read_text(encoding="utf-8") for path in PATHS[1:])
        self.assertNotIn("EngineeringDiagnosticsStore(", joined)
        self.assertNotIn("sqlite3", joined)
        self.assertNotIn("project_engineering_diagnostics", joined)


if __name__ == "__main__":
    unittest.main()
