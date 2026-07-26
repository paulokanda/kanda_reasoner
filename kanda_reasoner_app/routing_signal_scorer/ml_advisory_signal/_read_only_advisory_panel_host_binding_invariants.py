# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_host_binding_invariants.py
"""Explicit invariant validation for Phase 11 host binding.

This private helper owns validation mechanics only. It avoids reflection and
does not import the public facade, preserving one-way dependency flow from the
public host-binding module into this invariant owner.
"""

from __future__ import annotations

from typing import Any

__all__: list[str] = []


def validate_policy(
    policy: Any,
    *,
    source_review_feature_id: str,
    source_contract_feature_id: str,
    source_renderer_mount_implementation_id: str,
) -> None:
    """Validate the public implementation policy without reflection."""
    _require_text("host_container_id", policy.host_container_id)
    _require_text("host_container_label", policy.host_container_label)
    _require_text("feature_flag_name", policy.feature_flag_name)
    if policy.source_review_feature_id != source_review_feature_id:
        raise ValueError("source_review_feature_id must match Phase 11 contract review gate")
    if policy.source_contract_feature_id != source_contract_feature_id:
        raise ValueError("source_contract_feature_id must match Phase 11 contract")
    if (
        policy.source_renderer_mount_implementation_id
        != source_renderer_mount_implementation_id
    ):
        raise ValueError(
            "source_renderer_mount_implementation_id must match Phase 10 implementation"
        )
    if not isinstance(policy.max_host_sections, int) or policy.max_host_sections <= 0:
        raise ValueError("max_host_sections must be a positive integer")

    _require_true(
        "require_phase10_renderer_mount_descriptor_input",
        policy.require_phase10_renderer_mount_descriptor_input,
    )
    _require_true("require_disable_noop_control", policy.require_disable_noop_control)
    _require_true(
        "require_fail_open_on_missing_descriptor",
        policy.require_fail_open_on_missing_descriptor,
    )
    _require_true("require_block_unsafe_descriptor", policy.require_block_unsafe_descriptor)
    _require_true("require_bounded_host_sections", policy.require_bounded_host_sections)
    _require_true(
        "require_removable_noop_host_binding",
        policy.require_removable_noop_host_binding,
    )
    _require_true(
        "require_route_invariant_host_binding",
        policy.require_route_invariant_host_binding,
    )
    _require_true(
        "require_final_selection_invisible_host_binding",
        policy.require_final_selection_invisible_host_binding,
    )
    _require_true(
        "require_non_training_feedback_slot",
        policy.require_non_training_feedback_slot,
    )
    _require_true(
        "allow_read_only_host_binding_descriptor",
        policy.allow_read_only_host_binding_descriptor,
    )

    _require_false("feature_flag_default_enabled", policy.feature_flag_default_enabled)
    _require_false("allow_actual_host_binding", policy.allow_actual_host_binding)
    _require_false("allow_host_binding_activation", policy.allow_host_binding_activation)
    _require_false(
        "allow_runtime_app_host_visibility",
        policy.allow_runtime_app_host_visibility,
    )
    _require_false("allow_mounted_runtime_panel", policy.allow_mounted_runtime_panel)
    _require_false(
        "allow_host_event_subscription",
        policy.allow_host_event_subscription,
    )
    _require_false(
        "allow_host_callback_registration",
        policy.allow_host_callback_registration,
    )
    _require_false("allow_runtime_ui_mutation", policy.allow_runtime_ui_mutation)
    _require_false(
        "allow_runtime_telemetry_surface_wiring",
        policy.allow_runtime_telemetry_surface_wiring,
    )
    _require_false("allow_route_influence", policy.allow_route_influence)
    _require_false("allow_route_authority", policy.allow_route_authority)
    _require_false("allow_router_calls", policy.allow_router_calls)
    _require_false("allow_advisor_calls", policy.allow_advisor_calls)
    _require_false("allow_adapter_execution", policy.allow_adapter_execution)
    _require_false("allow_provider_calls", policy.allow_provider_calls)
    _require_false("allow_persistence", policy.allow_persistence)
    _require_false("allow_prompt_loading", policy.allow_prompt_loading)
    _require_false(
        "allow_prompt_registry_mutation",
        policy.allow_prompt_registry_mutation,
    )
    _require_false("allow_prompt_library_read", policy.allow_prompt_library_read)
    _require_false("allow_freeze_memory_read", policy.allow_freeze_memory_read)
    _require_false("allow_freeze_memory_write", policy.allow_freeze_memory_write)
    _require_false("allow_router_canon_read", policy.allow_router_canon_read)
    _require_false("allow_route_override_button", policy.allow_route_override_button)
    _require_false("allow_use_ml_route_button", policy.allow_use_ml_route_button)
    _require_false("allow_best_route_claim", policy.allow_best_route_claim)
    _require_false("allow_prompt_ranking", policy.allow_prompt_ranking)
    _require_false("allow_advisory_ranking", policy.allow_advisory_ranking)
    _require_false(
        "allow_free_text_route_advice",
        policy.allow_free_text_route_advice,
    )
    _require_false(
        "allow_free_text_explanations",
        policy.allow_free_text_explanations,
    )
    _require_false("allow_runtime_pilot_behavior", policy.allow_runtime_pilot_behavior)
    _require_false(
        "allow_runtime_copilot_decision_behavior",
        policy.allow_runtime_copilot_decision_behavior,
    )


