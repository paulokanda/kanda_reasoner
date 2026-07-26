from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_host_binding import (
    ReadOnlyAdvisoryPanelHostBindingDescriptor,
    ReadOnlyAdvisoryPanelHostBindingImplementationPolicy,
    ReadOnlyPanelHostBindingImplementationState,
    build_phase11_read_only_panel_host_binding_implementation_probe,
    build_read_only_advisory_panel_host_binding_descriptor,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_renderer_mount import (
    ReadOnlyAdvisoryPanelRendererMountPolicy,
    build_phase10_read_only_panel_renderer_mount_implementation_probe,
    build_read_only_advisory_panel_renderer_mount_descriptor,
)


def _enabled_policy() -> ReadOnlyAdvisoryPanelHostBindingImplementationPolicy:
    return ReadOnlyAdvisoryPanelHostBindingImplementationPolicy(
        host_container_id="test_host_container",
        host_container_label="Test Host Container",
        feature_flag_enabled=True,
    )


def _assert_forbidden_flags_false(descriptor: ReadOnlyAdvisoryPanelHostBindingDescriptor) -> None:
    forbidden = [
        "actual_host_binding_enabled",
        "host_binding_activation_enabled",
        "runtime_app_host_visibility_enabled",
        "mounted_runtime_panel_enabled",
        "host_event_subscription_enabled",
        "host_callback_registration_enabled",
        "runtime_ui_mutation_enabled",
        "runtime_telemetry_surface_wiring_enabled",
        "route_influence_enabled",
        "route_authority_enabled",
        "router_calls_enabled",
        "advisor_calls_enabled",
        "adapter_execution_enabled",
        "provider_calls_enabled",
        "persistence_enabled",
        "prompt_loading_enabled",
        "prompt_registry_mutation_enabled",
        "prompt_library_read_enabled",
        "freeze_memory_read_enabled",
        "freeze_memory_write_enabled",
        "router_canon_read_enabled",
        "route_override_button_enabled",
        "use_ml_route_button_enabled",
        "best_route_claim_enabled",
        "prompt_ranking_enabled",
        "advisory_ranking_enabled",
        "free_text_route_advice_enabled",
        "free_text_explanations_enabled",
        "runtime_pilot_behavior_enabled",
        "runtime_copilot_decision_behavior_enabled",
    ]
    for field_name in forbidden:
        assert getattr(descriptor, field_name) is False, field_name


def test_default_off_policy_returns_disabled_noop() -> None:
    policy = ReadOnlyAdvisoryPanelHostBindingImplementationPolicy(
        host_container_id="default_off_host",
        host_container_label="Default Off Host",
    )
    descriptor = build_read_only_advisory_panel_host_binding_descriptor(
        policy,
        build_phase10_read_only_panel_renderer_mount_implementation_probe(),
    )
    assert descriptor.state is ReadOnlyPanelHostBindingImplementationState.DISABLED_NOOP
    assert descriptor.feature_flag_enabled is False
    assert descriptor.read_only_host_binding_descriptor_ready is False
    assert descriptor.runtime_app_host_visibility_descriptor_ready is False
    assert descriptor.mounted_runtime_panel_descriptor_ready is False
    assert descriptor.host_bound_sections == ()
    assert descriptor.failure_state_codes == ("feature_flag_default_off",)
    _assert_forbidden_flags_false(descriptor)


def test_missing_descriptor_fails_open() -> None:
    descriptor = build_read_only_advisory_panel_host_binding_descriptor(_enabled_policy(), None)
    assert descriptor.state is ReadOnlyPanelHostBindingImplementationState.FAIL_OPEN_NO_DESCRIPTOR
    assert descriptor.read_only_host_binding_descriptor_ready is False
    assert descriptor.failure_state_codes == ("missing_or_invalid_renderer_mount_descriptor",)
    _assert_forbidden_flags_false(descriptor)


def test_unsafe_descriptor_is_blocked() -> None:
    unsafe = build_read_only_advisory_panel_renderer_mount_descriptor(
        ReadOnlyAdvisoryPanelRendererMountPolicy(
            mount_surface_id="unsafe_source",
            mount_surface_label="Unsafe Source",
        ),
        None,
    )
    descriptor = build_read_only_advisory_panel_host_binding_descriptor(_enabled_policy(), unsafe)
    assert descriptor.state is ReadOnlyPanelHostBindingImplementationState.BLOCKED_UNSAFE_DESCRIPTOR
    assert descriptor.read_only_host_binding_descriptor_ready is False
    assert descriptor.failure_state_codes == ("unsafe_renderer_mount_descriptor_rejected",)
    _assert_forbidden_flags_false(descriptor)


def test_safe_descriptor_builds_bounded_host_binding_descriptor() -> None:
    source = build_phase10_read_only_panel_renderer_mount_implementation_probe()
    descriptor = build_read_only_advisory_panel_host_binding_descriptor(_enabled_policy(), source)
    assert descriptor.state is ReadOnlyPanelHostBindingImplementationState.READ_ONLY_HOST_BINDING_DESCRIPTOR_READY
    assert descriptor.read_only_host_binding_descriptor_ready is True
    assert descriptor.runtime_app_host_visibility_descriptor_ready is True
    assert descriptor.mounted_runtime_panel_descriptor_ready is True
    assert descriptor.feature_flag_enabled is True
    assert descriptor.source_mount_surface_id == source.mount_surface_id
    assert descriptor.source_panel_id == source.source_panel_id
    assert descriptor.canonical_result_id == source.canonical_result_id
    assert len(descriptor.host_bound_sections) == len(source.rendered_sections)
    assert descriptor.host_bound_sections
    assert descriptor.consumes_phase10_renderer_mount_descriptor_only is True
    assert descriptor.read_only is True
    assert descriptor.telemetry_only is True
    assert descriptor.in_memory_only is True
    assert descriptor.bounded is True
    assert descriptor.fail_open is True
    assert descriptor.removable_noop is True
    assert descriptor.route_invariant is True
    assert descriptor.final_selection_invisible is True
    assert descriptor.non_authoritative is True
    for section in descriptor.host_bound_sections:
        assert section.read_only is True
        assert section.action_enabled is False
        assert section.route_authority_enabled is False
        assert section.route_influence_enabled is False
        assert section.host_callback_enabled is False
        assert section.free_text_route_advice_enabled is False
    _assert_forbidden_flags_false(descriptor)


def test_probe_stays_safe_and_ready() -> None:
    descriptor = build_phase11_read_only_panel_host_binding_implementation_probe()
    assert descriptor.feature_id == "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_implementation_v1"
    assert descriptor.state is ReadOnlyPanelHostBindingImplementationState.READ_ONLY_HOST_BINDING_DESCRIPTOR_READY
    assert descriptor.read_only_host_binding_descriptor_ready is True
    assert descriptor.critical_boundary_error_budget == 0
    _assert_forbidden_flags_false(descriptor)


def test_policy_rejects_unsafe_authority() -> None:
    try:
        ReadOnlyAdvisoryPanelHostBindingImplementationPolicy(
            host_container_id="unsafe",
            host_container_label="Unsafe",
            allow_route_authority=True,
        )
    except ValueError as exc:
        assert "allow_route_authority" in str(exc)
    else:
        raise AssertionError("unsafe host-binding policy should be rejected")


if __name__ == "__main__":
    test_default_off_policy_returns_disabled_noop()
    test_missing_descriptor_fails_open()
    test_unsafe_descriptor_is_blocked()
    test_safe_descriptor_builds_bounded_host_binding_descriptor()
    test_probe_stays_safe_and_ready()
    test_policy_rejects_unsafe_authority()
    print("VALIDATION OK: phase11 read-only advisory panel host binding implementation")
