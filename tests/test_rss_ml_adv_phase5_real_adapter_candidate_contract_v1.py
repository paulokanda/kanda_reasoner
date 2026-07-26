from dataclasses import FrozenInstanceError

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_real_adapter_candidate import (
    build_phase5_offline_candidate_probe,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.real_adapter_boundary_contract import (
    RealAdapterDescriptor,
    evaluate_real_adapter_boundary,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.real_adapter_candidate_contract import (
    FEATURE_ID,
    RealAdapterCandidateDescriptor,
    RealAdapterCandidateStatus,
    evaluate_real_adapter_candidate,
)


def _safe_boundary_decision():
    descriptor = RealAdapterDescriptor(
        adapter_label="safe_boundary",
        adapter_kind="descriptor_only_future_adapter_boundary",
        declared_input_contract_id="advisory_input_v1_offline_only",
        declared_output_contract_id="advisory_output_v1_bounded_flags_only",
    )
    return evaluate_real_adapter_boundary(descriptor)


def _safe_candidate_descriptor(**overrides):
    values = {
        "candidate_label": "safe_candidate",
        "candidate_family": "fixture_bound_offline_candidate_envelope",
        "boundary_decision": _safe_boundary_decision(),
        "declared_fixture_scope": "phase3_synthetic_fixture_catalog_only",
        "declared_evaluation_contract_id": (
            "rss_ml_adv_phase2_offline_evaluation_harness_contract_v1"
        ),
        "allowed_output_contract_id": "advisory_output_v1_bounded_flags_only",
        "allowed_reason_codes": ("AMBIGUOUS_REQUEST", "NO_RELEVANT_SIGNAL"),
    }
    values.update(overrides)
    return RealAdapterCandidateDescriptor(**values)


def test_candidate_probe_is_accepted_but_not_runtime_copilot():
    decision = build_phase5_offline_candidate_probe()

    assert decision.feature_id == FEATURE_ID
    assert decision.status == RealAdapterCandidateStatus.ACCEPTED_OFFLINE_CANDIDATE
    assert decision.accepted is True
    assert decision.forbidden_capabilities == ()
    assert decision.offline_fixture_bound_only is True
    assert decision.offline_descriptor_only is True
    assert decision.non_runtime is True
    assert decision.non_authoritative is True


def test_candidate_rejects_rejected_boundary_decision():
    bad_boundary = evaluate_real_adapter_boundary(
        RealAdapterDescriptor(
            adapter_label="bad_boundary",
            adapter_kind="descriptor_only_future_adapter_boundary",
            declared_input_contract_id="advisory_input_v1_offline_only",
            declared_output_contract_id="advisory_output_v1_bounded_flags_only",
            provider_calls_enabled=True,
        )
    )
    descriptor = _safe_candidate_descriptor(boundary_decision=bad_boundary)
    decision = evaluate_real_adapter_candidate(descriptor)

    assert decision.accepted is False
    assert decision.status == RealAdapterCandidateStatus.REJECTED_BOUNDARY_DECISION
    assert decision.forbidden_capabilities == ("boundary_decision_not_accepted",)


def test_candidate_rejects_forbidden_capabilities():
    descriptor = _safe_candidate_descriptor(
        candidate_execution_enabled=True,
        provider_calls_enabled=True,
        route_authority_enabled=True,
        runtime_copilot_behavior_enabled=True,
    )
    decision = evaluate_real_adapter_candidate(descriptor)

    assert decision.accepted is False
    assert decision.status == RealAdapterCandidateStatus.REJECTED_FORBIDDEN_CAPABILITY
    assert "candidate_execution_enabled" in decision.forbidden_capabilities
    assert "provider_calls_enabled" in decision.forbidden_capabilities
    assert "route_authority_enabled" in decision.forbidden_capabilities
    assert "runtime_copilot_behavior_enabled" in decision.forbidden_capabilities


def test_candidate_contract_is_immutable():
    descriptor = _safe_candidate_descriptor()
    decision = evaluate_real_adapter_candidate(descriptor)

    try:
        descriptor.candidate_label = "mutated"
        raise AssertionError("descriptor mutation unexpectedly succeeded")
    except FrozenInstanceError:
        pass

    try:
        decision.accepted = False
        raise AssertionError("decision mutation unexpectedly succeeded")
    except FrozenInstanceError:
        pass


def test_candidate_descriptor_invariants():
    try:
        _safe_candidate_descriptor(offline_fixture_bound_only=False)
        raise AssertionError("offline_fixture_bound_only False was accepted")
    except ValueError as exc:
        assert "offline_fixture_bound_only" in str(exc)

    try:
        _safe_candidate_descriptor(non_runtime=False)
        raise AssertionError("non_runtime False was accepted")
    except ValueError as exc:
        assert "non_runtime" in str(exc)


def main():
    test_candidate_probe_is_accepted_but_not_runtime_copilot()
    test_candidate_rejects_rejected_boundary_decision()
    test_candidate_rejects_forbidden_capabilities()
    test_candidate_contract_is_immutable()
    test_candidate_descriptor_invariants()


if __name__ == "__main__":
    main()
