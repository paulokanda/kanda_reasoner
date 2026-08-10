# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_passive_visibility_activation.py
"""Phase 13 read-only advisory panel passive visibility activation implementation.

This module implements a minimal in-memory passive visibility activation
_descriptor_ for the read-only advisory panel line. It consumes only the
Phase 12 runtime app-host visibility descriptor lineage and produces bounded
passive visibility slot metadata for a future app host.

It does not perform actual passive visibility activation, register or mutate a
passive visibility slot in a host, activate runtime app-host visibility, mount a
runtime panel, mutate runtime UI, wire telemetry surfaces, subscribe to host
events, register host callbacks, call the router, call an advisor, execute
adapters, call providers, persist data, read prompt libraries, read freeze
memory, read router canon, influence routes, grant ML route authority, or create
runtime Copilot decision behavior.
"""

from __future__ import annotations


__all__ = [
    'build_phase13_read_only_panel_passive_visibility_activation_implementation_probe',
    'build_read_only_advisory_panel_passive_visibility_activation_descriptor',
    'ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor',
    'ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy',
    'ReadOnlyAdvisoryPanelPassiveVisibilitySlot',
    'ReadOnlyPanelPassiveVisibilityActivationImplementationState',
]
from typing import Optional, Tuple

from ._passive_visibility_activation_models import (
    FEATURE_ID,
)
from .model_contracts.passive_visibility_activation import (
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor,
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy,
    ReadOnlyAdvisoryPanelPassiveVisibilitySlot,
    ReadOnlyPanelPassiveVisibilityActivationImplementationState,
)
from .read_only_advisory_panel_runtime_app_host_visibility import (
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor,
    ReadOnlyAdvisoryPanelRuntimeVisibleSection,
    ReadOnlyPanelRuntimeAppHostVisibilityImplementationState,
    build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe,
)


# Keep public class introspection paths on the original facade.
ReadOnlyPanelPassiveVisibilityActivationImplementationState.__module__ = __name__
ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy.__module__ = __name__
ReadOnlyAdvisoryPanelPassiveVisibilitySlot.__module__ = __name__
ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor.__module__ = __name__


