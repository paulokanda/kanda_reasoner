from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_app_host_visibility import (
    build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_passive_visibility_activation import (
    FEATURE_ID,
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor,
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy,
    ReadOnlyPanelPassiveVisibilityActivationImplementationState,
    build_phase13_read_only_panel_passive_visibility_activation_implementation_probe,
    build_read_only_advisory_panel_passive_visibility_activation_descriptor,
)


def test_phase13_passive_visibility_activation_default_off_is_disabled_noop():
    policy = ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy(
        passive_visibility_surface_id="phase13_disabled_probe",
        passive_visibility_surface_label="Phase 13 Disabled Probe",
    )
    descriptor = build_read_only_advisory_panel_passive_visibility_activation_descriptor(
        policy,
        build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe(),
    )
    assert isinstance(descriptor, ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor)
    assert descriptor.feature_id == FEATURE_ID
    assert descriptor.state is ReadOnlyPanelPassiveVisibilityActivationImplementationState.DISABLED_NOOP
    assert descriptor.feature_flag_enabled is False
    assert descriptor.read_only_passive_visibility_activation_descriptor_ready is False
    assert descriptor.passive_visibility_slot_descriptor_ready is False
    assert descriptor.runtime_app_host_visibility_descriptor_consumed is False
    assert descriptor.passive_visibility_slots == ()
    assert descriptor.failure_state_codes == ("feature_flag_default_off",)
    assert descriptor.actual_passive_visibility_activation_enabled is False
    assert descriptor.passive_visibility_slot_registration_enabled is False
    assert descriptor.passive_visibility_slot_mutation_enabled is False
    assert descriptor.runtime_ui_mutation_enabled is False
    assert descriptor.route_authority_enabled is False


def test_phase13_passive_visibility_activation_fail_open_missing_descriptor():
    policy = ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy(
        passive_visibility_surface_id="phase13_missing_descriptor_probe",
        passive_visibility_surface_label="Phase 13 Missing Descriptor Probe",
        feature_flag_enabled=True,
    )
    descriptor = build_read_only_advisory_panel_passive_visibility_activation_descriptor(policy, None)
    assert descriptor.state is ReadOnlyPanelPassiveVisibilityActivationImplementationState.FAIL_OPEN_NO_DESCRIPTOR
    assert descriptor.read_only_passive_visibility_activation_descriptor_ready is False
    assert descriptor.passive_visibility_slot_descriptor_ready is False
    assert descriptor.runtime_app_host_visibility_descriptor_consumed is False
    assert descriptor.passive_visibility_slots == ()
    assert descriptor.failure_state_codes == ("missing_or_invalid_runtime_app_host_visibility_descriptor",)
    assert descriptor.fail_open is True
    assert descriptor.actual_runtime_app_host_visibility_enabled is False
    assert descriptor.runtime_telemetry_surface_wiring_enabled is False
    assert descriptor.route_influence_enabled is False
    assert descriptor.route_authority_enabled is False


def test_phase13_passive_visibility_activation_builds_safe_read_only_descriptor():
    descriptor = build_phase13_read_only_panel_passive_visibility_activation_implementation_probe()
    assert descriptor.feature_id == FEATURE_ID
    assert descriptor.state is ReadOnlyPanelPassiveVisibilityActivationImplementationState.READ_ONLY_PASSIVE_VISIBILITY_ACTIVATION_DESCRIPTOR_READY
    assert descriptor.feature_flag_enabled is True
    assert descriptor.read_only_passive_visibility_activation_descriptor_ready is True
    assert descriptor.passive_visibility_slot_descriptor_ready is True
    assert descriptor.runtime_app_host_visibility_descriptor_consumed is True
    assert descriptor.passive_visibility_slots
    assert descriptor.read_only is True
    assert descriptor.telemetry_only is True
    assert descriptor.in_memory_only is True
    assert descriptor.bounded is True
    assert descriptor.removable_noop is True
    assert descriptor.route_invariant is True
    assert descriptor.final_selection_invisible is True
    assert descriptor.non_authoritative is True
    assert descriptor.consumes_phase12_runtime_app_host_visibility_descriptor_only is True
    assert descriptor.actual_passive_visibility_activation_enabled is False
    assert descriptor.passive_visibility_slot_registration_enabled is False
    assert descriptor.passive_visibility_slot_mutation_enabled is False
    assert descriptor.actual_runtime_app_host_visibility_enabled is False
    assert descriptor.visibility_activation_enabled is False
    assert descriptor.mounted_runtime_panel_enabled is False
    assert descriptor.runtime_panel_mount_side_effects_enabled is False
    assert descriptor.host_event_subscription_enabled is False
    assert descriptor.host_callback_registration_enabled is False
    assert descriptor.runtime_ui_mutation_enabled is False
    assert descriptor.runtime_telemetry_surface_wiring_enabled is False
    assert descriptor.route_influence_enabled is False
    assert descriptor.route_authority_enabled is False
    assert descriptor.router_calls_enabled is False
    assert descriptor.advisor_calls_enabled is False
    assert descriptor.provider_calls_enabled is False
    assert descriptor.persistence_enabled is False
    assert descriptor.runtime_copilot_decision_behavior_enabled is False
    assert descriptor.autonomous_ml_router_enabled is False
    assert descriptor.visible_ml_integration_complete is False
    assert descriptor.critical_boundary_error_budget == 0
    for slot in descriptor.passive_visibility_slots:
        assert slot.read_only is True
        assert slot.display_only is True
        assert slot.passive is True
        assert slot.action_enabled is False
        assert slot.slot_registered_in_host is False
        assert slot.slot_mutation_enabled is False
        assert slot.route_authority_enabled is False
        assert slot.route_influence_enabled is False
        assert slot.host_callback_enabled is False
        assert slot.telemetry_surface_wiring_enabled is False
        assert slot.free_text_route_advice_enabled is False


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_default_off_is_disabled_noop()
    test_phase13_passive_visibility_activation_fail_open_missing_descriptor()
    test_phase13_passive_visibility_activation_builds_safe_read_only_descriptor()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation implementation")
