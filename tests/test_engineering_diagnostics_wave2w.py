# project-path: tests/test_engineering_diagnostics_wave2w.py
"""Core contracts for the Engineering Safety two-level hierarchy Wave 2W."""

from __future__ import annotations

import ast
from pathlib import Path
from threading import Event
import unittest

from kanda_reasoner_app.engineering_diagnostics_gui.full_engineering_diagnostics_tab import (
    FULL_ENGINEERING_DIAGNOSTIC_COLLECTORS,
    collect_full_engineering_diagnostics_candidates,
)
from kanda_reasoner_app.engineering_diagnostics_gui.models import (
    EngineeringDiagnosticsGuiCancelled,
)

ROOT = Path(__file__).resolve().parents[1]
SAFETY = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
HOST = ROOT / "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py"
WORKSPACE = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py"
FULL = ROOT / "kanda_reasoner_app/engineering_diagnostics_gui/full_engineering_diagnostics_tab.py"


class _CandidateController:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def _candidate(self, label: str, _root: str, _generation: int, cancellation: Event):
        if cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled("cancelled")
        self.calls.append(label)
        return object()

    def collect_bom_candidate(self, *args):
        return self._candidate("BOM", *args)

    def collect_ruff_candidate(self, *args):
        return self._candidate("Ruff", *args)

    def collect_architecture_candidate(self, *args):
        return self._candidate("Architecture", *args)

    def collect_shadow_candidate(self, *args):
        return self._candidate("Shadow", *args)


class EngineeringDiagnosticsWave2WTests(unittest.TestCase):
    def test_engineering_safety_has_two_top_level_sections(self) -> None:
        text = SAFETY.read_text(encoding="utf-8")
        self.assertIn('setObjectName("engineering_safety_section_tabs")', text)
        self.assertIn('section_tabs.addTab(engineering_audit_page, "Engineering Audit")', text)
        self.assertNotIn('section_tabs.addTab(engineering_audit_page, "Engineering Diagnostics")', text)

    def test_engineering_audit_preserves_full_and_pontual_inner_tabs(self) -> None:
        text = SAFETY.read_text(encoding="utf-8")
        self.assertIn('audit_tabs.addTab(pontual_audit_page, "Pontual Audit")', text)
        self.assertIn("_install_complete_engineering_review(", text)
        self.assertIn("engineering_audit_layout.addWidget(audit_tabs, 1)", text)

    def test_host_preserves_wave2ob_public_pontual_factory_contract(self) -> None:
        text = HOST.read_text(encoding="utf-8")
        self.assertIn('"create_engineering_diagnostics_panel"', text)
        self.assertIn('"create_engineering_diagnostics_workspace"', text)
        self.assertIn("pontual_factory=pontual_factory", text)

    def test_diagnostics_workspace_is_added_as_second_section(self) -> None:
        text = HOST.read_text(encoding="utf-8")
        self.assertIn("section_tabs.addTab(workspace, _ENGINEERING_DIAGNOSTICS_LABEL)", text)
        self.assertIn("window._engineering_diagnostics_workspace = workspace", text)

    def test_diagnostics_workspace_has_full_and_pontual_modes(self) -> None:
        text = WORKSPACE.read_text(encoding="utf-8")
        self.assertIn('tabs.addTab(full_page, "Full Engineering Diagnostics")', text)
        self.assertIn('tabs.addTab(pontual_page, "Pontual Engineering Diagnostics")', text)

    def test_full_diagnostics_runs_all_supported_collectors(self) -> None:
        self.assertEqual(
            tuple(label for label, _method in FULL_ENGINEERING_DIAGNOSTIC_COLLECTORS),
            ("BOM", "Ruff", "Architecture", "Shadow"),
        )
        controller = _CandidateController()
        outcomes = collect_full_engineering_diagnostics_candidates(controller, ".", 1, Event())
        self.assertEqual(controller.calls, ["BOM", "Ruff", "Architecture", "Shadow"])
        self.assertEqual(len(outcomes), 4)
        self.assertTrue(all(outcome.candidate is not None for outcome in outcomes))

    def test_full_diagnostics_cancellation_fails_closed(self) -> None:
        cancellation = Event()
        cancellation.set()
        with self.assertRaises(EngineeringDiagnosticsGuiCancelled):
            collect_full_engineering_diagnostics_candidates(_CandidateController(), ".", 1, cancellation)

    def test_full_diagnostics_controls_and_sonar_are_canonical(self) -> None:
        text = FULL.read_text(encoding="utf-8")
        self.assertIn('QPushButton("Run All Engineering Diagnostics")', text)
        self.assertIn('setObjectName("full_engineering_diagnostics_run_button")', text)
        self.assertIn('QPushButton("Cancel Diagnostics")', text)
        self.assertIn('setObjectName("full_engineering_diagnostics_cancel_button")', text)
        self.assertIn('sonar.start("All collectors")', text)
        self.assertGreaterEqual(text.count("sonar.stop()"), 2)

    def test_full_cancel_waits_for_worker_settlement(self) -> None:
        text = FULL.read_text(encoding="utf-8")
        start = text.index("    def cancel_run() -> None:")
        end = text.index("    def set_project_root", start)
        block = text[start:end]
        self.assertIn("cancellation.set()", block)
        self.assertIn("sonar.stop()", block)
        self.assertIn("cancel_button.setEnabled(False)", block)
        self.assertNotIn('state["future"] = None', block)
        self.assertNotIn("set_busy(False)", block)

    def test_audit_commands_do_not_disable_diagnostics_controls(self) -> None:
        text = SAFETY.read_text(encoding="utf-8")
        self.assertIn("engineering_audit_page.findChildren(QPushButton)", text)
        self.assertNotIn("panel.findChildren(QPushButton)", text)

    def test_no_private_cross_box_imports(self) -> None:
        for path in (HOST, WORKSPACE, FULL):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports: list[str] = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
                elif isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
            joined = "\n".join(imports)
            self.assertNotIn("_reasoner_tools_gui_engineering_safety", joined)
            self.assertNotIn("sqlite3", joined)


if __name__ == "__main__":
    unittest.main()
