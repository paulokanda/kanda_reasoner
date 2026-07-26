# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_host_binding.py
"""Phase 11 read-only advisory panel host binding implementation.

This module implements a minimal in-memory host-binding descriptor for the
read-only advisory panel line. It consumes only the Phase 10 renderer/mount
descriptor lineage and produces bounded host-display binding metadata.

It does not mutate runtime UI, wire telemetry surfaces, subscribe to host
events, register host callbacks, call the router, call an advisor, execute
adapters, call providers, persist data, read prompt libraries, read freeze
memory, read router canon, influence routes, or grant ML route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase11_read_only_panel_host_binding_implementation_probe',
    'build_read_only_advisory_panel_host_binding_descriptor',
    'ReadOnlyAdvisoryPanelHostBindingDescriptor',
    'ReadOnlyAdvisoryPanelHostBindingImplementationPolicy',
    'ReadOnlyAdvisoryPanelHostBoundSection',
    'ReadOnlyPanelHostBindingImplementationState',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from ._read_only_advisory_panel_host_binding_invariants import (
    validate_descriptor,
    validate_host_bound_section,
    validate_policy,
)

from .read_only_advisory_panel_renderer_mount import (
    ReadOnlyAdvisoryPanelRenderedSection,
    ReadOnlyAdvisoryPanelRendererMountDescriptor,
    ReadOnlyPanelRendererMountImplementationState,
    build_phase10_read_only_panel_renderer_mount_implementation_probe,
)


FEATURE_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_implementation_v1"
SOURCE_REVIEW_FEATURE_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_contract_result_review_gate_v1"
SOURCE_CONTRACT_FEATURE_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_contract_v1"
SOURCE_RENDERER_MOUNT_IMPLEMENTATION_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1"


class ReadOnlyPanelHostBindingImplementationState(str, Enum):
    """Safe states for the read-only host-binding descriptor builder."""

    DISABLED_NOOP = "disabled_noop"
    FAIL_OPEN_NO_DESCRIPTOR = "fail_open_no_descriptor"
    BLOCKED_UNSAFE_DESCRIPTOR = "blocked_unsafe_descriptor"
    READ_ONLY_HOST_BINDING_DESCRIPTOR_READY = "read_only_host_binding_descriptor_ready"


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelHostBindingImplementationPolicy:
    """Policy for building a read-only host-binding descriptor.

    The feature flag is default-off. When explicitly enabled, this policy may
    build only an in-memory descriptor from the Phase 10 renderer/mount
    descriptor. It must not mutate runtime UI, subscribe to host events,
    register callbacks, or influence routing.
    """

    host_container_id: str
    host_container_label: str
    source_review_feature_id: str = SOURCE_REVIEW_FEATURE_ID
    source_contract_feature_id: str = SOURCE_CONTRACT_FEATURE_ID
    source_renderer_mount_implementation_id: str = SOURCE_RENDERER_MOUNT_IMPLEMENTATION_ID
    enabled: bool = True
    feature_flag_name: str = "ml_advisory_read_only_panel_host_binding"
    feature_flag_enabled: bool = False
    feature_flag_default_enabled: bool = False
    max_host_sections: int = 11
    require_phase10_renderer_mount_descriptor_input: bool = True
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_descriptor: bool = True
    require_block_unsafe_descriptor: bool = True
    require_bounded_host_sections: bool = True
    require_removable_noop_host_binding: bool = True
    require_route_invariant_host_binding: bool = True
    require_final_selection_invisible_host_binding: bool = True
    require_non_training_feedback_slot: bool = True
    allow_read_only_host_binding_descriptor: bool = True
    allow_actual_host_binding: bool = False
    allow_host_binding_activation: bool = False
    allow_runtime_app_host_visibility: bool = False
    allow_mounted_runtime_panel: bool = False
    allow_host_event_subscription: bool = False
    allow_host_callback_registration: bool = False
    allow_runtime_ui_mutation: bool = False
    allow_runtime_telemetry_surface_wiring: bool = False
    allow_route_influence: bool = False
    allow_route_authority: bool = False
    allow_router_calls: bool = False
    allow_advisor_calls: bool = False
    allow_adapter_execution: bool = False
    allow_provider_calls: bool = False
    allow_persistence: bool = False
    allow_prompt_loading: bool = False
    allow_prompt_registry_mutation: bool = False
    allow_prompt_library_read: bool = False
    allow_freeze_memory_read: bool = False
    allow_freeze_memory_write: bool = False
    allow_router_canon_read: bool = False
    allow_route_override_button: bool = False
    allow_use_ml_route_button: bool = False
    allow_best_route_claim: bool = False
    allow_prompt_ranking: bool = False
    allow_advisory_ranking: bool = False
    allow_free_text_route_advice: bool = False
    allow_free_text_explanations: bool = False
    allow_runtime_pilot_behavior: bool = False
    allow_runtime_copilot_decision_behavior: bool = False

    def __post_init__(self) -> None:
        """Validate the host-binding implementation policy."""
        validate_policy(
            self,
            source_review_feature_id=SOURCE_REVIEW_FEATURE_ID,
            source_contract_feature_id=SOURCE_CONTRACT_FEATURE_ID,
            source_renderer_mount_implementation_id=(
                SOURCE_RENDERER_MOUNT_IMPLEMENTATION_ID
            ),
        )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelHostBoundSection:
    """Bounded host-facing section copied from the Phase 10 descriptor."""

    section_key: str
    label: str
    value: str
    severity: str
    host_role: str = "advisory_observation"
    read_only: bool = True
    action_enabled: bool = False
    route_authority_enabled: bool = False
    route_influence_enabled: bool = False
    host_callback_enabled: bool = False
    free_text_route_advice_enabled: bool = False

    def __post_init__(self) -> None:
        """Validate one bounded host-facing section."""
        validate_host_bound_section(self)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelHostBindingDescriptor:
    """In-memory read-only host-binding descriptor.

    This is the Phase 11 implementation output. It is bounded host-facing
    metadata only, not an app-host mutation, host callback registration, host
    event subscription, router hook, or route authority surface.
    """

    feature_id: str
    host_container_id: str
    host_container_label: str
    state: ReadOnlyPanelHostBindingImplementationState
    feature_flag_name: str
    feature_flag_enabled: bool
    source_mount_surface_id: Optional[str]
    source_mount_surface_label: Optional[str]
    source_panel_id: Optional[str]
    source_panel_label: Optional[str]
    canonical_result_id: Optional[str]
    canonical_dispatch_label: Optional[str]
    final_selection_hash: Optional[str]
    host_bound_sections: Tuple[ReadOnlyAdvisoryPanelHostBoundSection, ...]
    failure_state_codes: Tuple[str, ...]
    non_training_feedback_slot_enabled: bool
    read_only_host_binding_descriptor_ready: bool
    runtime_app_host_visibility_descriptor_ready: bool
    mounted_runtime_panel_descriptor_ready: bool
    read_only: bool = True
    telemetry_only: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    consumes_phase10_renderer_mount_descriptor_only: bool = True
    actual_host_binding_enabled: bool = False
    host_binding_activation_enabled: bool = False
    runtime_app_host_visibility_enabled: bool = False
    mounted_runtime_panel_enabled: bool = False
    host_event_subscription_enabled: bool = False
    host_callback_registration_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    runtime_telemetry_surface_wiring_enabled: bool = False
    route_influence_enabled: bool = False
    route_authority_enabled: bool = False
    router_calls_enabled: bool = False
    advisor_calls_enabled: bool = False
    adapter_execution_enabled: bool = False
    provider_calls_enabled: bool = False
    persistence_enabled: bool = False
    prompt_loading_enabled: bool = False
    prompt_registry_mutation_enabled: bool = False
    prompt_library_read_enabled: bool = False
    freeze_memory_read_enabled: bool = False
    freeze_memory_write_enabled: bool = False
    router_canon_read_enabled: bool = False
    route_override_button_enabled: bool = False
    use_ml_route_button_enabled: bool = False
    best_route_claim_enabled: bool = False
    prompt_ranking_enabled: bool = False
    advisory_ranking_enabled: bool = False
    free_text_route_advice_enabled: bool = False
    free_text_explanations_enabled: bool = False
    runtime_pilot_behavior_enabled: bool = False
    runtime_copilot_decision_behavior_enabled: bool = False
    critical_boundary_error_budget: int = 0

    def __post_init__(self) -> None:
        """Validate the in-memory host-binding descriptor."""
        validate_descriptor(
            self,
            feature_id=FEATURE_ID,
            state_type=ReadOnlyPanelHostBindingImplementationState,
            ready_state=(
                ReadOnlyPanelHostBindingImplementationState
                .READ_ONLY_HOST_BINDING_DESCRIPTOR_READY
            ),
            host_section_type=ReadOnlyAdvisoryPanelHostBoundSection,
        )


def build_read_only_advisory_panel_host_binding_descriptor(
    policy: ReadOnlyAdvisoryPanelHostBindingImplementationPolicy,
    renderer_mount_descriptor: object | None,
) -> ReadOnlyAdvisoryPanelHostBindingDescriptor:
    """Build the Phase 11 read-only host-binding descriptor.

    The successful path requires an explicitly enabled feature flag and a safe
    Phase 10 renderer/mount descriptor. Missing or unsafe input fails open
    without UI mutation, telemetry surface wiring, route influence, provider
    calls, persistence, host event subscriptions, callback registration, or
    route authority.
    """

    if not isinstance(policy, ReadOnlyAdvisoryPanelHostBindingImplementationPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelHostBindingImplementationPolicy")

    if not policy.enabled or not policy.feature_flag_enabled:
        return _build_descriptor(
            policy=policy,
            renderer_mount_descriptor=None,
            state=ReadOnlyPanelHostBindingImplementationState.DISABLED_NOOP,
            host_sections=(),
            failure_codes=("feature_flag_default_off",),
            ready=False,
        )

    if not isinstance(renderer_mount_descriptor, ReadOnlyAdvisoryPanelRendererMountDescriptor):
        return _build_descriptor(
            policy=policy,
            renderer_mount_descriptor=None,
            state=ReadOnlyPanelHostBindingImplementationState.FAIL_OPEN_NO_DESCRIPTOR,
            host_sections=(),
            failure_codes=("missing_or_invalid_renderer_mount_descriptor",),
            ready=False,
        )

    if not _renderer_mount_descriptor_is_safe(renderer_mount_descriptor):
        return _build_descriptor(
            policy=policy,
            renderer_mount_descriptor=renderer_mount_descriptor,
            state=ReadOnlyPanelHostBindingImplementationState.BLOCKED_UNSAFE_DESCRIPTOR,
            host_sections=(),
            failure_codes=("unsafe_renderer_mount_descriptor_rejected",),
            ready=False,
        )

    host_sections = _bind_sections(renderer_mount_descriptor, policy.max_host_sections)
    return _build_descriptor(
        policy=policy,
        renderer_mount_descriptor=renderer_mount_descriptor,
        state=ReadOnlyPanelHostBindingImplementationState.READ_ONLY_HOST_BINDING_DESCRIPTOR_READY,
        host_sections=host_sections,
        failure_codes=(),
        ready=True,
    )


def build_phase11_read_only_panel_host_binding_implementation_probe() -> ReadOnlyAdvisoryPanelHostBindingDescriptor:
    """Build a safe feature-flag-enabled host-binding descriptor probe."""

    policy = ReadOnlyAdvisoryPanelHostBindingImplementationPolicy(
        host_container_id="phase11_read_only_panel_host_binding_descriptor",
        host_container_label="Phase 11 Read-Only Advisory Panel Host Binding",
        feature_flag_enabled=True,
    )
    descriptor = build_phase10_read_only_panel_renderer_mount_implementation_probe()
    return build_read_only_advisory_panel_host_binding_descriptor(policy, descriptor)


def _build_descriptor(
    *,
    policy: ReadOnlyAdvisoryPanelHostBindingImplementationPolicy,
    renderer_mount_descriptor: Optional[ReadOnlyAdvisoryPanelRendererMountDescriptor],
    state: ReadOnlyPanelHostBindingImplementationState,
    host_sections: Tuple[ReadOnlyAdvisoryPanelHostBoundSection, ...],
    failure_codes: Tuple[str, ...],
    ready: bool,
) -> ReadOnlyAdvisoryPanelHostBindingDescriptor:
    """Support build descriptor behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelHostBindingImplementationPolicy
        The policy value.
    renderer_mount_descriptor : Optional[ReadOnlyAdvisoryPanelRendererMountDescriptor]
        The renderer mount descriptor value.
    state : ReadOnlyPanelHostBindingImplementationState
        The state value.
    host_sections : Tuple[ReadOnlyAdvisoryPanelHostBoundSection, ...]
        The host sections value.
    failure_codes : Tuple[str, ...]
        The failure codes value.
    ready : bool
        The ready value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelHostBindingDescriptor
        The read only advisory panel host binding descriptor result.
    """
    
    return ReadOnlyAdvisoryPanelHostBindingDescriptor(
        feature_id=FEATURE_ID,
        host_container_id=policy.host_container_id,
        host_container_label=policy.host_container_label,
        state=state,
        feature_flag_name=policy.feature_flag_name,
        feature_flag_enabled=policy.feature_flag_enabled,
        source_mount_surface_id=renderer_mount_descriptor.mount_surface_id if renderer_mount_descriptor else None,
        source_mount_surface_label=renderer_mount_descriptor.mount_surface_label if renderer_mount_descriptor else None,
        source_panel_id=renderer_mount_descriptor.source_panel_id if renderer_mount_descriptor else None,
        source_panel_label=renderer_mount_descriptor.source_panel_label if renderer_mount_descriptor else None,
        canonical_result_id=renderer_mount_descriptor.canonical_result_id if renderer_mount_descriptor else None,
        canonical_dispatch_label=renderer_mount_descriptor.canonical_dispatch_label if renderer_mount_descriptor else None,
        final_selection_hash=renderer_mount_descriptor.final_selection_hash if renderer_mount_descriptor else None,
        host_bound_sections=host_sections,
        failure_state_codes=failure_codes,
        non_training_feedback_slot_enabled=(
            bool(renderer_mount_descriptor.non_training_feedback_slot_enabled)
            if renderer_mount_descriptor is not None else False
        ),
        read_only_host_binding_descriptor_ready=ready,
        runtime_app_host_visibility_descriptor_ready=ready,
        mounted_runtime_panel_descriptor_ready=ready,
    )


def _renderer_mount_descriptor_is_safe(descriptor: ReadOnlyAdvisoryPanelRendererMountDescriptor) -> bool:
    """Support renderer mount descriptor is safe behavior.
    
    Parameters
    ----------
    descriptor : ReadOnlyAdvisoryPanelRendererMountDescriptor
        The descriptor value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        descriptor.state is ReadOnlyPanelRendererMountImplementationState.READ_ONLY_MOUNT_DESCRIPTOR_READY
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
        and descriptor.consumes_phase9_activation_envelope_only is True
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


def _bind_sections(
    descriptor: ReadOnlyAdvisoryPanelRendererMountDescriptor,
    limit: int,
) -> Tuple[ReadOnlyAdvisoryPanelHostBoundSection, ...]:
    """Support bind sections behavior.
    
    Parameters
    ----------
    descriptor : ReadOnlyAdvisoryPanelRendererMountDescriptor
        The descriptor value.
    limit : int
        The limit value.
    
    Returns
    -------
    Tuple[ReadOnlyAdvisoryPanelHostBoundSection, ...]
        The tuple result.
    """
    
    bound = []
    for section in descriptor.rendered_sections[:limit]:
        bound.append(_bind_section(section))
    return tuple(bound)


def _bind_section(section: ReadOnlyAdvisoryPanelRenderedSection) -> ReadOnlyAdvisoryPanelHostBoundSection:
    """Support bind section behavior.
    
    Parameters
    ----------
    section : ReadOnlyAdvisoryPanelRenderedSection
        The section value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelHostBoundSection
        The read only advisory panel host bound section result.
    """
    
    return ReadOnlyAdvisoryPanelHostBoundSection(
        section_key=section.section_key,
        label=section.label,
        value=section.value,
        severity=section.severity,
    )
