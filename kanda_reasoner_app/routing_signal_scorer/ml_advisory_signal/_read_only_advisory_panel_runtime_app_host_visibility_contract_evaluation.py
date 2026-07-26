# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_runtime_app_host_visibility_contract_evaluation.py
"""Explicit request and source-descriptor evaluation for the Phase 12 contract.

This private helper owns request normalization, forbidden-capability membership
checks, and Phase 11 source-descriptor safety evaluation. It does not import the
public contract facade, so dependency direction remains facade -> helper.
"""

from __future__ import annotations

from typing import Mapping, Tuple

from .read_only_advisory_panel_host_binding import (
    ReadOnlyAdvisoryPanelHostBindingDescriptor,
    ReadOnlyPanelHostBindingImplementationState,
)

__all__ = []

FORBIDDEN_RUNTIME_APP_HOST_VISIBILITY_CAPABILITIES: Tuple[str, ...] = (
    "route_override_button",
    "use_ml_route_button",
    "best_route_claim",
    "prompt_ranking",
    "advisory_ranking",
    "free_text_route_advice",
    "free_text_explanation",
    "final_selection_hook",
    "prompt_selection_hook",
    "router_call",
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
    "route_influence",
    "route_authority",
    "actual_runtime_app_host_visibility",
    "runtime_app_host_visibility_activation",
    "mounted_runtime_panel",
    "runtime_panel_mount_side_effect",
    "host_event_subscription",
    "host_callback_registration",
    "runtime_ui_mutation",
    "runtime_telemetry_surface_wiring",
    "runtime_copilot_decision_behavior",
    "autonomous_ml_router",
)

REQUIRED_RUNTIME_APP_HOST_VISIBILITY_CONTRACT_LABELS: Tuple[str, ...] = (
    "read_only_panel_label",
    "advisory_role_label",
    "runtime_app_host_visibility_default_off_label",
    "canonical_route_unchanged_label",
    "no_route_authority_label",
    "confidence_not_correctness_label",
    "non_training_feedback_label",
)


def source_host_binding_descriptor_is_safe(descriptor: object) -> bool:
    """Return whether the Phase 11 descriptor satisfies every safety boundary."""
    return (
        isinstance(descriptor, ReadOnlyAdvisoryPanelHostBindingDescriptor)
        and descriptor.state
        is ReadOnlyPanelHostBindingImplementationState.READ_ONLY_HOST_BINDING_DESCRIPTOR_READY
        and descriptor.read_only_host_binding_descriptor_ready is True
        and descriptor.runtime_app_host_visibility_descriptor_ready is True
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
        and descriptor.consumes_phase10_renderer_mount_descriptor_only is True
        and descriptor.actual_host_binding_enabled is False
        and descriptor.host_binding_activation_enabled is False
        and descriptor.runtime_app_host_visibility_enabled is False
        and descriptor.mounted_runtime_panel_enabled is False
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
    )


def requested_capabilities(request: Mapping[str, object]) -> Tuple[str, ...]:
    """Return normalized explicit and boolean-enabled request capabilities."""
    result: list[str] = []
    capabilities = request.get("capabilities", ())
    if isinstance(capabilities, str):
        capabilities = (capabilities,)
    if isinstance(capabilities, (list, tuple, set)):
        result.extend(
            str(item).strip()
            for item in capabilities
            if str(item).strip()
        )
    for key, value in request.items():
        if isinstance(value, bool) and value is True:
            result.append(str(key).strip())
    return tuple(item for item in result if item)


def contains_any(requested: Tuple[str, ...], forbidden: Tuple[str, ...]) -> bool:
    """Return whether requested capabilities intersect one forbidden set."""
    requested_set = set(requested)
    return any(item in requested_set for item in forbidden)
