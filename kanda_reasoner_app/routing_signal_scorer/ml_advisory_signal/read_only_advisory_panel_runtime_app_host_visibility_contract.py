# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_runtime_app_host_visibility_contract.py
"""Phase 12 read-only advisory panel runtime app-host visibility contract.

Contract only. This module defines the narrow conditions for a future runtime
app-host visibility path that may consume the Phase 11 host-binding descriptor.
It does not make the advisory panel visible in the runtime app host, mutate UI,
wire telemetry surfaces, subscribe to host events, register callbacks, call the
router, call an advisor, execute adapters, call providers, persist data,
influence routes, or grant ML route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract',
    'build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe',
    'evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request',
    'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision',
    'ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy',
    'ReadOnlyPanelRuntimeAppHostVisibilityMode',
    'ReadOnlyPanelRuntimeAppHostVisibilityStatus',
]
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Tuple

from .read_only_advisory_panel_host_binding import (
    ReadOnlyAdvisoryPanelHostBindingDescriptor,
    ReadOnlyPanelHostBindingImplementationState,
    build_phase11_read_only_panel_host_binding_implementation_probe,
)

from ._read_only_advisory_panel_runtime_app_host_visibility_contract_evaluation import (
    FORBIDDEN_RUNTIME_APP_HOST_VISIBILITY_CAPABILITIES,
    REQUIRED_RUNTIME_APP_HOST_VISIBILITY_CONTRACT_LABELS,
    contains_any as _contains_any,
    requested_capabilities as _requested_capabilities,
    source_host_binding_descriptor_is_safe as _source_host_binding_descriptor_is_safe,
)
from ._read_only_advisory_panel_runtime_app_host_visibility_contract_invariants import (
    decision_forbidden_true_fields as _decision_forbidden_true_fields,
    decision_required_true_fields as _decision_required_true_fields,
    policy_required_false_fields as _policy_required_false_fields,
    policy_required_true_fields as _policy_required_true_fields,
    validate_decision as _validate_decision,
    validate_policy as _validate_policy,
)


FEATURE_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract_v1"
PREVIOUS_COMPLETION_HANDOFF_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_completion_handoff_v1"
SOURCE_HOST_BINDING_IMPLEMENTATION_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_implementation_v1"


class ReadOnlyPanelRuntimeAppHostVisibilityMode(str, Enum):
    """Contract-level modes for a future runtime app-host visibility path."""

    CONTRACT_ONLY = "contract_only"
    FUTURE_READ_ONLY_RUNTIME_APP_HOST_VISIBILITY = "future_read_only_runtime_app_host_visibility"
    BLOCKED = "blocked"


class ReadOnlyPanelRuntimeAppHostVisibilityStatus(str, Enum):
    """Decision status for a proposed runtime app-host visibility contract."""

    ACCEPTED_CONTRACT_ONLY = "accepted_contract_only"
    ACCEPTED_FUTURE_READ_ONLY_RUNTIME_APP_HOST_VISIBILITY_CONTRACT = (
        "accepted_future_read_only_runtime_app_host_visibility_contract"
    )
    BLOCKED_UNSAFE_AUTHORITY = "blocked_unsafe_authority"
    BLOCKED_UNSAFE_RUNTIME_VISIBILITY = "blocked_unsafe_runtime_visibility"
    BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT = "blocked_unsafe_data_or_side_effect"
    BLOCKED_UNSAFE_TEXT_OR_CONTROLS = "blocked_unsafe_text_or_controls"
    BLOCKED_UNSAFE_SOURCE_DESCRIPTOR = "blocked_unsafe_source_descriptor"





@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy:
    """Policy for a future read-only runtime app-host visibility contract."""

    visibility_mode: ReadOnlyPanelRuntimeAppHostVisibilityMode = (
        ReadOnlyPanelRuntimeAppHostVisibilityMode.CONTRACT_ONLY
    )
    source_completion_handoff_id: str = PREVIOUS_COMPLETION_HANDOFF_ID
    source_host_binding_implementation_id: str = SOURCE_HOST_BINDING_IMPLEMENTATION_ID
    require_phase11_host_binding_descriptor_input: bool = True
    require_explicit_feature_flag: bool = True
    feature_flag_default_enabled: bool = False
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_descriptor: bool = True
    require_block_unsafe_descriptor: bool = True
    require_route_invariant_visibility: bool = True
    require_final_selection_invisible_visibility: bool = True
    require_runtime_visibility_input_bounded: bool = True
    require_runtime_visibility_output_bounded: bool = True
    require_removable_noop_visibility: bool = True
    require_non_training_feedback_slot: bool = True
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
        """Validate the contract policy through explicit invariant checks."""
        _validate_policy(
            self,
            visibility_mode_type=ReadOnlyPanelRuntimeAppHostVisibilityMode,
            previous_completion_handoff_id=PREVIOUS_COMPLETION_HANDOFF_ID,
            source_host_binding_implementation_id=SOURCE_HOST_BINDING_IMPLEMENTATION_ID,
        )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision:
    """Decision returned by the Phase 12 runtime app-host visibility contract."""

    feature_id: str
    status: ReadOnlyPanelRuntimeAppHostVisibilityStatus
    accepted: bool
    visibility_mode: ReadOnlyPanelRuntimeAppHostVisibilityMode
    future_runtime_app_host_visibility_contract_ready: bool
    contract_only: bool
    phase11_host_binding_descriptor_input_required: bool
    explicit_feature_flag_required: bool
    feature_flag_default_enabled: bool
    disabled_noop_control_required: bool
    fail_open_on_missing_descriptor_required: bool
    block_unsafe_descriptor_required: bool
    route_invariant_visibility_required: bool
    final_selection_invisible_visibility_required: bool
    runtime_visibility_input_bounded_required: bool
    runtime_visibility_output_bounded_required: bool
    removable_noop_visibility_required: bool
    non_training_feedback_slot_required: bool
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
    source_descriptor_safe: bool
    critical_boundary_error_budget: int = 0

    def __post_init__(self) -> None:
        """Validate the contract decision through explicit invariant checks."""
        _validate_decision(
            self,
            feature_id=FEATURE_ID,
            status_type=ReadOnlyPanelRuntimeAppHostVisibilityStatus,
            visibility_mode_type=ReadOnlyPanelRuntimeAppHostVisibilityMode,
        )


def build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract(
    policy: ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy | None = None,
) -> ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision:
    """Build the contract-only Phase 12 runtime app-host visibility decision."""

    if policy is None:
        policy = ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy(
            visibility_mode=(
                ReadOnlyPanelRuntimeAppHostVisibilityMode.
                FUTURE_READ_ONLY_RUNTIME_APP_HOST_VISIBILITY
            )
        )
    if not isinstance(policy, ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy")

    source_descriptor = build_phase11_read_only_panel_host_binding_implementation_probe()
    if not _source_host_binding_descriptor_is_safe(source_descriptor):
        return _decision(
            policy,
            status=ReadOnlyPanelRuntimeAppHostVisibilityStatus.BLOCKED_UNSAFE_SOURCE_DESCRIPTOR,
            accepted=False,
            mode=ReadOnlyPanelRuntimeAppHostVisibilityMode.BLOCKED,
            source_descriptor_safe=False,
        )

    return _decision(
        policy,
        status=(
            ReadOnlyPanelRuntimeAppHostVisibilityStatus.
            ACCEPTED_FUTURE_READ_ONLY_RUNTIME_APP_HOST_VISIBILITY_CONTRACT
        ),
        accepted=True,
        mode=policy.visibility_mode,
        source_descriptor_safe=True,
    )


def evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request(
    request: Mapping[str, object],
    policy: ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy | None = None,
) -> ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision:
    """Evaluate a proposed future runtime app-host visibility request.

    The evaluator fails closed on route authority, runtime UI mutation,
    telemetry surface wiring, host event subscriptions, callbacks, provider
    calls, persistence, autonomous ML routing, or runtime Copilot decision
    behavior. Accepted decisions remain contract-only and do not perform any
    runtime app-host visibility side effects.
    """

    if not isinstance(request, Mapping):
        raise TypeError("request must be a mapping")
    if policy is None:
        policy = ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy(
            visibility_mode=(
                ReadOnlyPanelRuntimeAppHostVisibilityMode.
                FUTURE_READ_ONLY_RUNTIME_APP_HOST_VISIBILITY
            )
        )
    if not isinstance(policy, ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy")

    requested = _requested_capabilities(request)
    if _contains_any(
        requested,
        (
            "route_authority",
            "route_influence",
            "route_override_button",
            "use_ml_route_button",
            "best_route_claim",
            "final_selection_hook",
            "prompt_selection_hook",
            "autonomous_ml_router",
        ),
    ):
        return _decision(
            policy,
            status=ReadOnlyPanelRuntimeAppHostVisibilityStatus.BLOCKED_UNSAFE_AUTHORITY,
            accepted=False,
            mode=ReadOnlyPanelRuntimeAppHostVisibilityMode.BLOCKED,
            source_descriptor_safe=True,
        )
    if _contains_any(
        requested,
        (
            "actual_runtime_app_host_visibility",
            "runtime_app_host_visibility_activation",
            "mounted_runtime_panel",
            "runtime_panel_mount_side_effect",
            "runtime_ui_mutation",
            "runtime_telemetry_surface_wiring",
            "host_event_subscription",
            "host_callback_registration",
        ),
    ):
        return _decision(
            policy,
            status=ReadOnlyPanelRuntimeAppHostVisibilityStatus.BLOCKED_UNSAFE_RUNTIME_VISIBILITY,
            accepted=False,
            mode=ReadOnlyPanelRuntimeAppHostVisibilityMode.BLOCKED,
            source_descriptor_safe=True,
        )
    if _contains_any(
        requested,
        (
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
        ),
    ):
        return _decision(
            policy,
            status=ReadOnlyPanelRuntimeAppHostVisibilityStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT,
            accepted=False,
            mode=ReadOnlyPanelRuntimeAppHostVisibilityMode.BLOCKED,
            source_descriptor_safe=True,
        )
    if _contains_any(
        requested,
        (
            "prompt_ranking",
            "advisory_ranking",
            "free_text_route_advice",
            "free_text_explanation",
            "runtime_copilot_decision_behavior",
        ),
    ):
        return _decision(
            policy,
            status=ReadOnlyPanelRuntimeAppHostVisibilityStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS,
            accepted=False,
            mode=ReadOnlyPanelRuntimeAppHostVisibilityMode.BLOCKED,
            source_descriptor_safe=True,
        )

    return build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract(policy)


def build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe(
) -> ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision:
    """Return a safe probe decision for the Phase 12 contract."""

    return build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract()


def _decision(
    policy: ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy,
    *,
    status: ReadOnlyPanelRuntimeAppHostVisibilityStatus,
    accepted: bool,
    mode: ReadOnlyPanelRuntimeAppHostVisibilityMode,
    source_descriptor_safe: bool,
) -> ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision:
    """Support decision behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy
        The policy value.
    status : ReadOnlyPanelRuntimeAppHostVisibilityStatus
        The status value.
    accepted : bool
        The accepted value.
    mode : ReadOnlyPanelRuntimeAppHostVisibilityMode
        The selected mode.
    source_descriptor_safe : bool
        The source descriptor safe value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision
        The read only advisory panel runtime app host visibility decision result.
    """
    
    return ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision(
        feature_id=FEATURE_ID,
        status=status,
        accepted=accepted,
        visibility_mode=mode,
        future_runtime_app_host_visibility_contract_ready=accepted,
        contract_only=True,
        phase11_host_binding_descriptor_input_required=policy.require_phase11_host_binding_descriptor_input,
        explicit_feature_flag_required=policy.require_explicit_feature_flag,
        feature_flag_default_enabled=policy.feature_flag_default_enabled,
        disabled_noop_control_required=policy.require_disable_noop_control,
        fail_open_on_missing_descriptor_required=policy.require_fail_open_on_missing_descriptor,
        block_unsafe_descriptor_required=policy.require_block_unsafe_descriptor,
        route_invariant_visibility_required=policy.require_route_invariant_visibility,
        final_selection_invisible_visibility_required=policy.require_final_selection_invisible_visibility,
        runtime_visibility_input_bounded_required=policy.require_runtime_visibility_input_bounded,
        runtime_visibility_output_bounded_required=policy.require_runtime_visibility_output_bounded,
        removable_noop_visibility_required=policy.require_removable_noop_visibility,
        non_training_feedback_slot_required=policy.require_non_training_feedback_slot,
        actual_runtime_app_host_visibility_enabled=policy.allow_actual_runtime_app_host_visibility_in_this_phase,
        runtime_app_host_visibility_activation_enabled=(
            policy.allow_runtime_app_host_visibility_activation_in_this_phase
        ),
        mounted_runtime_panel_enabled=policy.allow_mounted_runtime_panel_in_this_phase,
        runtime_panel_mount_side_effects_enabled=policy.allow_runtime_panel_mount_side_effects,
        host_event_subscription_enabled=policy.allow_host_event_subscription,
        host_callback_registration_enabled=policy.allow_host_callback_registration,
        runtime_ui_mutation_enabled=policy.allow_runtime_ui_mutation,
        runtime_telemetry_surface_wiring_enabled=policy.allow_runtime_telemetry_surface_wiring,
        route_influence_enabled=policy.allow_route_influence,
        route_authority_enabled=policy.allow_route_authority,
        router_calls_enabled=policy.allow_router_calls,
        advisor_calls_enabled=policy.allow_advisor_calls,
        adapter_execution_enabled=policy.allow_adapter_execution,
        provider_calls_enabled=policy.allow_provider_calls,
        persistence_enabled=policy.allow_persistence,
        prompt_loading_enabled=policy.allow_prompt_loading,
        prompt_registry_mutation_enabled=policy.allow_prompt_registry_mutation,
        prompt_library_read_enabled=policy.allow_prompt_library_read,
        freeze_memory_read_enabled=policy.allow_freeze_memory_read,
        freeze_memory_write_enabled=policy.allow_freeze_memory_write,
        router_canon_read_enabled=policy.allow_router_canon_read,
        route_override_button_enabled=policy.allow_route_override_button,
        use_ml_route_button_enabled=policy.allow_use_ml_route_button,
        best_route_claim_enabled=policy.allow_best_route_claim,
        prompt_ranking_enabled=policy.allow_prompt_ranking,
        advisory_ranking_enabled=policy.allow_advisory_ranking,
        free_text_route_advice_enabled=policy.allow_free_text_route_advice,
        free_text_explanations_enabled=policy.allow_free_text_explanations,
        runtime_pilot_behavior_enabled=policy.allow_runtime_pilot_behavior,
        runtime_copilot_decision_behavior_enabled=policy.allow_runtime_copilot_decision_behavior,
        autonomous_ml_router_enabled=policy.allow_autonomous_ml_router,
        source_descriptor_safe=source_descriptor_safe,
    )














