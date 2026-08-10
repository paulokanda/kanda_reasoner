# project-path: tests/test_engineering_diagnostics_wave2s.py
"""Core public-contract tests for Engineering Diagnostics Wave 2S."""

from __future__ import annotations

from dataclasses import replace
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    AI_HYPOTHESIS_LABEL,
    ARCHITECTURE_PRODUCER_ID,
    BOM_PRODUCER_ID,
    REMEDIATION_ACTION_CLASSES,
    REMEDIATION_TRUST_ORDER,
    RUFF_PRODUCER_ID,
    SHADOW_PRODUCER_ID,
    DiagnosticAiHypothesis,
    DiagnosticFindingEnrichment,
    DiagnosticFrozenPathEnrichment,
    DiagnosticLifecycleHead,
    DiagnosticOwnerEnrichment,
    DiagnosticScopeEnrichment,
    build_diagnostic_remediation_intent,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_finding_fixture,
    wave2qa_run_record_fixture,
)


def _enrichment(
    *,
    scope: str = "ACTIVE",
    frozen: str = "UNFROZEN",
    owner_status: str = "READY",
    owner: str = "pkg.module",
    freeze_ids: tuple[str, ...] = (),
) -> DiagnosticFindingEnrichment:
    confidence = "high" if scope != "UNKNOWN" else "low"
    owner_confidence = "high" if owner_status == "READY" else "none"
    return DiagnosticFindingEnrichment(
        scope=DiagnosticScopeEnrichment(scope, confidence, "fixture", ("scope",)),
        frozen_path=DiagnosticFrozenPathEnrichment(
            frozen,
            governing_freeze_ids=freeze_ids,
            matched_protected_paths=("pkg/module.py",) if freeze_ids else (),
            evidence=("freeze",),
        ),
        owner=DiagnosticOwnerEnrichment(
            owner_status,
            owner_confidence,
            canonical_owner=owner if owner_status == "READY" else "",
            evidence=("owner",),
        ),
    )


def _head(state: str) -> DiagnosticLifecycleHead:
    return DiagnosticLifecycleHead(
        project_id="project-id-2qa",
        producer_id=RUFF_PRODUCER_ID,
        scope_fingerprint="scope-original",
        target_kind="ISSUE",
        target_id="issue-1",
        target_label="F401",
        current_state=state,
        generation=1,
    )


def _ruff_finding(*, safe: bool = True):
    return wave2qa_finding_fixture(
        "issue-1",
        "F401",
        "pkg/module.py",
        symbol="module.target",
        evidence={
            "fix_available": True,
            "fix_applicability": "safe" if safe else "unsafe",
            "fix_message": "Remove unused import.",
            "fix_edit_count": 1,
            "fix_executed": False,
        },
    )


