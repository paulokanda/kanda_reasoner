# project-path: tests/test_engineering_diagnostics_wave2r_gui_scale.py
"""GUI and scale contracts for Engineering Diagnostics Wave 2R."""

from __future__ import annotations

from contextlib import closing
from dataclasses import replace
import sqlite3
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    DiagnosticLifecycleTarget,
    DiagnosticStateError,
    EngineeringDiagnosticsStore,
)
from kanda_reasoner_app.engineering_diagnostics_gui.controller import (
    EngineeringDiagnosticsController,
)
from kanda_reasoner_app.engineering_diagnostics_gui.models import DiagnosticFindingView
from kanda_reasoner_app.engineering_diagnostics_gui.owner_ui import (
    build_finding_detail_lines,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_disposable_boundary_fixture,
    wave2qa_finding_fixture,
    wave2qa_persisted_run_fixture,
)


class EngineeringDiagnosticsWave2RGuiScaleTests(unittest.TestCase):
    def test_controller_projects_issue_decision_state(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            store.record_lifecycle_decision(
                boundary,
                run.run_id,
                target,
                action="CONFIRM",
                reason_code="HUMAN_REVIEW",
                rationale="Confirmed evidence.",
                author="tester",
                expected_generation=0,
                revisit_condition="Review after correction.",
            )
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.active_project_root,
                boundary_resolver=lambda _root: boundary,
                store_factory=lambda _boundary: store,
            )
            view = controller.load_run_view(boundary.active_project_root, run.run_id)
            selected = next(
                row for row in view.findings
                if row.record.issue_fingerprint == issue.issue_fingerprint
            )
            self.assertEqual(selected.decision_state, "CONFIRMED")
            self.assertEqual(selected.decision_generation, 1)

    def test_detail_retains_terminal_decision_and_finding_evidence(self) -> None:
        finding = wave2qa_finding_fixture("issue", "F401", "pkg/module.py")
        view = DiagnosticFindingView(
            finding,
            "persistent",
            decision_state="SUPPRESSED",
            decision_generation=2,
        )
        text = "\n".join(build_finding_detail_lines(view, "source"))
        self.assertIn("Lifecycle decision state: SUPPRESSED", text)
        self.assertIn("message issue", text)
        self.assertIn("Source excerpt:", text)

    def test_default_open_state_scales_to_25000_findings(self) -> None:
        rows = tuple(
            DiagnosticFindingView(
                wave2qa_finding_fixture(
                    "issue-" + str(index),
                    "F401",
                    "pkg/module_" + str(index % 50) + ".py",
                ),
                "current",
            )
            for index in range(25000)
        )
        self.assertEqual(len(rows), 25000)
        self.assertTrue(all(row.decision_state == "OPEN" for row in rows))


    def test_lifecycle_migration_rolls_back_on_table_contract_mismatch(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            database = (
                boundary.active_project_support_root
                / "project_engineering_diagnostics"
                / "engineering_diagnostics.sqlite3"
            )
            database.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(database)) as connection:
                connection.execute(
                    "CREATE TABLE diagnostic_lifecycle_heads "
                    "(project_id TEXT NOT NULL)"
                )
                connection.commit()
            with self.assertRaises(DiagnosticStateError) as context:
                EngineeringDiagnosticsStore(boundary)
            self.assertIn(
                "ENGINEERING_DIAGNOSTICS_LIFECYCLE_TABLE_CONTRACT_MISMATCH",
                str(context.exception),
            )
            with closing(sqlite3.connect(database)) as connection:
                tables = {
                    str(row[0])
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
                lifecycle_metadata = connection.execute(
                    "SELECT COUNT(*) FROM sqlite_master "
                    "WHERE type = 'table' AND name = "
                    "'diagnostic_lifecycle_metadata'"
                ).fetchone()[0]
            self.assertEqual(lifecycle_metadata, 0)
            self.assertNotIn("diagnostic_lifecycle_decisions", tables)

    def test_group_generation_defaults_to_zero_without_decision(self) -> None:
        finding = wave2qa_finding_fixture("issue", "F401", "pkg/module.py")
        view = DiagnosticFindingView(finding, "current")
        self.assertEqual(view.group_decision_generation("missing"), 0)

    def test_gui_source_exposes_all_required_human_actions(self) -> None:
        from pathlib import Path

        source = (
            Path(__file__).resolve().parents[1]
            / "kanda_reasoner_app"
            / "engineering_diagnostics_gui"
            / "lifecycle_ui.py"
        ).read_text(encoding="utf-8")
        for action in (
            "CONFIRM",
            "SUPPRESS",
            "ACCEPT_RISK",
            "MARK_FALSE_POSITIVE",
            "DEFER",
            "REOPEN",
        ):
            self.assertIn('"' + action + '"', source)
        self.assertIn("explicit accepted-risk confirmation", source.lower())


if __name__ == "__main__":
    unittest.main()
