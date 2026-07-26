# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_runtime_activation_contract_invariants.py
"""Private reflection-free invariants for the Phase 9 runtime activation contract."""

from __future__ import annotations

from typing import Any, Tuple

__all__: list[str] = []


def _validate_policy_invariants(
    policy: Any,
    *,
    activation_mode_type: Any,
    previous_completion_handoff_id: str,
) -> None:
    """Validate policy invariants through explicit attribute access."""
    if not isinstance(policy.activation_mode, activation_mode_type):
        raise TypeError("activation_mode must be ReadOnlyPanelRuntimeActivationMode")
    if policy.source_completion_handoff_id != previous_completion_handoff_id:
        raise ValueError("source_completion_handoff_id must match Phase 8 completion handoff")

    required_true = (
        ("require_phase8_panel_view_model_input", policy.require_phase8_panel_view_model_input),
        ("require_explicit_feature_flag", policy.require_explicit_feature_flag),
        ("require_disable_noop_control", policy.require_disable_noop_control),
        ("require_fail_open_on_missing_view_model", policy.require_fail_open_on_missing_view_model),
        ("require_route_invariant_runtime_mount", policy.require_route_invariant_runtime_mount),
        ("require_final_selection_invisible_runtime_mount", policy.require_final_selection_invisible_runtime_mount),
        ("require_renderer_adapter_to_be_separate_future_contract", policy.require_renderer_adapter_to_be_separate_future_contract),
        ("require_non_training_feedback_slot", policy.require_non_training_feedback_slot),
    )
    for field_name, enabled in required_true:
        if enabled is not True:
            raise ValueError(field_name + " must remain True")

    required_false = (
        ("feature_flag_default_enabled", policy.feature_flag_default_enabled),
        ("allow_actual_runtime_activation_in_this_phase", policy.allow_actual_runtime_activation_in_this_phase),
        ("allow_renderer_activation_in_this_phase", policy.allow_renderer_activation_in_this_phase),
        ("allow_mounted_panel_in_this_phase", policy.allow_mounted_panel_in_this_phase),
        ("allow_runtime_ui_mutation_in_this_phase", policy.allow_runtime_ui_mutation_in_this_phase),
        ("allow_runtime_telemetry_surface_wiring_in_this_phase", policy.allow_runtime_telemetry_surface_wiring_in_this_phase),
        ("allow_router_calls", policy.allow_router_calls),
        ("allow_advisor_calls", policy.allow_advisor_calls),
        ("allow_adapter_execution", policy.allow_adapter_execution),
        ("allow_provider_calls", policy.allow_provider_calls),
        ("allow_persistence", policy.allow_persistence),
        ("allow_prompt_loading", policy.allow_prompt_loading),
        ("allow_prompt_registry_mutation", policy.allow_prompt_registry_mutation),
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
        ("allow_free_text_route_advice", policy.allow_free_text_route_advice),
        ("allow_free_text_explanations", policy.allow_free_text_explanations),
        ("allow_runtime_copilot_decision_behavior", policy.allow_runtime_copilot_decision_behavior),
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
        raise ValueError("feature_id must match Phase 9 runtime activation contract")
    if not isinstance(decision.status, status_type):
        raise TypeError("status must be ReadOnlyPanelRuntimeActivationStatus")
    if not isinstance(decision.activation_mode, activation_mode_type):
        raise TypeError("activation_mode must be ReadOnlyPanelRuntimeActivationMode")

    _require_tuple_of_text("required_safe_labels", decision.required_safe_labels)
    _require_tuple_of_text("forbidden_capabilities", decision.forbidden_capabilities)

    required_true = (
        ("contract_only", decision.contract_only),
        ("phase8_view_model_input_required", decision.phase8_view_model_input_required),
        ("explicit_feature_flag_required", decision.explicit_feature_flag_required),
        ("disable_noop_control_required", decision.disable_noop_control_required),
        ("fail_open_on_missing_view_model_required", decision.fail_open_on_missing_view_model_required),
        ("route_invariant_runtime_mount_required", decision.route_invariant_runtime_mount_required),
        ("final_selection_invisible_runtime_mount_required", decision.final_selection_invisible_runtime_mount_required),
        ("renderer_adapter_separate_future_contract_required", decision.renderer_adapter_separate_future_contract_required),
        ("non_training_feedback_slot_required", decision.non_training_feedback_slot_required),
        ("final_router_remains_authoritative", decision.final_router_remains_authoritative),
        ("ml_advisory_signal_telemetry_only", decision.ml_advisory_signal_telemetry_only),
    )
    for field_name, enabled in required_true:
        if enabled is not True:
            raise ValueError(field_name + " must remain True")

    required_false = (
        ("actual_runtime_panel_activation_enabled", decision.actual_runtime_panel_activation_enabled),
        ("renderer_activation_enabled", decision.renderer_activation_enabled),
        ("mounted_panel_enabled", decision.mounted_panel_enabled),
        ("runtime_ui_mutation_enabled", decision.runtime_ui_mutation_enabled),
        ("runtime_telemetry_surface_wiring_enabled", decision.runtime_telemetry_surface_wiring_enabled),
        ("route_influence_enabled", decision.route_influence_enabled),
        ("route_authority_enabled", decision.route_authority_enabled),
        ("router_calls_enabled", decision.router_calls_enabled),
        ("advisor_calls_enabled", decision.advisor_calls_enabled),
        ("adapter_execution_enabled", decision.adapter_execution_enabled),
        ("provider_calls_enabled", decision.provider_calls_enabled),
        ("persistence_enabled", decision.persistence_enabled),
        ("prompt_loading_enabled", decision.prompt_loading_enabled),
        ("prompt_registry_mutation_enabled", decision.prompt_registry_mutation_enabled),
        ("prompt_library_read_enabled", decision.prompt_library_read_enabled),
        ("freeze_memory_read_enabled", decision.freeze_memory_read_enabled),
        ("freeze_memory_write_enabled", decision.freeze_memory_write_enabled),
        ("router_canon_read_enabled", decision.router_canon_read_enabled),
        ("route_override_button_enabled", decision.route_override_button_enabled),
        ("use_ml_route_button_enabled", decision.use_ml_route_button_enabled),
        ("best_route_claim_enabled", decision.best_route_claim_enabled),
        ("prompt_ranking_enabled", decision.prompt_ranking_enabled),
        ("advisory_ranking_enabled", decision.advisory_ranking_enabled),
        ("free_text_route_advice_enabled", decision.free_text_route_advice_enabled),
        ("free_text_explanations_enabled", decision.free_text_explanations_enabled),
        ("runtime_copilot_decision_behavior_enabled", decision.runtime_copilot_decision_behavior_enabled),
        ("feature_flag_default_enabled", decision.feature_flag_default_enabled),
    )
    for field_name, enabled in required_false:
        if enabled is not False:
            raise ValueError(field_name + " must remain False")

    if decision.critical_boundary_error_budget != 0:
        raise ValueError("critical_boundary_error_budget must remain zero")


def _require_tuple_of_text(name: str, value: Tuple[str, ...]) -> None:
    """Require a non-empty tuple of non-empty text values."""
    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    if not value:
        raise ValueError(name + " must not be empty")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(name + " items must be non-empty text")
