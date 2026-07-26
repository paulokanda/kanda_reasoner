from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_host_binding import (
    build_phase11_read_only_panel_host_binding_implementation_probe,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_app_host_visibility import (
    FEATURE_ID,
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy,
    ReadOnlyPanelRuntimeAppHostVisibilityImplementationState,
    build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe,
    build_read_only_advisory_panel_runtime_app_host_visibility_descriptor,
)


def test_phase12_visibility_implementation_default_off_is_disabled_noop():
    policy = ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy(
        visibility_surface_id="phase12_test_visibility",
        visibility_surface_label="Phase 12 Test Visibility",
    )
    descriptor = build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(
        policy,
        build_phase11_read_only_panel_host_binding_implementation_probe(),
    )
    assert descriptor.feature_id == FEATURE_ID
    assert descriptor.state is ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.DISABLED_NOOP
    assert descriptor.feature_flag_enabled is False
    assert descriptor.read_only_runtime_app_host_visibility_descriptor_ready is False
    assert descriptor.visible_sections == ()
    assert descriptor.failure_state_codes == ("feature_flag_default_off",)
    assert descriptor.actual_runtime_app_host_visibility_enabled is False
    assert descriptor.visibility_activation_enabled is False
    assert descriptor.runtime_ui_mutation_enabled is False
    assert descriptor.runtime_telemetry_surface_wiring_enabled is False
    assert descriptor.route_authority_enabled is False


def test_phase12_visibility_implementation_fail_open_missing_descriptor():
    policy = ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy(
        visibility_surface_id="phase12_test_visibility",
        visibility_surface_label="Phase 12 Test Visibility",
        feature_flag_enabled=True,
    )
    descriptor = build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(policy, None)
    assert descriptor.state is ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.FAIL_OPEN_NO_DESCRIPTOR
    assert descriptor.fail_open is True
    assert descriptor.read_only_runtime_app_host_visibility_descriptor_ready is False
    assert descriptor.visible_read_only_panel_descriptor_ready is False
    assert descriptor.visible_sections == ()
    assert descriptor.failure_state_codes == ("missing_or_invalid_host_binding_descriptor",)
    assert descriptor.runtime_ui_mutation_enabled is False
    assert descriptor.runtime_telemetry_surface_wiring_enabled is False
    assert descriptor.route_influence_enabled is False
    assert descriptor.route_authority_enabled is False


def test_phase12_visibility_implementation_builds_safe_read_only_descriptor():
    descriptor = build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe()
    assert descriptor.feature_id == FEATURE_ID
    assert descriptor.state is ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.READ_ONLY_VISIBILITY_DESCRIPTOR_READY
    assert descriptor.feature_flag_enabled is True
    assert descriptor.read_only_runtime_app_host_visibility_descriptor_ready is True
    assert descriptor.visible_read_only_panel_descriptor_ready is True
    assert descriptor.mounted_runtime_panel_descriptor_ready is True
    assert descriptor.visible_sections
    assert descriptor.read_only is True
    assert descriptor.telemetry_only is True
    assert descriptor.in_memory_only is True
    assert descriptor.bounded is True
    assert descriptor.removable_noop is True
    assert descriptor.route_invariant is True
    assert descriptor.final_selection_invisible is True
    assert descriptor.non_authoritative is True
    assert descriptor.consumes_phase11_host_binding_descriptor_only is True
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
    assert descriptor.critical_boundary_error_budget == 0
    for section in descriptor.visible_sections:
        assert section.read_only is True
        assert section.display_only is True
        assert section.action_enabled is False
        assert section.route_authority_enabled is False
        assert section.route_influence_enabled is False
        assert section.host_callback_enabled is False
        assert section.free_text_route_advice_enabled is False


if __name__ == "__main__":
    test_phase12_visibility_implementation_default_off_is_disabled_noop()
    test_phase12_visibility_implementation_fail_open_missing_descriptor()
    test_phase12_visibility_implementation_builds_safe_read_only_descriptor()
    print("VALIDATION OK: phase12 read-only advisory panel runtime app-host visibility implementation")
