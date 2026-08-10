# project-path: tests/test_engineering_diagnostics_wave2v_gui_scale.py
"""GUI projection and physical contracts retained from Wave 2V."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py"
SONAR = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_sonar.py"
HOST = ROOT / "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py"
WORKSPACE = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py"


class EngineeringDiagnosticsWave2VGuiScaleTests(unittest.TestCase):
    def test_touched_product_modules_remain_below_500_lines(self) -> None:
        for path in (PANEL, SONAR, HOST, WORKSPACE):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 500)

    def test_pontual_run_console_keeps_single_worker_executor(self) -> None:
        text = PANEL.read_text(encoding="utf-8")
        self.assertEqual(text.count("ThreadPoolExecutor(max_workers=1)"), 1)
        self.assertEqual(text.count("executor.submit("), 1)


if __name__ == "__main__":
    unittest.main()
