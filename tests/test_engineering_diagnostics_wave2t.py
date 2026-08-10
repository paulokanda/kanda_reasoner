# project-path: tests/test_engineering_diagnostics_wave2t.py
"""Focused public-contract tests for Engineering Diagnostics Wave 2T."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    SHADOW_PRODUCER_ID,
)
from kanda_reasoner_app.engineering_diagnostics_gui import (
    EngineeringDiagnosticsNavigationRequest,
    build_engineering_diagnostics_navigation_summary,
    request_engineering_diagnostics_navigation,
)
from kanda_reasoner_app.engineering_diagnostics_gui.source_identity import (
    project_source_fingerprint,
)
from kanda_reasoner_app.manage_architecture.full_audit_diagnostics_drillthrough import (
    build_full_audit_diagnostic_links,
)


class EngineeringDiagnosticsWave2TTests(unittest.TestCase):
    def test_navigation_request_normalizes_supported_filters(self) -> None:
        request = EngineeringDiagnosticsNavigationRequest(
            RUFF_PRODUCER_ID,
            compatible_run_id=" run-1 ",
            baseline_state="NEW",
            rule_family=" F821 ",
            severity="ERROR",
        )
        self.assertEqual(request.compatible_run_id, "run-1")
        self.assertEqual(request.baseline_state, "new")
        self.assertEqual(request.rule_family, "F821")
        self.assertEqual(request.severity, "error")

    def test_navigation_request_rejects_unsupported_values(self) -> None:
        with self.assertRaises(ValueError):
            EngineeringDiagnosticsNavigationRequest("unknown")
        with self.assertRaises(ValueError):
            EngineeringDiagnosticsNavigationRequest(
                BOM_PRODUCER_ID,
                baseline_state="resolved",
            )
        with self.assertRaises(ValueError):
            EngineeringDiagnosticsNavigationRequest(
                BOM_PRODUCER_ID,
                severity="critical",
            )

    def test_full_audit_parser_preserves_wave2m_assessment_text(self) -> None:
        report = "\n".join(
            (
                "COMPLETE ENGINEERING REVIEW",
                "[01/03] Source Hygiene - Scan BOM",
                "Command: bom-scan",
                "Outcome: PASS",
                "Execution: PASS",
                "Assessment: PASS_WITH_FINDINGS",
                "Assessment reason: BOM findings were retained.",
                "-" * 72,
                "[02/03] Source Hygiene - Ruff Quality",
                "Command: ruff-quality",
                "Outcome: PASS",
                "Execution: PASS",
                "Assessment: DEGRADED",
                "Assessment reason: Coverage was incomplete.",
                "-" * 72,
                "[03/03] Utilities - List Tools",
                "Command: list-tools",
                "Outcome: PASS",
                "Execution: PASS",
                "Assessment: CLEAN",
                "Assessment reason: Informational command.",
                "-" * 72,
            )
        )
        links = build_full_audit_diagnostic_links(report)
        self.assertEqual([item.command_name for item in links], ["bom-scan", "ruff-quality"])
        self.assertEqual(links[0].assessment, "PASS_WITH_FINDINGS")
        self.assertEqual(links[1].assessment, "DEGRADED")
        self.assertEqual(links[1].assessment_reason, "Coverage was incomplete.")
        self.assertIn("Assessment: DEGRADED", report)

    def test_full_audit_parser_maps_only_direct_collectors(self) -> None:
        report = "\n".join(
            (
                "[01/02] Source Hygiene - Shadow Audit",
                "Command: shadow-audit",
                "Execution: PASS",
                "Assessment: PASS_WITH_FINDINGS",
                "Assessment reason: Conflicts found.",
                "-" * 72,
                "[02/02] Project Symbol Atlas - Pre-Patch Gate",
                "Command: pre-patch-gate",
                "Execution: PASS",
                "Assessment: CLEAN",
                "Assessment reason: Gate passed.",
                "-" * 72,
            )
        )
        links = build_full_audit_diagnostic_links(report)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].producer_id, SHADOW_PRODUCER_ID)

    def test_public_navigation_uses_only_panel_contract(self) -> None:
        calls: list[EngineeringDiagnosticsNavigationRequest] = []
        panel = SimpleNamespace(
            apply_engineering_diagnostics_navigation=lambda request: calls.append(request) or True
        )
        request = EngineeringDiagnosticsNavigationRequest(BOM_PRODUCER_ID)
        self.assertTrue(request_engineering_diagnostics_navigation(panel, request))
        self.assertEqual(calls, [request])
        with self.assertRaises(RuntimeError):
            request_engineering_diagnostics_navigation(object(), request)

    def test_summary_chooses_newest_source_compatible_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "module.py").write_text("value = 1\n", encoding="utf-8")
            source = project_source_fingerprint(root)
            stale = SimpleNamespace(
                run_id="stale",
                producer_id=RUFF_PRODUCER_ID,
                completion_status="COMPLETED",
                source_fingerprint="old",
                provenance={"raw_finding_count": 99},
                finding_count=99,
            )
            current = SimpleNamespace(
                run_id="current",
                producer_id=RUFF_PRODUCER_ID,
                completion_status="COMPLETED",
                source_fingerprint=source,
                provenance={"raw_finding_count": 4},
                finding_count=3,
            )
            findings = (
                SimpleNamespace(record=SimpleNamespace(
                    severity="error", issue_fingerprint="new-error"
                )),
                SimpleNamespace(record=SimpleNamespace(
                    severity="warning", issue_fingerprint="new-warning"
                )),
                SimpleNamespace(record=SimpleNamespace(
                    severity="error", issue_fingerprint="persistent"
                )),
            )
            view = SimpleNamespace(
                comparison=SimpleNamespace(
                    status="COMPARED",
                    new_issue_fingerprints=("new-error", "new-warning"),
                ),
                findings=findings,
                groups=(SimpleNamespace(group_id="g1"), SimpleNamespace(group_id="g1")),
            )
            controller = SimpleNamespace(
                list_runs=lambda *_args, **_kwargs: (stale, current),
                load_run_view=lambda *_args, **_kwargs: view,
            )
            summary = build_engineering_diagnostics_navigation_summary(
                controller,
                root,
                RUFF_PRODUCER_ID,
            )
        self.assertEqual(summary.compatible_run_id, "current")
        self.assertEqual(summary.raw_finding_count, 4)
        self.assertEqual(summary.canonical_issue_count, 3)
        self.assertEqual(summary.diagnostic_group_count, 1)
        self.assertEqual(summary.new_high_priority_count, 1)

    def test_summary_fails_closed_without_compatible_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "module.py").write_text("value = 1\n", encoding="utf-8")
            controller = SimpleNamespace(
                list_runs=lambda *_args, **_kwargs: (),
            )
            summary = build_engineering_diagnostics_navigation_summary(
                controller,
                root,
                BOM_PRODUCER_ID,
            )
        self.assertFalse(summary.available)
        self.assertEqual(summary.comparison_status, "NO_COMPATIBLE_RUN")


if __name__ == "__main__":
    unittest.main()
