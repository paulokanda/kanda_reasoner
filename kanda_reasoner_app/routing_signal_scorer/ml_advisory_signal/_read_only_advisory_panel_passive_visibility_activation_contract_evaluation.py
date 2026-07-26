# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_passive_visibility_activation_contract_evaluation.py
"""Private pure evaluation helpers for the Phase 13 activation contract."""

from __future__ import annotations

from typing import Mapping

from .read_only_advisory_panel_runtime_app_host_visibility import (
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor,
    ReadOnlyPanelRuntimeAppHostVisibilityImplementationState,
)

__all__: list[str] = []


def _source_descriptor_is_safe(descriptor: object) -> bool:
    """Support source descriptor is safe behavior.
    
    Parameters
    ----------
    descriptor : object
        The descriptor value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not isinstance(descriptor, ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor):
        return False
    return (
        descriptor.state is ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.READ_ONLY_VISIBILITY_DESCRIPTOR_READY
        and descriptor.read_only_runtime_app_host_visibility_descriptor_ready is True
        and descriptor.visible_read_only_panel_descriptor_ready is True
        and descriptor.mounted_runtime_panel_descriptor_ready is True
        and descriptor.read_only is True
        and descriptor.telemetry_only is True
        and descriptor.in_memory_only is True
        and descriptor.bounded is True
        and descriptor.fail_open is True
        and descriptor.removable_noop is True
        and descriptor.route_invariant is True
        and descriptor.final_selection_invisible is True
        and descriptor.non_authoritative is True
        and descriptor.consumes_phase11_host_binding_descriptor_only is True
        and descriptor.actual_runtime_app_host_visibility_enabled is False
        and descriptor.visibility_activation_enabled is False
        and descriptor.mounted_runtime_panel_enabled is False
        and descriptor.runtime_panel_mount_side_effects_enabled is False
        and descriptor.host_event_subscription_enabled is False
        and descriptor.host_callback_registration_enabled is False
        and descriptor.runtime_ui_mutation_enabled is False
        and descriptor.runtime_telemetry_surface_wiring_enabled is False
        and descriptor.route_influence_enabled is False
        and descriptor.route_authority_enabled is False
        and descriptor.router_calls_enabled is False
        and descriptor.advisor_calls_enabled is False
        and descriptor.adapter_execution_enabled is False
        and descriptor.provider_calls_enabled is False
        and descriptor.persistence_enabled is False
        and descriptor.prompt_loading_enabled is False
        and descriptor.prompt_registry_mutation_enabled is False
        and descriptor.prompt_library_read_enabled is False
        and descriptor.freeze_memory_read_enabled is False
        and descriptor.freeze_memory_write_enabled is False
        and descriptor.router_canon_read_enabled is False
        and descriptor.runtime_copilot_decision_behavior_enabled is False
        and descriptor.autonomous_ml_router_enabled is False
    )


def _request_capabilities(request: Mapping[str, object]) -> set[str]:
    """Support request capabilities behavior.
    
    Parameters
    ----------
    request : Mapping[str, object]
        The request value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    raw = request.get("capabilities", ())
    if isinstance(raw, str):
        return {raw}
    if isinstance(raw, (list, tuple, set, frozenset)):
        return {str(item) for item in raw}
    return set()


def _truthy(request: Mapping[str, object], key: str) -> bool:
    """Support truthy behavior.
    
    Parameters
    ----------
    request : Mapping[str, object]
        The request value.
    key : str
        The key value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return bool(request.get(key))


def _authority_capabilities() -> set[str]:
    """Support authority capabilities behavior.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {"route_authority", "route_influence", "router_call", "final_selection_hook", "prompt_selection_hook"}


def _activation_capabilities() -> set[str]:
    """Support activation capabilities behavior.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {
        "actual_passive_visibility_activation",
        "passive_visibility_activation",
        "passive_visibility_slot_registration",
        "passive_visibility_slot_mutation",
        "actual_runtime_app_host_visibility",
        "runtime_app_host_visibility_activation",
        "mounted_runtime_panel",
        "runtime_panel_mount_side_effect",
    }


def _side_effect_capabilities() -> set[str]:
    """Support side effect capabilities behavior.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {
        "host_event_subscription",
        "host_callback_registration",
        "runtime_ui_mutation",
        "runtime_telemetry_surface_wiring",
        "advisor_call",
        "adapter_execution",
        "provider_call",
        "persistence_write",
        "prompt_loading",
        "prompt_registry_mutation",
        "prompt_library_read",
        "freeze_memory_read",
        "freeze_memory_write",
        "router_canon_read",
        "runtime_copilot_decision_behavior",
        "autonomous_ml_router",
    }


def _text_or_control_capabilities() -> set[str]:
    """Support text or control capabilities behavior.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    return {
        "route_override_button",
        "use_ml_route_button",
        "best_route_claim",
        "prompt_ranking",
        "advisory_ranking",
        "free_text_route_advice",
        "free_text_explanation",
    }
