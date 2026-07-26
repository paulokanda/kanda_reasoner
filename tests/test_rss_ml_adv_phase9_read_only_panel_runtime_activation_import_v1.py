from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    ReadOnlyPanelRuntimeActivationMode,
    ReadOnlyPanelRuntimeActivationStatus,
    build_phase9_read_only_panel_runtime_activation_contract_probe,
    evaluate_phase9_read_only_advisory_panel_runtime_activation_request,
)


def test_phase9_runtime_activation_import_boundary():
    policy = ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_mode=ReadOnlyPanelRuntimeActivationMode.FUTURE_READ_ONLY_RUNTIME_PANEL,
    )
    decision = build_phase9_read_only_panel_runtime_activation_contract_probe()
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelRuntimeActivationStatus.ACCEPTED_FUTURE_READ_ONLY_RUNTIME_PANEL_CONTRACT
    assert decision.actual_runtime_panel_activation_enabled is False
    blocked = evaluate_phase9_read_only_advisory_panel_runtime_activation_request(
        policy=policy,
        requested_capabilities={"route_authority": True},
    )
    assert blocked.accepted is False
    assert blocked.route_authority_enabled is False


if __name__ == "__main__":
    test_phase9_runtime_activation_import_boundary()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation import boundary")
