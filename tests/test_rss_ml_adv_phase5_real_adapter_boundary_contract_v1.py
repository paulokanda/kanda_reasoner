from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.real_adapter_boundary_contract import (
    FEATURE_ID,
    RealAdapterBoundaryStatus,
    RealAdapterDescriptor,
    evaluate_real_adapter_boundary,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.offline_real_adapter_boundary import (
    build_phase5_offline_real_adapter_boundary_probe,
)


def test_phase5_accepts_descriptor_only_adapter_boundary():
    descriptor = RealAdapterDescriptor(
        adapter_label="safe_descriptor",
        adapter_kind="future_adapter_metadata_only",
        declared_input_contract_id="advisory_input_v1",
        declared_output_contract_id="advisory_output_v1",
    )
    decision = evaluate_real_adapter_boundary(descriptor)
    assert decision.feature_id == FEATURE_ID
    assert decision.accepted is True
    assert decision.status == RealAdapterBoundaryStatus.ACCEPTED_DESCRIPTOR_ONLY
    assert decision.forbidden_capabilities == ()
    assert decision.offline_descriptor_only is True
    assert decision.non_runtime is True
    assert decision.non_authoritative is True
    assert "no_provider_calls" in decision.boundary_notes
    assert "no_route_authority" in decision.boundary_notes


def test_phase5_rejects_forbidden_provider_capability():
    descriptor = RealAdapterDescriptor(
        adapter_label="unsafe_descriptor",
        adapter_kind="future_adapter_metadata_only",
        declared_input_contract_id="advisory_input_v1",
        declared_output_contract_id="advisory_output_v1",
        provider_calls_enabled=True,
    )
    decision = evaluate_real_adapter_boundary(descriptor)
    assert decision.accepted is False
    assert decision.status == RealAdapterBoundaryStatus.REJECTED_FORBIDDEN_CAPABILITY
    assert "provider_calls_enabled" in decision.forbidden_capabilities
    assert "forbidden_capability_rejected" in decision.boundary_notes


def test_phase5_probe_is_descriptor_only():
    decision = build_phase5_offline_real_adapter_boundary_probe()
    assert decision.accepted is True
    assert decision.forbidden_capabilities == ()
    assert decision.adapter_label == "phase5_offline_real_adapter_boundary_probe"


print("VALIDATION OK: test_rss_ml_adv_phase5_real_adapter_boundary_contract_v1")
