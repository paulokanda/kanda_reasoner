# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_renderer_mount_support.py
"""Private support helpers for the read-only advisory panel renderer mount implementation."""
from __future__ import annotations

from typing import Any, Optional, Tuple

from .read_only_advisory_panel_runtime_activation import (
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelope,
    ReadOnlyPanelRuntimeActivationEnvelopeState,
)

__all__: list[str] = []


def _activation_envelope_is_safe(envelope: ReadOnlyAdvisoryPanelRuntimeActivationEnvelope) -> bool:
    """Support activation envelope is safe behavior.
    
    Parameters
    ----------
    envelope : ReadOnlyAdvisoryPanelRuntimeActivationEnvelope
        The envelope value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        envelope.state is ReadOnlyPanelRuntimeActivationEnvelopeState.READY_READ_ONLY_ACTIVATION_ENVELOPE
        and envelope.runtime_activation_envelope_ready is True
        and envelope.panel_view_model is not None
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


def _render_sections(
    envelope: ReadOnlyAdvisoryPanelRuntimeActivationEnvelope,
    limit: int,
    section_type: Any,
) -> Tuple[Any, ...]:
    """Support render sections behavior.
    
    Parameters
    ----------
    envelope : ReadOnlyAdvisoryPanelRuntimeActivationEnvelope
        The envelope value.
    limit : int
        The limit value.
    section_type : Any
        The section type value.
    
    Returns
    -------
    Tuple[Any, ...]
        The tuple result.
    """
    
    panel = envelope.panel_view_model
    if panel is None:
        return ()
    rendered = []
    for section in panel.sections[:limit]:
        rendered.append(_render_section(section, section_type))
    return tuple(rendered)


def _render_section(section: Any, section_type: Any) -> Any:
    """Support render section behavior.
    
    Parameters
    ----------
    section : Any
        The section value.
    section_type : Any
        The section type value.
    
    Returns
    -------
    Any
        The any result.
    """
    
    return section_type(
        section_key=section.kind.value,
        label=section.label,
        value=section.value,
        severity=section.severity,
    )


def _build_renderer_mount_descriptor(
    *,
    policy: Any,
    activation_envelope: Optional[ReadOnlyAdvisoryPanelRuntimeActivationEnvelope],
    descriptor_type: Any,
    feature_id: str,
    state: Any,
    rendered_sections: Tuple[Any, ...],
    failure_codes: Tuple[str, ...],
    ready: bool,
) -> Any:
    """Support build renderer mount descriptor behavior.
    
    Parameters
    ----------
    policy : Any
        The policy value.
    activation_envelope : Optional[ReadOnlyAdvisoryPanelRuntimeActivationEnvelope]
        The activation envelope value.
    descriptor_type : Any
        The descriptor type value.
    feature_id : str
        The feature id value.
    state : Any
        The state value.
    rendered_sections : Tuple[Any, ...]
        The rendered sections value.
    failure_codes : Tuple[str, ...]
        The failure codes value.
    ready : bool
        The ready value.
    
    Returns
    -------
    Any
        The any result.
    """
    
    panel_view_model = None
    if activation_envelope is not None:
        panel_view_model = activation_envelope.panel_view_model
    return descriptor_type(
        feature_id=feature_id,
        mount_surface_id=policy.mount_surface_id,
        mount_surface_label=policy.mount_surface_label,
        state=state,
        feature_flag_name=policy.feature_flag_name,
        feature_flag_enabled=policy.feature_flag_enabled,
        source_activation_surface_id=activation_envelope.activation_surface_id if activation_envelope else None,
        source_activation_surface_label=activation_envelope.activation_surface_label if activation_envelope else None,
        source_panel_id=activation_envelope.source_panel_id if activation_envelope else None,
        source_panel_label=activation_envelope.source_panel_label if activation_envelope else None,
        canonical_result_id=activation_envelope.canonical_result_id if activation_envelope else None,
        canonical_dispatch_label=activation_envelope.canonical_dispatch_label if activation_envelope else None,
        final_selection_hash=activation_envelope.final_selection_hash if activation_envelope else None,
        rendered_sections=rendered_sections,
        failure_state_codes=failure_codes,
        non_training_feedback_slot_enabled=(
            bool(panel_view_model.non_training_feedback_slot_enabled) if panel_view_model is not None else False
        ),
        read_only_mount_descriptor_ready=ready,
        visible_read_only_panel_ready=ready,
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
        "require_disable_noop_control",
        "require_fail_open_on_missing_envelope",
        "require_block_unsafe_envelope",
        "require_bounded_rendered_sections",
        "require_removable_noop_mount",
        "require_route_invariant_mount",
        "require_final_selection_invisible_mount",
        "require_non_training_feedback_slot",
        "allow_read_only_mount_descriptor",
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
        "allow_runtime_ui_mutation",
        "allow_runtime_telemetry_surface_wiring",
        "allow_route_influence",
        "allow_route_authority",
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
        "allow_route_override_button",
        "allow_use_ml_route_button",
        "allow_best_route_claim",
        "allow_prompt_ranking",
        "allow_advisory_ranking",
        "allow_free_text_route_advice",
        "allow_free_text_explanations",
        "allow_runtime_pilot_behavior",
        "allow_runtime_copilot_decision_behavior",
    )


def _descriptor_required_true_fields() -> Tuple[str, ...]:
    """Support descriptor required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "read_only",
        "telemetry_only",
        "in_memory_only",
        "bounded",
        "fail_open",
        "removable_noop",
        "route_invariant",
        "final_selection_invisible",
        "non_authoritative",
        "consumes_phase9_activation_envelope_only",
    )


def _descriptor_forbidden_true_fields() -> Tuple[str, ...]:
    """Support descriptor forbidden true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
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
    )


def _require_text(name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be non-empty text")


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
    for item in value:
        _require_text(name + " item", item)


def _require_tuple_of_rendered_sections(
    name: str,
    value: Tuple[Any, ...],
    section_type: Any,
) -> None:
    """Support require tuple of rendered sections behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[Any, ...]
        The input value.
    section_type : Any
        The section type value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    for item in value:
        if not isinstance(item, section_type):
            raise TypeError(name + " items must be ReadOnlyAdvisoryPanelRenderedSection")
