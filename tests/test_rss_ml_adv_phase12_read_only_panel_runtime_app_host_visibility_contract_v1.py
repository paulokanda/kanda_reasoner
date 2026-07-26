from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_app_host_visibility_contract import (
    FEATURE_ID,
    ReadOnlyPanelRuntimeAppHostVisibilityMode,
    ReadOnlyPanelRuntimeAppHostVisibilityStatus,
    build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract,
    build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe,
    evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request,
)


def test_phase12_contract_accepts_future_visibility_contract_only():
    decision = build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract()
    assert decision.feature_id == FEATURE_ID
    assert decision.accepted is True
    assert decision.contract_only is True
    assert decision.future_runtime_app_host_visibility_contract_ready is True
    assert decision.visibility_mode is ReadOnlyPanelRuntimeAppHostVisibilityMode.FUTURE_READ_ONLY_RUNTIME_APP_HOST_VISIBILITY
    assert decision.status is ReadOnlyPanelRuntimeAppHostVisibilityStatus.ACCEPTED_FUTURE_READ_ONLY_RUNTIME_APP_HOST_VISIBILITY_CONTRACT
    assert decision.source_descriptor_safe is True
    assert decision.phase11_host_binding_descriptor_input_required is True
    assert decision.explicit_feature_flag_required is True
    assert decision.feature_flag_default_enabled is False
    assert decision.disabled_noop_control_required is True
    assert decision.fail_open_on_missing_descriptor_required is True
    assert decision.block_unsafe_descriptor_required is True
    assert decision.runtime_visibility_input_bounded_required is True
    assert decision.runtime_visibility_output_bounded_required is True
    assert decision.removable_noop_visibility_required is True
    assert decision.route_invariant_visibility_required is True
    assert decision.final_selection_invisible_visibility_required is True
    assert decision.non_training_feedback_slot_required is True
    assert decision.actual_runtime_app_host_visibility_enabled is False
    assert decision.runtime_app_host_visibility_activation_enabled is False
    assert decision.mounted_runtime_panel_enabled is False
    assert decision.runtime_panel_mount_side_effects_enabled is False
    assert decision.runtime_ui_mutation_enabled is False
    assert decision.runtime_telemetry_surface_wiring_enabled is False
    assert decision.host_event_subscription_enabled is False
    assert decision.host_callback_registration_enabled is False
    assert decision.route_influence_enabled is False
    assert decision.route_authority_enabled is False
    assert decision.router_calls_enabled is False
    assert decision.advisor_calls_enabled is False
    assert decision.provider_calls_enabled is False
    assert decision.persistence_enabled is False
    assert decision.runtime_copilot_decision_behavior_enabled is False
    assert decision.autonomous_ml_router_enabled is False
    assert decision.critical_boundary_error_budget == 0


def test_phase12_contract_blocks_runtime_visibility_side_effects_and_route_authority():
    unsafe_visibility = evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request({
        "capabilities": ["actual_runtime_app_host_visibility"]
    })
    assert unsafe_visibility.accepted is False
    assert unsafe_visibility.status is ReadOnlyPanelRuntimeAppHostVisibilityStatus.BLOCKED_UNSAFE_RUNTIME_VISIBILITY
    assert unsafe_visibility.actual_runtime_app_host_visibility_enabled is False
    assert unsafe_visibility.runtime_ui_mutation_enabled is False

    unsafe_authority = evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request({
        "route_authority": True,
    })
    assert unsafe_authority.accepted is False
    assert unsafe_authority.status is ReadOnlyPanelRuntimeAppHostVisibilityStatus.BLOCKED_UNSAFE_AUTHORITY
    assert unsafe_authority.route_authority_enabled is False
    assert unsafe_authority.route_influence_enabled is False


def test_phase12_probe_remains_non_authoritative_and_contract_only():
    decision = build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe()
    assert decision.accepted is True
    assert decision.contract_only is True
    assert decision.actual_runtime_app_host_visibility_enabled is False
    assert decision.mounted_runtime_panel_enabled is False
    assert decision.router_calls_enabled is False
    assert decision.advisor_calls_enabled is False
    assert decision.runtime_copilot_decision_behavior_enabled is False
    assert decision.autonomous_ml_router_enabled is False


if __name__ == "__main__":
    test_phase12_contract_accepts_future_visibility_contract_only()
    test_phase12_contract_blocks_runtime_visibility_side_effects_and_route_authority()
    test_phase12_probe_remains_non_authoritative_and_contract_only()
    print("VALIDATION OK: phase12 read-only advisory panel runtime app-host visibility contract")
