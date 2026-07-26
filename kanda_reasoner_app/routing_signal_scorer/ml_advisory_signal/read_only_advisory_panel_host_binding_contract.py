# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_host_binding_contract.py
"""Phase 11 read-only advisory panel host binding contract.

Contract only. This module defines the narrow conditions for a future
read-only host binding path that may consume the Phase 10 renderer/mount
descriptor. It does not bind into the runtime app host, mutate UI, wire
telemetry surfaces, call the router, call an advisor, execute adapters, call
providers, persist data, influence routes, or grant ML route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase11_read_only_advisory_panel_host_binding_contract',
    'build_phase11_read_only_panel_host_binding_contract_probe',
    'evaluate_phase11_read_only_advisory_panel_host_binding_request',
    'ReadOnlyAdvisoryPanelHostBindingDecision',
    'ReadOnlyAdvisoryPanelHostBindingPolicy',
    'ReadOnlyPanelHostBindingMode',
    'ReadOnlyPanelHostBindingStatus',
]
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Tuple

from .read_only_advisory_panel_renderer_mount import (
    ReadOnlyAdvisoryPanelRendererMountDescriptor,
    build_phase10_read_only_panel_renderer_mount_implementation_probe,
)
from ._read_only_advisory_panel_host_binding_evaluation import (
    _build_host_binding_decision,
    _decision_required_false_fields,
    _decision_required_true_fields,
    _policy_required_false_fields,
    _policy_required_true_fields,
    _renderer_mount_descriptor_is_safe,
    _require_tuple_of_text,
    _status_for_requested_capabilities,
)


FEATURE_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_contract_v1"
PREVIOUS_COMPLETION_HANDOFF_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_completion_handoff_v1"
SOURCE_RENDERER_MOUNT_IMPLEMENTATION_ID = "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1"


class ReadOnlyPanelHostBindingMode(str, Enum):
    """Contract-level modes for a future read-only host binding path."""

    CONTRACT_ONLY = "contract_only"
    FUTURE_READ_ONLY_HOST_BINDING = "future_read_only_host_binding"
    BLOCKED = "blocked"


class ReadOnlyPanelHostBindingStatus(str, Enum):
    """Decision status for a proposed future host binding contract."""

    ACCEPTED_CONTRACT_ONLY = "accepted_contract_only"
    ACCEPTED_FUTURE_READ_ONLY_HOST_BINDING_CONTRACT = "accepted_future_read_only_host_binding_contract"
    BLOCKED_UNSAFE_AUTHORITY = "blocked_unsafe_authority"
    BLOCKED_UNSAFE_RUNTIME_HOST_BINDING = "blocked_unsafe_runtime_host_binding"
    BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT = "blocked_unsafe_data_or_side_effect"
    BLOCKED_UNSAFE_TEXT_OR_CONTROLS = "blocked_unsafe_text_or_controls"
    BLOCKED_UNSAFE_SOURCE_DESCRIPTOR = "blocked_unsafe_source_descriptor"


FORBIDDEN_HOST_BINDING_CAPABILITIES: Tuple[str, ...] = (
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
    "actual_host_binding",
    "host_binding_activation",
    "runtime_app_host_visibility",
    "mounted_runtime_panel",
    "host_event_subscription",
    "host_callback_registration",
    "runtime_ui_mutation",
    "runtime_telemetry_surface_wiring",
    "runtime_copilot_decision_behavior",
)

REQUIRED_HOST_BINDING_CONTRACT_LABELS: Tuple[str, ...] = (
    "read_only_panel_label",
    "advisory_role_label",
    "host_binding_default_off_label",
    "canonical_route_unchanged_label",
    "no_route_authority_label",
    "confidence_not_correctness_label",
    "non_training_feedback_label",
)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelHostBindingPolicy:
    """Policy for a future read-only advisory panel host-binding contract."""

    host_binding_mode: ReadOnlyPanelHostBindingMode = ReadOnlyPanelHostBindingMode.CONTRACT_ONLY
    source_completion_handoff_id: str = PREVIOUS_COMPLETION_HANDOFF_ID
    source_renderer_mount_implementation_id: str = SOURCE_RENDERER_MOUNT_IMPLEMENTATION_ID
    require_phase10_renderer_mount_descriptor_input: bool = True
    require_explicit_feature_flag: bool = True
    feature_flag_default_enabled: bool = False
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_descriptor: bool = True
    require_block_unsafe_descriptor: bool = True
    require_route_invariant_host_binding: bool = True
    require_final_selection_invisible_host_binding: bool = True
    require_host_input_bounded: bool = True
    require_host_output_bounded: bool = True
    require_removable_noop_host_binding: bool = True
    require_non_training_feedback_slot: bool = True
    allow_actual_host_binding_in_this_phase: bool = False
    allow_host_binding_activation_in_this_phase: bool = False
    allow_runtime_app_host_visibility_in_this_phase: bool = False
    allow_mounted_runtime_panel_in_this_phase: bool = False
    allow_host_event_subscription: bool = False
    allow_host_callback_registration: bool = False
    allow_runtime_ui_mutation: bool = False
    allow_runtime_telemetry_surface_wiring: bool = False
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
        
        if not isinstance(self.host_binding_mode, ReadOnlyPanelHostBindingMode):
            raise TypeError("host_binding_mode must be ReadOnlyPanelHostBindingMode")
        if self.source_completion_handoff_id != PREVIOUS_COMPLETION_HANDOFF_ID:
            raise ValueError("source_completion_handoff_id must match Phase 10 completion handoff")
        if self.source_renderer_mount_implementation_id != SOURCE_RENDERER_MOUNT_IMPLEMENTATION_ID:
            raise ValueError("source_renderer_mount_implementation_id must match Phase 10 implementation")
        for field_name in _policy_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _policy_required_false_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelHostBindingDecision:
    """Decision returned by the Phase 11 host-binding contract evaluator."""

    feature_id: str
    status: ReadOnlyPanelHostBindingStatus
    accepted: bool
    host_binding_mode: ReadOnlyPanelHostBindingMode
    future_host_binding_contract_ready: bool
    contract_only: bool
    phase10_renderer_mount_descriptor_input_required: bool
    explicit_feature_flag_required: bool
    feature_flag_default_enabled: bool
    disabled_noop_control_required: bool
    fail_open_on_missing_descriptor_required: bool
    block_unsafe_descriptor_required: bool
    route_invariant_host_binding_required: bool
    final_selection_invisible_host_binding_required: bool
    host_input_bounded_required: bool
    host_output_bounded_required: bool
    removable_noop_host_binding_required: bool
    non_training_feedback_slot_required: bool
    actual_host_binding_enabled: bool
    host_binding_activation_enabled: bool
    runtime_app_host_visibility_enabled: bool
    mounted_runtime_panel_enabled: bool
    host_event_subscription_enabled: bool
    host_callback_registration_enabled: bool
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
            raise ValueError("feature_id must match Phase 11 host binding contract")
        if not isinstance(self.status, ReadOnlyPanelHostBindingStatus):
            raise TypeError("status must be ReadOnlyPanelHostBindingStatus")
        if not isinstance(self.host_binding_mode, ReadOnlyPanelHostBindingMode):
            raise TypeError("host_binding_mode must be ReadOnlyPanelHostBindingMode")
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


def build_phase11_read_only_advisory_panel_host_binding_contract(
    policy: Optional[ReadOnlyAdvisoryPanelHostBindingPolicy] = None,
    renderer_mount_descriptor: Optional[ReadOnlyAdvisoryPanelRendererMountDescriptor] = None,
) -> ReadOnlyAdvisoryPanelHostBindingDecision:
    """Build the default safe host-binding contract decision.

    The decision may mark a future host-binding contract as ready, but it never
    enables actual host binding, app-host visibility, UI mutation, telemetry
    surface wiring, or route authority.
    """

    return evaluate_phase11_read_only_advisory_panel_host_binding_request(
        policy=policy or ReadOnlyAdvisoryPanelHostBindingPolicy(),
        requested_capabilities={},
        renderer_mount_descriptor=renderer_mount_descriptor,
    )


def evaluate_phase11_read_only_advisory_panel_host_binding_request(
    policy: Optional[ReadOnlyAdvisoryPanelHostBindingPolicy] = None,
    requested_capabilities: Optional[Mapping[str, bool]] = None,
    renderer_mount_descriptor: Optional[ReadOnlyAdvisoryPanelRendererMountDescriptor] = None,
) -> ReadOnlyAdvisoryPanelHostBindingDecision:
    """Evaluate whether a future host-binding request stays inside the contract."""

    policy = policy or ReadOnlyAdvisoryPanelHostBindingPolicy()
    if not isinstance(policy, ReadOnlyAdvisoryPanelHostBindingPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelHostBindingPolicy")
    requested = requested_capabilities or {}
    if not isinstance(requested, Mapping):
        raise TypeError("requested_capabilities must be a mapping")

    blocked_status = _status_for_requested_capabilities(requested, ReadOnlyPanelHostBindingStatus)
    if blocked_status is not None:
        return _decision(policy=policy, status=blocked_status, accepted=False, ready=False)

    if policy.host_binding_mode is ReadOnlyPanelHostBindingMode.CONTRACT_ONLY:
        return _decision(
            policy=policy,
            status=ReadOnlyPanelHostBindingStatus.ACCEPTED_CONTRACT_ONLY,
            accepted=True,
            ready=False,
        )

    if policy.host_binding_mode is ReadOnlyPanelHostBindingMode.FUTURE_READ_ONLY_HOST_BINDING:
        if not _renderer_mount_descriptor_is_safe(renderer_mount_descriptor):
            return _decision(
                policy=policy,
                status=ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_SOURCE_DESCRIPTOR,
                accepted=False,
                ready=False,
            )
        return _decision(
            policy=policy,
            status=ReadOnlyPanelHostBindingStatus.ACCEPTED_FUTURE_READ_ONLY_HOST_BINDING_CONTRACT,
            accepted=True,
            ready=True,
        )

    return _decision(
        policy=policy,
        status=ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING,
        accepted=False,
        ready=False,
    )


def build_phase11_read_only_panel_host_binding_contract_probe() -> ReadOnlyAdvisoryPanelHostBindingDecision:
    """Build a safe future-host-binding contract probe for validation tests."""

    policy = ReadOnlyAdvisoryPanelHostBindingPolicy(
        host_binding_mode=ReadOnlyPanelHostBindingMode.FUTURE_READ_ONLY_HOST_BINDING,
    )
    return evaluate_phase11_read_only_advisory_panel_host_binding_request(
        policy=policy,
        requested_capabilities={},
        renderer_mount_descriptor=build_phase10_read_only_panel_renderer_mount_implementation_probe(),
    )


def _decision(
    *,
    policy: ReadOnlyAdvisoryPanelHostBindingPolicy,
    status: ReadOnlyPanelHostBindingStatus,
    accepted: bool,
    ready: bool,
) -> ReadOnlyAdvisoryPanelHostBindingDecision:
    """Support decision behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelHostBindingPolicy
        The policy value.
    status : ReadOnlyPanelHostBindingStatus
        The status value.
    accepted : bool
        The accepted value.
    ready : bool
        The ready value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelHostBindingDecision
        The read only advisory panel host binding decision result.
    """
    
    return _build_host_binding_decision(
        policy=policy,
        decision_type=ReadOnlyAdvisoryPanelHostBindingDecision,
        feature_id=FEATURE_ID,
        status=status,
        accepted=accepted,
        ready=ready,
        required_safe_labels=REQUIRED_HOST_BINDING_CONTRACT_LABELS,
        forbidden_capabilities=FORBIDDEN_HOST_BINDING_CAPABILITIES,
    )
