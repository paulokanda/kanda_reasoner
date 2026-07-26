# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/guarded_advisory_surface_wiring_contract.py
"""Guarded Phase 7 advisory surface wiring contract.

Contract only. This module defines the safe shape for future automatic
router/app/UI use and future visible advisory panel logic. It does not
activate runtime UI, advisory panel wiring, provider calls, adapter
execution, persistence, router logic changes, router final selection
changes, or route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase7_guarded_advisory_surface_wiring_contract',
    'evaluate_phase7_guarded_advisory_surface_wiring_request',
    'GuardedAdvisorySurfaceWiringContract',
    'GuardedAdvisorySurfaceWiringDecision',
    'GuardedAdvisorySurfaceWiringPolicy',
    'SurfaceVisibilityMode',
]
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from .web_book_informed_surface_wiring_contract import (
    build_phase7_web_book_informed_surface_wiring_contract,
)


FEATURE_ID = "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_v1"
SOURCE_RESEARCH_FEATURE_ID = (
    "rss_ml_adv_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1"
)

REQUIRED_GAIN_CODES = (
    "authority_separation_final_router_invariant",
    "confusable_deputy_privilege_denial",
    "guardrail_adjacency_before_side_effects",
    "structured_typed_payload_no_free_text_route_advice",
    "explicit_uncertainty_status_role_and_scope_labeling",
    "user_control_disable_noop_and_non_training_feedback",
    "eval_first_gates_for_code_payload_model_and_ui_changes",
    "slo_error_budget_and_regression_budget_for_advisory_surface",
    "monitoring_readiness_without_persistence_or_privileged_reads",
    "latency_cost_and_availability_budget_before_provider_activation",
    "rollback_and_kill_switch_as_first_class_boundary_requirements",
    "modular_typed_interface_no_hidden_registry_or_global_state_coupling",
    "security_threat_model_for_prompt_injection_output_handling_disclosure_agency_supply_chain_dos",
    "route_influence_limited_to_future_deterministic_recheck_request_not_override",
)


class SurfaceVisibilityMode(str, Enum):
    """Visibility modes allowed by the contract definition only."""

    HIDDEN = "hidden"
    DEVELOPER_DEBUG_READ_ONLY = "developer_debug_read_only"
    FUTURE_PANEL_READ_ONLY = "future_panel_read_only"


@dataclass(frozen=True)
class GuardedAdvisorySurfaceWiringPolicy:
    """Contract policy for future advisory surface wiring."""

    surface_id: str
    source_research_feature_id: str
    allowed_visibility_modes: Tuple[SurfaceVisibilityMode, ...]
    required_gain_codes: Tuple[str, ...]
    contract_only: bool = True
    automatic_use_contract_defined: bool = True
    visible_panel_contract_defined: bool = True
    must_run_after_canonical_router_final_selection: bool = True
    requires_router_result_copy_unchanged: bool = True
    requires_already_computed_advisory_output: bool = True
    requires_guarded_display_payload: bool = True
    requires_typed_bounded_fields: bool = True
    requires_no_free_text_route_advice: bool = True
    requires_uncertainty_status_role_scope_labels: bool = True
    requires_disable_noop_control: bool = True
    requires_non_training_feedback_slot: bool = True
    requires_eval_first_gate_before_future_implementation: bool = True
    requires_slo_error_budget_before_activation: bool = True
    requires_latency_cost_availability_budget_before_provider_activation: bool = True
    requires_kill_switch_and_rollback: bool = True
    read_only: bool = True
    telemetry_only: bool = True
    route_invariant: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    real_ml_enabled: bool = False
    adapter_execution_enabled: bool = False
    candidate_execution_enabled: bool = False
    provider_calls_enabled: bool = False
    network_calls_enabled: bool = False
    api_keys_enabled: bool = False
    embeddings_enabled: bool = False
    vector_store_enabled: bool = False
    persistence_enabled: bool = False
    report_persistence_enabled: bool = False
    prompt_loading_enabled: bool = False
    prompt_library_read_enabled: bool = False
    prompt_registry_mutation_enabled: bool = False
    freeze_memory_read_enabled: bool = False
    freeze_memory_write_enabled: bool = False
    router_canon_read_enabled: bool = False
    runtime_shadow_mode_enabled: bool = False
    runtime_advisory_panel_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    runtime_telemetry_surface_wired: bool = False
    router_prompt_logic_modified: bool = False
    router_final_selection_modified: bool = False
    route_authority_enabled: bool = False
    advisory_rankings_enabled: bool = False
    free_text_route_advice_enabled: bool = False
    free_text_explanations_enabled: bool = False
    training_enabled: bool = False
    calibration_enabled: bool = False
    model_improvement_enabled: bool = False
    runtime_pilot_behavior_enabled: bool = False
    runtime_copilot_decision_behavior_enabled: bool = False
    critical_boundary_error_budget: int = 0

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("surface_id", self.surface_id)
        if self.source_research_feature_id != SOURCE_RESEARCH_FEATURE_ID:
            raise ValueError("source_research_feature_id must match web-and-book research flux")
        _require_tuple_of_enum(
            "allowed_visibility_modes",
            self.allowed_visibility_modes,
            SurfaceVisibilityMode,
        )
        _require_tuple_of_text("required_gain_codes", self.required_gain_codes)
        if tuple(self.required_gain_codes) != REQUIRED_GAIN_CODES:
            raise ValueError("required_gain_codes must exactly match the accepted web-and-book gains")
        for field_name in _required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")
        if self.critical_boundary_error_budget != 0:
            raise ValueError("critical_boundary_error_budget must remain zero")


@dataclass(frozen=True)
class GuardedAdvisorySurfaceWiringContract:
    """Immutable contract for future automatic use and visible surface wiring."""

    feature_id: str
    source_research_feature_id: str
    policy: GuardedAdvisorySurfaceWiringPolicy
    automatic_use_rule: str
    visible_surface_rule: str
    route_effect_rule: str
    required_future_implementation_tests: Tuple[str, ...]
    prohibited_attempts: Tuple[str, ...]
    research_gain_count: int

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 7 guarded surface wiring contract")
        if self.source_research_feature_id != SOURCE_RESEARCH_FEATURE_ID:
            raise ValueError("source_research_feature_id must match Phase 7 research flux")
        if not isinstance(self.policy, GuardedAdvisorySurfaceWiringPolicy):
            raise TypeError("policy must be GuardedAdvisorySurfaceWiringPolicy")
        _require_text("automatic_use_rule", self.automatic_use_rule)
        _require_text("visible_surface_rule", self.visible_surface_rule)
        _require_text("route_effect_rule", self.route_effect_rule)
        _require_tuple_of_text(
            "required_future_implementation_tests",
            self.required_future_implementation_tests,
        )
        _require_tuple_of_text("prohibited_attempts", self.prohibited_attempts)
        if self.research_gain_count != len(REQUIRED_GAIN_CODES):
            raise ValueError("research_gain_count must match required gains")


@dataclass(frozen=True)
class GuardedAdvisorySurfaceWiringDecision:
    """Decision for a proposed Phase 7 surface wiring request."""

    may_define_auto_use_contract: bool
    may_define_visible_panel_contract: bool
    may_activate_runtime_wiring: bool
    may_show_runtime_panel: bool
    may_affect_route_choice: bool
    required_next_step: str
    reason: str


def build_phase7_guarded_advisory_surface_wiring_contract(
) -> GuardedAdvisorySurfaceWiringContract:
    """Build the contract from the frozen web-and-book research flux."""

    research_contract = build_phase7_web_book_informed_surface_wiring_contract()
    if tuple(research_contract.gain_codes()) != REQUIRED_GAIN_CODES:
        raise ValueError("research gains do not match required guarded wiring gates")
    if research_contract.direct_route_authority_allowed:
        raise ValueError("source research contract must deny direct route authority")

    policy = GuardedAdvisorySurfaceWiringPolicy(
        surface_id="phase7_guarded_advisory_surface_wiring_contract_v1",
        source_research_feature_id=SOURCE_RESEARCH_FEATURE_ID,
        allowed_visibility_modes=(
            SurfaceVisibilityMode.HIDDEN,
            SurfaceVisibilityMode.DEVELOPER_DEBUG_READ_ONLY,
            SurfaceVisibilityMode.FUTURE_PANEL_READ_ONLY,
        ),
        required_gain_codes=REQUIRED_GAIN_CODES,
    )

    return GuardedAdvisorySurfaceWiringContract(
        feature_id=FEATURE_ID,
        source_research_feature_id=SOURCE_RESEARCH_FEATURE_ID,
        policy=policy,
        automatic_use_rule=(
            "Future implementation may call the advisory display path only after the canonical "
            "router has finalized its route, and must copy that route result unchanged."
        ),
        visible_surface_rule=(
            "Future panel may be read-only telemetry only, with bounded typed fields, "
            "uncertainty/status/role/scope labels, disable/no-op controls, non-training "
            "feedback, and no free-text route advice."
        ),
        route_effect_rule=(
            "Direct route choice effect remains blocked. Future work may only study a "
            "deterministic re-check request under a separate governed contract."
        ),
        required_future_implementation_tests=(
            "route_result_copied_unchanged",
            "final_selection_invisible",
            "no_runtime_panel_without_explicit_contract",
            "typed_payload_only_no_free_text_route_advice",
            "disable_noop_returns_no_surface",
            "guardrails_adjacent_to_side_effect_boundaries",
            "no_provider_network_persistence_or_privileged_reads",
            "kill_switch_and_rollback_available",
        ),
        prohibited_attempts=(
            "direct_route_override",
            "advisory_ranked_prompt_selection",
            "provider_backed_runtime_calls",
            "persistent_advisory_logs",
            "prompt_library_or_router_canon_reads",
            "runtime_copilot_decision_behavior",
        ),
        research_gain_count=len(research_contract.gain_codes()),
    )


def evaluate_phase7_guarded_advisory_surface_wiring_request(
    *,
    auto_use_after_router: bool,
    visible_panel: bool,
    activate_runtime_wiring: bool = False,
    affect_route_choice: bool = False,
    provider_backed: bool = False,
    persistent_logging: bool = False,
    ui_mutation: bool = False,
) -> GuardedAdvisorySurfaceWiringDecision:
    """Evaluate a proposed next-step request under the contract.

    This function does not wire runtime UI or call a router. It only classifies
    whether a future contract may define the requested shape.
    """

    if affect_route_choice:
        return GuardedAdvisorySurfaceWiringDecision(
            may_define_auto_use_contract=False,
            may_define_visible_panel_contract=False,
            may_activate_runtime_wiring=False,
            may_show_runtime_panel=False,
            may_affect_route_choice=False,
            required_next_step="separate_high_risk_deterministic_recheck_contract_required_not_direct_override",
            reason="Direct ML route influence is blocked; only deterministic re-check request logic may be studied later.",
        )

    if provider_backed:
        return GuardedAdvisorySurfaceWiringDecision(
            may_define_auto_use_contract=False,
            may_define_visible_panel_contract=False,
            may_activate_runtime_wiring=False,
            may_show_runtime_panel=False,
            may_affect_route_choice=False,
            required_next_step="provider_budgeted_adapter_boundary_required_before_any_activation",
            reason="Provider-backed behavior requires a separate latency/cost/availability/privacy/fallback budget contract.",
        )

    if persistent_logging:
        return GuardedAdvisorySurfaceWiringDecision(
            may_define_auto_use_contract=False,
            may_define_visible_panel_contract=False,
            may_activate_runtime_wiring=False,
            may_show_runtime_panel=False,
            may_affect_route_choice=False,
            required_next_step="privacy_bounded_monitoring_contract_required_before_any_persistence",
            reason="Persistence is blocked until a separate monitoring/privacy contract exists.",
        )

    if ui_mutation:
        return GuardedAdvisorySurfaceWiringDecision(
            may_define_auto_use_contract=False,
            may_define_visible_panel_contract=False,
            may_activate_runtime_wiring=False,
            may_show_runtime_panel=False,
            may_affect_route_choice=False,
            required_next_step="ui_mutation_contract_required_before_runtime_panel_or_surface_changes",
            reason="UI mutation is not allowed in this contract-only step.",
        )

    if activate_runtime_wiring:
        return GuardedAdvisorySurfaceWiringDecision(
            may_define_auto_use_contract=auto_use_after_router,
            may_define_visible_panel_contract=visible_panel,
            may_activate_runtime_wiring=False,
            may_show_runtime_panel=False,
            may_affect_route_choice=False,
            required_next_step="phase_7_surface_wiring_implementation_contract_and_review_gate_required",
            reason="This step defines wiring rules only; runtime activation requires a later implementation contract and review gate.",
        )

    if auto_use_after_router or visible_panel:
        return GuardedAdvisorySurfaceWiringDecision(
            may_define_auto_use_contract=auto_use_after_router,
            may_define_visible_panel_contract=visible_panel,
            may_activate_runtime_wiring=False,
            may_show_runtime_panel=False,
            may_affect_route_choice=False,
            required_next_step="phase_7_guarded_advisory_surface_wiring_contract_result_review_gate_v1",
            reason="Automatic use and visible panel can be defined only as route-invariant read-only telemetry contracts here.",
        )

    return GuardedAdvisorySurfaceWiringDecision(
        may_define_auto_use_contract=False,
        may_define_visible_panel_contract=False,
        may_activate_runtime_wiring=False,
        may_show_runtime_panel=False,
        may_affect_route_choice=False,
        required_next_step="no_surface_wiring_requested",
        reason="No automatic use or panel contract requested.",
    )


def _required_true_fields() -> Tuple[str, ...]:
    """Support required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "contract_only",
        "automatic_use_contract_defined",
        "visible_panel_contract_defined",
        "must_run_after_canonical_router_final_selection",
        "requires_router_result_copy_unchanged",
        "requires_already_computed_advisory_output",
        "requires_guarded_display_payload",
        "requires_typed_bounded_fields",
        "requires_no_free_text_route_advice",
        "requires_uncertainty_status_role_scope_labels",
        "requires_disable_noop_control",
        "requires_non_training_feedback_slot",
        "requires_eval_first_gate_before_future_implementation",
        "requires_slo_error_budget_before_activation",
        "requires_latency_cost_availability_budget_before_provider_activation",
        "requires_kill_switch_and_rollback",
        "read_only",
        "telemetry_only",
        "route_invariant",
        "in_memory_only",
        "bounded",
        "fail_open",
        "removable_noop",
        "final_selection_invisible",
        "non_authoritative",
    )