def build_read_only_advisory_panel_passive_visibility_activation_descriptor(
    policy: ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy,
    runtime_visibility_descriptor: object | None,
) -> ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor:
    """Build the Phase 13 read-only passive visibility activation descriptor.

    The successful path requires an explicitly enabled feature flag and a safe
    Phase 12 runtime app-host visibility descriptor. Missing or unsafe input
    fails open without passive slot registration, visibility activation, UI
    mutation, telemetry surface wiring, route influence, provider calls,
    persistence, host event subscriptions, callback registration, or route
    authority.
    """

    if not isinstance(policy, ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy")

    if not policy.enabled or not policy.feature_flag_enabled:
        return _build_descriptor(
            policy=policy,
            runtime_visibility_descriptor=None,
            state=ReadOnlyPanelPassiveVisibilityActivationImplementationState.DISABLED_NOOP,
            passive_visibility_slots=(),
            failure_codes=("feature_flag_default_off",),
            ready=False,
        )

    if not isinstance(runtime_visibility_descriptor, ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor):
        return _build_descriptor(
            policy=policy,
            runtime_visibility_descriptor=None,
            state=ReadOnlyPanelPassiveVisibilityActivationImplementationState.FAIL_OPEN_NO_DESCRIPTOR,
            passive_visibility_slots=(),
            failure_codes=("missing_or_invalid_runtime_app_host_visibility_descriptor",),
            ready=False,
        )

    if not _runtime_visibility_descriptor_is_safe(runtime_visibility_descriptor):
        return _build_descriptor(
            policy=policy,
            runtime_visibility_descriptor=runtime_visibility_descriptor,
            state=ReadOnlyPanelPassiveVisibilityActivationImplementationState.BLOCKED_UNSAFE_DESCRIPTOR,
            passive_visibility_slots=(),
            failure_codes=("unsafe_runtime_app_host_visibility_descriptor_rejected",),
            ready=False,
        )

    slots = _make_passive_visibility_slots(runtime_visibility_descriptor, policy.max_passive_visibility_slots)
    return _build_descriptor(
        policy=policy,
        runtime_visibility_descriptor=runtime_visibility_descriptor,
        state=ReadOnlyPanelPassiveVisibilityActivationImplementationState.READ_ONLY_PASSIVE_VISIBILITY_ACTIVATION_DESCRIPTOR_READY,
        passive_visibility_slots=slots,
        failure_codes=(),
        ready=True,
    )


def build_phase13_read_only_panel_passive_visibility_activation_implementation_probe(
) -> ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor:
    """Build a safe feature-flag-enabled passive visibility activation descriptor probe."""

    policy = ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy(
        passive_visibility_surface_id="phase13_read_only_panel_passive_visibility_activation_descriptor",
        passive_visibility_surface_label="Phase 13 Read-Only Advisory Panel Passive Visibility Activation",
        feature_flag_enabled=True,
    )
    descriptor = build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe()
    return build_read_only_advisory_panel_passive_visibility_activation_descriptor(policy, descriptor)


def _build_descriptor(
    *,
    policy: ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy,
    runtime_visibility_descriptor: Optional[ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor],
    state: ReadOnlyPanelPassiveVisibilityActivationImplementationState,
    passive_visibility_slots: Tuple[ReadOnlyAdvisoryPanelPassiveVisibilitySlot, ...],
    failure_codes: Tuple[str, ...],
    ready: bool,
) -> ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor:
    """Support build descriptor behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy
        The policy value.
    runtime_visibility_descriptor : Optional[ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor]
        The runtime visibility descriptor value.
    state : ReadOnlyPanelPassiveVisibilityActivationImplementationState
        The state value.
    passive_visibility_slots : Tuple[ReadOnlyAdvisoryPanelPassiveVisibilitySlot, ...]
        The passive visibility slots value.
    failure_codes : Tuple[str, ...]
        The failure codes value.
    ready : bool
        The ready value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor
        The read only advisory panel passive visibility activation descriptor result.
    """
    
    return ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor(
        feature_id=FEATURE_ID,
        passive_visibility_surface_id=policy.passive_visibility_surface_id,
        passive_visibility_surface_label=policy.passive_visibility_surface_label,
        state=state,
        feature_flag_name=policy.feature_flag_name,
        feature_flag_enabled=policy.feature_flag_enabled,
        source_visibility_surface_id=(
            runtime_visibility_descriptor.visibility_surface_id if runtime_visibility_descriptor else None
        ),
        source_visibility_surface_label=(
            runtime_visibility_descriptor.visibility_surface_label if runtime_visibility_descriptor else None
        ),
        source_host_container_id=(
            runtime_visibility_descriptor.source_host_container_id if runtime_visibility_descriptor else None
        ),
        source_host_container_label=(
            runtime_visibility_descriptor.source_host_container_label if runtime_visibility_descriptor else None
        ),
        source_mount_surface_id=(
            runtime_visibility_descriptor.source_mount_surface_id if runtime_visibility_descriptor else None
        ),
        source_mount_surface_label=(
            runtime_visibility_descriptor.source_mount_surface_label if runtime_visibility_descriptor else None
        ),
        source_panel_id=runtime_visibility_descriptor.source_panel_id if runtime_visibility_descriptor else None,
        source_panel_label=runtime_visibility_descriptor.source_panel_label if runtime_visibility_descriptor else None,
        canonical_result_id=runtime_visibility_descriptor.canonical_result_id if runtime_visibility_descriptor else None,
        canonical_dispatch_label=(
            runtime_visibility_descriptor.canonical_dispatch_label if runtime_visibility_descriptor else None
        ),
        final_selection_hash=runtime_visibility_descriptor.final_selection_hash if runtime_visibility_descriptor else None,
        passive_visibility_slots=passive_visibility_slots,
        failure_state_codes=failure_codes,
        non_training_feedback_slot_enabled=(
            bool(runtime_visibility_descriptor.non_training_feedback_slot_enabled)
            if runtime_visibility_descriptor is not None else False
        ),
        read_only_passive_visibility_activation_descriptor_ready=ready,
        passive_visibility_slot_descriptor_ready=ready,
        runtime_app_host_visibility_descriptor_consumed=ready,
    )


def _runtime_visibility_descriptor_is_safe(
    descriptor: ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor,
) -> bool:
    """Support runtime visibility descriptor is safe behavior.
    
    Parameters
    ----------
    descriptor : ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor
        The descriptor value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
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


def _make_passive_visibility_slots(
    descriptor: ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor,
    limit: int,
) -> Tuple[ReadOnlyAdvisoryPanelPassiveVisibilitySlot, ...]:
    """Support make passive visibility slots behavior.
    
    Parameters
    ----------
    descriptor : ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor
        The descriptor value.
    limit : int
        The limit value.
    
    Returns
    -------
    Tuple[ReadOnlyAdvisoryPanelPassiveVisibilitySlot, ...]
        The tuple result.
    """
    
    slots = []
    for section in descriptor.visible_sections[:limit]:
        slots.append(_make_passive_visibility_slot(section))
    return tuple(slots)


def _make_passive_visibility_slot(
    section: ReadOnlyAdvisoryPanelRuntimeVisibleSection,
) -> ReadOnlyAdvisoryPanelPassiveVisibilitySlot:
    """Support make passive visibility slot behavior.
    
    Parameters
    ----------
    section : ReadOnlyAdvisoryPanelRuntimeVisibleSection
        The section value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelPassiveVisibilitySlot
        The read only advisory panel passive visibility slot result.
    """
    
    return ReadOnlyAdvisoryPanelPassiveVisibilitySlot(
        slot_key=section.section_key,
        label=section.label,
        value=section.value,
        severity=section.severity,
        host_role=section.host_role,
    )