def validate_host_bound_section(section: Any) -> None:
    """Validate one bounded host-facing section explicitly."""
    _require_text("section_key", section.section_key)
    _require_text("label", section.label)
    _require_text("value", section.value)
    _require_text("severity", section.severity)
    _require_text("host_role", section.host_role)
    if len(section.section_key) > 80:
        raise ValueError("section_key must remain bounded")
    if len(section.label) > 96:
        raise ValueError("label must remain bounded")
    if len(section.value) > 240:
        raise ValueError("value must remain bounded")
    if len(section.host_role) > 80:
        raise ValueError("host_role must remain bounded")
    if section.read_only is not True:
        raise ValueError("host-bound section must remain read-only")
    if section.action_enabled is not False:
        raise ValueError("host-bound section actions are forbidden")
    if section.route_authority_enabled is not False:
        raise ValueError("host-bound section route authority is forbidden")
    if section.route_influence_enabled is not False:
        raise ValueError("host-bound section route influence is forbidden")
    if section.host_callback_enabled is not False:
        raise ValueError("host-bound section callbacks are forbidden")
    if section.free_text_route_advice_enabled is not False:
        raise ValueError("host-bound section free-text route advice is forbidden")


def validate_descriptor(
    descriptor: Any,
    *,
    feature_id: str,
    state_type: type,
    ready_state: Any,
    host_section_type: type,
) -> None:
    """Validate one public host-binding descriptor without reflection."""
    if descriptor.feature_id != feature_id:
        raise ValueError("feature_id must match Phase 11 host binding implementation")
    _require_text("host_container_id", descriptor.host_container_id)
    _require_text("host_container_label", descriptor.host_container_label)
    _require_text("feature_flag_name", descriptor.feature_flag_name)
    if not isinstance(descriptor.state, state_type):
        raise TypeError("state must be ReadOnlyPanelHostBindingImplementationState")

    _require_optional_text("source_mount_surface_id", descriptor.source_mount_surface_id)
    _require_optional_text(
        "source_mount_surface_label",
        descriptor.source_mount_surface_label,
    )
    _require_optional_text("source_panel_id", descriptor.source_panel_id)
    _require_optional_text("source_panel_label", descriptor.source_panel_label)
    _require_optional_text("canonical_result_id", descriptor.canonical_result_id)
    _require_optional_text(
        "canonical_dispatch_label",
        descriptor.canonical_dispatch_label,
    )
    _require_optional_text("final_selection_hash", descriptor.final_selection_hash)

    _require_tuple_of_host_sections(
        "host_bound_sections",
        descriptor.host_bound_sections,
        host_section_type,
    )
    _require_tuple_of_text("failure_state_codes", descriptor.failure_state_codes)

    _require_true("read_only", descriptor.read_only)
    _require_true("telemetry_only", descriptor.telemetry_only)
    _require_true("in_memory_only", descriptor.in_memory_only)
    _require_true("bounded", descriptor.bounded)
    _require_true("fail_open", descriptor.fail_open)
    _require_true("removable_noop", descriptor.removable_noop)
    _require_true("route_invariant", descriptor.route_invariant)
    _require_true("final_selection_invisible", descriptor.final_selection_invisible)
    _require_true("non_authoritative", descriptor.non_authoritative)
    _require_true(
        "consumes_phase10_renderer_mount_descriptor_only",
        descriptor.consumes_phase10_renderer_mount_descriptor_only,
    )

    _require_false("actual_host_binding_enabled", descriptor.actual_host_binding_enabled)
    _require_false(
        "host_binding_activation_enabled",
        descriptor.host_binding_activation_enabled,
    )
    _require_false(
        "runtime_app_host_visibility_enabled",
        descriptor.runtime_app_host_visibility_enabled,
    )
    _require_false("mounted_runtime_panel_enabled", descriptor.mounted_runtime_panel_enabled)
    _require_false(
        "host_event_subscription_enabled",
        descriptor.host_event_subscription_enabled,
    )
    _require_false(
        "host_callback_registration_enabled",
        descriptor.host_callback_registration_enabled,
    )
    _require_false("runtime_ui_mutation_enabled", descriptor.runtime_ui_mutation_enabled)
    _require_false(
        "runtime_telemetry_surface_wiring_enabled",
        descriptor.runtime_telemetry_surface_wiring_enabled,
    )
    _require_false("route_influence_enabled", descriptor.route_influence_enabled)
    _require_false("route_authority_enabled", descriptor.route_authority_enabled)
    _require_false("router_calls_enabled", descriptor.router_calls_enabled)
    _require_false("advisor_calls_enabled", descriptor.advisor_calls_enabled)
    _require_false("adapter_execution_enabled", descriptor.adapter_execution_enabled)
    _require_false("provider_calls_enabled", descriptor.provider_calls_enabled)
    _require_false("persistence_enabled", descriptor.persistence_enabled)
    _require_false("prompt_loading_enabled", descriptor.prompt_loading_enabled)
    _require_false(
        "prompt_registry_mutation_enabled",
        descriptor.prompt_registry_mutation_enabled,
    )
    _require_false("prompt_library_read_enabled", descriptor.prompt_library_read_enabled)
    _require_false("freeze_memory_read_enabled", descriptor.freeze_memory_read_enabled)
    _require_false("freeze_memory_write_enabled", descriptor.freeze_memory_write_enabled)
    _require_false("router_canon_read_enabled", descriptor.router_canon_read_enabled)
    _require_false(
        "route_override_button_enabled",
        descriptor.route_override_button_enabled,
    )
    _require_false(
        "use_ml_route_button_enabled",
        descriptor.use_ml_route_button_enabled,
    )
    _require_false("best_route_claim_enabled", descriptor.best_route_claim_enabled)
    _require_false("prompt_ranking_enabled", descriptor.prompt_ranking_enabled)
    _require_false("advisory_ranking_enabled", descriptor.advisory_ranking_enabled)
    _require_false(
        "free_text_route_advice_enabled",
        descriptor.free_text_route_advice_enabled,
    )
    _require_false(
        "free_text_explanations_enabled",
        descriptor.free_text_explanations_enabled,
    )
    _require_false(
        "runtime_pilot_behavior_enabled",
        descriptor.runtime_pilot_behavior_enabled,
    )
    _require_false(
        "runtime_copilot_decision_behavior_enabled",
        descriptor.runtime_copilot_decision_behavior_enabled,
    )

    if descriptor.critical_boundary_error_budget != 0:
        raise ValueError("critical_boundary_error_budget must remain zero")
    if descriptor.read_only_host_binding_descriptor_ready is True:
        if descriptor.state is not ready_state:
            raise ValueError(
                "ready descriptor must use READ_ONLY_HOST_BINDING_DESCRIPTOR_READY state"
            )
        if descriptor.runtime_app_host_visibility_descriptor_ready is not True:
            raise ValueError(
                "ready descriptor must mark host-visibility descriptor readiness"
            )
        if descriptor.mounted_runtime_panel_descriptor_ready is not True:
            raise ValueError(
                "ready descriptor must mark mounted-panel descriptor readiness"
            )
        if not descriptor.host_bound_sections:
            raise ValueError("ready descriptor requires host-bound sections")
    else:
        if descriptor.state is ready_state:
            raise ValueError(
                "READY state requires read_only_host_binding_descriptor_ready=True"
            )
        if descriptor.runtime_app_host_visibility_descriptor_ready is not False:
            raise ValueError(
                "non-ready descriptor must not mark host-visibility readiness"
            )
        if descriptor.mounted_runtime_panel_descriptor_ready is not False:
            raise ValueError(
                "non-ready descriptor must not mark mounted-panel readiness"
            )


def _require_text(name: str, value: str) -> None:
    """Require non-empty text using the existing error contract."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be non-empty text")


def _require_optional_text(name: str, value: Any) -> None:
    """Require text only when an optional value is present."""
    if value is not None:
        _require_text(name, value)


def _require_tuple_of_text(name: str, value: Any) -> None:
    """Require a tuple containing only non-empty text values."""
    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    for item in value:
        _require_text(name + " item", item)


def _require_tuple_of_host_sections(
    name: str,
    value: Any,
    host_section_type: type,
) -> None:
    """Require a tuple containing only the public host-section type."""
    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    for item in value:
        if not isinstance(item, host_section_type):
            raise TypeError(
                name + " items must be ReadOnlyAdvisoryPanelHostBoundSection"
            )


def _require_true(name: str, value: Any) -> None:
    """Require an exact True invariant."""
    if value is not True:
        raise ValueError(name + " must remain True")


def _require_false(name: str, value: Any) -> None:
    """Require an exact False invariant."""
    if value is not False:
        raise ValueError(name + " must remain False")
