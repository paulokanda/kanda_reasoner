# project-path: tests/test_engineering_diagnostics_wave2r.py
"""Core public-contract tests for Engineering Diagnostics Wave 2R."""

from __future__ import annotations

import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    DiagnosticConflictError,
    DiagnosticLifecycleTarget,
    DiagnosticStateError,
    EngineeringDiagnosticsStore,
    allowed_lifecycle_actions,
    build_deterministic_diagnostic_groups,
    validate_lifecycle_transition,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_disposable_boundary_fixture,
    wave2qa_persisted_run_fixture,
)


def _decision(
    store,
    boundary,
    run_id: str,
    target: DiagnosticLifecycleTarget,
    action: str,
    generation: int,
    **overrides,
):
    values = {
        "reason_code": "HUMAN_REVIEW",
        "rationale": "Reviewed deterministic diagnostic evidence.",
        "author": "tester",
        "expected_generation": generation,
        "revisit_condition": "Review after the next compatible diagnostic run.",
        "related_ticket": "KANDA-2R",
        "related_wave": "",
        "explicit_confirmation": False,
    }
    values.update(overrides)
    return store.record_lifecycle_decision(
        boundary,
        run_id,
        target,
        action=action,
        **values,
    )


class EngineeringDiagnosticsWave2RTests(unittest.TestCase):
    def test_transition_contract_is_deterministic(self) -> None:
        self.assertEqual(validate_lifecycle_transition("OPEN", "CONFIRM"), "CONFIRMED")
        self.assertIn("SUPPRESS", allowed_lifecycle_actions("OPEN"))
        with self.assertRaises(DiagnosticStateError):
            validate_lifecycle_transition("OPEN", "MARK_RESOLVED")

    def test_confirm_issue_persists_append_only_history(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE",
                issue.issue_fingerprint,
                issue.code,
                (issue.issue_fingerprint,),
            )
            state = _decision(store, boundary, run.run_id, target, "CONFIRM", 0)
            self.assertEqual(state.heads[0].current_state, "CONFIRMED")
            self.assertEqual(state.heads[0].generation, 1)
            self.assertEqual(state.decisions[0].previous_state, "OPEN")
            self.assertEqual(state.decisions[0].resulting_state, "CONFIRMED")
            self.assertEqual(store.list_findings(boundary, run.run_id), (issue,) + store.list_findings(boundary, run.run_id)[1:])

    def test_accepted_risk_requires_explicit_confirmation(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            with self.assertRaises(DiagnosticStateError):
                _decision(store, boundary, run.run_id, target, "ACCEPT_RISK", 0)
            state = _decision(
                store,
                boundary,
                run.run_id,
                target,
                "ACCEPT_RISK",
                0,
                explicit_confirmation=True,
                reason_code="ACCEPTED_RISK",
            )
            self.assertEqual(state.heads[0].current_state, "ACCEPTED_RISK")
            self.assertTrue(state.decisions[0].explicit_confirmation)

    def test_suppression_requires_reason_and_revisit_metadata(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            with self.assertRaises(DiagnosticStateError):
                _decision(
                    store,
                    boundary,
                    run.run_id,
                    target,
                    "SUPPRESS",
                    0,
                    rationale="",
                )
            with self.assertRaises(DiagnosticStateError):
                _decision(
                    store,
                    boundary,
                    run.run_id,
                    target,
                    "SUPPRESS",
                    0,
                    revisit_condition="",
                )

    def test_deferred_decision_requires_governed_wave(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            with self.assertRaises(DiagnosticStateError):
                _decision(store, boundary, run.run_id, target, "DEFER", 0)
            state = _decision(
                store,
                boundary,
                run.run_id,
                target,
                "DEFER",
                0,
                related_wave="Wave 2S",
                reason_code="GOVERNED_WAVE_REQUIRED",
            )
            self.assertEqual(state.heads[0].current_state, "DEFERRED")
            self.assertEqual(state.decisions[0].related_wave, "Wave 2S")

    def test_stale_generation_fails_closed(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            _decision(store, boundary, run.run_id, target, "CONFIRM", 0)
            with self.assertRaises(DiagnosticConflictError):
                _decision(store, boundary, run.run_id, target, "PLAN_FIX", 0)

    def test_false_positive_remains_searchable_and_finding_is_retained(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            before = store.list_findings(boundary, run.run_id)
            issue = before[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            state = _decision(
                store,
                boundary,
                run.run_id,
                target,
                "MARK_FALSE_POSITIVE",
                0,
                reason_code="VALIDATED_FALSE_POSITIVE",
            )
            self.assertEqual(state.heads[0].current_state, "FALSE_POSITIVE")
            self.assertEqual(store.list_findings(boundary, run.run_id), before)
            self.assertEqual(
                store.get_lifecycle_state(boundary, run.run_id).decisions[0].target_id,
                issue.issue_fingerprint,
            )

    def test_baseline_acceptance_does_not_accept_risk(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            draft = store.create_draft_baseline(boundary, run.run_id, label="baseline")
            store.activate_baseline(
                boundary,
                draft.baseline_id,
                expected_generation=draft.generation,
            )
            lifecycle = store.get_lifecycle_state(boundary, run.run_id)
            self.assertEqual(lifecycle.heads, ())
            self.assertEqual(lifecycle.decisions, ())

    def test_group_decision_validates_all_current_members(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            findings = store.list_findings(boundary, run.run_id)
            group = build_deterministic_diagnostic_groups(run, findings)[0]
            target = DiagnosticLifecycleTarget(
                "GROUP",
                group.group_id,
                group.label,
                group.member_issue_fingerprints,
            )
            state = _decision(store, boundary, run.run_id, target, "CONFIRM", 0)
            self.assertEqual(state.heads[0].target_kind, "GROUP")
            self.assertEqual(state.heads[0].target_id, group.group_id)
            invalid = DiagnosticLifecycleTarget(
                "GROUP",
                "invented",
                "Invented",
                ("missing-fingerprint",),
            )
            with self.assertRaises(DiagnosticStateError):
                _decision(store, boundary, run.run_id, invalid, "CONFIRM", 0)

    def test_terminal_decision_can_be_reopened_with_history(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            state = _decision(store, boundary, run.run_id, target, "SUPPRESS", 0)
            state = _decision(store, boundary, run.run_id, target, "REOPEN", 1)
            self.assertEqual(state.heads[0].current_state, "REOPENED")
            self.assertEqual(
                [item.action for item in reversed(state.decisions)],
                ["SUPPRESS", "REOPEN"],
            )

    def test_expiration_or_revisit_condition_is_mandatory(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = wave2qa_persisted_run_fixture(store, boundary)
            issue = store.list_findings(boundary, run.run_id)[0]
            target = DiagnosticLifecycleTarget(
                "ISSUE", issue.issue_fingerprint, issue.code, (issue.issue_fingerprint,)
            )
            with self.assertRaises(DiagnosticStateError):
                _decision(
                    store,
                    boundary,
                    run.run_id,
                    target,
                    "CONFIRM",
                    0,
                    revisit_condition="",
                    expires_at_utc="",
                )


if __name__ == "__main__":
    unittest.main()
