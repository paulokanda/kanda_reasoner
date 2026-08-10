# project-path: tests/test_engineering_diagnostics_wave2pb.py
"""Focused public-contract tests for Engineering Diagnostics Wave 2P-B."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tempfile
import time
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    DiagnosticFindingRecord,
    DiagnosticOwnerEnrichment,
    EngineeringDiagnosticsEnricher,
    build_diagnostic_owner_snapshot,
    classify_diagnostic_owner,
)
from kanda_reasoner_app.engineering_diagnostics_gui.models import (
    DiagnosticFindingView,
)
from kanda_reasoner_app.engineering_diagnostics_gui.owner_ui import (
    build_finding_detail_lines,
)
from kanda_reasoner_app.reasoner_symbol_atlas import (
    ProjectModuleRecord,
    ProjectSymbol,
)


def _record(
    path: str,
    role: str,
    *,
    symbol: str = "",
    symbol_role: str = "canonical_owner",
    test: bool = False,
) -> ProjectModuleRecord:
    symbols = ()
    if symbol:
        symbols = (
            ProjectSymbol(
                name=symbol,
                kind="function",
                module=path.removesuffix(".py").replace("/", "."),
                path=path,
                line=10,
                owner_role=symbol_role,
            ),
        )
    return ProjectModuleRecord(
        module=path.removesuffix(".py").replace("/", "."),
        path=path,
        owner_role=role,
        is_test_file=test,
        symbols=symbols,
        evidence=("fixture",),
    )


def _finding(
    path: str = "pkg/owner.py",
    symbol: str = "target",
) -> DiagnosticFindingRecord:
    return DiagnosticFindingRecord(
        run_id="run-1",
        issue_fingerprint="issue-original",
        evidence_digest="evidence-original",
        code="RULE",
        relative_path=path,
        message="message",
        severity="warning",
        confidence="medium",
        semantic_key="semantic",
        symbol_id=symbol,
        location_key="location",
        category="category",
        line=10,
        evidence={"source": "fixture"},
        suggested_action="",
    )


class EngineeringDiagnosticsWave2PBTests(unittest.TestCase):
    def test_ready_requires_one_active_canonical_owner(self) -> None:
        snapshot = build_diagnostic_owner_snapshot(
            ".",
            records=(_record("pkg/owner.py", "canonical_owner", symbol="target"),),
        )
        result = classify_diagnostic_owner(snapshot, _finding())
        self.assertEqual(result.status, "READY")
        self.assertEqual(result.canonical_owner, "pkg/owner.py::target")
        self.assertIn("pkg/owner.py::target", result.active_candidates)

    def test_competing_active_owners_preserve_uncertainty(self) -> None:
        snapshot = build_diagnostic_owner_snapshot(
            ".",
            records=(
                _record("pkg/one.py", "canonical_owner", symbol="target"),
                _record("pkg/two.py", "canonical_owner", symbol="target"),
            ),
        )
        result = classify_diagnostic_owner(snapshot, _finding("pkg/missing.py"))
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertEqual(result.confidence, "medium")
        self.assertEqual(result.canonical_owner, "")

    def test_historical_candidate_cannot_be_promoted(self) -> None:
        snapshot = build_diagnostic_owner_snapshot(
            ".",
            records=(
                _record(
                    ".project_reference/old.py",
                    "canonical_owner",
                    symbol="target",
                ),
            ),
        )
        result = classify_diagnostic_owner(snapshot, _finding("pkg/missing.py"))
        self.assertEqual(result.status, "NO_OWNER")
        self.assertFalse(result.active_candidates)
        self.assertTrue(result.historical_candidates)

    def test_test_and_generated_candidates_are_inactive(self) -> None:
        snapshot = build_diagnostic_owner_snapshot(
            ".",
            records=(
                _record("tests/test_owner.py", "test_only", symbol="target", test=True),
                _record("generated/owner.py", "generated_or_stale", symbol="target"),
            ),
        )
        result = classify_diagnostic_owner(snapshot, _finding("pkg/missing.py"))
        self.assertEqual(result.status, "NO_OWNER")
        self.assertEqual(len(result.historical_candidates), 2)

    def test_active_noncanonical_candidate_needs_review(self) -> None:
        snapshot = build_diagnostic_owner_snapshot(
            ".",
            records=(_record("pkg/facade.py", "facade", symbol="target", symbol_role="facade"),),
        )
        result = classify_diagnostic_owner(snapshot, _finding("pkg/facade.py"))
        self.assertEqual(result.status, "NEEDS_REVIEW")
        self.assertEqual(result.confidence, "low")

    def test_no_matching_candidate_reports_no_owner(self) -> None:
        snapshot = build_diagnostic_owner_snapshot(".", records=())
        result = classify_diagnostic_owner(snapshot, _finding())
        self.assertEqual(result.status, "NO_OWNER")
        self.assertEqual(result.confidence, "none")

    def test_classifier_failure_degrades_without_guessing(self) -> None:
        def broken(_root: str | Path):
            raise RuntimeError("atlas unavailable")

        snapshot = build_diagnostic_owner_snapshot(".", classifier=broken)
        result = classify_diagnostic_owner(snapshot, _finding())
        self.assertEqual(result.status, "DEGRADED")
        self.assertEqual(result.canonical_owner, "")
        self.assertIn("atlas unavailable", " ".join(result.evidence))

    def test_enrichment_preserves_finding_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "pkg").mkdir()
            (root / "pkg" / "owner.py").write_text(
                "def target():\n    return 1\n",
                encoding="utf-8",
            )
            finding = _finding()
            snapshot = build_diagnostic_owner_snapshot(
                root,
                records=(_record("pkg/owner.py", "canonical_owner", symbol="target"),),
            )
            enriched = EngineeringDiagnosticsEnricher(
                root,
                owner_snapshot=snapshot,
            ).enrich(finding)
        self.assertEqual(finding.issue_fingerprint, "issue-original")
        self.assertEqual(finding.evidence_digest, "evidence-original")
        self.assertEqual(enriched.owner.status, "READY")

    def test_batch_enrichment_uses_prebuilt_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "pkg").mkdir()
            (root / "pkg" / "owner.py").write_text(
                "def target():\n    return 1\n",
                encoding="utf-8",
            )
            snapshot = build_diagnostic_owner_snapshot(
                root,
                records=(_record("pkg/owner.py", "canonical_owner", symbol="target"),),
            )
            enricher = EngineeringDiagnosticsEnricher(root, owner_snapshot=snapshot)
            findings = tuple(
                replace(_finding(), issue_fingerprint=str(index))
                for index in range(25000)
            )
            started = time.perf_counter()
            results = enricher.enrich_many(findings)
            elapsed = time.perf_counter() - started
        self.assertEqual(len(results), 25000)
        self.assertTrue(all(item.owner.status == "READY" for item in results))
        self.assertLess(elapsed, 5.0)

    def test_gui_detail_exposes_owner_evidence(self) -> None:
        owner = DiagnosticOwnerEnrichment(
            "READY",
            "high",
            canonical_owner="pkg/owner.py::target",
            active_candidates=("pkg/owner.py::target",),
            selection_method="exact_path_and_symbol",
            evidence=("deterministic",),
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = build_diagnostic_owner_snapshot(root, records=())
            enrichment = EngineeringDiagnosticsEnricher(
                root,
                owner_snapshot=snapshot,
            ).enrich(_finding())
        view = DiagnosticFindingView(
            _finding(),
            "current",
            replace(enrichment, owner=owner),
        )
        rendered = "\n".join(build_finding_detail_lines(view, "excerpt"))
        self.assertIn("Owner status: READY", rendered)
        self.assertIn("Canonical owner: pkg/owner.py::target", rendered)
        self.assertIn("Owner evidence:\ndeterministic", rendered)


if __name__ == "__main__":
    unittest.main()
