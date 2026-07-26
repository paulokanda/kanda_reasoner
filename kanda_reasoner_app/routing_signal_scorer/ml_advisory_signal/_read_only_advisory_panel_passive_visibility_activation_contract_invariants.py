# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_passive_visibility_activation_contract_invariants.py
"""Private reflection-free invariants for the Phase 13 activation contract."""

from __future__ import annotations

from typing import Any

__all__: list[str] = []


def _validate_policy_invariants(
    policy: Any,
    *,
    activation_mode_type: Any,
    previous_completion_handoff_id: str,
    source_runtime_app_host_visibility_implementation_id: str,
) -> None:
    """Validate policy invariants through explicit attribute access."""
    if not isinstance(policy.activation_mode, activation_mode_type):
        raise TypeError("activation_mode must be ReadOnlyPanelPassiveVisibilityActivationMode")
    if policy.source_completion_handoff_id != previous_completion_handoff_id:
        raise ValueError("source_completion_handoff_id must match Phase 12 completion handoff")
    if (
        policy.source_runtime_app_host_visibility_implementation_id
        != source_runtime_app_host_visibility_implementation_id
    ):
        raise ValueError(
            "source_runtime_app_host_visibility_implementation_id must match Phase 12 implementation"
        )

    required_true = (
        (
            "require_phase12_runtime_app_host_visibility_descriptor_input",
            policy.require_phase12_runtime_app_host_visibility_descriptor_input,
        ),
        ("require_explicit_feature_flag", policy.require_explicit_feature_flag),
        ("require_disable_noop_control", policy.require_disable_noop_control),
        (
            "require_fail_open_on_missing_descriptor",
            policy.require_fail_open_on_missing_descriptor,
        ),
        ("require_block_unsafe_descriptor", policy.require_block_unsafe_descriptor),
        (
            "require_bounded_passive_visibility_input",
            policy.require_bounded_passive_visibility_input,
        ),
        (
            "require_bounded_passive_visibility_output",
            policy.require_bounded_passive_visibility_output,
        ),
        (
            "require_read_only_passive_visibility_slot",
            policy.require_read_only_passive_visibility_slot,
        ),
        (
            "require_removable_noop_activation",
            policy.require_removable_noop_activation,
        ),
        (
            "require_route_invariant_activation",
            policy.require_route_invariant_activation,
        ),
        (
            "require_final_selection_invisible_activation",
            policy.require_final_selection_invisible_activation,
        ),
        (
            "require_non_training_feedback_slot",
            policy.require_non_training_feedback_slot,
        ),
        (
            "allow_future_passive_visibility_activation_contract",
            policy.allow_future_passive_visibility_activation_contract,
        ),
    )
    for field_name, enabled in required_true:
        if enabled is not True:
            raise ValueError(field_name + " must remain True")

    required_false = (
        ("feature_flag_default_enabled", policy.feature_flag_default_enabled),
        (
            "allow_actual_passive_visibility_activation_in_this_phase",
            policy.allow_actual_passive_visibility_activation_in_this_phase,
        ),
        (
            "allow_passive_visibility_slot_registration_in_this_phase",
            policy.allow_passive_visibility_slot_registration_in_this_phase,
        ),
        (
            "allow_passive_visibility_slot_mutation_in_this_phase",
            policy.allow_passive_visibility_slot_mutation_in_this_phase,
        ),
        (
            "allow_actual_runtime_app_host_visibility_in_this_phase",
            policy.allow_actual_runtime_app_host_visibility_in_this_phase,
        ),
        (
            "allow_runtime_app_host_visibility_activation_in_this_phase",
            policy.allow_runtime_app_host_visibility_activation_in_this_phase,
        ),
        (
            "allow_mounted_runtime_panel_in_this_phase",
            policy.allow_mounted_runtime_panel_in_this_phase,
        ),
        (
            "allow_runtime_panel_mount_side_effects",
            policy.allow_runtime_panel_mount_side_effects,
        ),
        ("allow_host_event_subscription", policy.allow_host_event_subscription),
        (
            "allow_host_callback_registration",
            policy.allow_host_callback_registration,
        ),
        ("allow_runtime_ui_mutation", policy.allow_runtime_ui_mutation),
        (
            "allow_runtime_telemetry_surface_wiring",
            policy.allow_runtime_telemetry_surface_wiring,
        ),
        ("allow_router_calls", policy.allow_router_calls),
        ("allow_advisor_calls", policy.allow_advisor_calls),
        ("allow_adapter_execution", policy.allow_adapter_execution),
        ("allow_provider_calls", policy.allow_provider_calls),
        ("allow_persistence", policy.allow_persistence),
        ("allow_prompt_loading", policy.allow_prompt_loading),
        (
            "allow_prompt_registry_mutation",
            policy.allow_prompt_registry_mutation,
        ),
        ("allow_prompt_library_read", policy.allow_prompt_library_read),
        ("allow_freeze_memory_read", policy.allow_freeze_memory_read),
        ("allow_freeze_memory_write", policy.allow_freeze_memory_write),
        ("allow_router_canon_read", policy.allow_router_canon_read),
        ("allow_route_influence", policy.allow_route_influence),
        ("allow_route_authority", policy.allow_route_authority),
        ("allow_route_override_button", policy.allow_route_override_button),
        ("allow_use_ml_route_button", policy.allow_use_ml_route_button),
        ("allow_best_route_claim", policy.allow_best_route_claim),
        ("allow_prompt_ranking", policy.allow_prompt_ranking),
        ("allow_advisory_ranking", policy.allow_advisory_ranking),
        (
            "allow_free_text_route_advice",
            policy.allow_free_text_route_advice,
        ),
        (
            "allow_free_text_explanations",
            policy.allow_free_text_explanations,
        ),
        (
            "allow_runtime_pilot_behavior",
            policy.allow_runtime_pilot_behavior,
        ),
        (
            "allow_runtime_copilot_decision_behavior",
            policy.allow_runtime_copilot_decision_behavior,
        ),
        ("allow_autonomous_ml_router", policy.allow_autonomous_ml_router),
    )
    for field_name, enabled in required_false:
        if enabled is not False:
            raise ValueError(field_name + " must remain False")


