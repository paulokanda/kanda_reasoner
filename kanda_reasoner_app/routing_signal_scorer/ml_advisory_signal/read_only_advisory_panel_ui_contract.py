# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_ui_contract.py
"""Phase 8 read-only advisory panel UI contract.

Contract only. This module defines the safe UI contract for a future visible
Copilot/advisory panel. It does not render UI, mutate UI, attach to runtime
screens, call the router, call an advisor, execute adapters, persist data, or
influence route choice.
"""

from __future__ import annotations


__all__ = [
    'build_phase8_read_only_advisory_panel_ui_contract',
    'evaluate_phase8_read_only_advisory_panel_ui_request',
    'ReadOnlyAdvisoryPanelUIContractDecision',
    'ReadOnlyAdvisoryPanelUIContractPolicy',
    'ReadOnlyPanelContractStatus',
    'ReadOnlyPanelVisibilityMode',
]
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Tuple


FEATURE_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_v1"
PREVIOUS_COMPLETION_HANDOFF_ID = (
    "rss_ml_adv_phase7_read_only_advisory_surface_wiring_completion_handoff_v1"
)


class ReadOnlyPanelVisibilityMode(str, Enum):
    """Contract-level visibility modes for a future panel."""

    CONTRACT_ONLY = "contract_only"
    FUTURE_READ_ONLY_PANEL = "future_read_only_panel"
    BLOCKED = "blocked"


class ReadOnlyPanelContractStatus(str, Enum):
    """Outcome of evaluating whether a future panel spec is safe."""

    ACCEPTED_CONTRACT_ONLY = "accepted_contract_only"
    BLOCKED_UNSAFE_AUTHORITY = "blocked_unsafe_authority"
    BLOCKED_UNSAFE_UI_MUTATION = "blocked_unsafe_ui_mutation"
    BLOCKED_UNSAFE_DATA_SOURCE = "blocked_unsafe_data_source"
    BLOCKED_UNSAFE_TEXT_OR_RANKING = "blocked_unsafe_text_or_ranking"


ALLOWED_PANEL_SECTIONS: Tuple[str, ...] = (
    "advisory_role_label",
    "canonical_route_unchanged_label",
    "advisory_status",
    "boundary_status",
    "confidence_band",
    "reason_codes_bounded",
    "guardrail_state",
    "disabled_noop_state",
    "non_training_feedback_slot",
)

FORBIDDEN_PANEL_CAPABILITIES: Tuple[str, ...] = (
    "route_override_button",
    "use_ml_route_button",
    "best_route_claim",
    "prompt_ranking",
    "free_text_route_advice",
    "free_text_explanation",
    "final_selection_hook",
    "prompt_selection_hook",
    "router_call",
    "advisor_call",
    "adapter_execution",
    "provider_call",
    "persistence_write",
    "runtime_ui_mutation",
    "runtime_panel_activation",
    "route_authority",
)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelUIContractPolicy:
    """Policy for a future visible read-only advisory panel."""

    visibility_mode: ReadOnlyPanelVisibilityMode = ReadOnlyPanelVisibilityMode.CONTRACT_ONLY
    require_surface_envelope_input: bool = True
    require_canonical_route_unchanged_label: bool = True
    require_advisory_role_label: bool = True
    require_uncertainty_status_role_scope_labels: bool = True
    require_disable_noop_control: bool = True
    require_non_training_feedback_slot: bool = True
    allow_free_text_route_advice: bool = False
    allow_free_text_explanations: bool = False
    allow_advisory_rankings: bool = False
    allow_route_override: bool = False
    allow_runtime_panel_activation: bool = False
    allow_runtime_ui_mutation: bool = False
    allow_runtime_telemetry_surface_wiring: bool = False
    allow_router_calls: bool = False
    allow_advisor_calls: bool = False
    allow_adapter_execution: bool = False
    allow_provider_calls: bool = False
    allow_persistence: bool = False
    allow_route_influence: bool = False
    allow_route_authority: bool = False


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelUIContractDecision:
    """Decision returned by the Phase 8 contract evaluator."""

    feature_id: str
    status: ReadOnlyPanelContractStatus
    accepted: bool
    visibility_mode: ReadOnlyPanelVisibilityMode
    allowed_sections: Tuple[str, ...]
    forbidden_capabilities: Tuple[str, ...]
    panel_contract_only: bool
    runtime_panel_activation_enabled: bool
    runtime_ui_mutation_enabled: bool
    runtime_telemetry_surface_wiring_enabled: bool
    route_authority_enabled: bool
    route_influence_enabled: bool
    router_calls_enabled: bool
    advisor_calls_enabled: bool
    adapter_execution_enabled: bool
    provider_calls_enabled: bool
    persistence_enabled: bool
    final_router_remains_authoritative: bool
    canonical_route_unchanged_label_required: bool
    advisory_role_label_required: bool
    non_training_feedback_slot_required: bool
    reason: str


def build_phase8_read_only_advisory_panel_ui_contract(
    policy: ReadOnlyAdvisoryPanelUIContractPolicy | None = None,
) -> ReadOnlyAdvisoryPanelUIContractDecision:
    """Build the default contract-only approval decision.

    The returned decision is intentionally non-runtime: it describes the safe
    panel contract only. It does not activate a panel or wire a UI surface.
    """

    policy = policy or ReadOnlyAdvisoryPanelUIContractPolicy()
    return evaluate_phase8_read_only_advisory_panel_ui_request(policy=policy)


