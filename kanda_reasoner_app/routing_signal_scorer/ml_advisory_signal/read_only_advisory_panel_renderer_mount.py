# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_renderer_mount.py
"""Phase 10 read-only advisory panel renderer/mount implementation.

This module implements a minimal in-memory renderer/mount descriptor for a
future read-only advisory panel. It consumes only the Phase 9 runtime activation
envelope lineage and converts already-approved Phase 8 panel sections into a
bounded local display descriptor.

It does not mutate UI, wire telemetry surfaces, call the router, call an
advisor, execute adapters, call providers, persist data, read prompt libraries,
read freeze memory, read router canon, influence routes, or grant ML route
authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase10_read_only_panel_renderer_mount_implementation_probe',
    'build_read_only_advisory_panel_renderer_mount_descriptor',
    'ReadOnlyAdvisoryPanelRenderedSection',
    'ReadOnlyAdvisoryPanelRendererMountDescriptor',
    'ReadOnlyPanelRendererMountImplementationState',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from .read_only_advisory_panel_runtime_activation import (
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelope,
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
)
from ._read_only_advisory_panel_renderer_mount_support import (
    _activation_envelope_is_safe,
    _build_renderer_mount_descriptor,
    _descriptor_forbidden_true_fields,
    _descriptor_required_true_fields,
    _policy_required_false_fields,
    _policy_required_true_fields,
    _render_sections,
    _require_text,
    _require_tuple_of_rendered_sections,
    _require_tuple_of_text,
)


FEATURE_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1"
SOURCE_REVIEW_FEATURE_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_result_review_gate_v1"


class ReadOnlyPanelRendererMountImplementationState(str, Enum):
    """Safe states for the local read-only renderer/mount descriptor."""

    DISABLED_NOOP = "disabled_noop"
    FAIL_OPEN_NO_ENVELOPE = "fail_open_no_envelope"
    BLOCKED_UNSAFE_ENVELOPE = "blocked_unsafe_envelope"
    READ_ONLY_MOUNT_DESCRIPTOR_READY = "read_only_mount_descriptor_ready"


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRendererMountPolicy:
    """Policy for building a local read-only renderer/mount descriptor.

    The feature flag is default-off. When explicitly enabled, this policy may
    build only an in-memory local display descriptor from the Phase 9 activation
    envelope. It must not mutate runtime UI or influence routing.
    """

    mount_surface_id: str
    mount_surface_label: str
    source_review_feature_id: str = SOURCE_REVIEW_FEATURE_ID
    enabled: bool = True
    feature_flag_name: str = "ml_advisory_read_only_panel_renderer_mount"
    feature_flag_enabled: bool = False
    feature_flag_default_enabled: bool = False
    max_rendered_sections: int = 11
    require_phase9_activation_envelope_input: bool = True
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_envelope: bool = True
    require_block_unsafe_envelope: bool = True
    require_bounded_rendered_sections: bool = True
    require_removable_noop_mount: bool = True
    require_route_invariant_mount: bool = True
    require_final_selection_invisible_mount: bool = True
    require_non_training_feedback_slot: bool = True
    allow_read_only_mount_descriptor: bool = True
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
        """Support post init behavior.
        """
        
        _require_text("mount_surface_id", self.mount_surface_id)
        _require_text("mount_surface_label", self.mount_surface_label)
        _require_text("feature_flag_name", self.feature_flag_name)
        if self.source_review_feature_id != SOURCE_REVIEW_FEATURE_ID:
            raise ValueError("source_review_feature_id must match Phase 10 contract result review gate")
        if not isinstance(self.max_rendered_sections, int) or self.max_rendered_sections <= 0:
            raise ValueError("max_rendered_sections must be a positive integer")
        for field_name in _policy_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _policy_required_false_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRenderedSection:
    """Bounded local display section copied from the Phase 8 view model."""

    section_key: str
    label: str
    value: str
    severity: str
    read_only: bool = True
    action_enabled: bool = False
    route_authority_enabled: bool = False
    route_influence_enabled: bool = False
    free_text_route_advice_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("section_key", self.section_key)
        _require_text("label", self.label)
        _require_text("value", self.value)
        _require_text("severity", self.severity)
        if len(self.section_key) > 80:
            raise ValueError("section_key must remain bounded")
        if len(self.label) > 96:
            raise ValueError("label must remain bounded")
        if len(self.value) > 240:
            raise ValueError("value must remain bounded")
        if self.read_only is not True:
            raise ValueError("rendered section must remain read-only")
        if self.action_enabled is not False:
            raise ValueError("rendered section actions are forbidden")
        if self.route_authority_enabled is not False:
            raise ValueError("rendered section route authority is forbidden")
        if self.route_influence_enabled is not False:
            raise ValueError("rendered section route influence is forbidden")
        if self.free_text_route_advice_enabled is not False:
            raise ValueError("rendered section free-text route advice is forbidden")


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRendererMountDescriptor:
    """In-memory local read-only renderer/mount descriptor.

    This is the Phase 10 implementation output. It is a bounded descriptor for a
    local read-only panel surface, not a router hook and not a mutable UI action.
    """

    feature_id: str
    mount_surface_id: str
    mount_surface_label: str
    state: ReadOnlyPanelRendererMountImplementationState
    feature_flag_name: str
    feature_flag_enabled: bool
    source_activation_surface_id: Optional[str]
    source_activation_surface_label: Optional[str]
    source_panel_id: Optional[str]
    source_panel_label: Optional[str]
    canonical_result_id: Optional[str]
    canonical_dispatch_label: Optional[str]
    final_selection_hash: Optional[str]
    rendered_sections: Tuple[ReadOnlyAdvisoryPanelRenderedSection, ...]
    failure_state_codes: Tuple[str, ...]
    non_training_feedback_slot_enabled: bool
    read_only_mount_descriptor_ready: bool
    visible_read_only_panel_ready: bool
    read_only: bool = True
    telemetry_only: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    consumes_phase9_activation_envelope_only: bool = True
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
        """Support post init behavior.
        """
        
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 10 renderer mount implementation")
        _require_text("mount_surface_id", self.mount_surface_id)
        _require_text("mount_surface_label", self.mount_surface_label)
        _require_text("feature_flag_name", self.feature_flag_name)
        if not isinstance(self.state, ReadOnlyPanelRendererMountImplementationState):
            raise TypeError("state must be ReadOnlyPanelRendererMountImplementationState")
        for optional_text in (
            "source_activation_surface_id",
            "source_activation_surface_label",
            "source_panel_id",
            "source_panel_label",
            "canonical_result_id",
            "canonical_dispatch_label",
            "final_selection_hash",
        ):
            value = getattr(self, optional_text)
            if value is not None:
                _require_text(optional_text, value)
        _require_tuple_of_rendered_sections("rendered_sections", self.rendered_sections, ReadOnlyAdvisoryPanelRenderedSection)
        _require_tuple_of_text("failure_state_codes", self.failure_state_codes)
        for field_name in _descriptor_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _descriptor_forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")
        if self.critical_boundary_error_budget != 0:
            raise ValueError("critical_boundary_error_budget must remain zero")
        if self.read_only_mount_descriptor_ready is True:
            if self.state is not ReadOnlyPanelRendererMountImplementationState.READ_ONLY_MOUNT_DESCRIPTOR_READY:
                raise ValueError("ready descriptor must use READ_ONLY_MOUNT_DESCRIPTOR_READY state")
            if self.visible_read_only_panel_ready is not True:
                raise ValueError("ready descriptor must set visible_read_only_panel_ready")
            if not self.rendered_sections:
                raise ValueError("ready descriptor requires rendered sections")
        else:
            if self.state is ReadOnlyPanelRendererMountImplementationState.READ_ONLY_MOUNT_DESCRIPTOR_READY:
                raise ValueError("READY state requires read_only_mount_descriptor_ready=True")
            if self.visible_read_only_panel_ready is not False:
                raise ValueError("non-ready descriptor must not be visible-ready")


def build_read_only_advisory_panel_renderer_mount_descriptor(
    policy: ReadOnlyAdvisoryPanelRendererMountPolicy,
    activation_envelope: object | None,
) -> ReadOnlyAdvisoryPanelRendererMountDescriptor:
    """Build the Phase 10 local read-only renderer/mount descriptor.

    The successful path requires an explicitly enabled feature flag and a safe
    Phase 9 activation envelope. Missing or unsafe input fails open without UI
    mutation, route influence, provider calls, persistence, or route authority.
    """

    if not isinstance(policy, ReadOnlyAdvisoryPanelRendererMountPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelRendererMountPolicy")

    if not policy.enabled or not policy.feature_flag_enabled:
        return _build_renderer_mount_descriptor(
            policy=policy,
            activation_envelope=None,
            descriptor_type=ReadOnlyAdvisoryPanelRendererMountDescriptor,
            feature_id=FEATURE_ID,
            state=ReadOnlyPanelRendererMountImplementationState.DISABLED_NOOP,
            rendered_sections=(),
            failure_codes=("feature_flag_default_off",),
            ready=False,
        )

    if not isinstance(activation_envelope, ReadOnlyAdvisoryPanelRuntimeActivationEnvelope):
        return _build_renderer_mount_descriptor(
            policy=policy,
            activation_envelope=None,
            descriptor_type=ReadOnlyAdvisoryPanelRendererMountDescriptor,
            feature_id=FEATURE_ID,
            state=ReadOnlyPanelRendererMountImplementationState.FAIL_OPEN_NO_ENVELOPE,
            rendered_sections=(),
            failure_codes=("missing_or_invalid_activation_envelope",),
            ready=False,
        )

    if not _activation_envelope_is_safe(activation_envelope):
        return _build_renderer_mount_descriptor(
            policy=policy,
            activation_envelope=activation_envelope,
            descriptor_type=ReadOnlyAdvisoryPanelRendererMountDescriptor,
            feature_id=FEATURE_ID,
            state=ReadOnlyPanelRendererMountImplementationState.BLOCKED_UNSAFE_ENVELOPE,
            rendered_sections=(),
            failure_codes=("unsafe_activation_envelope_rejected",),
            ready=False,
        )

    rendered_sections = _render_sections(
        activation_envelope, policy.max_rendered_sections, ReadOnlyAdvisoryPanelRenderedSection
    )
    return _build_renderer_mount_descriptor(
        policy=policy,
        activation_envelope=activation_envelope,
        descriptor_type=ReadOnlyAdvisoryPanelRendererMountDescriptor,
        feature_id=FEATURE_ID,
        state=ReadOnlyPanelRendererMountImplementationState.READ_ONLY_MOUNT_DESCRIPTOR_READY,
        rendered_sections=rendered_sections,
        failure_codes=(),
        ready=True,
    )


def build_phase10_read_only_panel_renderer_mount_implementation_probe() -> ReadOnlyAdvisoryPanelRendererMountDescriptor:
    """Build a safe feature-flag-enabled local mount descriptor probe."""

    policy = ReadOnlyAdvisoryPanelRendererMountPolicy(
        mount_surface_id="phase10_read_only_panel_renderer_mount_descriptor",
        mount_surface_label="Phase 10 Read-Only Advisory Panel Renderer Mount",
        feature_flag_enabled=True,
    )
    envelope = build_phase9_read_only_panel_runtime_activation_implementation_probe()
    return build_read_only_advisory_panel_renderer_mount_descriptor(policy, envelope)






















