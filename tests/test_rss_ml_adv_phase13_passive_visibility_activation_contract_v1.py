from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_passive_visibility_activation_contract import (
    FEATURE_ID,
    ReadOnlyPanelPassiveVisibilityActivationMode,
    ReadOnlyPanelPassiveVisibilityActivationStatus,
    build_phase13_read_only_advisory_panel_passive_visibility_activation_contract,
    build_phase13_read_only_panel_passive_visibility_activation_contract_probe,
    evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request,
)


def test_phase13_contract_accepts_future_passive_visibility_activation_contract_only():
    decision = build_phase13_read_only_advisory_panel_passive_visibility_activation_contract()
    assert decision.feature_id == FEATURE_ID
    assert decision.accepted is True
    assert decision.contract_only is True
    assert decision.future_passive_visibility_activation_contract_ready is True
    assert decision.activation_mode is ReadOnlyPanelPassiveVisibilityActivationMode.FUTURE_PASSIVE_VISIBILITY_ACTIVATION
    assert decision.status is ReadOnlyPanelPassiveVisibilityActivationStatus.ACCEPTED_FUTURE_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT
    assert decision.source_descriptor_safe is True
    assert decision.phase12_runtime_app_host_visibility_descriptor_input_required is True
    assert decision.explicit_feature_flag_required is True
    assert decision.feature_flag_default_enabled is False
    assert decision.disabled_noop_control_required is True
    assert decision.fail_open_on_missing_descriptor_required is True
    assert decision.block_unsafe_descriptor_required is True
    assert decision.bounded_passive_visibility_input_required is True
    assert decision.bounded_passive_visibility_output_required is True
    assert decision.read_only_passive_visibility_slot_required is True
    assert decision.removable_noop_activation_required is True
    assert decision.route_invariant_activation_required is True
    assert decision.final_selection_invisible_activation_required is True
    assert decision.non_training_feedback_slot_required is True
    assert decision.actual_passive_visibility_activation_enabled is False
    assert decision.passive_visibility_slot_registration_enabled is False
    assert decision.passive_visibility_slot_mutation_enabled is False
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
    assert decision.visible_ml_integration_complete is False
    assert decision.critical_boundary_error_budget == 0


def test_phase13_contract_blocks_activation_and_route_authority():
    unsafe_activation = evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request({
        "capabilities": ["passive_visibility_activation"]
    })
    assert unsafe_activation.accepted is False
    assert unsafe_activation.status is ReadOnlyPanelPassiveVisibilityActivationStatus.BLOCKED_UNSAFE_ACTIVATION
    assert unsafe_activation.actual_passive_visibility_activation_enabled is False
    assert unsafe_activation.passive_visibility_slot_registration_enabled is False
    assert unsafe_activation.runtime_ui_mutation_enabled is False

    unsafe_authority = evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request({
        "route_authority": True,
    })
    assert unsafe_authority.accepted is False
    assert unsafe_authority.status is ReadOnlyPanelPassiveVisibilityActivationStatus.BLOCKED_UNSAFE_AUTHORITY
    assert unsafe_authority.route_authority_enabled is False
    assert unsafe_authority.route_influence_enabled is False


def test_phase13_probe_remains_non_authoritative_and_contract_only():
    decision = build_phase13_read_only_panel_passive_visibility_activation_contract_probe()
    assert decision.accepted is True
    assert decision.contract_only is True
    assert decision.actual_passive_visibility_activation_enabled is False
    assert decision.actual_runtime_app_host_visibility_enabled is False
    assert decision.mounted_runtime_panel_enabled is False
    assert decision.router_calls_enabled is False
    assert decision.advisor_calls_enabled is False
    assert decision.runtime_copilot_decision_behavior_enabled is False
    assert decision.autonomous_ml_router_enabled is False
    assert decision.visible_ml_integration_complete is False


if __name__ == "__main__":
    test_phase13_contract_accepts_future_passive_visibility_activation_contract_only()
    test_phase13_contract_blocks_activation_and_route_authority()
    test_phase13_probe_remains_non_authoritative_and_contract_only()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation contract")
