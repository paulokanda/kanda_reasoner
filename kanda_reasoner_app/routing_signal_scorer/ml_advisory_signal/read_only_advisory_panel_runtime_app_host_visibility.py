# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_runtime_app_host_visibility.py
"""Phase 12 read-only advisory panel runtime app-host visibility implementation.

This module implements a minimal in-memory runtime app-host visibility
_descriptor_ for the read-only advisory panel line. It consumes only the
Phase 11 host-binding descriptor lineage and produces bounded display metadata
for a future app host.

It does not mutate runtime UI, wire telemetry surfaces, subscribe to host
events, register host callbacks, call the router, call an advisor, execute
adapters, call providers, persist data, read prompt libraries, read freeze
memory, read router canon, influence routes, grant ML route authority, or create
runtime Copilot decision behavior.
"""

from __future__ import annotations


__all__ = [
    'build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe',
    'build_read_only_advisory_panel_runtime_app_host_visibility_descriptor',
    'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor',
    'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy',
    'ReadOnlyAdvisoryPanelRuntimeVisibleSection',
    'ReadOnlyPanelRuntimeAppHostVisibilityImplementationState',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from .read_only_advisory_panel_host_binding import (
    ReadOnlyAdvisoryPanelHostBindingDescriptor,
    ReadOnlyAdvisoryPanelHostBoundSection,
    ReadOnlyPanelHostBindingImplementationState,
    build_phase11_read_only_panel_host_binding_implementation_probe,
)
from ._read_only_advisory_panel_runtime_app_host_visibility_invariants import (
    _require_tuple_of_visible_sections as _require_tuple_of_visible_sections_impl,
    validate_descriptor,
    validate_policy,
    validate_visible_section,
)


FEATURE_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1"
SOURCE_REVIEW_FEATURE_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract_result_review_gate_v1"
SOURCE_CONTRACT_FEATURE_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract_v1"
SOURCE_HOST_BINDING_IMPLEMENTATION_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_implementation_v1"


class ReadOnlyPanelRuntimeAppHostVisibilityImplementationState(str, Enum):
    """Safe states for the read-only runtime app-host visibility descriptor builder."""

    DISABLED_NOOP = "disabled_noop"
    FAIL_OPEN_NO_DESCRIPTOR = "fail_open_no_descriptor"
    BLOCKED_UNSAFE_DESCRIPTOR = "blocked_unsafe_descriptor"
    READ_ONLY_VISIBILITY_DESCRIPTOR_READY = "read_only_visibility_descriptor_ready"


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy:
    """Policy for building a read-only runtime app-host visibility descriptor.

    The feature flag is default-off. When explicitly enabled, this policy may
    build only an in-memory visibility descriptor from the Phase 11 host-binding
    descriptor. It must not mutate runtime UI, wire telemetry surfaces, subscribe
    to host events, register callbacks, or influence routing.
    """

    visibility_surface_id: str
    visibility_surface_label: str
    source_review_feature_id: str = SOURCE_REVIEW_FEATURE_ID
    source_contract_feature_id: str = SOURCE_CONTRACT_FEATURE_ID
    source_host_binding_implementation_id: str = SOURCE_HOST_BINDING_IMPLEMENTATION_ID
    enabled: bool = True
    feature_flag_name: str = "ml_advisory_read_only_panel_runtime_app_host_visibility"
    feature_flag_enabled: bool = False
    feature_flag_default_enabled: bool = False
    max_visible_sections: int = 11
    require_phase11_host_binding_descriptor_input: bool = True
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_descriptor: bool = True
    require_block_unsafe_descriptor: bool = True
    require_bounded_visible_sections: bool = True
    require_removable_noop_visibility: bool = True
    require_route_invariant_visibility: bool = True
    require_final_selection_invisible_visibility: bool = True
    require_non_training_feedback_slot: bool = True
    allow_read_only_runtime_app_host_visibility_descriptor: bool = True
    allow_actual_runtime_app_host_visibility: bool = False
    allow_visibility_activation: bool = False
    allow_mounted_runtime_panel: bool = False
    allow_runtime_panel_mount_side_effects: bool = False
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
    allow_autonomous_ml_router: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        validate_policy(
            self,
            source_review_feature_id=SOURCE_REVIEW_FEATURE_ID,
            source_contract_feature_id=SOURCE_CONTRACT_FEATURE_ID,
            source_host_binding_implementation_id=SOURCE_HOST_BINDING_IMPLEMENTATION_ID,
        )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeVisibleSection:
    """Bounded runtime-visible section copied from the Phase 11 host descriptor."""

    section_key: str
    label: str
    value: str
    severity: str
    host_role: str = "read_only_advisory_observation"
    read_only: bool = True
    display_only: bool = True
    action_enabled: bool = False
    route_authority_enabled: bool = False
    route_influence_enabled: bool = False
    host_callback_enabled: bool = False
    free_text_route_advice_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        validate_visible_section(self)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor:
    """In-memory read-only runtime app-host visibility descriptor.

    This is the Phase 12 implementation output. It is bounded display metadata
    only, not a UI mutation, mounted runtime panel, host event subscription,
    host callback registration, router hook, or route authority surface.
    """

    feature_id: str
    visibility_surface_id: str
    visibility_surface_label: str
    state: ReadOnlyPanelRuntimeAppHostVisibilityImplementationState
    feature_flag_name: str
    feature_flag_enabled: bool
    source_host_container_id: Optional[str]
    source_host_container_label: Optional[str]
    source_mount_surface_id: Optional[str]
    source_mount_surface_label: Optional[str]
    source_panel_id: Optional[str]
    source_panel_label: Optional[str]
    canonical_result_id: Optional[str]
    canonical_dispatch_label: Optional[str]
    final_selection_hash: Optional[str]
    visible_sections: Tuple[ReadOnlyAdvisoryPanelRuntimeVisibleSection, ...]
    failure_state_codes: Tuple[str, ...]
    non_training_feedback_slot_enabled: bool
    read_only_runtime_app_host_visibility_descriptor_ready: bool
    visible_read_only_panel_descriptor_ready: bool
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
    consumes_phase11_host_binding_descriptor_only: bool = True
    actual_runtime_app_host_visibility_enabled: bool = False
    visibility_activation_enabled: bool = False
    mounted_runtime_panel_enabled: bool = False
    runtime_panel_mount_side_effects_enabled: bool = False
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
    autonomous_ml_router_enabled: bool = False
    critical_boundary_error_budget: int = 0

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        validate_descriptor(
            self,
            feature_id=FEATURE_ID,
            state_type=ReadOnlyPanelRuntimeAppHostVisibilityImplementationState,
            ready_state=(
                ReadOnlyPanelRuntimeAppHostVisibilityImplementationState
                .READ_ONLY_VISIBILITY_DESCRIPTOR_READY
            ),
            visible_section_type=ReadOnlyAdvisoryPanelRuntimeVisibleSection,
        )


def build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(
    policy: ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy,
    host_binding_descriptor: object | None,
) -> ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor:
    """Build the Phase 12 read-only runtime app-host visibility descriptor.

    The successful path requires an explicitly enabled feature flag and a safe
    Phase 11 host-binding descriptor. Missing or unsafe input fails open without
    UI mutation, telemetry surface wiring, route influence, provider calls,
    persistence, host event subscriptions, callback registration, or route
    authority.
    """

    if not isinstance(policy, ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy")

    if not policy.enabled or not policy.feature_flag_enabled:
        return _build_descriptor(
            policy=policy,
            host_binding_descriptor=None,
            state=ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.DISABLED_NOOP,
            visible_sections=(),
            failure_codes=("feature_flag_default_off",),
            ready=False,
        )

    if not isinstance(host_binding_descriptor, ReadOnlyAdvisoryPanelHostBindingDescriptor):
        return _build_descriptor(
            policy=policy,
            host_binding_descriptor=None,
            state=ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.FAIL_OPEN_NO_DESCRIPTOR,
            visible_sections=(),
            failure_codes=("missing_or_invalid_host_binding_descriptor",),
            ready=False,
        )

    if not _host_binding_descriptor_is_safe(host_binding_descriptor):
        return _build_descriptor(
            policy=policy,
            host_binding_descriptor=host_binding_descriptor,
            state=ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.BLOCKED_UNSAFE_DESCRIPTOR,
            visible_sections=(),
            failure_codes=("unsafe_host_binding_descriptor_rejected",),
            ready=False,
        )

    visible_sections = _make_visible_sections(host_binding_descriptor, policy.max_visible_sections)
    return _build_descriptor(
        policy=policy,
        host_binding_descriptor=host_binding_descriptor,
        state=ReadOnlyPanelRuntimeAppHostVisibilityImplementationState.READ_ONLY_VISIBILITY_DESCRIPTOR_READY,
        visible_sections=visible_sections,
        failure_codes=(),
        ready=True,
    )


def build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe(
) -> ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor:
    """Build a safe feature-flag-enabled runtime app-host visibility descriptor probe."""

    policy = ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy(
        visibility_surface_id="phase12_read_only_panel_runtime_app_host_visibility_descriptor",
        visibility_surface_label="Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility",
        feature_flag_enabled=True,
    )
    descriptor = build_phase11_read_only_panel_host_binding_implementation_probe()
    return build_read_only_advisory_panel_runtime_app_host_visibility_descriptor(policy, descriptor)


def _build_descriptor(
    *,
    policy: ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy,
    host_binding_descriptor: Optional[ReadOnlyAdvisoryPanelHostBindingDescriptor],
    state: ReadOnlyPanelRuntimeAppHostVisibilityImplementationState,
    visible_sections: Tuple[ReadOnlyAdvisoryPanelRuntimeVisibleSection, ...],
    failure_codes: Tuple[str, ...],
    ready: bool,
) -> ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor:
    """Support build descriptor behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy
        The policy value.
    host_binding_descriptor : Optional[ReadOnlyAdvisoryPanelHostBindingDescriptor]
        The host binding descriptor value.
    state : ReadOnlyPanelRuntimeAppHostVisibilityImplementationState
        The state value.
    visible_sections : Tuple[ReadOnlyAdvisoryPanelRuntimeVisibleSection, ...]
        The visible sections value.
    failure_codes : Tuple[str, ...]
        The failure codes value.
    ready : bool
        The ready value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor
        The read only advisory panel runtime app host visibility descriptor result.
    """
    
    return ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor(
        feature_id=FEATURE_ID,
        visibility_surface_id=policy.visibility_surface_id,
        visibility_surface_label=policy.visibility_surface_label,
        state=state,
        feature_flag_name=policy.feature_flag_name,
        feature_flag_enabled=policy.feature_flag_enabled,
        source_host_container_id=host_binding_descriptor.host_container_id if host_binding_descriptor else None,
        source_host_container_label=host_binding_descriptor.host_container_label if host_binding_descriptor else None,
        source_mount_surface_id=host_binding_descriptor.source_mount_surface_id if host_binding_descriptor else None,
        source_mount_surface_label=host_binding_descriptor.source_mount_surface_label if host_binding_descriptor else None,
        source_panel_id=host_binding_descriptor.source_panel_id if host_binding_descriptor else None,
        source_panel_label=host_binding_descriptor.source_panel_label if host_binding_descriptor else None,
        canonical_result_id=host_binding_descriptor.canonical_result_id if host_binding_descriptor else None,
        canonical_dispatch_label=host_binding_descriptor.canonical_dispatch_label if host_binding_descriptor else None,
        final_selection_hash=host_binding_descriptor.final_selection_hash if host_binding_descriptor else None,
        visible_sections=visible_sections,
        failure_state_codes=failure_codes,
        non_training_feedback_slot_enabled=(
            bool(host_binding_descriptor.non_training_feedback_slot_enabled)
            if host_binding_descriptor is not None else False
        ),
        read_only_runtime_app_host_visibility_descriptor_ready=ready,
        visible_read_only_panel_descriptor_ready=ready,
        mounted_runtime_panel_descriptor_ready=ready,
    )


def _host_binding_descriptor_is_safe(descriptor: ReadOnlyAdvisoryPanelHostBindingDescriptor) -> bool:
    """Support host binding descriptor is safe behavior.
    
    Parameters
    ----------
    descriptor : ReadOnlyAdvisoryPanelHostBindingDescriptor
        The descriptor value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        descriptor.state is ReadOnlyPanelHostBindingImplementationState.READ_ONLY_HOST_BINDING_DESCRIPTOR_READY
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


def _make_visible_sections(
    descriptor: ReadOnlyAdvisoryPanelHostBindingDescriptor,
    limit: int,
) -> Tuple[ReadOnlyAdvisoryPanelRuntimeVisibleSection, ...]:
    """Support make visible sections behavior.
    
    Parameters
    ----------
    descriptor : ReadOnlyAdvisoryPanelHostBindingDescriptor
        The descriptor value.
    limit : int
        The limit value.
    
    Returns
    -------
    Tuple[ReadOnlyAdvisoryPanelRuntimeVisibleSection, ...]
        The tuple result.
    """
    
    visible = []
    for section in descriptor.host_bound_sections[:limit]:
        visible.append(_make_visible_section(section))
    return tuple(visible)


def _make_visible_section(
    section: ReadOnlyAdvisoryPanelHostBoundSection,
) -> ReadOnlyAdvisoryPanelRuntimeVisibleSection:
    """Support make visible section behavior.
    
    Parameters
    ----------
    section : ReadOnlyAdvisoryPanelHostBoundSection
        The section value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelRuntimeVisibleSection
        The read only advisory panel runtime visible section result.
    """
    
    return ReadOnlyAdvisoryPanelRuntimeVisibleSection(
        section_key=section.section_key,
        label=section.label,
        value=section.value,
        severity=section.severity,
        host_role=section.host_role,
    )



def _require_tuple_of_visible_sections(
    name: str,
    value: Tuple[ReadOnlyAdvisoryPanelRuntimeVisibleSection, ...],
) -> None:
    """Preserve the legacy private tuple-validation helper signature."""
    _require_tuple_of_visible_sections_impl(
        name,
        value,
        ReadOnlyAdvisoryPanelRuntimeVisibleSection,
    )
