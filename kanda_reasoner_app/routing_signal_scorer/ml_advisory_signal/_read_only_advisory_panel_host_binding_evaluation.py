# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_host_binding_evaluation.py
"""Private evaluation helpers for the read-only advisory panel host binding contract."""
from __future__ import annotations

from typing import Any, Mapping, Optional, Tuple

from .read_only_advisory_panel_renderer_mount import (
    ReadOnlyAdvisoryPanelRendererMountDescriptor,
    ReadOnlyPanelRendererMountImplementationState,
)

__all__: list[str] = []


def _renderer_mount_descriptor_is_safe(
    descriptor: Optional[ReadOnlyAdvisoryPanelRendererMountDescriptor],
) -> bool:
    """Support renderer mount descriptor is safe behavior.
    
    Parameters
    ----------
    descriptor : Optional[ReadOnlyAdvisoryPanelRendererMountDescriptor]
        The descriptor value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        isinstance(descriptor, ReadOnlyAdvisoryPanelRendererMountDescriptor)
        and descriptor.state is ReadOnlyPanelRendererMountImplementationState.READ_ONLY_MOUNT_DESCRIPTOR_READY
        and descriptor.read_only_mount_descriptor_ready is True
        and descriptor.visible_read_only_panel_ready is True
        and descriptor.read_only is True
        and descriptor.telemetry_only is True
        and descriptor.in_memory_only is True
        and descriptor.bounded is True
        and descriptor.fail_open is True
        and descriptor.removable_noop is True
        and descriptor.route_invariant is True
        and descriptor.final_selection_invisible is True
        and descriptor.non_authoritative is True
        and descriptor.runtime_ui_mutation_enabled is False
        and descriptor.runtime_telemetry_surface_wiring_enabled is False
        and descriptor.route_influence_enabled is False
        and descriptor.route_authority_enabled is False
        and descriptor.router_calls_enabled is False
        and descriptor.advisor_calls_enabled is False
        and descriptor.provider_calls_enabled is False
        and descriptor.persistence_enabled is False
        and descriptor.runtime_copilot_decision_behavior_enabled is False
    )


def _status_for_requested_capabilities(
    requested: Mapping[str, bool],
    status_type: Any,
) -> Optional[Any]:
    """Support status for requested capabilities behavior.
    
    Parameters
    ----------
    requested : Mapping[str, bool]
        The requested value.
    status_type : Any
        The status type value.
    
    Returns
    -------
    Optional[Any]
        The optional result.
    """
    
    authority = {
        "route_authority", "route_influence", "route_override_button", "use_ml_route_button",
        "best_route_claim", "final_selection_hook", "prompt_selection_hook",
        "runtime_copilot_decision_behavior",
    }
    runtime_host_binding = {
        "actual_host_binding", "host_binding_activation", "runtime_app_host_visibility",
        "mounted_runtime_panel", "host_event_subscription", "host_callback_registration",
        "runtime_ui_mutation", "runtime_telemetry_surface_wiring",
    }
    data_or_side_effect = {
        "router_call", "advisor_call", "adapter_execution", "provider_call", "persistence_write",
        "prompt_loading", "prompt_registry_mutation", "prompt_library_read", "freeze_memory_read",
        "freeze_memory_write", "router_canon_read",
    }
    text_or_controls = {
        "prompt_ranking", "advisory_ranking", "free_text_route_advice", "free_text_explanation",
    }
    for key, enabled in requested.items():
        if enabled is not True:
            continue
        if key in authority:
            return status_type.BLOCKED_UNSAFE_AUTHORITY
        if key in runtime_host_binding:
            return status_type.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING
        if key in data_or_side_effect:
            return status_type.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT
        if key in text_or_controls:
            return status_type.BLOCKED_UNSAFE_TEXT_OR_CONTROLS
    return None


def _build_host_binding_decision(
    *,
    policy: Any,
    decision_type: Any,
    feature_id: str,
    status: Any,
    accepted: bool,
    ready: bool,
    required_safe_labels: Tuple[str, ...],
    forbidden_capabilities: Tuple[str, ...],
) -> Any:
    """Support build host binding decision behavior.
    
    Parameters
    ----------
    policy : Any
        The policy value.
    decision_type : Any
        The decision type value.
    feature_id : str
        The feature id value.
    status : Any
        The status value.
    accepted : bool
        The accepted value.
    ready : bool
        The ready value.
    required_safe_labels : Tuple[str, ...]
        The required safe labels value.
    forbidden_capabilities : Tuple[str, ...]
        The forbidden capabilities value.
    
    Returns
    -------
    Any
        The any result.
    """
    
    return decision_type(
        feature_id=feature_id,
        status=status,
        accepted=accepted,
        host_binding_mode=policy.host_binding_mode,
        future_host_binding_contract_ready=ready,
        contract_only=True,
        phase10_renderer_mount_descriptor_input_required=policy.require_phase10_renderer_mount_descriptor_input,
        explicit_feature_flag_required=policy.require_explicit_feature_flag,
        feature_flag_default_enabled=policy.feature_flag_default_enabled,
        disabled_noop_control_required=policy.require_disable_noop_control,
        fail_open_on_missing_descriptor_required=policy.require_fail_open_on_missing_descriptor,
        block_unsafe_descriptor_required=policy.require_block_unsafe_descriptor,
        route_invariant_host_binding_required=policy.require_route_invariant_host_binding,
        final_selection_invisible_host_binding_required=policy.require_final_selection_invisible_host_binding,
        host_input_bounded_required=policy.require_host_input_bounded,
        host_output_bounded_required=policy.require_host_output_bounded,
        removable_noop_host_binding_required=policy.require_removable_noop_host_binding,
        non_training_feedback_slot_required=policy.require_non_training_feedback_slot,
        actual_host_binding_enabled=False,
        host_binding_activation_enabled=False,
        runtime_app_host_visibility_enabled=False,
        mounted_runtime_panel_enabled=False,
        host_event_subscription_enabled=False,
        host_callback_registration_enabled=False,
        runtime_ui_mutation_enabled=False,
        runtime_telemetry_surface_wiring_enabled=False,
        route_influence_enabled=False,
        route_authority_enabled=False,
        router_calls_enabled=False,
        advisor_calls_enabled=False,
        adapter_execution_enabled=False,
        provider_calls_enabled=False,
        persistence_enabled=False,
        prompt_loading_enabled=False,
        prompt_registry_mutation_enabled=False,
        prompt_library_read_enabled=False,
        freeze_memory_read_enabled=False,
        freeze_memory_write_enabled=False,
        router_canon_read_enabled=False,
        route_override_button_enabled=False,
        use_ml_route_button_enabled=False,
        best_route_claim_enabled=False,
        prompt_ranking_enabled=False,
        advisory_ranking_enabled=False,
        free_text_route_advice_enabled=False,
        free_text_explanations_enabled=False,
        runtime_copilot_decision_behavior_enabled=False,
        required_safe_labels=required_safe_labels,
        forbidden_capabilities=forbidden_capabilities,
        final_router_remains_authoritative=True,
        ml_advisory_signal_telemetry_only=True,
        critical_boundary_error_budget=0,
    )


def _policy_required_true_fields() -> Tuple[str, ...]:
    """Support policy required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "require_phase10_renderer_mount_descriptor_input",
        "require_explicit_feature_flag",
        "require_disable_noop_control",
        "require_fail_open_on_missing_descriptor",
        "require_block_unsafe_descriptor",
        "require_route_invariant_host_binding",
        "require_final_selection_invisible_host_binding",
        "require_host_input_bounded",
        "require_host_output_bounded",
        "require_removable_noop_host_binding",
        "require_non_training_feedback_slot",
    )


