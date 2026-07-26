# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_fixture_catalog.py
"""Synthetic Phase 3 offline fixture catalog.

These fixtures are hand-authored, synthetic, in-memory, and caller-supplied in
shape. They are not harvested from real prompts, prompt library files, freeze
memory, router canon, telemetry, or provider output.
"""

from __future__ import annotations

from .contract import AdvisoryInput
from .fixture_catalog_contract import (
    FEATURE_ID,
    OfflineFixtureCatalog,
    OfflineFixtureCatalogEntry,
    OfflineFixtureIntent,
)
from .offline_evaluation_contract import (
    OfflineEvaluationFixture,
    OfflineEvaluationStatus,
)


CATALOG_ID = "phase3_synthetic_offline_fixture_catalog_v1"
_SAFE_SCOPE = (
    "synthetic_only",
    "in_memory_only",
    "no_prompt_library_read",
    "no_freeze_memory_read",
    "no_router_canon_read",
    "no_route_authority",
)


def build_phase3_synthetic_fixture_catalog() -> OfflineFixtureCatalog:
    """Build the immutable synthetic fixture catalog for offline evaluation."""

    entries = (
        _entry(
            entry_id="phase3_low_signal_control_001",
            intent=OfflineFixtureIntent.LOW_SIGNAL_CONTROL,
            ambiguity_score=0.05,
            conflict_score=0.05,
            candidate_group_ids=("synthetic_group_alpha",),
            risk_family_id=None,
            before="governed_choice_alpha",
            after="governed_choice_alpha",
            expected_status=OfflineEvaluationStatus.PASSED,
        ),
        _entry(
            entry_id="phase3_ambiguity_signal_001",
            intent=OfflineFixtureIntent.AMBIGUITY_SIGNAL,
            ambiguity_score=0.85,
            conflict_score=0.10,
            candidate_group_ids=("synthetic_group_alpha", "synthetic_group_beta"),
            risk_family_id=None,
            before="governed_choice_beta",
            after="governed_choice_beta",
            expected_status=OfflineEvaluationStatus.PASSED,
        ),
        _entry(
            entry_id="phase3_conflict_signal_001",
            intent=OfflineFixtureIntent.CONFLICT_SIGNAL,
            ambiguity_score=0.25,
            conflict_score=0.90,
            candidate_group_ids=("synthetic_group_gamma", "synthetic_group_delta"),
            risk_family_id=None,
            before="governed_choice_gamma",
            after="governed_choice_gamma",
            expected_status=OfflineEvaluationStatus.PASSED,
        ),
        _entry(
            entry_id="phase3_prompt_gap_signal_001",
            intent=OfflineFixtureIntent.PROMPT_GAP_SIGNAL,
            ambiguity_score=0.80,
            conflict_score=0.20,
            candidate_group_ids=("synthetic_group_epsilon",),
            risk_family_id="prompt_gap",
            before="governed_choice_delta",
            after="governed_choice_delta",
            expected_status=OfflineEvaluationStatus.PASSED,
        ),
        _entry(
            entry_id="phase3_route_variance_rejection_001",
            intent=OfflineFixtureIntent.ROUTE_VARIANCE_REJECTION,
            ambiguity_score=0.70,
            conflict_score=0.70,
            candidate_group_ids=("synthetic_group_zeta", "synthetic_group_eta"),
            risk_family_id=None,
            before="governed_choice_before_variance",
            after="governed_choice_after_variance",
            expected_status=OfflineEvaluationStatus.REJECTED_ROUTE_VARIANCE,
        ),
    )
    return OfflineFixtureCatalog(
        catalog_id=CATALOG_ID,
        feature_id=FEATURE_ID,
        entries=entries,
        catalog_scope=(
            "synthetic caller-supplied-shape offline fixtures only; no real "
            "prompt-selection cases; no runtime integration"
        ),
    )


def _entry(
    *,
    entry_id: str,
    intent: OfflineFixtureIntent,
    ambiguity_score: float,
    conflict_score: float,
    candidate_group_ids: tuple[str, ...],
    risk_family_id: str | None,
    before: str,
    after: str,
    expected_status: OfflineEvaluationStatus,
) -> OfflineFixtureCatalogEntry:
    """Support entry behavior.
    
    Parameters
    ----------
    entry_id : str
        The entry id value.
    intent : OfflineFixtureIntent
        The intent value.
    ambiguity_score : float
        The ambiguity score value.
    conflict_score : float
        The conflict score value.
    candidate_group_ids : tuple[str, ...]
        The candidate group ids value.
    risk_family_id : str | None
        The risk family id value.
    before : str
        The before value.
    after : str
        The after value.
    expected_status : OfflineEvaluationStatus
        The expected status value.
    
    Returns
    -------
    OfflineFixtureCatalogEntry
        The offline fixture catalog entry result.
    """
    
    fixture = OfflineEvaluationFixture(
        fixture_id=entry_id,
        advisory_input=AdvisoryInput(
            scenario_id=entry_id,
            sanitized_context_hash="synthetic_hash_" + entry_id,
            candidate_prompt_group_ids=candidate_group_ids,
            ambiguity_score=ambiguity_score,
            conflict_score=conflict_score,
            risk_family_id=risk_family_id,
        ),
        governed_decision_before_advisory=before,
        governed_decision_after_advisory=after,
    )
    return OfflineFixtureCatalogEntry(
        catalog_entry_id=entry_id,
        intent=intent,
        fixture=fixture,
        expected_status=expected_status,
        expected_route_invariant=(before == after),
        safety_scope_codes=_SAFE_SCOPE,
    )
