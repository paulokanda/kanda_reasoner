# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_runtime_app_host_visibility_contract_invariants.py
"""Explicit invariant validation for the Phase 12 app-host visibility contract.

This private helper owns policy and decision invariant mechanics only. It uses
explicit attribute access, preserves validation order and error text, and does
not import the public facade.
"""

from __future__ import annotations

from typing import Any, Tuple

__all__ = []


def validate_policy(
    policy: Any,
    *,
    visibility_mode_type: type,
    previous_completion_handoff_id: str,
    source_host_binding_implementation_id: str,
) -> None:
    """Validate one contract policy without reflective field lookup."""
    if not isinstance(policy.visibility_mode, visibility_mode_type):
        raise TypeError("visibility_mode must be ReadOnlyPanelRuntimeAppHostVisibilityMode")
    if policy.source_completion_handoff_id != previous_completion_handoff_id:
        raise ValueError("source_completion_handoff_id must match Phase 11 completion handoff")
    if policy.source_host_binding_implementation_id != source_host_binding_implementation_id:
        raise ValueError("source_host_binding_implementation_id must match Phase 11 implementation")

    _require_true(
        "require_phase11_host_binding_descriptor_input",
        policy.require_phase11_host_binding_descriptor_input,
    )
    _require_true("require_explicit_feature_flag", policy.require_explicit_feature_flag)
    _require_true("require_disable_noop_control", policy.require_disable_noop_control)
    _require_true(
        "require_fail_open_on_missing_descriptor",
        policy.require_fail_open_on_missing_descriptor,
    )
    _require_true("require_block_unsafe_descriptor", policy.require_block_unsafe_descriptor)
    _require_true(
        "require_route_invariant_visibility",
        policy.require_route_invariant_visibility,
    )
    _require_true(
        "require_final_selection_invisible_visibility",
        policy.require_final_selection_invisible_visibility,
    )
    _require_true(
        "require_runtime_visibility_input_bounded",
        policy.require_runtime_visibility_input_bounded,
    )
    _require_true(
        "require_runtime_visibility_output_bounded",
        policy.require_runtime_visibility_output_bounded,
    )
    _require_true(
        "require_removable_noop_visibility",
        policy.require_removable_noop_visibility,
    )
    _require_true(
        "require_non_training_feedback_slot",
        policy.require_non_training_feedback_slot,
    )

    _require_false("feature_flag_default_enabled", policy.feature_flag_default_enabled)
    _require_false(
        "allow_actual_runtime_app_host_visibility_in_this_phase",
        policy.allow_actual_runtime_app_host_visibility_in_this_phase,
    )
    _require_false(
        "allow_runtime_app_host_visibility_activation_in_this_phase",
        policy.allow_runtime_app_host_visibility_activation_in_this_phase,
    )
    _require_false(
        "allow_mounted_runtime_panel_in_this_phase",
        policy.allow_mounted_runtime_panel_in_this_phase,
    )
    _require_false(
        "allow_runtime_panel_mount_side_effects",
        policy.allow_runtime_panel_mount_side_effects,
    )
    _require_false("allow_host_event_subscription", policy.allow_host_event_subscription)
    _require_false(
        "allow_host_callback_registration",
        policy.allow_host_callback_registration,
    )
    _require_false("allow_runtime_ui_mutation", policy.allow_runtime_ui_mutation)
    _require_false(
        "allow_runtime_telemetry_surface_wiring",
        policy.allow_runtime_telemetry_surface_wiring,
    )
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
    _require_false("allow_route_influence", policy.allow_route_influence)
    _require_false("allow_route_authority", policy.allow_route_authority)
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
    _require_false("allow_autonomous_ml_router", policy.allow_autonomous_ml_router)


