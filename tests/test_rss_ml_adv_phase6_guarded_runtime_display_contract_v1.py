from dataclasses import FrozenInstanceError

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.guarded_runtime_display_contract import (
    FEATURE_ID,
    GuardedRuntimeAdvisoryDisplayPolicy,
    GuardedRuntimeAdvisoryDisplayStatus,
    evaluate_guarded_runtime_display_contract,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_guarded_runtime_display import (
    build_phase6_guarded_display_contract_probe,
)


def _safe_policy(**overrides):
    values = {
        "display_label": "safe_display_contract",
        "source_contract_id": "advisory_output_v1_bounded_flags_only",
        "prerequisite_feature_id": (
            "rss_ml_adv_phase5_real_adapter_candidate_result_review_gate_v1"
        ),
        "allowed_surface": "contract_only_read_only_telemetry_shape",
        "allowed_display_fields": (
            "advisory_status",
            "abstain_reason_codes",
            "boundary_status",
        ),
        "allowed_failure_states": (
            "advisor_unavailable",
            "advisor_abstained",
            "boundary_rejected",
        ),
    }
    values.update(overrides)
    return GuardedRuntimeAdvisoryDisplayPolicy(**values)


def test_phase6_probe_is_accepted_as_contract_only_not_runtime_display():
    decision = build_phase6_guarded_display_contract_probe()

    assert decision.feature_id == FEATURE_ID
    assert decision.status == GuardedRuntimeAdvisoryDisplayStatus.ACCEPTED_CONTRACT_ONLY
    assert decision.accepted is True
    assert decision.forbidden_capabilities == ()
    assert decision.contract_only is True
    assert decision.read_only is True
    assert decision.telemetry_only is True
    assert decision.route_invariant is True
    assert decision.final_selection_invisible is True
    assert decision.non_authoritative is True
    assert decision.runtime_display_enabled is False
    assert decision.runtime_advisory_panel_enabled is False
    assert decision.route_authority_enabled is False


def test_phase6_contract_rejects_missing_required_guard():
    try:
        _safe_policy(route_invariant=False)
        raise AssertionError("route_invariant False was accepted")
    except ValueError as exc:
        assert "route_invariant" in str(exc)


def test_phase6_contract_rejects_forbidden_capabilities():
    policy = _safe_policy(
        runtime_display_implementation_enabled=True,
        runtime_advisory_panel_enabled=True,
        provider_calls_enabled=True,
        route_authority_enabled=True,
        runtime_copilot_behavior_enabled=True,
    )
    decision = evaluate_guarded_runtime_display_contract(policy)

    assert decision.accepted is False
    assert decision.status == GuardedRuntimeAdvisoryDisplayStatus.REJECTED_FORBIDDEN_CAPABILITY
    assert "runtime_display_implementation_enabled" in decision.forbidden_capabilities
    assert "runtime_advisory_panel_enabled" in decision.forbidden_capabilities
    assert "provider_calls_enabled" in decision.forbidden_capabilities
    assert "route_authority_enabled" in decision.forbidden_capabilities
    assert "runtime_copilot_behavior_enabled" in decision.forbidden_capabilities


def test_phase6_contract_is_immutable():
    policy = _safe_policy()
    decision = evaluate_guarded_runtime_display_contract(policy)

    try:
        policy.display_label = "mutated"
        raise AssertionError("policy mutation unexpectedly succeeded")
    except FrozenInstanceError:
        pass

    try:
        decision.accepted = False
        raise AssertionError("decision mutation unexpectedly succeeded")
    except FrozenInstanceError:
        pass


def main():
    test_phase6_probe_is_accepted_as_contract_only_not_runtime_display()
    test_phase6_contract_rejects_missing_required_guard()
    test_phase6_contract_rejects_forbidden_capabilities()
    test_phase6_contract_is_immutable()


if __name__ == "__main__":
    main()
    print("VALIDATION OK: rss_ml_adv_phase6_guarded_runtime_advisory_display_contract_v1")
