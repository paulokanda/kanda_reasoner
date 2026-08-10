# project-path: tests/test_engineering_diagnostics_wave2qa.py
"""Core public-contract tests for Engineering Diagnostics Wave 2Q-A."""

from __future__ import annotations

from dataclasses import replace
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    ARCHITECTURE_PRODUCER_ID,
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    DiagnosticConflictError,
    DiagnosticStateError,
    EngineeringDiagnosticsStore,
    build_deterministic_diagnostic_groups,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_disposable_boundary_fixture,
    wave2qa_finding_fixture,
    wave2qa_persisted_run_fixture,
    wave2qa_run_record_fixture,
)


class EngineeringDiagnosticsWave2QACoreTests(unittest.TestCase):
    def test_bom_groups_same_rule_and_file_deterministically(self) -> None:
        run = replace(wave2qa_run_record_fixture(BOM_PRODUCER_ID), finding_count=3)
        findings = (
            wave2qa_finding_fixture("a", "BOM_UTF8", "pkg/a.py"),
            wave2qa_finding_fixture("b", "BOM_UTF8", "pkg/a.py"),
            wave2qa_finding_fixture("c", "BOM_UTF8", "pkg/b.py"),
        )
        first = build_deterministic_diagnostic_groups(run, findings)
        second = build_deterministic_diagnostic_groups(run, tuple(reversed(findings)))
        self.assertEqual(first, second)
        self.assertEqual(len(first), 1)
        self.assertEqual(first[0].recipe_id, "bom.rule_file.v1")
        self.assertEqual(first[0].member_issue_fingerprints, ("a", "b"))
        self.assertFalse(first[0].evidence["root_cause_claimed"])

    def test_group_identity_is_stable_across_compatible_runs(self) -> None:
        first_run = replace(
            wave2qa_run_record_fixture(BOM_PRODUCER_ID, "run-first"),
            finding_count=2,
        )
        second_run = replace(first_run, run_id="run-second", attempt_id="attempt-second")
        first_findings = (
            wave2qa_finding_fixture("a", "BOM_UTF8", "pkg/a.py", run_id="run-first"),
            wave2qa_finding_fixture("b", "BOM_UTF8", "pkg/a.py", run_id="run-first"),
        )
        second_findings = tuple(
            replace(finding, run_id="run-second") for finding in first_findings
        )
        first_group = build_deterministic_diagnostic_groups(
            first_run,
            first_findings,
        )[0]
        second_group = build_deterministic_diagnostic_groups(
            second_run,
            second_findings,
        )[0]
        self.assertEqual(first_group.group_id, second_group.group_id)

    def test_ruff_exposes_file_structural_and_package_recipes(self) -> None:
        run = replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=3)
        findings = (
            wave2qa_finding_fixture("a", "F401", "pkg/a.py", symbol="Class.method"),
            wave2qa_finding_fixture("b", "F401", "pkg/a.py", symbol="Class.other"),
            wave2qa_finding_fixture("c", "F401", "pkg/b.py", symbol="Other.method"),
        )
        groups = build_deterministic_diagnostic_groups(run, findings)
        recipes = {group.recipe_id: group for group in groups}
        self.assertIn("ruff.rule_file.v1", recipes)
        self.assertIn("ruff.rule_structural_parent.v1", recipes)
        self.assertIn("ruff.rule_package.v1", recipes)
        self.assertEqual(recipes["ruff.rule_package.v1"].confidence, "medium")
        self.assertEqual(len(recipes["ruff.rule_package.v1"].member_issue_fingerprints), 3)

    def test_architecture_groups_explicit_owner_and_boundary(self) -> None:
        run = replace(wave2qa_run_record_fixture(ARCHITECTURE_PRODUCER_ID), finding_count=2)
        evidence = {"owner": "Box A", "boundary": "A -> B"}
        findings = (
            wave2qa_finding_fixture("a", "PRIVATE_REACH_IN", "pkg/a.py", evidence=evidence),
            wave2qa_finding_fixture("b", "PRIVATE_REACH_IN", "pkg/b.py", evidence=evidence),
        )
        groups = build_deterministic_diagnostic_groups(run, findings)
        recipes = {group.recipe_id: group for group in groups}
        self.assertEqual(recipes["architecture.rule_boundary.v1"].confidence, "high")
        self.assertEqual(recipes["architecture.rule_owner_box.v1"].confidence, "medium")

    def test_single_findings_are_not_promoted_to_noise_reduction_groups(self) -> None:
        run = replace(wave2qa_run_record_fixture(BOM_PRODUCER_ID), finding_count=1)
        groups = build_deterministic_diagnostic_groups(
            run,
            (wave2qa_finding_fixture("a", "BOM_UTF8", "pkg/a.py"),),
        )
        self.assertEqual(groups, ())

    def test_grouping_preserves_finding_and_scan_identity(self) -> None:
        run = replace(wave2qa_run_record_fixture(BOM_PRODUCER_ID), finding_count=2)
        findings = (
            wave2qa_finding_fixture("a", "BOM_UTF8", "pkg/a.py"),
            wave2qa_finding_fixture("b", "BOM_UTF8", "pkg/a.py"),
        )
        before = tuple((item.issue_fingerprint, item.evidence_digest) for item in findings)
        build_deterministic_diagnostic_groups(run, findings)
        after = tuple((item.issue_fingerprint, item.evidence_digest) for item in findings)
        self.assertEqual(before, after)
        self.assertEqual(run.scan_identity, "scan-original")

    def test_manual_group_decisions_are_atomic_and_persistent(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            findings = store.list_findings(boundary, run.run_id)
            state = store.get_manual_grouping_state(boundary, run.run_id)
            state = store.create_manual_group(
                boundary,
                run.run_id,
                label="Imports cleanup",
                author="tester",
                reason="Group repeated import findings.",
                expected_generation=state.generation,
            )
            group = state.groups[0]
            state = store.assign_issue_to_manual_group(
                boundary,
                run.run_id,
                findings[0].issue_fingerprint,
                group.group_id,
                author="tester",
                reason="Same reviewed correction family.",
                expected_generation=state.generation,
            )
            self.assertIn(findings[0].issue_fingerprint, state.groups[0].member_issue_fingerprints)
            state = store.mark_manual_group_reviewed(
                boundary,
                run.run_id,
                group.group_id,
                author="tester",
                reason="Evidence reviewed.",
                expected_generation=state.generation,
            )
            self.assertEqual(state.groups[0].review_state, "REVIEWED")
            self.assertEqual(
                {decision.action for decision in state.decisions},
                {"CREATE_GROUP", "ASSIGN_ISSUE", "MARK_REVIEWED"},
            )
            reloaded = store.get_manual_grouping_state(boundary, run.run_id)
            self.assertEqual(reloaded, state)

    def test_move_and_ungroup_retain_append_only_history(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            finding = store.list_findings(boundary, run.run_id)[0]
            state = store.get_manual_grouping_state(boundary, run.run_id)
            for label in ("First", "Second"):
                state = store.create_manual_group(
                    boundary,
                    run.run_id,
                    label=label,
                    author="tester",
                    reason="Create " + label,
                    expected_generation=state.generation,
                )
            first, second = state.groups
            state = store.assign_issue_to_manual_group(
                boundary,
                run.run_id,
                finding.issue_fingerprint,
                first.group_id,
                author="tester",
                reason="Initial assignment.",
                expected_generation=state.generation,
            )
            state = store.assign_issue_to_manual_group(
                boundary,
                run.run_id,
                finding.issue_fingerprint,
                second.group_id,
                author="tester",
                reason="Move after review.",
                expected_generation=state.generation,
            )
            move = next(
                item for item in state.decisions
                if item.action == "ASSIGN_ISSUE" and item.previous_group_id
            )
            self.assertEqual(move.previous_group_id, first.group_id)
            state = store.ungroup_manual_issue(
                boundary,
                run.run_id,
                finding.issue_fingerprint,
                author="tester",
                reason="No longer belongs.",
                expected_generation=state.generation,
            )
            self.assertFalse(any(group.member_issue_fingerprints for group in state.groups))
            self.assertIn("UNGROUP_ISSUE", {item.action for item in state.decisions})

    def test_membership_change_invalidates_review_state(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            findings = store.list_findings(boundary, run.run_id)
            state = store.create_manual_group(
                boundary,
                run.run_id,
                label="Reviewed group",
                author="tester",
                reason="Create group.",
                expected_generation=0,
            )
            group_id = state.groups[0].group_id
            state = store.assign_issue_to_manual_group(
                boundary,
                run.run_id,
                findings[0].issue_fingerprint,
                group_id,
                author="tester",
                reason="Initial member.",
                expected_generation=state.generation,
            )
            state = store.mark_manual_group_reviewed(
                boundary,
                run.run_id,
                group_id,
                author="tester",
                reason="Initial membership reviewed.",
                expected_generation=state.generation,
            )
            self.assertEqual(state.groups[0].review_state, "REVIEWED")
            state = store.assign_issue_to_manual_group(
                boundary,
                run.run_id,
                findings[1].issue_fingerprint,
                group_id,
                author="tester",
                reason="Membership changed.",
                expected_generation=state.generation,
            )
            self.assertEqual(state.groups[0].review_state, "UNREVIEWED")
            self.assertEqual(state.groups[0].reviewed_at_utc, "")

    def test_stale_grouping_generation_fails_closed(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            state = store.get_manual_grouping_state(boundary, run.run_id)
            store.create_manual_group(
                boundary,
                run.run_id,
                label="Current",
                author="tester",
                reason="Create current state.",
                expected_generation=state.generation,
            )
            with self.assertRaises(DiagnosticConflictError):
                store.create_manual_group(
                    boundary,
                    run.run_id,
                    label="Stale",
                    author="tester",
                    reason="Stale operation.",
                    expected_generation=state.generation,
                )

    def test_unknown_issue_and_scope_mismatch_are_rejected(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            state = store.create_manual_group(
                boundary,
                run.run_id,
                label="Group",
                author="tester",
                reason="Create group.",
                expected_generation=0,
            )
            with self.assertRaises(DiagnosticStateError):
                store.assign_issue_to_manual_group(
                    boundary,
                    run.run_id,
                    "unknown-fingerprint",
                    state.groups[0].group_id,
                    author="tester",
                    reason="Invalid issue.",
                    expected_generation=state.generation,
                )


if __name__ == "__main__":
    unittest.main()
