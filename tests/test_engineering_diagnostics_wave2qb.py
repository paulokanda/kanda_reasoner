# project-path: tests/test_engineering_diagnostics_wave2qb.py
"""Core public-contract tests for Engineering Diagnostics Wave 2Q-B."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from threading import Event
import tempfile
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    SHADOW_PRODUCER_ID,
    DiagnosticValidationError,
    ShadowCollectionCancelled,
    build_deterministic_diagnostic_groups,
    build_shadow_diagnostic_run,
    build_shadow_relational_graph,
    collect_shadow_findings,
    issue_fingerprint,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_disposable_boundary_fixture,
    wave2qa_finding_fixture,
    wave2qa_run_record_fixture,
)


class _PublicShadowReport:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def to_dict(self) -> dict[str, object]:
        return dict(self._payload)


def _source_path() -> Path:
    import kanda_reasoner_app.source_hygiene.shadow_audit as shadow_audit

    return Path(str(shadow_audit.__file__)).resolve(strict=True)


def _report(root: Path, findings: list[dict[str, object]]) -> _PublicShadowReport:
    return _PublicShadowReport(
        {
            "report_type": "shadow_conflict_audit",
            "project_root": str(root.resolve()),
            "findings": findings,
        }
    )


def _duplicate_finding(issue: str, symbol: str, owners: list[str], run_id: str = "run-2qb"):
    return wave2qa_finding_fixture(
        issue,
        "DUPLICATE_PUBLIC_SYMBOL",
        "ARCHITECTURE.md",
        symbol=symbol,
        evidence={"symbol": symbol, "owners": owners},
        run_id=run_id,
    )


def _facade_finding(issue: str, symbol: str, path: str, run_id: str = "run-2qb"):
    return wave2qa_finding_fixture(
        issue,
        "BEHAVIOR_DEFINED_IN_FACADE",
        path,
        symbol=symbol,
        evidence={"symbol": symbol},
        run_id=run_id,
    )


class EngineeringDiagnosticsWave2QBCoreTests(unittest.TestCase):
    def test_collector_consumes_public_report_and_copies_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            findings = [
                {
                    "code": "UNBOUND_ALL_EXPORT",
                    "path": "pkg/__init__.py",
                    "line": 7,
                    "message": "Stale export.",
                    "severity": "warning",
                    "confidence": "high",
                    "evidence": {"exported_name": "Missing"},
                    "suggested_action": "Remove it.",
                }
            ]
            collection = collect_shadow_findings(
                root,
                auditor=lambda project_root, max_files=None: _report(root, findings),
                audit_source_path=_source_path(),
            )
            self.assertEqual(collection.assessment, "ISSUES")
            self.assertTrue(collection.coverage_valid)
            self.assertEqual(collection.issues[0].evidence["exported_name"], "Missing")
            findings[0]["evidence"] = {"exported_name": "Changed"}
            self.assertEqual(collection.issues[0].evidence["exported_name"], "Missing")

    def test_collector_cancellation_fails_before_public_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            event = Event()
            event.set()
            called = []
            with self.assertRaises(ShadowCollectionCancelled):
                collect_shadow_findings(
                    temporary,
                    cancellation=event,
                    auditor=lambda project_root, max_files=None: called.append(project_root),
                    audit_source_path=_source_path(),
                )
            self.assertEqual(called, [])

    def test_collector_rejects_wrong_project_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            wrong = root / "other"
            wrong.mkdir()
            with self.assertRaisesRegex(Exception, "PROJECT_MISMATCH"):
                collect_shadow_findings(
                    root,
                    auditor=lambda project_root, max_files=None: _report(wrong, []),
                    audit_source_path=_source_path(),
                )

    def test_normalizer_preserves_identity_when_message_wording_changes(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            root = boundary.active_project_root
            base = {
                "code": "DUPLICATE_PUBLIC_SYMBOL",
                "path": "<project>",
                "severity": "warning",
                "confidence": "medium",
                "evidence": {"symbol": "Thing", "owners": ["a.py", "b.py"]},
                "suggested_action": "Review owner.",
            }
            first = dict(base, message="First wording.")
            second = dict(base, message="Second wording.")
            collections = [
                collect_shadow_findings(
                    root,
                    auditor=lambda project_root, max_files=None, item=item: _report(root, [item]),
                    audit_source_path=_source_path(),
                )
                for item in (first, second)
            ]
            runs = [
                build_shadow_diagnostic_run(
                    collection,
                    boundary=boundary,
                    attempt_id="attempt-" + str(index),
                    source_fingerprint="source",
                    operation_generation=1,
                )
                for index, collection in enumerate(collections)
            ]
            fingerprints = [issue_fingerprint(SHADOW_PRODUCER_ID, run.findings[0]) for run in runs]
            self.assertEqual(fingerprints[0], fingerprints[1])

    def test_invalid_public_coverage_cannot_be_persisted_as_complete(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            root = boundary.active_project_root
            collection = collect_shadow_findings(
                root,
                auditor=lambda project_root, max_files=None: _report(
                    root,
                    [
                        {
                            "code": "SHADOW_AUDIT_PARSE_ERROR",
                            "path": "bad.py",
                            "message": "parse failed",
                            "severity": "error",
                            "confidence": "high",
                        }
                    ],
                ),
                audit_source_path=_source_path(),
            )
            self.assertFalse(collection.coverage_valid)
            with self.assertRaisesRegex(DiagnosticValidationError, "COVERAGE_INVALID"):
                build_shadow_diagnostic_run(
                    collection,
                    boundary=boundary,
                    attempt_id="attempt",
                    source_fingerprint="source",
                    operation_generation=1,
                )

    def test_relational_graph_uses_declared_node_and_edge_taxonomy(self) -> None:
        run = replace(
            wave2qa_run_record_fixture(SHADOW_PRODUCER_ID, "run-2qb"),
            finding_count=2,
        )
        findings = (
            _duplicate_finding("dup", "Thing", ["pkg/__init__.py", "pkg/impl.py"]),
            _facade_finding("facade", "Thing", "pkg/__init__.py"),
        )
        graph = build_shadow_relational_graph(run, findings)
        self.assertTrue({"file", "symbol", "facade", "implementation_owner"}.issubset({n.kind for n in graph.nodes}))
        self.assertTrue({"duplicate_of", "reexports", "facade_of", "implements"}.issubset({e.kind for e in graph.edges}))
        self.assertTrue(all(edge.evidence["deterministic"] for edge in graph.edges))

    def test_connected_component_becomes_group_only_with_two_findings(self) -> None:
        run = replace(wave2qa_run_record_fixture(SHADOW_PRODUCER_ID, "run-2qb"), finding_count=2)
        findings = (
            _duplicate_finding("dup", "Thing", ["pkg/__init__.py", "pkg/impl.py"]),
            _facade_finding("facade", "Thing", "pkg/__init__.py"),
        )
        groups = build_deterministic_diagnostic_groups(run, findings)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].recipe_id, "shadow.relational_component.v1")
        self.assertEqual(groups[0].member_issue_fingerprints, ("dup", "facade"))
        self.assertFalse(groups[0].evidence["root_cause_claimed"])
        self.assertFalse(groups[0].evidence["ai_grouping_used"])

    def test_single_shadow_finding_is_not_promoted_to_group(self) -> None:
        run = replace(wave2qa_run_record_fixture(SHADOW_PRODUCER_ID, "run-2qb"), finding_count=1)
        groups = build_deterministic_diagnostic_groups(
            run,
            (_duplicate_finding("dup", "Thing", ["a.py", "b.py"]),),
        )
        self.assertEqual(groups, ())

    def test_relational_group_identity_is_stable_across_runs(self) -> None:
        first_run = replace(wave2qa_run_record_fixture(SHADOW_PRODUCER_ID, "run-first"), finding_count=2)
        second_run = replace(first_run, run_id="run-second", attempt_id="attempt-second")
        first = (
            _duplicate_finding("dup", "Thing", ["pkg/__init__.py", "pkg/impl.py"], "run-first"),
            _facade_finding("facade", "Thing", "pkg/__init__.py", "run-first"),
        )
        second = tuple(replace(item, run_id="run-second") for item in first)
        self.assertEqual(
            build_deterministic_diagnostic_groups(first_run, first)[0].group_id,
            build_deterministic_diagnostic_groups(second_run, second)[0].group_id,
        )

    def test_disjoint_relations_remain_separate_components(self) -> None:
        run = replace(wave2qa_run_record_fixture(SHADOW_PRODUCER_ID, "run-2qb"), finding_count=4)
        findings = (
            _duplicate_finding("dup-a", "A", ["a/__init__.py", "a/impl.py"]),
            _facade_finding("facade-a", "A", "a/__init__.py"),
            _duplicate_finding("dup-b", "B", ["b/__init__.py", "b/impl.py"]),
            _facade_finding("facade-b", "B", "b/__init__.py"),
        )
        groups = build_deterministic_diagnostic_groups(run, findings)
        self.assertEqual(len(groups), 2)
        self.assertEqual({group.member_issue_fingerprints for group in groups}, {("dup-a", "facade-a"), ("dup-b", "facade-b")})

    def test_unbound_export_relates_to_facade_behavior(self) -> None:
        run = replace(wave2qa_run_record_fixture(SHADOW_PRODUCER_ID, "run-2qb"), finding_count=2)
        unbound = wave2qa_finding_fixture(
            "unbound",
            "UNBOUND_ALL_EXPORT",
            "pkg/__init__.py",
            symbol="Thing",
            evidence={"exported_name": "Thing"},
            run_id="run-2qb",
        )
        groups = build_deterministic_diagnostic_groups(
            run,
            (unbound, _facade_finding("facade", "Thing", "pkg/__init__.py")),
        )
        self.assertEqual(len(groups), 1)
        graph = build_shadow_relational_graph(run, (unbound, _facade_finding("facade", "Thing", "pkg/__init__.py")))
        self.assertIn("unbound_export", {edge.kind for edge in graph.edges})


if __name__ == "__main__":
    unittest.main()