def _policy_required_false_fields() -> Tuple[str, ...]:
    """Support policy required false fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "feature_flag_default_enabled",
        "allow_actual_host_binding_in_this_phase",
        "allow_host_binding_activation_in_this_phase",
        "allow_runtime_app_host_visibility_in_this_phase",
        "allow_mounted_runtime_panel_in_this_phase",
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
        "allow_runtime_copilot_decision_behavior",
    )


def _decision_required_true_fields() -> Tuple[str, ...]:
    """Support decision required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "contract_only",
        "phase10_renderer_mount_descriptor_input_required",
        "explicit_feature_flag_required",
        "disabled_noop_control_required",
        "fail_open_on_missing_descriptor_required",
        "block_unsafe_descriptor_required",
        "route_invariant_host_binding_required",
        "final_selection_invisible_host_binding_required",
        "host_input_bounded_required",
        "host_output_bounded_required",
        "removable_noop_host_binding_required",
        "non_training_feedback_slot_required",
        "final_router_remains_authoritative",
        "ml_advisory_signal_telemetry_only",
    )


def _decision_required_false_fields() -> Tuple[str, ...]:
    """Support decision required false fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
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
        "runtime_copilot_decision_behavior_enabled",
        "feature_flag_default_enabled",
    )


def _require_tuple_of_text(name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple of text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[str, ...]
        The input value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    if not value:
        raise ValueError(name + " must not be empty")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(name + " items must be non-empty text")
