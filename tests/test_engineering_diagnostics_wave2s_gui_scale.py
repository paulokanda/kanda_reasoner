# project-path: tests/test_engineering_diagnostics_wave2s_gui_scale.py
"""GUI projection and scale tests for Engineering Diagnostics Wave 2S."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import time
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    RUFF_PRODUCER_ID,
    DiagnosticComparison,
    DiagnosticFindingEnrichment,
    DiagnosticFrozenPathEnrichment,
    DiagnosticOwnerEnrichment,
    DiagnosticScopeEnrichment,
    build_diagnostic_remediation_intents,
)
from kanda_reasoner_app.engineering_diagnostics_gui.finding_view_builder import (
    build_diagnostic_finding_views,
)
from kanda_reasoner_app.engineering_diagnostics_gui.owner_ui import (
    build_finding_detail_lines,
)
from kanda_reasoner_app.engineering_diagnostics_gui.table_columns import (
    ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_finding_fixture,
    wave2qa_run_record_fixture,
)


def _enrichment() -> DiagnosticFindingEnrichment:
    return DiagnosticFindingEnrichment(
        DiagnosticScopeEnrichment("ACTIVE", "high", "fixture", ("scope",)),
        DiagnosticFrozenPathEnrichment("UNFROZEN", evidence=("freeze",)),
        DiagnosticOwnerEnrichment(
            "READY",
            "high",
            canonical_owner="pkg.module",
            evidence=("owner",),
        ),
    )


def _finding(index: int):
    return replace(
        wave2qa_finding_fixture(
            "issue-" + str(index),
            "F401",
            "pkg/module_" + str(index % 100) + ".py",
            symbol="module.target",
            evidence={
                "fix_available": True,
                "fix_applicability": "safe",
                "fix_message": "Remove unused import.",
                "fix_edit_count": 1,
                "fix_executed": False,
            },
        ),
        suggested_action="Review Ruff F401 evidence.",
    )


class _Enricher:
    def enrich_many(self, findings):
        enrichment = _enrichment()
        return tuple(enrichment for _finding_record in findings)


class EngineeringDiagnosticsWave2SGuiScaleTests(unittest.TestCase):
    def test_batch_remediation_handles_25000_findings(self) -> None:
        findings = tuple(_finding(index) for index in range(25000))
        run = replace(
            wave2qa_run_record_fixture(RUFF_PRODUCER_ID, "run-2s-scale"),
            finding_count=len(findings),
        )
        enrichments = tuple(_enrichment() for _finding_record in findings)
        started = time.perf_counter()
        intents = build_diagnostic_remediation_intents(
            run,
            findings,
            enrichments,
            {},
            {},
        )
        elapsed = time.perf_counter() - started
        self.assertEqual(len(intents), 25000)
        self.assertTrue(
            all(item.action_class == "SAFE_MECHANICAL_FIX_AVAILABLE" for item in intents)
        )
        self.assertLess(elapsed, 10.0)

    def test_finding_view_builder_attaches_remediation_intent(self) -> None:
        finding = _finding(1)
        run = replace(
            wave2qa_run_record_fixture(RUFF_PRODUCER_ID, "run-2s-view"),
            finding_count=1,
        )
        comparison = DiagnosticComparison(
            run_id=run.run_id,
            baseline_id=None,
            status="NO_ACTIVE_BASELINE",
            new_issue_fingerprints=(),
            persistent_issue_fingerprints=(),
            resolved_issue_fingerprints=(),
        )
        rows = build_diagnostic_finding_views(
            run,
            (finding,),
            comparison,
            _Enricher(),
            {},
            {},
        )
        self.assertEqual(rows[0].remediation_action_class, "SAFE_MECHANICAL_FIX_AVAILABLE")
        self.assertFalse(rows[0].remediation_intent.executable_patch)

    def test_detail_renders_non_executable_remediation_and_validation_plan(self) -> None:
        finding = _finding(2)
        run = replace(
            wave2qa_run_record_fixture(RUFF_PRODUCER_ID, "run-2s-detail"),
            finding_count=1,
        )
        comparison = DiagnosticComparison(
            run_id=run.run_id,
            baseline_id=None,
            status="NO_ACTIVE_BASELINE",
            new_issue_fingerprints=(),
            persistent_issue_fingerprints=(),
            resolved_issue_fingerprints=(),
        )
        view = build_diagnostic_finding_views(
            run,
            (finding,),
            comparison,
            _Enricher(),
            {},
            {},
        )[0]
        detail = "\n".join(build_finding_detail_lines(view, "source"))
        self.assertIn("Remediation intent:", detail)
        self.assertIn("Executable patch: false", detail)
        self.assertIn("Validation commands:", detail)
        self.assertNotIn("confirmed root cause", detail.lower())

    def test_table_contract_exposes_remediation_without_new_filter_signature(self) -> None:
        self.assertIn(
            ("remediation_action_class", "Remediation"),
            ENGINEERING_DIAGNOSTICS_TABLE_COLUMNS,
        )
        source = (
            Path(__file__).resolve().parents[1]
            / "kanda_reasoner_app"
            / "engineering_diagnostics_gui"
            / "diagnostic_table_model.py"
        ).read_text(encoding="utf-8")
        self.assertIn("view.remediation_action_class", source)
        self.assertIn("elif len(args) == 6:", source)


if __name__ == "__main__":
    unittest.main()