def validate_decision(
    decision: Any,
    *,
    feature_id: str,
    status_type: type,
    visibility_mode_type: type,
) -> None:
    """Validate one contract decision without reflective field lookup."""
    if decision.feature_id != feature_id:
        raise ValueError("feature_id must match Phase 12 runtime app-host visibility contract")
    if not isinstance(decision.status, status_type):
        raise TypeError("status must be ReadOnlyPanelRuntimeAppHostVisibilityStatus")
    if not isinstance(decision.visibility_mode, visibility_mode_type):
        raise TypeError("visibility_mode must be ReadOnlyPanelRuntimeAppHostVisibilityMode")

    _require_true("contract_only", decision.contract_only)
    _require_true(
        "phase11_host_binding_descriptor_input_required",
        decision.phase11_host_binding_descriptor_input_required,
    )
    _require_true(
        "explicit_feature_flag_required",
        decision.explicit_feature_flag_required,
    )
    _require_true(
        "disabled_noop_control_required",
        decision.disabled_noop_control_required,
    )
    _require_true(
        "fail_open_on_missing_descriptor_required",
        decision.fail_open_on_missing_descriptor_required,
    )
    _require_true(
        "block_unsafe_descriptor_required",
        decision.block_unsafe_descriptor_required,
    )
    _require_true(
        "route_invariant_visibility_required",
        decision.route_invariant_visibility_required,
    )
    _require_true(
        "final_selection_invisible_visibility_required",
        decision.final_selection_invisible_visibility_required,
    )
    _require_true(
        "runtime_visibility_input_bounded_required",
        decision.runtime_visibility_input_bounded_required,
    )
    _require_true(
        "runtime_visibility_output_bounded_required",
        decision.runtime_visibility_output_bounded_required,
    )
    _require_true(
        "removable_noop_visibility_required",
        decision.removable_noop_visibility_required,
    )
    _require_true(
        "non_training_feedback_slot_required",
        decision.non_training_feedback_slot_required,
    )

    _require_false("feature_flag_default_enabled", decision.feature_flag_default_enabled)
    _require_false(
        "actual_runtime_app_host_visibility_enabled",
        decision.actual_runtime_app_host_visibility_enabled,
    )
    _require_false(
        "runtime_app_host_visibility_activation_enabled",
        decision.runtime_app_host_visibility_activation_enabled,
    )
    _require_false("mounted_runtime_panel_enabled", decision.mounted_runtime_panel_enabled)
    _require_false(
        "runtime_panel_mount_side_effects_enabled",
        decision.runtime_panel_mount_side_effects_enabled,
    )
    _require_false(
        "host_event_subscription_enabled",
        decision.host_event_subscription_enabled,
    )
    _require_false(
        "host_callback_registration_enabled",
        decision.host_callback_registration_enabled,
    )
    _require_false("runtime_ui_mutation_enabled", decision.runtime_ui_mutation_enabled)
    _require_false(
        "runtime_telemetry_surface_wiring_enabled",
        decision.runtime_telemetry_surface_wiring_enabled,
    )
    _require_false("route_influence_enabled", decision.route_influence_enabled)
    _require_false("route_authority_enabled", decision.route_authority_enabled)
    _require_false("router_calls_enabled", decision.router_calls_enabled)
    _require_false("advisor_calls_enabled", decision.advisor_calls_enabled)
    _require_false("adapter_execution_enabled", decision.adapter_execution_enabled)
    _require_false("provider_calls_enabled", decision.provider_calls_enabled)
    _require_false("persistence_enabled", decision.persistence_enabled)
    _require_false("prompt_loading_enabled", decision.prompt_loading_enabled)
    _require_false(
        "prompt_registry_mutation_enabled",
        decision.prompt_registry_mutation_enabled,
    )
    _require_false(
        "prompt_library_read_enabled",
        decision.prompt_library_read_enabled,
    )
    _require_false("freeze_memory_read_enabled", decision.freeze_memory_read_enabled)
    _require_false("freeze_memory_write_enabled", decision.freeze_memory_write_enabled)
    _require_false("router_canon_read_enabled", decision.router_canon_read_enabled)
    _require_false(
        "route_override_button_enabled",
        decision.route_override_button_enabled,
    )
    _require_false(
        "use_ml_route_button_enabled",
        decision.use_ml_route_button_enabled,
    )
    _require_false("best_route_claim_enabled", decision.best_route_claim_enabled)
    _require_false("prompt_ranking_enabled", decision.prompt_ranking_enabled)
    _require_false("advisory_ranking_enabled", decision.advisory_ranking_enabled)
    _require_false(
        "free_text_route_advice_enabled",
        decision.free_text_route_advice_enabled,
    )
    _require_false(
        "free_text_explanations_enabled",
        decision.free_text_explanations_enabled,
    )
    _require_false(
        "runtime_pilot_behavior_enabled",
        decision.runtime_pilot_behavior_enabled,
    )
    _require_false(
        "runtime_copilot_decision_behavior_enabled",
        decision.runtime_copilot_decision_behavior_enabled,
    )
    _require_false(
        "autonomous_ml_router_enabled",
        decision.autonomous_ml_router_enabled,
    )

    if decision.critical_boundary_error_budget != 0:
        raise ValueError("critical_boundary_error_budget must remain zero")
    if decision.accepted and decision.source_descriptor_safe is not True:
        raise ValueError("accepted decisions require a safe source descriptor")