class EngineeringDiagnosticsWave2STests(unittest.TestCase):
    def test_action_class_taxonomy_matches_roadmap(self) -> None:
        self.assertEqual(
            REMEDIATION_ACTION_CLASSES,
            frozenset(
                {
                    "FIX_NOW",
                    "PLAN_GOVERNED_WAVE",
                    "HUMAN_DECISION_REQUIRED",
                    "EVIDENCE_REQUIRED",
                    "SAFE_MECHANICAL_FIX_AVAILABLE",
                    "DEFERRED_TECHNICAL_DEBT",
                    "SUPPRESS_WITH_JUSTIFICATION",
                    "DO_NOT_TOUCH",
                }
            ),
        )

    def test_trust_order_is_fixed_and_ai_is_last(self) -> None:
        self.assertEqual(REMEDIATION_TRUST_ORDER[0], "TOOL_DETERMINISTIC_METADATA")
        self.assertEqual(REMEDIATION_TRUST_ORDER[-1], "AI_ASSISTED_HYPOTHESIS")

    def test_safe_ruff_fix_is_advice_not_execution(self) -> None:
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
            _ruff_finding(),
            _enrichment(),
        )
        self.assertEqual(intent.action_class, "SAFE_MECHANICAL_FIX_AVAILABLE")
        self.assertEqual(intent.mechanical_safety, "SAFE_MECHANICAL")
        self.assertFalse(intent.executable_patch)
        self.assertFalse(intent.source_mutation_allowed)
        self.assertIn("fix_executed=False", intent.deterministic_evidence)

    def test_bom_exact_file_is_safe_mechanical_candidate(self) -> None:
        finding = wave2qa_finding_fixture("bom-1", "UTF8_BOM", "pkg/module.py")
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(BOM_PRODUCER_ID), finding_count=1),
            replace(finding, suggested_action="Remove the exact UTF-8 BOM."),
            _enrichment(),
        )
        self.assertEqual(intent.action_class, "SAFE_MECHANICAL_FIX_AVAILABLE")
        self.assertEqual(intent.fix_applicability, "EXACT_FILE")

    def test_frozen_path_overrides_safe_fix_and_ai_hypothesis(self) -> None:
        hypothesis = DiagnosticAiHypothesis(
            text="Apply the safe Ruff edit immediately.",
            supporting_issue_fingerprints=("issue-1",),
            deterministic_evidence_refs=("issue_fingerprint=issue-1",),
        )
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
            _ruff_finding(),
            _enrichment(frozen="FROZEN", freeze_ids=("freeze-2r",)),
            ai_hypothesis=hypothesis,
        )
        self.assertEqual(intent.action_class, "PLAN_GOVERNED_WAVE")
        self.assertEqual(intent.mechanical_safety, "BLOCKED_BY_FREEZE")
        self.assertEqual(intent.ai_hypothesis.label, AI_HYPOTHESIS_LABEL)

    def test_owner_needs_review_blocks_mechanical_advice(self) -> None:
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
            _ruff_finding(),
            _enrichment(owner_status="NEEDS_REVIEW", owner=""),
        )
        self.assertEqual(intent.action_class, "HUMAN_DECISION_REQUIRED")
        self.assertEqual(intent.semantic_review_requirement, "OWNER_REVIEW_REQUIRED")

    def test_missing_owner_requires_evidence(self) -> None:
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(ARCHITECTURE_PRODUCER_ID), finding_count=1),
            wave2qa_finding_fixture("arch-1", "BOUNDARY", "pkg/module.py"),
            _enrichment(owner_status="NO_OWNER", owner=""),
        )
        self.assertEqual(intent.action_class, "EVIDENCE_REQUIRED")
        self.assertEqual(intent.canonical_owner, "")

    def test_non_active_generated_source_is_do_not_touch(self) -> None:
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
            _ruff_finding(),
            _enrichment(scope="GENERATED"),
        )
        self.assertEqual(intent.action_class, "DO_NOT_TOUCH")
        self.assertEqual(intent.fix_applicability, "NOT_APPLICABLE")

    def test_accepted_risk_is_not_silently_reopened(self) -> None:
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
            _ruff_finding(),
            _enrichment(),
            lifecycle_head=_head("ACCEPTED_RISK"),
        )
        self.assertEqual(intent.action_class, "DO_NOT_TOUCH")

    def test_suppressed_finding_retains_justification_action(self) -> None:
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
            _ruff_finding(),
            _enrichment(),
            lifecycle_head=_head("SUPPRESSED"),
        )
        self.assertEqual(intent.action_class, "SUPPRESS_WITH_JUSTIFICATION")

    def test_deferred_finding_retains_governed_wave_requirement(self) -> None:
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
            _ruff_finding(),
            _enrichment(),
            lifecycle_head=_head("DEFERRED"),
        )
        self.assertEqual(intent.action_class, "DEFERRED_TECHNICAL_DEBT")
        self.assertEqual(intent.required_governed_wave, "LIFECYCLE_RELATED_WAVE")

    def test_shadow_finding_requires_semantic_human_review(self) -> None:
        finding = wave2qa_finding_fixture(
            "shadow-1",
            "DUPLICATE_PUBLIC_SYMBOL",
            "ARCHITECTURE.md",
            evidence={"symbol": "Thing", "owners": ["a.py", "b.py"]},
        )
        intent = build_diagnostic_remediation_intent(
            replace(wave2qa_run_record_fixture(SHADOW_PRODUCER_ID), finding_count=1),
            finding,
            _enrichment(),
        )
        self.assertEqual(intent.action_class, "HUMAN_DECISION_REQUIRED")
        self.assertEqual(intent.mechanical_safety, "SEMANTIC_REVIEW_REQUIRED")

    def test_ai_hypothesis_requires_exact_label_and_deterministic_citation(self) -> None:
        with self.assertRaises(ValueError):
            DiagnosticAiHypothesis(
                text="Guess",
                supporting_issue_fingerprints=("issue-1",),
                deterministic_evidence_refs=("evidence",),
                label="AI recommendation",
            )
        with self.assertRaises(ValueError):
            build_diagnostic_remediation_intent(
                replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=1),
                _ruff_finding(),
                _enrichment(),
                ai_hypothesis=DiagnosticAiHypothesis(
                    text="Guess",
                    supporting_issue_fingerprints=("other",),
                    deterministic_evidence_refs=("evidence",),
                ),
            )

    def test_intent_identity_is_stable_across_compatible_runs(self) -> None:
        first = replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID, "run-a"), finding_count=1)
        second = replace(first, run_id="run-b", attempt_id="attempt-b")
        finding_a = _ruff_finding()
        finding_b = replace(finding_a, run_id="run-b")
        self.assertEqual(
            build_diagnostic_remediation_intent(first, finding_a, _enrichment()).intent_id,
            build_diagnostic_remediation_intent(second, finding_b, _enrichment()).intent_id,
        )


if __name__ == "__main__":
    unittest.main()
