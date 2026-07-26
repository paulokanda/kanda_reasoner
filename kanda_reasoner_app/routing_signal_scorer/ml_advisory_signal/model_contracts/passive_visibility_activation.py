# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/model_contracts/passive_visibility_activation.py
"""Stable public models for read-only advisory panel passive visibility activation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from .._passive_visibility_activation_invariants import (
    _descriptor_forbidden_true_fields,
    _descriptor_required_true_fields,
    _policy_required_false_fields,
    _policy_required_true_fields,
    _require_text,
    _require_tuple_of_text,
)

FEATURE_ID = "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_v1"
SOURCE_REVIEW_FEATURE_ID = "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_contract_result_review_gate_v1"
SOURCE_CONTRACT_FEATURE_ID = "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_contract_v1"
SOURCE_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1"

__all__ = [
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor",
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy",
    "ReadOnlyAdvisoryPanelPassiveVisibilitySlot",
    "ReadOnlyPanelPassiveVisibilityActivationImplementationState",
]


class ReadOnlyPanelPassiveVisibilityActivationImplementationState(str, Enum):
    """Safe states for the passive visibility activation descriptor builder."""

    DISABLED_NOOP = "disabled_noop"
    FAIL_OPEN_NO_DESCRIPTOR = "fail_open_no_descriptor"
    BLOCKED_UNSAFE_DESCRIPTOR = "blocked_unsafe_descriptor"
    READ_ONLY_PASSIVE_VISIBILITY_ACTIVATION_DESCRIPTOR_READY = (
        "read_only_passive_visibility_activation_descriptor_ready"
    )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy:
    """Policy for building a read-only passive visibility activation descriptor.

    The feature flag is default-off. When explicitly enabled, this policy may
    build only in-memory passive visibility slot metadata from the Phase 12
    runtime app-host visibility descriptor. It must not activate UI, register
    slots in a host, wire telemetry surfaces, subscribe to events, register
    callbacks, or influence routing.
    """

    passive_visibility_surface_id: str
    passive_visibility_surface_label: str
    source_review_feature_id: str = SOURCE_REVIEW_FEATURE_ID
    source_contract_feature_id: str = SOURCE_CONTRACT_FEATURE_ID
    source_runtime_app_host_visibility_implementation_id: str = SOURCE_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_ID
    enabled: bool = True
    feature_flag_name: str = "ml_advisory_read_only_panel_passive_visibility_activation"
    feature_flag_enabled: bool = False
    feature_flag_default_enabled: bool = False
    max_passive_visibility_slots: int = 11
    require_phase12_runtime_app_host_visibility_descriptor_input: bool = True
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_descriptor: bool = True
    require_block_unsafe_descriptor: bool = True
    require_bounded_passive_visibility_slots: bool = True
    require_read_only_passive_visibility_slot: bool = True
    require_removable_noop_activation: bool = True
    require_route_invariant_activation: bool = True
    require_final_selection_invisible_activation: bool = True
    require_non_training_feedback_slot: bool = True
    allow_read_only_passive_visibility_activation_descriptor: bool = True
    allow_actual_passive_visibility_activation: bool = False
    allow_passive_visibility_slot_registration: bool = False
    allow_passive_visibility_slot_mutation: bool = False
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

        _require_text("passive_visibility_surface_id", self.passive_visibility_surface_id)
        _require_text("passive_visibility_surface_label", self.passive_visibility_surface_label)
        _require_text("feature_flag_name", self.feature_flag_name)
        if self.source_review_feature_id != SOURCE_REVIEW_FEATURE_ID:
            raise ValueError("source_review_feature_id must match Phase 13 contract review gate")
        if self.source_contract_feature_id != SOURCE_CONTRACT_FEATURE_ID:
            raise ValueError("source_contract_feature_id must match Phase 13 contract")
        if self.source_runtime_app_host_visibility_implementation_id != SOURCE_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_ID:
            raise ValueError("source_runtime_app_host_visibility_implementation_id must match Phase 12 implementation")
        if not isinstance(self.max_passive_visibility_slots, int) or self.max_passive_visibility_slots <= 0:
            raise ValueError("max_passive_visibility_slots must be a positive integer")
        for field_name in _policy_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _policy_required_false_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelPassiveVisibilitySlot:
    """Bounded passive visibility slot copied from a Phase 12 visible section."""

    slot_key: str
    label: str
    value: str
    severity: str
    host_role: str = "read_only_advisory_observation"
    read_only: bool = True
    display_only: bool = True
    passive: bool = True
    action_enabled: bool = False
    slot_registered_in_host: bool = False
    slot_mutation_enabled: bool = False
    route_authority_enabled: bool = False
    route_influence_enabled: bool = False
    host_callback_enabled: bool = False
    telemetry_surface_wiring_enabled: bool = False
    free_text_route_advice_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """

        _require_text("slot_key", self.slot_key)
        _require_text("label", self.label)
        _require_text("value", self.value)
        _require_text("severity", self.severity)
        _require_text("host_role", self.host_role)
        if len(self.slot_key) > 90:
            raise ValueError("slot_key must remain bounded")
        if len(self.label) > 96:
            raise ValueError("label must remain bounded")
        if len(self.value) > 240:
            raise ValueError("value must remain bounded")
        if len(self.host_role) > 80:
            raise ValueError("host_role must remain bounded")
        if self.read_only is not True:
            raise ValueError("passive visibility slot must remain read-only")
        if self.display_only is not True:
            raise ValueError("passive visibility slot must remain display-only")
        if self.passive is not True:
            raise ValueError("passive visibility slot must remain passive")
        for field_name in (
            "action_enabled",
            "slot_registered_in_host",
            "slot_mutation_enabled",
            "route_authority_enabled",
            "route_influence_enabled",
            "host_callback_enabled",
            "telemetry_surface_wiring_enabled",
            "free_text_route_advice_enabled",
        ):
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " is forbidden for passive visibility slots")


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor:
    """In-memory read-only passive visibility activation descriptor.

    This is the Phase 13 implementation output. It is bounded passive slot
    metadata only, not passive slot registration, host UI mutation, telemetry
    surface wiring, runtime panel mounting, host callback registration, router
    hook, or route authority surface.
    """

    feature_id: str
    passive_visibility_surface_id: str
    passive_visibility_surface_label: str
    state: ReadOnlyPanelPassiveVisibilityActivationImplementationState
    feature_flag_name: str
    feature_flag_enabled: bool
    source_visibility_surface_id: Optional[str]
    source_visibility_surface_label: Optional[str]
    source_host_container_id: Optional[str]
    source_host_container_label: Optional[str]
    source_mount_surface_id: Optional[str]
    source_mount_surface_label: Optional[str]
    source_panel_id: Optional[str]
    source_panel_label: Optional[str]
    canonical_result_id: Optional[str]
    canonical_dispatch_label: Optional[str]
    final_selection_hash: Optional[str]
    passive_visibility_slots: Tuple[ReadOnlyAdvisoryPanelPassiveVisibilitySlot, ...]
    failure_state_codes: Tuple[str, ...]
    non_training_feedback_slot_enabled: bool
    read_only_passive_visibility_activation_descriptor_ready: bool
    passive_visibility_slot_descriptor_ready: bool
    runtime_app_host_visibility_descriptor_consumed: bool
    read_only: bool = True
    telemetry_only: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    consumes_phase12_runtime_app_host_visibility_descriptor_only: bool = True
    actual_passive_visibility_activation_enabled: bool = False
    passive_visibility_slot_registration_enabled: bool = False
    passive_visibility_slot_mutation_enabled: bool = False
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
    visible_ml_integration_complete: bool = False
    critical_boundary_error_budget: int = 0

    def __post_init__(self) -> None:
        """Support post init behavior.
        """

        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 13 passive visibility activation implementation")
        _require_text("passive_visibility_surface_id", self.passive_visibility_surface_id)
        _require_text("passive_visibility_surface_label", self.passive_visibility_surface_label)
        _require_text("feature_flag_name", self.feature_flag_name)
        if not isinstance(self.state, ReadOnlyPanelPassiveVisibilityActivationImplementationState):
            raise TypeError("state must be ReadOnlyPanelPassiveVisibilityActivationImplementationState")
        for optional_text in (
            "source_visibility_surface_id",
            "source_visibility_surface_label",
            "source_host_container_id",
            "source_host_container_label",
            "source_mount_surface_id",
            "source_mount_surface_label",
            "source_panel_id",
            "source_panel_label",
            "canonical_result_id",
            "canonical_dispatch_label",
            "final_selection_hash",
        ):
            value = getattr(self, optional_text)
            if value is not None:
                _require_text(optional_text, value)
        _require_tuple_of_passive_visibility_slots("passive_visibility_slots", self.passive_visibility_slots)
        _require_tuple_of_text("failure_state_codes", self.failure_state_codes)
        for field_name in _descriptor_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _descriptor_forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")
        if self.critical_boundary_error_budget != 0:
            raise ValueError("critical_boundary_error_budget must remain zero")
        if self.read_only_passive_visibility_activation_descriptor_ready is True:
            if self.state is not ReadOnlyPanelPassiveVisibilityActivationImplementationState.READ_ONLY_PASSIVE_VISIBILITY_ACTIVATION_DESCRIPTOR_READY:
                raise ValueError("ready descriptor must use READ_ONLY_PASSIVE_VISIBILITY_ACTIVATION_DESCRIPTOR_READY state")
            if self.passive_visibility_slot_descriptor_ready is not True:
                raise ValueError("ready descriptor must mark passive slot descriptor readiness")
            if self.runtime_app_host_visibility_descriptor_consumed is not True:
                raise ValueError("ready descriptor must consume runtime app-host visibility descriptor")
            if not self.passive_visibility_slots:
                raise ValueError("ready descriptor requires passive visibility slots")
        else:
            if self.state is ReadOnlyPanelPassiveVisibilityActivationImplementationState.READ_ONLY_PASSIVE_VISIBILITY_ACTIVATION_DESCRIPTOR_READY:
                raise ValueError("READY state requires read_only_passive_visibility_activation_descriptor_ready=True")
            if self.passive_visibility_slot_descriptor_ready is not False:
                raise ValueError("non-ready descriptor must not mark passive slot descriptor readiness")
            if self.runtime_app_host_visibility_descriptor_consumed is not False:
                raise ValueError("non-ready descriptor must not mark runtime descriptor consumed")


def _require_tuple_of_passive_visibility_slots(
    name: str,
    value: Tuple[ReadOnlyAdvisoryPanelPassiveVisibilitySlot, ...],
) -> None:
    """Support require tuple of passive visibility slots behavior.

    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[ReadOnlyAdvisoryPanelPassiveVisibilitySlot, ...]
        The input value.
    """

    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    for item in value:
        if not isinstance(item, ReadOnlyAdvisoryPanelPassiveVisibilitySlot):
            raise TypeError(name + " items must be ReadOnlyAdvisoryPanelPassiveVisibilitySlot")