def evaluate_phase8_read_only_advisory_panel_ui_request(
    *,
    policy: ReadOnlyAdvisoryPanelUIContractPolicy,
    requested_capabilities: Mapping[str, bool] | None = None,
) -> ReadOnlyAdvisoryPanelUIContractDecision:
    """Evaluate whether a future panel request stays inside the safe contract."""

    requested_capabilities = requested_capabilities or {}

    if requested_capabilities.get("runtime_ui_mutation", False) or policy.allow_runtime_ui_mutation:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_UI_MUTATION, policy, "runtime UI mutation is forbidden")
    if requested_capabilities.get("runtime_panel_activation", False) or policy.allow_runtime_panel_activation:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_UI_MUTATION, policy, "runtime panel activation is not allowed by this contract")
    if requested_capabilities.get("runtime_telemetry_surface_wiring", False) or policy.allow_runtime_telemetry_surface_wiring:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_UI_MUTATION, policy, "runtime telemetry surface wiring is not allowed by this contract")
    if requested_capabilities.get("route_authority", False) or policy.allow_route_authority:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_AUTHORITY, policy, "route authority is forbidden")
    if requested_capabilities.get("route_influence", False) or policy.allow_route_influence:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_AUTHORITY, policy, "route influence is forbidden")
    if requested_capabilities.get("router_call", False) or policy.allow_router_calls:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE, policy, "panel must not call router")
    if requested_capabilities.get("advisor_call", False) or policy.allow_advisor_calls:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE, policy, "panel must not call advisor")
    if requested_capabilities.get("adapter_execution", False) or policy.allow_adapter_execution:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE, policy, "adapter execution is forbidden")
    if requested_capabilities.get("provider_call", False) or policy.allow_provider_calls:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE, policy, "provider calls are forbidden")
    if requested_capabilities.get("persistence", False) or policy.allow_persistence:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_DATA_SOURCE, policy, "persistence is forbidden")
    if requested_capabilities.get("free_text_route_advice", False) or policy.allow_free_text_route_advice:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_TEXT_OR_RANKING, policy, "free-text route advice is forbidden")
    if requested_capabilities.get("free_text_explanations", False) or policy.allow_free_text_explanations:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_TEXT_OR_RANKING, policy, "free-text explanations are forbidden in this UI contract")
    if requested_capabilities.get("advisory_rankings", False) or policy.allow_advisory_rankings:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_TEXT_OR_RANKING, policy, "advisory rankings are forbidden")
    if requested_capabilities.get("route_override", False) or policy.allow_route_override:
        return _blocked(ReadOnlyPanelContractStatus.BLOCKED_UNSAFE_AUTHORITY, policy, "route override is forbidden")

    return ReadOnlyAdvisoryPanelUIContractDecision(
        feature_id=FEATURE_ID,
        status=ReadOnlyPanelContractStatus.ACCEPTED_CONTRACT_ONLY,
        accepted=True,
        visibility_mode=policy.visibility_mode,
        allowed_sections=ALLOWED_PANEL_SECTIONS,
        forbidden_capabilities=FORBIDDEN_PANEL_CAPABILITIES,
        panel_contract_only=True,
        runtime_panel_activation_enabled=False,
        runtime_ui_mutation_enabled=False,
        runtime_telemetry_surface_wiring_enabled=False,
        route_authority_enabled=False,
        route_influence_enabled=False,
        router_calls_enabled=False,
        advisor_calls_enabled=False,
        adapter_execution_enabled=False,
        provider_calls_enabled=False,
        persistence_enabled=False,
        final_router_remains_authoritative=True,
        canonical_route_unchanged_label_required=policy.require_canonical_route_unchanged_label,
        advisory_role_label_required=policy.require_advisory_role_label,
        non_training_feedback_slot_required=policy.require_non_training_feedback_slot,
        reason="accepted as contract-only read-only advisory panel UI boundary",
    )


def _blocked(
    status: ReadOnlyPanelContractStatus,
    policy: ReadOnlyAdvisoryPanelUIContractPolicy,
    reason: str,
) -> ReadOnlyAdvisoryPanelUIContractDecision:
    """Support blocked behavior.
    
    Parameters
    ----------
    status : ReadOnlyPanelContractStatus
        The status value.
    policy : ReadOnlyAdvisoryPanelUIContractPolicy
        The policy value.
    reason : str
        The reason value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelUIContractDecision
        The read only advisory panel uicontract decision result.
    """
    
    return ReadOnlyAdvisoryPanelUIContractDecision(
        feature_id=FEATURE_ID,
        status=status,
        accepted=False,
        visibility_mode=ReadOnlyPanelVisibilityMode.BLOCKED,
        allowed_sections=ALLOWED_PANEL_SECTIONS,
        forbidden_capabilities=FORBIDDEN_PANEL_CAPABILITIES,
        panel_contract_only=True,
        runtime_panel_activation_enabled=False,
        runtime_ui_mutation_enabled=False,
        runtime_telemetry_surface_wiring_enabled=False,
        route_authority_enabled=False,
        route_influence_enabled=False,
        router_calls_enabled=False,
        advisor_calls_enabled=False,
        adapter_execution_enabled=False,
        provider_calls_enabled=False,
        persistence_enabled=False,
        final_router_remains_authoritative=True,
        canonical_route_unchanged_label_required=policy.require_canonical_route_unchanged_label,
        advisory_role_label_required=policy.require_advisory_role_label,
        non_training_feedback_slot_required=policy.require_non_training_feedback_slot,
        reason=reason,
    )
