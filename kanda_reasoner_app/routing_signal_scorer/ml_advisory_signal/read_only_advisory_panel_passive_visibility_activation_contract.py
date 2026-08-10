# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_passive_visibility_activation_contract.py
"""Phase 13 read-only advisory panel passive visibility activation contract.

Contract only. This module defines the boundary for a future passive visibility
activation path that may consume the Phase 12 runtime app-host visibility
descriptor. It does not activate visibility, register a passive slot, mutate UI,
wire telemetry surfaces, subscribe to host events, register callbacks, call the
router, call an advisor, execute adapters, call providers, persist data,
influence routes, or grant route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase13_read_only_advisory_panel_passive_visibility_activation_contract',
    'build_phase13_read_only_panel_passive_visibility_activation_contract_probe',
    'evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request',
    'ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision',
    'ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy',
    'ReadOnlyPanelPassiveVisibilityActivationMode',
    'ReadOnlyPanelPassiveVisibilityActivationStatus',
]
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Tuple

from .read_only_advisory_panel_runtime_app_host_visibility import (
    build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe,
)
from ._read_only_advisory_panel_passive_visibility_activation_contract_evaluation import (
    _activation_capabilities,
    _authority_capabilities,
    _request_capabilities,
    _side_effect_capabilities,
    _source_descriptor_is_safe,
    _text_or_control_capabilities,
    _truthy,
)
from ._read_only_advisory_panel_passive_visibility_activation_contract_invariants import (
    _validate_decision_invariants,
    _validate_policy_invariants,
)


FEATURE_ID = "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_contract_v1"
PREVIOUS_COMPLETION_HANDOFF_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_completion_handoff_v1"
SOURCE_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1"


class ReadOnlyPanelPassiveVisibilityActivationMode(str, Enum):
    """Contract-level modes for a future passive visibility activation path."""

    CONTRACT_ONLY = "contract_only"
    FUTURE_PASSIVE_VISIBILITY_ACTIVATION = "future_passive_visibility_activation"
    BLOCKED = "blocked"


class ReadOnlyPanelPassiveVisibilityActivationStatus(str, Enum):
    """Decision status for the Phase 13 passive visibility activation contract."""

    ACCEPTED_CONTRACT_ONLY = "accepted_contract_only"
    ACCEPTED_FUTURE_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT = (
        "accepted_future_passive_visibility_activation_contract"
    )
    BLOCKED_UNSAFE_AUTHORITY = "blocked_unsafe_authority"
    BLOCKED_UNSAFE_ACTIVATION = "blocked_unsafe_activation"
    BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT = "blocked_unsafe_data_or_side_effect"
    BLOCKED_UNSAFE_TEXT_OR_CONTROLS = "blocked_unsafe_text_or_controls"
    BLOCKED_UNSAFE_SOURCE_DESCRIPTOR = "blocked_unsafe_source_descriptor"


FORBIDDEN_PASSIVE_VISIBILITY_ACTIVATION_CAPABILITIES: Tuple[str, ...] = (
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
    "actual_passive_visibility_activation",
    "passive_visibility_activation",
    "passive_visibility_slot_registration",
    "passive_visibility_slot_mutation",
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

REQUIRED_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT_LABELS: Tuple[str, ...] = (
    "read_only_panel_label",
    "advisory_role_label",
    "passive_visibility_activation_default_off_label",
    "canonical_route_unchanged_label",
    "no_route_authority_label",
    "confidence_not_correctness_label",
    "non_training_feedback_label",
)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy:
    """Policy for a future passive visibility activation contract."""

    activation_mode: ReadOnlyPanelPassiveVisibilityActivationMode = (
        ReadOnlyPanelPassiveVisibilityActivationMode.CONTRACT_ONLY
    )
    source_completion_handoff_id: str = PREVIOUS_COMPLETION_HANDOFF_ID
    source_runtime_app_host_visibility_implementation_id: str = SOURCE_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_ID
    require_phase12_runtime_app_host_visibility_descriptor_input: bool = True
    require_explicit_feature_flag: bool = True
    feature_flag_default_enabled: bool = False
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_descriptor: bool = True
    require_block_unsafe_descriptor: bool = True
    require_bounded_passive_visibility_input: bool = True
    require_bounded_passive_visibility_output: bool = True
    require_read_only_passive_visibility_slot: bool = True
    require_removable_noop_activation: bool = True
    require_route_invariant_activation: bool = True
    require_final_selection_invisible_activation: bool = True
    require_non_training_feedback_slot: bool = True
    allow_future_passive_visibility_activation_contract: bool = True
    allow_actual_passive_visibility_activation_in_this_phase: bool = False
    allow_passive_visibility_slot_registration_in_this_phase: bool = False
    allow_passive_visibility_slot_mutation_in_this_phase: bool = False
    allow_actual_runtime_app_host_visibility_in_this_phase: bool = False
    allow_runtime_app_host_visibility_activation_in_this_phase: bool = False
    allow_mounted_runtime_panel_in_this_phase: bool = False
    allow_runtime_panel_mount_side_effects: bool = False
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
    allow_runtime_pilot_behavior: bool = False
    allow_runtime_copilot_decision_behavior: bool = False
    allow_autonomous_ml_router: bool = False

    def __post_init__(self) -> None:
        """Validate immutable policy invariants without reflection."""

        _validate_policy_invariants(
            self,
            activation_mode_type=ReadOnlyPanelPassiveVisibilityActivationMode,
            previous_completion_handoff_id=PREVIOUS_COMPLETION_HANDOFF_ID,
            source_runtime_app_host_visibility_implementation_id=(
                SOURCE_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_ID
            ),
        )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision:
    """Decision returned by the Phase 13 passive visibility activation contract."""

    feature_id: str
    status: ReadOnlyPanelPassiveVisibilityActivationStatus
    accepted: bool
    activation_mode: ReadOnlyPanelPassiveVisibilityActivationMode
    future_passive_visibility_activation_contract_ready: bool
    contract_only: bool
    source_descriptor_safe: bool
    phase12_runtime_app_host_visibility_descriptor_input_required: bool
    explicit_feature_flag_required: bool
    feature_flag_default_enabled: bool
    disabled_noop_control_required: bool
    fail_open_on_missing_descriptor_required: bool
    block_unsafe_descriptor_required: bool
    bounded_passive_visibility_input_required: bool
    bounded_passive_visibility_output_required: bool
    read_only_passive_visibility_slot_required: bool
    removable_noop_activation_required: bool
    route_invariant_activation_required: bool
    final_selection_invisible_activation_required: bool
    non_training_feedback_slot_required: bool
    actual_passive_visibility_activation_enabled: bool
    passive_visibility_slot_registration_enabled: bool
    passive_visibility_slot_mutation_enabled: bool
    actual_runtime_app_host_visibility_enabled: bool
    runtime_app_host_visibility_activation_enabled: bool
    mounted_runtime_panel_enabled: bool
    runtime_panel_mount_side_effects_enabled: bool
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
    runtime_pilot_behavior_enabled: bool
    runtime_copilot_decision_behavior_enabled: bool
    autonomous_ml_router_enabled: bool
    visible_ml_integration_complete: bool
    critical_boundary_error_budget: int

    def __post_init__(self) -> None:
        """Validate immutable decision invariants without reflection."""

        _validate_decision_invariants(
            self,
            feature_id=FEATURE_ID,
            status_type=ReadOnlyPanelPassiveVisibilityActivationStatus,
            activation_mode_type=ReadOnlyPanelPassiveVisibilityActivationMode,
        )


def build_phase13_read_only_advisory_panel_passive_visibility_activation_contract(
    policy: ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy | None = None,
    source_descriptor: object | None = None,
) -> ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision:
    """Build the contract decision for a future passive visibility activation path."""

    if policy is None:
        policy = ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy(
            activation_mode=ReadOnlyPanelPassiveVisibilityActivationMode.FUTURE_PASSIVE_VISIBILITY_ACTIVATION,
        )
    if not isinstance(policy, ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy")
    if source_descriptor is None:
        source_descriptor = build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe()
    source_safe = _source_descriptor_is_safe(source_descriptor)
    if not source_safe:
        return _decision(
            policy=policy,
            status=ReadOnlyPanelPassiveVisibilityActivationStatus.BLOCKED_UNSAFE_SOURCE_DESCRIPTOR,
            accepted=False,
            source_safe=False,
        )
    return _decision(
        policy=policy,
        status=ReadOnlyPanelPassiveVisibilityActivationStatus.ACCEPTED_FUTURE_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT,
        accepted=True,
        source_safe=True,
    )


def evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request(
    request: Mapping[str, object] | None,
) -> ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision:
    """Evaluate a proposed Phase 13 request without granting any runtime capability."""

    policy = ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy(
        activation_mode=ReadOnlyPanelPassiveVisibilityActivationMode.FUTURE_PASSIVE_VISIBILITY_ACTIVATION,
    )
    if request is None:
        return build_phase13_read_only_advisory_panel_passive_visibility_activation_contract(policy)
    if not isinstance(request, Mapping):
        raise TypeError("request must be a mapping or None")

    capabilities = _request_capabilities(request)
    if _truthy(request, "route_authority") or _truthy(request, "route_influence") or capabilities.intersection(_authority_capabilities()):
        return _decision(
            policy=policy,
            status=ReadOnlyPanelPassiveVisibilityActivationStatus.BLOCKED_UNSAFE_AUTHORITY,
            accepted=False,
            source_safe=True,
        )
    if capabilities.intersection(_activation_capabilities()) or _truthy(request, "passive_visibility_activation"):
        return _decision(
            policy=policy,
            status=ReadOnlyPanelPassiveVisibilityActivationStatus.BLOCKED_UNSAFE_ACTIVATION,
            accepted=False,
            source_safe=True,
        )
    if capabilities.intersection(_side_effect_capabilities()):
        return _decision(
            policy=policy,
            status=ReadOnlyPanelPassiveVisibilityActivationStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT,
            accepted=False,
            source_safe=True,
        )
    if capabilities.intersection(_text_or_control_capabilities()):
        return _decision(
            policy=policy,
            status=ReadOnlyPanelPassiveVisibilityActivationStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS,
            accepted=False,
            source_safe=True,
        )
    return build_phase13_read_only_advisory_panel_passive_visibility_activation_contract(policy)


def build_phase13_read_only_panel_passive_visibility_activation_contract_probe(
) -> ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision:
    """Build a safe contract probe for Phase 13 passive visibility activation."""

    return build_phase13_read_only_advisory_panel_passive_visibility_activation_contract()


def _decision(
    *,
    policy: ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy,
    status: ReadOnlyPanelPassiveVisibilityActivationStatus,
    accepted: bool,
    source_safe: bool,
) -> ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision:
    """Support decision behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy
        The policy value.
    status : ReadOnlyPanelPassiveVisibilityActivationStatus
        The status value.
    accepted : bool
        The accepted value.
    source_safe : bool
        The source safe value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision
        The read only advisory panel passive visibility activation decision result.
    """
    
    return ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision(
        feature_id=FEATURE_ID,
        status=status,
        accepted=accepted,
        activation_mode=policy.activation_mode if accepted else ReadOnlyPanelPassiveVisibilityActivationMode.BLOCKED,
        future_passive_visibility_activation_contract_ready=accepted,
        contract_only=True,
        source_descriptor_safe=source_safe,
        phase12_runtime_app_host_visibility_descriptor_input_required=policy.require_phase12_runtime_app_host_visibility_descriptor_input,
        explicit_feature_flag_required=policy.require_explicit_feature_flag,
        feature_flag_default_enabled=policy.feature_flag_default_enabled,
        disabled_noop_control_required=policy.require_disable_noop_control,
        fail_open_on_missing_descriptor_required=policy.require_fail_open_on_missing_descriptor,
        block_unsafe_descriptor_required=policy.require_block_unsafe_descriptor,
        bounded_passive_visibility_input_required=policy.require_bounded_passive_visibility_input,
        bounded_passive_visibility_output_required=policy.require_bounded_passive_visibility_output,
        read_only_passive_visibility_slot_required=policy.require_read_only_passive_visibility_slot,
        removable_noop_activation_required=policy.require_removable_noop_activation,
        route_invariant_activation_required=policy.require_route_invariant_activation,
        final_selection_invisible_activation_required=policy.require_final_selection_invisible_activation,
        non_training_feedback_slot_required=policy.require_non_training_feedback_slot,
        actual_passive_visibility_activation_enabled=False,
        passive_visibility_slot_registration_enabled=False,
        passive_visibility_slot_mutation_enabled=False,
        actual_runtime_app_host_visibility_enabled=False,
        runtime_app_host_visibility_activation_enabled=False,
        mounted_runtime_panel_enabled=False,
        runtime_panel_mount_side_effects_enabled=False,
        host_event_subscription_enabled=False,
        host_callback_registration_enabled=False,
        runtime_ui_mutation_enabled=False,
        runtime_telemetry_surface_wiring_enabled=False,
        route_influence_enabled=False,
        route_authority_enabled=False,
        router_calls_enabled=False,
        advisor_calls_enabled=False,
        adapter_execution_enabled=False,
        provider_calls_enabled=False,
        persistence_enabled=False,
        prompt_loading_enabled=False,
        prompt_registry_mutation_enabled=False,
        prompt_library_read_enabled=False,
        freeze_memory_read_enabled=False,
        freeze_memory_write_enabled=False,
        router_canon_read_enabled=False,
        route_override_button_enabled=False,
        use_ml_route_button_enabled=False,
        best_route_claim_enabled=False,
        prompt_ranking_enabled=False,
        advisory_ranking_enabled=False,
        free_text_route_advice_enabled=False,
        free_text_explanations_enabled=False,
        runtime_pilot_behavior_enabled=False,
        runtime_copilot_decision_behavior_enabled=False,
        autonomous_ml_router_enabled=False,
        visible_ml_integration_complete=False,
        critical_boundary_error_budget=0,
    )