def policy_required_true_fields() -> Tuple[str, ...]:
    """Return legacy policy True-invariant field names in validation order."""
    return (
        "require_phase11_host_binding_descriptor_input",
        "require_explicit_feature_flag",
        "require_disable_noop_control",
        "require_fail_open_on_missing_descriptor",
        "require_block_unsafe_descriptor",
        "require_route_invariant_visibility",
        "require_final_selection_invisible_visibility",
        "require_runtime_visibility_input_bounded",
        "require_runtime_visibility_output_bounded",
        "require_removable_noop_visibility",
        "require_non_training_feedback_slot",
    )


def policy_required_false_fields() -> Tuple[str, ...]:
    """Return legacy policy False-invariant field names in validation order."""
    return (
        "feature_flag_default_enabled",
        "allow_actual_runtime_app_host_visibility_in_this_phase",
        "allow_runtime_app_host_visibility_activation_in_this_phase",
        "allow_mounted_runtime_panel_in_this_phase",
        "allow_runtime_panel_mount_side_effects",
        "allow_host_event_subscription",
        "allow_host_callback_registration",
        "allow_runtime_ui_mutation",
        "allow_runtime_telemetry_surface_wiring",
        "allow_router_calls",
        "allow_advisor_calls",
        "allow_adapter_execution",
        "allow_provider_calls",
        "allow_persistence",
        "allow_prompt_loading",
        "allow_prompt_registry_mutation",
        "allow_prompt_library_read",
        "allow_freeze_memory_read",
        "allow_freeze_memory_write",
        "allow_router_canon_read",
        "allow_route_influence",
        "allow_route_authority",
        "allow_route_override_button",
        "allow_use_ml_route_button",
        "allow_best_route_claim",
        "allow_prompt_ranking",
        "allow_advisory_ranking",
        "allow_free_text_route_advice",
        "allow_free_text_explanations",
        "allow_runtime_pilot_behavior",
        "allow_runtime_copilot_decision_behavior",
        "allow_autonomous_ml_router",
    )


def decision_required_true_fields() -> Tuple[str, ...]:
    """Return legacy decision True-invariant field names in validation order."""
    return (
        "contract_only",
        "phase11_host_binding_descriptor_input_required",
        "explicit_feature_flag_required",
        "disabled_noop_control_required",
        "fail_open_on_missing_descriptor_required",
        "block_unsafe_descriptor_required",
        "route_invariant_visibility_required",
        "final_selection_invisible_visibility_required",
        "runtime_visibility_input_bounded_required",
        "runtime_visibility_output_bounded_required",
        "removable_noop_visibility_required",
        "non_training_feedback_slot_required",
    )


def decision_forbidden_true_fields() -> Tuple[str, ...]:
    """Return legacy decision forbidden-True field names in validation order."""
    return (
        "feature_flag_default_enabled",
        "actual_runtime_app_host_visibility_enabled",
        "runtime_app_host_visibility_activation_enabled",
        "mounted_runtime_panel_enabled",
        "runtime_panel_mount_side_effects_enabled",
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
        "autonomous_ml_router_enabled",
    )


def _require_true(name: str, value: object) -> None:
    """Require one safety invariant to remain exactly True."""
    if value is not True:
        raise ValueError(name + " must remain True")


def _require_false(name: str, value: object) -> None:
    """Require one safety invariant to remain exactly False."""
    if value is not False:
        raise ValueError(name + " must remain False")