def _forbidden_true_fields() -> Tuple[str, ...]:
    """Support forbidden true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "real_ml_enabled",
        "adapter_execution_enabled",
        "candidate_execution_enabled",
        "provider_calls_enabled",
        "network_calls_enabled",
        "api_keys_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "report_persistence_enabled",
        "prompt_loading_enabled",
        "prompt_library_read_enabled",
        "prompt_registry_mutation_enabled",
        "freeze_memory_read_enabled",
        "freeze_memory_write_enabled",
        "router_canon_read_enabled",
        "runtime_shadow_mode_enabled",
        "runtime_advisory_panel_enabled",
        "runtime_ui_mutation_enabled",
        "runtime_telemetry_surface_wired",
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_route_advice_enabled",
        "free_text_explanations_enabled",
        "training_enabled",
        "calibration_enabled",
        "model_improvement_enabled",
        "runtime_pilot_behavior_enabled",
        "runtime_copilot_decision_behavior_enabled",
    )


def _require_text(name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str):
        raise TypeError(name + " must be str")
    if not value.strip():
        raise ValueError(name + " must not be empty")


def _require_tuple_of_text(name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple of text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[str, ...]
        The input value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(name + " must be tuple")
    for item in value:
        _require_text(name + " item", item)


def _require_tuple_of_enum(name: str, value: Tuple[Enum, ...], enum_type: type) -> None:
    """Support require tuple of enum behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[Enum, ...]
        The input value.
    enum_type : type
        The enum type value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(name + " must be tuple")
    for item in value:
        if not isinstance(item, enum_type):
            raise TypeError(name + " contains invalid enum")