def _validate_decision_invariants(
    decision: Any,
    *,
    feature_id: str,
    status_type: Any,
    activation_mode_type: Any,
) -> None:
    """Validate decision invariants through explicit attribute access."""
    if decision.feature_id != feature_id:
        raise ValueError(
            "feature_id must match Phase 13 passive visibility activation contract"
        )
    if not isinstance(decision.status, status_type):
        raise TypeError("status must be ReadOnlyPanelPassiveVisibilityActivationStatus")
    if not isinstance(decision.activation_mode, activation_mode_type):
        raise TypeError("activation_mode must be ReadOnlyPanelPassiveVisibilityActivationMode")

    required_true = (
        ("contract_only", decision.contract_only),
        (
            "phase12_runtime_app_host_visibility_descriptor_input_required",
            decision.phase12_runtime_app_host_visibility_descriptor_input_required,
        ),
        ("explicit_feature_flag_required", decision.explicit_feature_flag_required),
        ("disabled_noop_control_required", decision.disabled_noop_control_required),
        (
            "fail_open_on_missing_descriptor_required",
            decision.fail_open_on_missing_descriptor_required,
        ),
        ("block_unsafe_descriptor_required", decision.block_unsafe_descriptor_required),
        (
            "bounded_passive_visibility_input_required",
            decision.bounded_passive_visibility_input_required,
        ),
        (
            "bounded_passive_visibility_output_required",
            decision.bounded_passive_visibility_output_required,
        ),
        (
            "read_only_passive_visibility_slot_required",
            decision.read_only_passive_visibility_slot_required,
        ),
        (
            "removable_noop_activation_required",
            decision.removable_noop_activation_required,
        ),
        (
            "route_invariant_activation_required",
            decision.route_invariant_activation_required,
        ),
        (
            "final_selection_invisible_activation_required",
            decision.final_selection_invisible_activation_required,
        ),
        (
            "non_training_feedback_slot_required",
            decision.non_training_feedback_slot_required,
        ),
    )
    for field_name, enabled in required_true:
        if enabled is not True:
            raise ValueError(field_name + " must remain True")

    required_false = (
        ("feature_flag_default_enabled", decision.feature_flag_default_enabled),
        (
            "actual_passive_visibility_activation_enabled",
            decision.actual_passive_visibility_activation_enabled,
        ),
        (
            "passive_visibility_slot_registration_enabled",
            decision.passive_visibility_slot_registration_enabled,
        ),
        (
            "passive_visibility_slot_mutation_enabled",
            decision.passive_visibility_slot_mutation_enabled,
        ),
        (
            "actual_runtime_app_host_visibility_enabled",
            decision.actual_runtime_app_host_visibility_enabled,
        ),
        (
            "runtime_app_host_visibility_activation_enabled",
            decision.runtime_app_host_visibility_activation_enabled,
        ),
        ("mounted_runtime_panel_enabled", decision.mounted_runtime_panel_enabled),
        (
            "runtime_panel_mount_side_effects_enabled",
            decision.runtime_panel_mount_side_effects_enabled,
        ),
        ("host_event_subscription_enabled", decision.host_event_subscription_enabled),
        (
            "host_callback_registration_enabled",
            decision.host_callback_registration_enabled,
        ),
        ("runtime_ui_mutation_enabled", decision.runtime_ui_mutation_enabled),
        (
            "runtime_telemetry_surface_wiring_enabled",
            decision.runtime_telemetry_surface_wiring_enabled,
        ),
        ("route_influence_enabled", decision.route_influence_enabled),
        ("route_authority_enabled", decision.route_authority_enabled),
        ("router_calls_enabled", decision.router_calls_enabled),
        ("advisor_calls_enabled", decision.advisor_calls_enabled),
        ("adapter_execution_enabled", decision.adapter_execution_enabled),
        ("provider_calls_enabled", decision.provider_calls_enabled),
        ("persistence_enabled", decision.persistence_enabled),
        ("prompt_loading_enabled", decision.prompt_loading_enabled),
        (
            "prompt_registry_mutation_enabled",
            decision.prompt_registry_mutation_enabled,
        ),
        ("prompt_library_read_enabled", decision.prompt_library_read_enabled),
        ("freeze_memory_read_enabled", decision.freeze_memory_read_enabled),
        ("freeze_memory_write_enabled", decision.freeze_memory_write_enabled),
        ("router_canon_read_enabled", decision.router_canon_read_enabled),
        ("route_override_button_enabled", decision.route_override_button_enabled),
        ("use_ml_route_button_enabled", decision.use_ml_route_button_enabled),
        ("best_route_claim_enabled", decision.best_route_claim_enabled),
        ("prompt_ranking_enabled", decision.prompt_ranking_enabled),
        ("advisory_ranking_enabled", decision.advisory_ranking_enabled),
        (
            "free_text_route_advice_enabled",
            decision.free_text_route_advice_enabled,
        ),
        (
            "free_text_explanations_enabled",
            decision.free_text_explanations_enabled,
        ),
        (
            "runtime_pilot_behavior_enabled",
            decision.runtime_pilot_behavior_enabled,
        ),
        (
            "runtime_copilot_decision_behavior_enabled",
            decision.runtime_copilot_decision_behavior_enabled,
        ),
        ("autonomous_ml_router_enabled", decision.autonomous_ml_router_enabled),
        ("visible_ml_integration_complete", decision.visible_ml_integration_complete),
    )
    for field_name, enabled in required_false:
        if enabled is not False:
            raise ValueError(field_name + " must remain False")
    if decision.critical_boundary_error_budget != 0:
        raise ValueError("critical_boundary_error_budget must remain zero")
