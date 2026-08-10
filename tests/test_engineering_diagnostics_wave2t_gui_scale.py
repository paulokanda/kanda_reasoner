# project-path: tests/test_engineering_diagnostics_wave2t_gui_scale.py
"""Public navigation and scale tests for Engineering Diagnostics Wave 2T."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import tempfile
import time
import unittest

from kanda_reasoner_app.engineering_diagnostics import RUFF_PRODUCER_ID
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


class EngineeringDiagnosticsWave2TGuiScaleTests(unittest.TestCase):
    def test_full_audit_parser_handles_large_report_quickly(self) -> None:
        block = "\n".join(
            (
                "[01/23] Source Hygiene - Ruff Quality",
                "Command: ruff-quality",
                "Outcome: PASS",
                "Execution: PASS",
                "Assessment: PASS_WITH_FINDINGS",
                "Assessment reason: Findings retained.",
                "-" * 72,
            )
        )
        report = "COMPLETE ENGINEERING REVIEW\n" + block * 25000
        started = time.perf_counter()
        links = build_full_audit_diagnostic_links(report)
        elapsed = time.perf_counter() - started
        self.assertEqual(len(links), 25000)
        self.assertLess(elapsed, 5.0)

    def test_public_navigation_contract_is_read_only(self) -> None:
        calls: list[EngineeringDiagnosticsNavigationRequest] = []
        panel = SimpleNamespace(
            apply_engineering_diagnostics_navigation=lambda request: calls.append(request) or True
        )
        request = EngineeringDiagnosticsNavigationRequest(
            RUFF_PRODUCER_ID,
            compatible_run_id="run-1",
            baseline_state="current",
        )
        self.assertTrue(request_engineering_diagnostics_navigation(panel, request))
        self.assertEqual(calls, [request])
        self.assertFalse(hasattr(panel, "write_source"))
        self.assertFalse(hasattr(panel, "sqlite_connection"))

    def test_summary_filters_25000_incompatible_runs_quickly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "module.py").write_text("value = 1\n", encoding="utf-8")
            source = project_source_fingerprint(root)
            stale = tuple(
                SimpleNamespace(
                    run_id="stale-" + str(index),
                    producer_id=RUFF_PRODUCER_ID,
                    completion_status="COMPLETED",
                    source_fingerprint="old",
                    provenance={},
                    finding_count=0,
                )
                for index in range(25000)
            )
            current = SimpleNamespace(
                run_id="current",
                producer_id=RUFF_PRODUCER_ID,
                completion_status="COMPLETED",
                source_fingerprint=source,
                provenance={"raw_finding_count": 0},
                finding_count=0,
            )
            view = SimpleNamespace(
                comparison=SimpleNamespace(
                    status="COMPARED",
                    new_issue_fingerprints=(),
                ),
                findings=(),
                groups=(),
            )
            controller = SimpleNamespace(
                list_runs=lambda *_args, **_kwargs: stale + (current,),
                load_run_view=lambda *_args, **_kwargs: view,
            )
            started = time.perf_counter()
            summary = build_engineering_diagnostics_navigation_summary(
                controller,
                root,
                RUFF_PRODUCER_ID,
            )
            elapsed = time.perf_counter() - started
        self.assertEqual(summary.compatible_run_id, "current")
        self.assertLess(elapsed, 5.0)

    def test_parser_does_not_rewrite_wave2m_report_text(self) -> None:
        report = "\n".join(
            (
                "[01/01] Source Hygiene - Ruff Quality",
                "Command: ruff-quality",
                "Execution: PASS",
                "Assessment: DEGRADED",
                "Assessment reason: Exact Wave 2M reason.",
                "-" * 72,
            )
        )
        before = report.encode("utf-8")
        links = build_full_audit_diagnostic_links(report)
        self.assertEqual(links[0].assessment, "DEGRADED")
        self.assertEqual(report.encode("utf-8"), before)


if __name__ == "__main__":
    unittest.main()
