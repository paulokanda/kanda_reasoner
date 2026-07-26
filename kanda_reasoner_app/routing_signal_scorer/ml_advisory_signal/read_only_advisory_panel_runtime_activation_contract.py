# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_runtime_activation_contract.py
"""Phase 9 read-only advisory panel runtime activation contract.

Contract only. This module defines the narrow conditions for a future runtime
visible advisory panel activation. It does not activate a panel, mount UI,
render screens, mutate UI, wire telemetry into runtime surfaces, call the
router, call an advisor, execute adapters, call providers, persist data,
influence routes, or grant ML route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase9_read_only_advisory_panel_runtime_activation_contract',
    'build_phase9_read_only_panel_runtime_activation_contract_probe',
    'evaluate_phase9_read_only_advisory_panel_runtime_activation_request',
    'ReadOnlyAdvisoryPanelRuntimeActivationDecision',
    'ReadOnlyPanelRuntimeActivationMode',
    'ReadOnlyPanelRuntimeActivationStatus',
]
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Tuple

from .read_only_advisory_panel_ui import (
    ReadOnlyAdvisoryPanelUIState,
    ReadOnlyAdvisoryPanelViewModel,
    build_phase8_read_only_advisory_panel_ui_probe,
)
from ._read_only_advisory_panel_runtime_activation_contract_evaluation import (
    _status_for_requested_capabilities,
    _view_model_is_safe,
)
from ._read_only_advisory_panel_runtime_activation_contract_invariants import (
    _validate_decision_invariants,
    _validate_policy_invariants,
)


FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_v1"
PREVIOUS_COMPLETION_HANDOFF_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_completion_handoff_v1"


class ReadOnlyPanelRuntimeActivationMode(str, Enum):
    """Contract-level activation modes for a future visible panel."""

    CONTRACT_ONLY = "contract_only"
    FUTURE_READ_ONLY_RUNTIME_PANEL = "future_read_only_runtime_panel"
    BLOCKED = "blocked"


class ReadOnlyPanelRuntimeActivationStatus(str, Enum):
    """Decision status for a proposed future panel activation contract."""

    ACCEPTED_CONTRACT_ONLY = "accepted_contract_only"
    ACCEPTED_FUTURE_READ_ONLY_RUNTIME_PANEL_CONTRACT = "accepted_future_read_only_runtime_panel_contract"
    BLOCKED_UNSAFE_AUTHORITY = "blocked_unsafe_authority"
    BLOCKED_UNSAFE_RUNTIME_WIRING = "blocked_unsafe_runtime_wiring"
    BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT = "blocked_unsafe_data_or_side_effect"
    BLOCKED_UNSAFE_TEXT_OR_CONTROLS = "blocked_unsafe_text_or_controls"
    BLOCKED_UNSAFE_SOURCE_MODEL = "blocked_unsafe_source_model"


FORBIDDEN_RUNTIME_ACTIVATION_CAPABILITIES: Tuple[str, ...] = (
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
    "runtime_copilot_decision_behavior",
)

REQUIRED_SAFE_RUNTIME_CONTRACT_LABELS: Tuple[str, ...] = (
    "advisory_role_label",
    "canonical_route_unchanged_label",
    "no_route_authority_label",
    "confidence_not_correctness_label",
    "non_training_feedback_label",
)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeActivationPolicy:
    """Policy for a future runtime visible read-only advisory panel."""

    activation_mode: ReadOnlyPanelRuntimeActivationMode = ReadOnlyPanelRuntimeActivationMode.CONTRACT_ONLY
    source_completion_handoff_id: str = PREVIOUS_COMPLETION_HANDOFF_ID
    require_phase8_panel_view_model_input: bool = True
    require_explicit_feature_flag: bool = True
    feature_flag_default_enabled: bool = False
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_view_model: bool = True
    require_route_invariant_runtime_mount: bool = True
    require_final_selection_invisible_runtime_mount: bool = True
    require_renderer_adapter_to_be_separate_future_contract: bool = True
    require_non_training_feedback_slot: bool = True
    allow_actual_runtime_activation_in_this_phase: bool = False
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
        _validate_policy_invariants(
            self,
            activation_mode_type=ReadOnlyPanelRuntimeActivationMode,
            previous_completion_handoff_id=PREVIOUS_COMPLETION_HANDOFF_ID,
        )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeActivationDecision:
    """Decision returned by the Phase 9 activation contract evaluator."""

    feature_id: str
    status: ReadOnlyPanelRuntimeActivationStatus
    accepted: bool
    activation_mode: ReadOnlyPanelRuntimeActivationMode
    future_runtime_panel_contract_ready: bool
    contract_only: bool
    actual_runtime_panel_activation_enabled: bool
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
    phase8_view_model_input_required: bool
    explicit_feature_flag_required: bool
    feature_flag_default_enabled: bool
    disable_noop_control_required: bool
    fail_open_on_missing_view_model_required: bool
    route_invariant_runtime_mount_required: bool
    final_selection_invisible_runtime_mount_required: bool
    renderer_adapter_separate_future_contract_required: bool
    non_training_feedback_slot_required: bool
    required_safe_labels: Tuple[str, ...]
    forbidden_capabilities: Tuple[str, ...]
    final_router_remains_authoritative: bool
    ml_advisory_signal_telemetry_only: bool
    critical_boundary_error_budget: int

    def __post_init__(self) -> None:
        _validate_decision_invariants(
            self,
            feature_id=FEATURE_ID,
            status_type=ReadOnlyPanelRuntimeActivationStatus,
            activation_mode_type=ReadOnlyPanelRuntimeActivationMode,
        )


def build_phase9_read_only_advisory_panel_runtime_activation_contract(
    policy: Optional[ReadOnlyAdvisoryPanelRuntimeActivationPolicy] = None,
    panel_view_model: Optional[ReadOnlyAdvisoryPanelViewModel] = None,
) -> ReadOnlyAdvisoryPanelRuntimeActivationDecision:
    """Build the default safe contract decision.

    The decision may mark a future runtime panel contract as ready, but it never
    enables actual runtime activation in this phase.
    """

    policy = policy or ReadOnlyAdvisoryPanelRuntimeActivationPolicy()
    status = ReadOnlyPanelRuntimeActivationStatus.ACCEPTED_CONTRACT_ONLY
    ready = False
    if policy.activation_mode is ReadOnlyPanelRuntimeActivationMode.FUTURE_READ_ONLY_RUNTIME_PANEL:
        status = ReadOnlyPanelRuntimeActivationStatus.ACCEPTED_FUTURE_READ_ONLY_RUNTIME_PANEL_CONTRACT
        ready = _view_model_is_safe(panel_view_model)
        if not ready:
            status = ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_SOURCE_MODEL
    return _decision(policy=policy, status=status, accepted=status.name.startswith("ACCEPTED"), ready=ready)


def evaluate_phase9_read_only_advisory_panel_runtime_activation_request(
    *,
    policy: Optional[ReadOnlyAdvisoryPanelRuntimeActivationPolicy] = None,
    requested_capabilities: Optional[Mapping[str, bool]] = None,
    panel_view_model: Optional[ReadOnlyAdvisoryPanelViewModel] = None,
) -> ReadOnlyAdvisoryPanelRuntimeActivationDecision:
    """Evaluate a proposed future runtime activation request.

    Unsafe requested capabilities are blocked. Safe future activation requests are
    accepted only as contract readiness; this function still does not mount a
    panel or wire UI.
    """

    policy = policy or ReadOnlyAdvisoryPanelRuntimeActivationPolicy()
    requested_capabilities = requested_capabilities or {}
    status = _status_for_requested_capabilities(
        requested_capabilities,
        ReadOnlyPanelRuntimeActivationStatus,
    )
    if status is not None:
        return _decision(policy=policy, status=status, accepted=False, ready=False)
    return build_phase9_read_only_advisory_panel_runtime_activation_contract(
        policy=policy,
        panel_view_model=panel_view_model,
    )


def build_phase9_read_only_panel_runtime_activation_contract_probe() -> ReadOnlyAdvisoryPanelRuntimeActivationDecision:
    """Build a safe future-activation contract probe for validation tests."""

    view_model = build_phase8_read_only_advisory_panel_ui_probe()
    policy = ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_mode=ReadOnlyPanelRuntimeActivationMode.FUTURE_READ_ONLY_RUNTIME_PANEL,
    )
    return evaluate_phase9_read_only_advisory_panel_runtime_activation_request(
        policy=policy,
        requested_capabilities={},
        panel_view_model=view_model,
    )


def _decision(
    *,
    policy: ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    status: ReadOnlyPanelRuntimeActivationStatus,
    accepted: bool,
    ready: bool,
) -> ReadOnlyAdvisoryPanelRuntimeActivationDecision:
    """Support decision behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelRuntimeActivationPolicy
        The policy value.
    status : ReadOnlyPanelRuntimeActivationStatus
        The status value.
    accepted : bool
        The accepted value.
    ready : bool
        The ready value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelRuntimeActivationDecision
        The read only advisory panel runtime activation decision result.
    """
    
    return ReadOnlyAdvisoryPanelRuntimeActivationDecision(
        feature_id=FEATURE_ID,
        status=status,
        accepted=accepted,
        activation_mode=policy.activation_mode,
        future_runtime_panel_contract_ready=ready,
        contract_only=True,
        actual_runtime_panel_activation_enabled=False,
        renderer_activation_enabled=False,
        mounted_panel_enabled=False,
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
        runtime_copilot_decision_behavior_enabled=False,
        phase8_view_model_input_required=policy.require_phase8_panel_view_model_input,
        explicit_feature_flag_required=policy.require_explicit_feature_flag,
        feature_flag_default_enabled=policy.feature_flag_default_enabled,
        disable_noop_control_required=policy.require_disable_noop_control,
        fail_open_on_missing_view_model_required=policy.require_fail_open_on_missing_view_model,
        route_invariant_runtime_mount_required=policy.require_route_invariant_runtime_mount,
        final_selection_invisible_runtime_mount_required=policy.require_final_selection_invisible_runtime_mount,
        renderer_adapter_separate_future_contract_required=policy.require_renderer_adapter_to_be_separate_future_contract,
        non_training_feedback_slot_required=policy.require_non_training_feedback_slot,
        required_safe_labels=REQUIRED_SAFE_RUNTIME_CONTRACT_LABELS,
        forbidden_capabilities=FORBIDDEN_RUNTIME_ACTIVATION_CAPABILITIES,
        final_router_remains_authoritative=True,
        ml_advisory_signal_telemetry_only=True,
        critical_boundary_error_budget=0,
    )


