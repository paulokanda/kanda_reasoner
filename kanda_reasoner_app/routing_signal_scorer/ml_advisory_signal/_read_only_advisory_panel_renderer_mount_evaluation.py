# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_renderer_mount_evaluation.py
"""Private evaluation helpers for the read-only advisory panel renderer mount contract."""
from __future__ import annotations

from typing import Any, Mapping, Optional, Tuple

from .read_only_advisory_panel_runtime_activation import (
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelope,
    ReadOnlyPanelRuntimeActivationEnvelopeState,
)

__all__: list[str] = []


def _activation_envelope_is_safe(envelope: Optional[ReadOnlyAdvisoryPanelRuntimeActivationEnvelope]) -> bool:
    """Support activation envelope is safe behavior.
    
    Parameters
    ----------
    envelope : Optional[ReadOnlyAdvisoryPanelRuntimeActivationEnvelope]
        The envelope value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        isinstance(envelope, ReadOnlyAdvisoryPanelRuntimeActivationEnvelope)
        and envelope.state is ReadOnlyPanelRuntimeActivationEnvelopeState.READY_READ_ONLY_ACTIVATION_ENVELOPE
        and envelope.runtime_activation_envelope_ready is True
        and envelope.read_only is True
        and envelope.telemetry_only is True
        and envelope.in_memory_only is True
        and envelope.bounded is True
        and envelope.fail_open is True
        and envelope.removable_noop is True
        and envelope.route_invariant is True
        and envelope.final_selection_invisible is True
        and envelope.renderer_neutral is True
        and envelope.non_authoritative is True
        and envelope.actual_runtime_panel_activation_enabled is False
        and envelope.renderer_activation_enabled is False
        and envelope.mounted_panel_enabled is False
        and envelope.runtime_ui_mutation_enabled is False
        and envelope.runtime_telemetry_surface_wiring_enabled is False
        and envelope.route_influence_enabled is False
        and envelope.route_authority_enabled is False
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
    runtime_wiring = {
        "actual_runtime_panel_activation", "actual_renderer_mount", "renderer_activation",
        "mounted_panel", "runtime_ui_mutation", "runtime_telemetry_surface_wiring",
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
        if key in runtime_wiring:
            return status_type.BLOCKED_UNSAFE_RUNTIME_WIRING
        if key in data_or_side_effect:
            return status_type.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT
        if key in text_or_controls:
            return status_type.BLOCKED_UNSAFE_TEXT_OR_CONTROLS
    return None


def _build_renderer_mount_decision(
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
    """Support build renderer mount decision behavior.
    
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
        mount_mode=policy.mount_mode,
        future_renderer_mount_contract_ready=ready,
        contract_only=True,
        phase9_activation_envelope_input_required=policy.require_phase9_activation_envelope_input,
        explicit_feature_flag_required=policy.require_explicit_feature_flag,
        feature_flag_default_enabled=policy.feature_flag_default_enabled,
        disabled_noop_control_required=policy.require_disable_noop_control,
        fail_open_on_missing_envelope_required=policy.require_fail_open_on_missing_envelope,
        route_invariant_mount_required=policy.require_route_invariant_mount,
        final_selection_invisible_mount_required=policy.require_final_selection_invisible_mount,
        renderer_input_bounded_required=policy.require_renderer_input_bounded,
        renderer_output_bounded_required=policy.require_renderer_output_bounded,
        removable_noop_mount_required=policy.require_removable_noop_mount,
        non_training_feedback_slot_required=policy.require_non_training_feedback_slot,
        actual_runtime_panel_activation_enabled=False,
        actual_renderer_mount_enabled=False,
        renderer_activation_enabled=False,
        mounted_panel_enabled=False,
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
        "require_phase9_activation_envelope_input",
        "require_explicit_feature_flag",
        "require_disable_noop_control",
        "require_fail_open_on_missing_envelope",
        "require_route_invariant_mount",
        "require_final_selection_invisible_mount",
        "require_renderer_input_bounded",
        "require_renderer_output_bounded",
        "require_removable_noop_mount",
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
        "allow_actual_runtime_panel_activation_in_this_phase",
        "allow_actual_renderer_mount_in_this_phase",
        "allow_renderer_activation_in_this_phase",
        "allow_mounted_panel_in_this_phase",
        "allow_runtime_ui_mutation_in_this_phase",
        "allow_runtime_telemetry_surface_wiring_in_this_phase",
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
        "phase9_activation_envelope_input_required",
        "explicit_feature_flag_required",
        "disabled_noop_control_required",
        "fail_open_on_missing_envelope_required",
        "route_invariant_mount_required",
        "final_selection_invisible_mount_required",
        "renderer_input_bounded_required",
        "renderer_output_bounded_required",
        "removable_noop_mount_required",
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
        "actual_runtime_panel_activation_enabled",
        "actual_renderer_mount_enabled",
        "renderer_activation_enabled",
        "mounted_panel_enabled",
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
