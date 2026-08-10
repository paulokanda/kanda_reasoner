# project-path: tests/test_engineering_diagnostics_wave2v.py
"""Corrective contracts for the Wave 2V run console after hierarchy split."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOST = ROOT / "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py"
PANEL = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py"
SONAR = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_sonar.py"
WORKSPACE = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py"


class EngineeringDiagnosticsWave2VTests(unittest.TestCase):
    def test_diagnostics_remains_nested_in_engineering_safety(self) -> None:
        text = HOST.read_text(encoding="utf-8")
        self.assertIn('"engineering_safety_section_tabs"', text)
        self.assertIn("section_tabs.addTab(workspace", text)
        self.assertNotIn(
            "tab_widget.addTab(\n        window._engineering_diagnostics_page",
            text,
        )

    def test_pontual_diagnostics_retains_wave2v_run_and_cancel_controls(self) -> None:
        text = PANEL.read_text(encoding="utf-8")
        self.assertIn('QPushButton("Run Engineering Diagnostics")', text)
        self.assertIn('setObjectName("engineering_diagnostics_run_button")', text)
        self.assertIn('QPushButton("Cancel Diagnostics")', text)
        self.assertIn('setObjectName("engineering_diagnostics_cancel_button")', text)

    def test_pontual_diagnostics_sonar_contract_is_preserved(self) -> None:
        text = PANEL.read_text(encoding="utf-8")
        self.assertIn("sonar.start(producer_label())", text)
        self.assertGreaterEqual(text.count("sonar.stop()"), 2)
        self.assertIn("panel.engineering_diagnostics_sonar = sonar", text)

    def test_sonar_uses_public_template_without_private_reach_in(self) -> None:
        text = SONAR.read_text(encoding="utf-8")
        self.assertIn("GreenSonarActivityMonitor", text)
        self.assertIn('title="Engineering Diagnostics"', text)
        self.assertNotIn("widget().setObjectName", text)
        self.assertNotIn("_green_sonar", text)

    def test_public_run_and_cancel_projection_exists(self) -> None:
        text = PANEL.read_text(encoding="utf-8")
        self.assertIn("panel.start_engineering_diagnostics = start_scan", text)
        self.assertIn("panel.cancel_engineering_diagnostics = cancel_scan", text)
        self.assertIn("panel.engineering_diagnostics_run_button = run_button", text)
        self.assertIn("panel.engineering_diagnostics_cancel_button = cancel_button", text)

    def test_cancel_waits_for_worker_settlement_before_reenabling_run(self) -> None:
        text = PANEL.read_text(encoding="utf-8")
        start = text.index("    def cancel_scan() -> None:")
        end = text.index("    def activate_baseline() -> None:", start)
        block = text[start:end]
        self.assertIn("cancellation.set()", block)
        self.assertIn("sonar.stop()", block)
        self.assertIn("cancel_button.setEnabled(False)", block)
        self.assertNotIn('state["future"] = None', block)
        self.assertNotIn("set_busy(False)", block)

    def test_full_audit_drillthrough_targets_pontual_diagnostics(self) -> None:
        text = HOST.read_text(encoding="utf-8")
        self.assertIn("section_tabs.setCurrentWidget(workspace)", text)
        self.assertIn("workspace.select_pontual_engineering_diagnostics()", text)
        self.assertIn("select_diagnostics_tab=select_diagnostics_tab", text)

    def test_workspace_keeps_one_shared_controller(self) -> None:
        text = WORKSPACE.read_text(encoding="utf-8")
        self.assertEqual(text.count("EngineeringDiagnosticsController("), 1)
        self.assertEqual(text.count("controller=active_controller"), 2)

    def test_no_full_audit_or_pontual_private_reach_in(self) -> None:
        for path in (HOST, PANEL, SONAR, WORKSPACE):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports: list[str] = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
                elif isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
            joined = "\n".join(imports)
            self.assertNotIn("_reasoner_tools_gui_engineering_safety_full_audit", joined)
            self.assertNotIn("engineering_safety_pontual", joined)


if __name__ == "__main__":
    unittest.main()
