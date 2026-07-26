# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_renderer_mount_contract.py
"""Phase 10 read-only advisory panel renderer mount contract.

Contract only. This module defines the narrow conditions for a future
read-only renderer/mount path that may consume the Phase 9 activation envelope.
It does not activate a renderer, mount a panel, mutate UI, wire runtime
telemetry, call the router, call an advisor, execute adapters, call providers,
persist data, influence routes, or grant ML route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase10_read_only_advisory_panel_renderer_mount_contract',
    'build_phase10_read_only_panel_renderer_mount_contract_probe',
    'evaluate_phase10_read_only_advisory_panel_renderer_mount_request',
    'ReadOnlyAdvisoryPanelRendererMountDecision',
    'ReadOnlyPanelRendererMountMode',
    'ReadOnlyPanelRendererMountStatus',
]
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Tuple

from .read_only_advisory_panel_runtime_activation import (
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelope,
    ReadOnlyPanelRuntimeActivationEnvelopeState,
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
)
from ._read_only_advisory_panel_renderer_mount_evaluation import (
    _activation_envelope_is_safe,
    _build_renderer_mount_decision,
    _decision_required_false_fields,
    _decision_required_true_fields,
    _policy_required_false_fields,
    _policy_required_true_fields,
    _require_tuple_of_text,
    _status_for_requested_capabilities,
)


FEATURE_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_v1"
PREVIOUS_COMPLETION_HANDOFF_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_completion_handoff_v1"
SOURCE_ACTIVATION_IMPLEMENTATION_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1"


class ReadOnlyPanelRendererMountMode(str, Enum):
    """Contract-level modes for a future read-only renderer mount."""

    CONTRACT_ONLY = "contract_only"
    FUTURE_READ_ONLY_RENDERER_MOUNT = "future_read_only_renderer_mount"
    BLOCKED = "blocked"


class ReadOnlyPanelRendererMountStatus(str, Enum):
    """Decision status for a proposed future renderer/mount contract."""

    ACCEPTED_CONTRACT_ONLY = "accepted_contract_only"
    ACCEPTED_FUTURE_READ_ONLY_RENDERER_MOUNT_CONTRACT = "accepted_future_read_only_renderer_mount_contract"
    BLOCKED_UNSAFE_AUTHORITY = "blocked_unsafe_authority"
    BLOCKED_UNSAFE_RUNTIME_WIRING = "blocked_unsafe_runtime_wiring"
    BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT = "blocked_unsafe_data_or_side_effect"
    BLOCKED_UNSAFE_TEXT_OR_CONTROLS = "blocked_unsafe_text_or_controls"
    BLOCKED_UNSAFE_SOURCE_ENVELOPE = "blocked_unsafe_source_envelope"


FORBIDDEN_RENDERER_MOUNT_CAPABILITIES: Tuple[str, ...] = (
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
    "actual_runtime_panel_activation",
    "actual_renderer_mount",
    "renderer_activation",
    "mounted_panel",
    "runtime_ui_mutation",
    "runtime_telemetry_surface_wiring",
    "runtime_copilot_decision_behavior",
)

REQUIRED_RENDERER_MOUNT_CONTRACT_LABELS: Tuple[str, ...] = (
    "read_only_panel_label",
    "advisory_role_label",
    "canonical_route_unchanged_label",
    "no_route_authority_label",
    "confidence_not_correctness_label",
    "non_training_feedback_label",
    "feature_flag_default_off_label",
)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRendererMountPolicy:
    """Policy for a future read-only advisory panel renderer/mount contract."""

    mount_mode: ReadOnlyPanelRendererMountMode = ReadOnlyPanelRendererMountMode.CONTRACT_ONLY
    source_completion_handoff_id: str = PREVIOUS_COMPLETION_HANDOFF_ID
    source_activation_implementation_id: str = SOURCE_ACTIVATION_IMPLEMENTATION_ID
    require_phase9_activation_envelope_input: bool = True
    require_explicit_feature_flag: bool = True
    feature_flag_default_enabled: bool = False
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_envelope: bool = True
    require_route_invariant_mount: bool = True
    require_final_selection_invisible_mount: bool = True
    require_renderer_input_bounded: bool = True
    require_renderer_output_bounded: bool = True
    require_removable_noop_mount: bool = True
    require_non_training_feedback_slot: bool = True
    allow_actual_runtime_panel_activation_in_this_phase: bool = False
    allow_actual_renderer_mount_in_this_phase: bool = False
    allow_renderer_activation_in_this_phase: bool = False
    allow_mounted_panel_in_this_phase: bool = False
    allow_runtime_ui_mutation_in_this_phase: bool = False
    allow_runtime_telemetry_surface_wiring_in_this_phase: bool = False
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
    allow_route_influence: bool = False
    allow_route_authority: bool = False
    allow_route_override_button: bool = False
    allow_use_ml_route_button: bool = False
    allow_best_route_claim: bool = False
    allow_prompt_ranking: bool = False
    allow_advisory_ranking: bool = False
    allow_free_text_route_advice: bool = False
    allow_free_text_explanations: bool = False
    allow_runtime_copilot_decision_behavior: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        if not isinstance(self.mount_mode, ReadOnlyPanelRendererMountMode):
            raise TypeError("mount_mode must be ReadOnlyPanelRendererMountMode")
        if self.source_completion_handoff_id != PREVIOUS_COMPLETION_HANDOFF_ID:
            raise ValueError("source_completion_handoff_id must match Phase 9 completion handoff")
        if self.source_activation_implementation_id != SOURCE_ACTIVATION_IMPLEMENTATION_ID:
            raise ValueError("source_activation_implementation_id must match Phase 9 activation implementation")
        for field_name in _policy_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _policy_required_false_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRendererMountDecision:
    """Decision returned by the Phase 10 renderer/mount contract evaluator."""

    feature_id: str
    status: ReadOnlyPanelRendererMountStatus
    accepted: bool
    mount_mode: ReadOnlyPanelRendererMountMode
    future_renderer_mount_contract_ready: bool
    contract_only: bool
    phase9_activation_envelope_input_required: bool
    explicit_feature_flag_required: bool
    feature_flag_default_enabled: bool
    disabled_noop_control_required: bool
    fail_open_on_missing_envelope_required: bool
    route_invariant_mount_required: bool
    final_selection_invisible_mount_required: bool
    renderer_input_bounded_required: bool
    renderer_output_bounded_required: bool
    removable_noop_mount_required: bool
    non_training_feedback_slot_required: bool
    actual_runtime_panel_activation_enabled: bool
    actual_renderer_mount_enabled: bool
    renderer_activation_enabled: bool
    mounted_panel_enabled: bool
    runtime_ui_mutation_enabled: bool
    runtime_telemetry_surface_wiring_enabled: bool
    route_influence_enabled: bool
    route_authority_enabled: bool
    router_calls_enabled: bool
    advisor_calls_enabled: bool
    adapter_execution_enabled: bool
    provider_calls_enabled: bool
    persistence_enabled: bool
    prompt_loading_enabled: bool
    prompt_registry_mutation_enabled: bool
    prompt_library_read_enabled: bool
    freeze_memory_read_enabled: bool
    freeze_memory_write_enabled: bool
    router_canon_read_enabled: bool
    route_override_button_enabled: bool
    use_ml_route_button_enabled: bool
    best_route_claim_enabled: bool
    prompt_ranking_enabled: bool
    advisory_ranking_enabled: bool
    free_text_route_advice_enabled: bool
    free_text_explanations_enabled: bool
    runtime_copilot_decision_behavior_enabled: bool
    required_safe_labels: Tuple[str, ...]
    forbidden_capabilities: Tuple[str, ...]
    final_router_remains_authoritative: bool
    ml_advisory_signal_telemetry_only: bool
    critical_boundary_error_budget: int

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 10 renderer mount contract")
        if not isinstance(self.status, ReadOnlyPanelRendererMountStatus):
            raise TypeError("status must be ReadOnlyPanelRendererMountStatus")
        if not isinstance(self.mount_mode, ReadOnlyPanelRendererMountMode):
            raise TypeError("mount_mode must be ReadOnlyPanelRendererMountMode")
        _require_tuple_of_text("required_safe_labels", self.required_safe_labels)
        _require_tuple_of_text("forbidden_capabilities", self.forbidden_capabilities)
        for field_name in _decision_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _decision_required_false_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")
        if self.critical_boundary_error_budget != 0:
            raise ValueError("critical_boundary_error_budget must remain zero")


def build_phase10_read_only_advisory_panel_renderer_mount_contract(
    policy: Optional[ReadOnlyAdvisoryPanelRendererMountPolicy] = None,
    activation_envelope: Optional[ReadOnlyAdvisoryPanelRuntimeActivationEnvelope] = None,
) -> ReadOnlyAdvisoryPanelRendererMountDecision:
    """Build the default safe renderer/mount contract decision.

    The decision may mark a future renderer/mount contract as ready, but it
    never enables actual renderer activation, mounts a panel, mutates UI, wires
    runtime telemetry, or influences routing in this phase.
    """

    policy = policy or ReadOnlyAdvisoryPanelRendererMountPolicy()
    status = ReadOnlyPanelRendererMountStatus.ACCEPTED_CONTRACT_ONLY
    ready = False
    if policy.mount_mode is ReadOnlyPanelRendererMountMode.FUTURE_READ_ONLY_RENDERER_MOUNT:
        ready = _activation_envelope_is_safe(activation_envelope)
        status = ReadOnlyPanelRendererMountStatus.ACCEPTED_FUTURE_READ_ONLY_RENDERER_MOUNT_CONTRACT
        if not ready:
            status = ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_SOURCE_ENVELOPE
    return _decision(policy=policy, status=status, accepted=status.name.startswith("ACCEPTED"), ready=ready)


def evaluate_phase10_read_only_advisory_panel_renderer_mount_request(
    *,
    policy: Optional[ReadOnlyAdvisoryPanelRendererMountPolicy] = None,
    requested_capabilities: Optional[Mapping[str, bool]] = None,
    activation_envelope: Optional[ReadOnlyAdvisoryPanelRuntimeActivationEnvelope] = None,
) -> ReadOnlyAdvisoryPanelRendererMountDecision:
    """Evaluate a proposed future renderer/mount contract request."""

    policy = policy or ReadOnlyAdvisoryPanelRendererMountPolicy()
    requested_capabilities = requested_capabilities or {}
    status = _status_for_requested_capabilities(requested_capabilities, ReadOnlyPanelRendererMountStatus)
    if status is not None:
        return _decision(policy=policy, status=status, accepted=False, ready=False)
    return build_phase10_read_only_advisory_panel_renderer_mount_contract(
        policy=policy,
        activation_envelope=activation_envelope,
    )


def build_phase10_read_only_panel_renderer_mount_contract_probe() -> ReadOnlyAdvisoryPanelRendererMountDecision:
    """Build a safe future-renderer/mount contract probe for validation tests."""

    policy = ReadOnlyAdvisoryPanelRendererMountPolicy(
        mount_mode=ReadOnlyPanelRendererMountMode.FUTURE_READ_ONLY_RENDERER_MOUNT,
    )
    return evaluate_phase10_read_only_advisory_panel_renderer_mount_request(
        policy=policy,
        requested_capabilities={},
        activation_envelope=build_phase9_read_only_panel_runtime_activation_implementation_probe(),
    )


def _decision(
    *,
    policy: ReadOnlyAdvisoryPanelRendererMountPolicy,
    status: ReadOnlyPanelRendererMountStatus,
    accepted: bool,
    ready: bool,
) -> ReadOnlyAdvisoryPanelRendererMountDecision:
    """Support decision behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelRendererMountPolicy
        The policy value.
    status : ReadOnlyPanelRendererMountStatus
        The status value.
    accepted : bool
        The accepted value.
    ready : bool
        The ready value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelRendererMountDecision
        The read only advisory panel renderer mount decision result.
    """
    
    return _build_renderer_mount_decision(
        policy=policy,
        decision_type=ReadOnlyAdvisoryPanelRendererMountDecision,
        feature_id=FEATURE_ID,
        status=status,
        accepted=accepted,
        ready=ready,
        required_safe_labels=REQUIRED_RENDERER_MOUNT_CONTRACT_LABELS,
        forbidden_capabilities=FORBIDDEN_RENDERER_MOUNT_CAPABILITIES,
    )
















