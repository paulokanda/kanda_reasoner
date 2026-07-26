# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_guarded_runtime_display.py
"""Offline probe for Phase 6 guarded display contract.

The probe builds an accepted contract-only decision without implementing a
runtime display and without reading files, opening network resources, calling
providers, executing adapters, or selecting routes.
"""

from __future__ import annotations

from .guarded_runtime_display_contract import (
    GuardedRuntimeAdvisoryDisplayDecision,
    GuardedRuntimeAdvisoryDisplayPolicy,
    evaluate_guarded_runtime_display_contract,
)


def build_phase6_guarded_display_contract_probe() -> GuardedRuntimeAdvisoryDisplayDecision:
    """Build the safe contract-only Phase 6 display probe."""

    policy = GuardedRuntimeAdvisoryDisplayPolicy(
        display_label="phase6_contract_only_probe",
        source_contract_id="advisory_output_v1_bounded_flags_only",
        prerequisite_feature_id=(
            "rss_ml_adv_phase5_real_adapter_candidate_result_review_gate_v1"
        ),
        allowed_surface="contract_only_read_only_telemetry_shape",
        allowed_display_fields=(
            "advisory_status",
            "abstain_reason_codes",
            "boundary_status",
        ),
        allowed_failure_states=(
            "advisor_unavailable",
            "advisor_abstained",
            "boundary_rejected",
        ),
    )
    return evaluate_guarded_runtime_display_contract(policy)
