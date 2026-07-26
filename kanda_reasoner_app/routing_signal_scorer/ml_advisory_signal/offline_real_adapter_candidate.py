# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_real_adapter_candidate.py
"""Offline helper for Phase 5 real-adapter candidate probes.

The helper builds a fixture-bound candidate descriptor and evaluates the
contract. It never executes an adapter and never calls a provider.
"""

from __future__ import annotations

from .offline_real_adapter_boundary import (
    build_phase5_offline_real_adapter_boundary_probe,
)
from .real_adapter_candidate_contract import (
    RealAdapterCandidateDecision,
    RealAdapterCandidateDescriptor,
    evaluate_real_adapter_candidate,
)


PHASE5_CANDIDATE_LABEL = "phase5_offline_real_adapter_candidate_probe"


def build_phase5_offline_candidate_probe() -> RealAdapterCandidateDecision:
    """Build a safe fixture-bound candidate boundary decision."""

    boundary_decision = build_phase5_offline_real_adapter_boundary_probe()
    descriptor = RealAdapterCandidateDescriptor(
        candidate_label=PHASE5_CANDIDATE_LABEL,
        candidate_family="fixture_bound_offline_candidate_envelope",
        boundary_decision=boundary_decision,
        declared_fixture_scope="phase3_synthetic_fixture_catalog_only",
        declared_evaluation_contract_id=(
            "rss_ml_adv_phase2_offline_evaluation_harness_contract_v1"
        ),
        allowed_output_contract_id="advisory_output_v1_bounded_flags_only",
        allowed_reason_codes=(
            "AMBIGUOUS_REQUEST",
            "MISSING_REQUIRED_CONTEXT",
            "CONFLICTING_SIGNALS",
            "NO_RELEVANT_SIGNAL",
        ),
    )
    return evaluate_real_adapter_candidate(descriptor)
