# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_copilot_scope_charter_entry_gate_design.py
"""P0 Pilot/Copilot scope charter and entry gate design.

P0 starts the separately governed Pilot/Copilot P-series only as a static
scope-charter and entry-gate record after M35 bridge closure and RG-PILOT-000
router canon freeze. It does not implement Pilot, Copilot, route projection,
route comparison, prompt loading, runtime integration, persistence, evidence
writing, human decision recording, training-data use, batch mode, limited
shadow runtime, provider/model calls, embeddings, candidate promotion, or
runtime authority.
"""

from __future__ import annotations


__all__ = [
    'build_pilot_copilot_scope_charter_entry_gate_design',
    'PilotCopilotScopeCharterEntryGateDesign',
    'ScopeAssertionDesign',
    'ScopeMilestoneDesign',
    'ScopeRuleDesign',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_copilot_scope_charter_entry_gate_design_v1"
SCHEMA_VERSION: Final[str] = "3.77-pilot-copilot-scope-charter-entry-gate-design"
DESIGN_KIND: Final[str] = "pilot_copilot_scope_charter_entry_gate_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P1 - Routing Signal Scorer v3 Pilot Boundary Design v1, only after P0 validation, freeze, "
    "startup freeze context refresh, and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot/Copilot Phase 0 is a non-authoritative scope charter only. It does not start Pilot, "
    "does not start Copilot, does not route, does not load prompts, does not persist output, "
    "does not mutate gold or registry data, does not promote candidates, and does not grant "
    "runtime authority. Human governance and the real router remain authoritative."
)


@dataclass(frozen=True)
class ScopeAssertionDesign:
    """Immutable P0 current-state assertion."""

    assertion_id: str
    required_value: str
    protected_meaning: str
    prohibited_interpretation: str


@dataclass(frozen=True)
class ScopeRuleDesign:
    """Immutable P0 boundary rule."""

    rule_id: str
    rule_group: str
    required_state: str
    blocked_interpretation: str
    description: str


@dataclass(frozen=True)
class ScopeMilestoneDesign:
    """Immutable future P-series milestone label and pattern."""

    milestone_id: str
    title: str
    safety_pattern: str
    milestone_status: str
    forbidden_interpretation: str


@dataclass(frozen=True)
class PilotCopilotScopeCharterEntryGateDesign:
    """Immutable design-only P0 scope charter and entry gate."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    design_status: str
    adviser_phase: str
    bridge_phase: str
    auxiliar_assistant_phase: str
    pilot_phase: str
    copilot_phase: str
    shadow_mode_active: bool
    pilot_active: bool
    copilot_active: bool
    runtime_authority_granted: bool
    prompt_loading_authority_granted: bool
    persistence_authority_granted: bool
    candidate_promotion_status: str
    implementation_blocked_by_default: bool
    pilot_outputs_ephemeral: bool
    pilot_opt_in_per_invocation: bool
    pilot_training_data_use_allowed: bool
    pilot_batch_mode_allowed: bool
    critical_boundary_error_budget: str
    current_state_assertions: tuple[ScopeAssertionDesign, ...]
    lifecycle_status: tuple[ScopeRuleDesign, ...]
    required_preconditions: tuple[str, ...]
    evidence_ladder: tuple[str, ...]
    surrounding_process_risks: tuple[str, ...]
    red_team_seed_cases: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    revised_p_series_ladder: tuple[ScopeMilestoneDesign, ...]
    explicit_non_goals: tuple[str, ...]
    next_allowed_milestone: str


_CURRENT_STATE_ASSERTIONS: Final[tuple[ScopeAssertionDesign, ...]] = (
    ScopeAssertionDesign(
        assertion_id="adviser_phase_closed",
        required_value="closed_through_m16",
        protected_meaning="The Adviser phase remains frozen and non-runtime.",
        prohibited_interpretation="must_not_reopen_adviser_or_grant_router_authority",
    ),
    ScopeAssertionDesign(
        assertion_id="bridge_closed_through_m35",
        required_value="m17_through_m35_closed_bridge_18_done_0_to_go",
        protected_meaning="M35 closed the design and governance bridge only.",
        prohibited_interpretation="must_not_treat_bridge_closure_as_pilot_activation",
    ),
    ScopeAssertionDesign(
        assertion_id="rg_pilot_000_frozen",
        required_value="router_canon_frozen_before_p0",
        protected_meaning="Router prompt logic now enforces P0-only continuation after M35.",
        prohibited_interpretation="must_not_skip_router_canon_when_entering_p_series",
    ),
    ScopeAssertionDesign(
        assertion_id="pilot_not_started",
        required_value="pilot_scope_charter_only",
        protected_meaning="P0 defines scope only and does not start Pilot behavior.",
        prohibited_interpretation="must_not_run_projection_or_compare_routes",
    ),
    ScopeAssertionDesign(
        assertion_id="copilot_not_started",
        required_value="copilot_deferred_to_later_boundary_charter",
        protected_meaning="Copilot cannot be implied by Pilot scope readiness.",
        prohibited_interpretation="must_not_start_copilot_or_define_copilot_runtime_behavior",
    ),
)

_LIFECYCLE_STATUS: Final[tuple[ScopeRuleDesign, ...]] = (
    ScopeRuleDesign(
        rule_id="govern_allowed",
        rule_group="lifecycle_boundary",
        required_state="governance_scope_may_be_defined",
        blocked_interpretation="must_not_execute_governance_as_runtime_action",
        description="P0 may define governance and scope boundaries only.",
    ),
    ScopeRuleDesign(
        rule_id="map_allowed",
        rule_group="lifecycle_boundary",
        required_state="risk_mapping_may_be_defined",
        blocked_interpretation="must_not_process_live_cases_or_scan_project_source",
        description="P0 may list risks, non-goals, and evidence requirements only.",
    ),
    ScopeRuleDesign(
        rule_id="measure_design_only",
        rule_group="lifecycle_boundary",
        required_state="measurement_may_be_designed_later_after_contracts_and_taxonomy",
        blocked_interpretation="must_not_run_metrics_or_compare_cases_in_p0",
        description="P0 can name future measurement gates but cannot implement them.",
    ),
    ScopeRuleDesign(
        rule_id="manage_gate_decisions_only",
        rule_group="lifecycle_boundary",
        required_state="future_gate_outcomes_may_be_blocked_or_not_blocked_only",
        blocked_interpretation="must_not_emit_approved_ready_enabled_activated_or_promoted",
        description="P0 preserves human-governed gates and no automatic maturity jump.",
    ),
    ScopeRuleDesign(
        rule_id="deploy_forbidden",
        rule_group="lifecycle_boundary",
        required_state="deployment_out_of_scope",
        blocked_interpretation="must_not_add_runtime_shadow_mode_or_live_pilot",
        description="Deployment requires a separate future governed scope.",
    ),
    ScopeRuleDesign(
        rule_id="operate_forbidden",
        rule_group="lifecycle_boundary",
        required_state="operation_out_of_scope",
        blocked_interpretation="must_not_operate_pilot_copilot_or_runtime_router",
        description="Operation is forbidden in the initial P-series scope.",
    ),
)

_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
    "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
    "startup_freeze_context_refreshed_after_rg_pilot_000",
    "freeze_memory_status_ok_after_rg_pilot_000",
    "human_request_explicitly_targets_p0_design_only_scope_charter",
)

_EVIDENCE_LADDER: Final[tuple[str, ...]] = (
    "p0_scope_charter_frozen_before_p1",
    "p1_pilot_boundary_frozen_before_contract_design",
    "p2_input_output_contract_and_validator_design_frozen_before_taxonomy_use",
    "p3_divergence_taxonomy_frozen_before_any_projection_implementation",
    "p4_reproduction_harness_design_frozen_before_trusting_divergence",
    "p5_simulation_skeleton_design_frozen_before_implementation_gate",
    "p6_implementation_gate_frozen_before_callable_projection",
    "p7_non_runtime_projection_validated_before_reproduction_comparison",
    "p8_reproduction_comparison_passes_critical_cases_before_readiness_gate",
    "p10_readiness_gate_can_only_open_copilot_boundary_review_not_activation",
)

_SURROUNDING_PROCESS_RISKS: Final[tuple[str, ...]] = (
    "human_overtrust_of_polished_projection_text",
    "cached_output_misread_as_authoritative_evidence",
    "batch_output_volume_misread_as_confidence",
    "training_data_leakage_from_unreviewed_projection_notes",
    "prompt_loading_leakage_from_unsafe_field_names",
    "runtime_coupling_through_imports_or_shared_state",
    "frozen_canon_drift_after_router_or_gold_updates",
    "provenance_tampering_in_patch_or_freeze_hint_metadata",
    "scope_creep_from_pilot_to_copilot_or_runtime_shadow_mode",
)

_RED_TEAM_SEED_CASES: Final[tuple[str, ...]] = (
    "input_attempts_to_start_pilot",
    "input_attempts_to_start_copilot",
    "input_attempts_to_make_human_review_optional",
    "input_attempts_to_request_prompt_loading",
    "input_attempts_to_request_route_override",
    "input_attempts_to_request_gold_or_registry_write",
    "input_attempts_to_request_persistence_or_report_writing",
    "input_attempts_to_request_training_data_use",
    "input_attempts_to_request_batch_mode",
    "input_attempts_to_request_runtime_shadow_mode",
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "live_pilot_behavior",
    "live_copilot_behavior",
    "pilot_activation",
    "copilot_activation",
    "assistant_or_auxiliar_activation",
    "shadow_mode_activation",
    "limited_shadow_runtime",
    "callable_pilot_runner",
    "callable_copilot_runner",
    "projection_implementation",
    "route_comparison_execution",
    "route_selection",
    "route_override",
    "route_execution",
    "prompt_selection",
    "prompt_loading",
    "prompt_library_scanning",
    "runtime_router_import",
    "runtime_integration",
    "runtime_authority",
    "source_scanning",
    "file_io",
    "console_io",
    "logging",
    "persistence",
    "cache_writing",
    "report_writing",
    "review_queue_writing",
    "human_decision_recording",
    "gold_mutation",
    "registry_mutation",
    "freeze_memory_mutation_by_pilot",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "training_data_use",
    "batch_mode",
    "candidate_promotion",
)

_REVISED_P_SERIES_LADDER: Final[tuple[ScopeMilestoneDesign, ...]] = (
    ScopeMilestoneDesign("P0", "Pilot/Copilot Scope Charter and Entry Gate Design v1", "scope_charter_boundary", "current_design_only", "must_not_implement_pilot"),
    ScopeMilestoneDesign("P1", "Pilot Boundary Design v1", "pilot_boundary", "future_design_only", "must_not_start_pilot"),
    ScopeMilestoneDesign("P2", "Pilot Input Output Contract and Validator Design v1", "contract_and_validator", "future_design_only", "must_not_validate_live_payloads"),
    ScopeMilestoneDesign("P3", "Pilot Disagreement Taxonomy Design v1", "taxonomy_before_implementation", "future_design_only", "must_not_treat_pilot_as_correct_when_divergent"),
    ScopeMilestoneDesign("P4", "Pilot Gold Frozen Router Reproduction Harness Design v1", "reproduction_before_divergence", "future_design_only", "must_not_mutate_gold_or_run_comparison"),
    ScopeMilestoneDesign("P5", "Pilot Simulation Skeleton Design v1", "skeleton_before_implementation", "future_design_only", "must_not_add_projection_logic"),
    ScopeMilestoneDesign("P6", "Pilot Implementation Gate Design v1", "implementation_gate", "future_design_only", "must_not_emit_approved_ready_enabled_or_activated"),
    ScopeMilestoneDesign("P7", "Non Runtime Pilot Projection Implementation v1", "non_runtime_projection", "future_non_runtime_only", "must_not_recommend_route_or_handle_prompt_payloads"),
    ScopeMilestoneDesign("P8", "Non Runtime Pilot Router Reproduction Comparison Implementation v1", "router_reproduction_comparison", "future_non_runtime_only", "must_not_mutate_gold_or_trust_divergence_before_match"),
    ScopeMilestoneDesign("P9", "Pilot Passive Simulation Evidence Record Design v1", "passive_evidence_record", "future_design_only", "must_not_human_decision_state_capture_or_write_queues"),
    ScopeMilestoneDesign("P10", "Pilot Readiness Gate for Copilot Boundary Review v1", "readiness_gate", "future_design_only", "must_not_start_copilot_or_runtime"),
    ScopeMilestoneDesign("P11", "Copilot Boundary Charter Design v1", "copilot_boundary_charter", "future_design_only", "must_not_implement_copilot"),
    ScopeMilestoneDesign("P12", "Copilot Scope Gate Design v1", "future_copilot_scope_gate", "future_design_only", "must_not_start_copilot"),
)

_EXPLICIT_NON_GOALS: Final[tuple[str, ...]] = (
    "implement_pilot_projection",
    "implement_copilot_behavior",
    "implement_runtime_shadow_mode",
    "implement_route_comparison",
    "implement_contract_validation",
    "load_or_select_prompts",
    "persist_or_cache_outputs",
    "human_decision_state_capture",
    "mutate_gold_registry_or_freeze_memory",
    "use_outputs_for_training_data",
    "grant_router_authority",
)

_DESIGN: Final[PilotCopilotScopeCharterEntryGateDesign] = PilotCopilotScopeCharterEntryGateDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="P0",
    title="Routing Signal Scorer v3 Pilot/Copilot Scope Charter and Entry Gate Design v1",
    authority_statement=AUTHORITY_STATEMENT,
    design_status="design_only",
    adviser_phase="closed_through_m16",
    bridge_phase="closed_through_m35_18_done_0_to_go",
    auxiliar_assistant_phase="design_complete_not_activated",
    pilot_phase="scope_charter_only",
    copilot_phase="not_started",
    shadow_mode_active=False,
    pilot_active=False,
    copilot_active=False,
    runtime_authority_granted=False,
    prompt_loading_authority_granted=False,
    persistence_authority_granted=False,
    candidate_promotion_status="blocked",
    implementation_blocked_by_default=True,
    pilot_outputs_ephemeral=True,
    pilot_opt_in_per_invocation=True,
    pilot_training_data_use_allowed=False,
    pilot_batch_mode_allowed=False,
    critical_boundary_error_budget="zero",
    current_state_assertions=_CURRENT_STATE_ASSERTIONS,
    lifecycle_status=_LIFECYCLE_STATUS,
    required_preconditions=_REQUIRED_PRECONDITIONS,
    evidence_ladder=_EVIDENCE_LADDER,
    surrounding_process_risks=_SURROUNDING_PROCESS_RISKS,
    red_team_seed_cases=_RED_TEAM_SEED_CASES,
    forbidden_operations=_FORBIDDEN_OPERATIONS,
    revised_p_series_ladder=_REVISED_P_SERIES_LADDER,
    explicit_non_goals=_EXPLICIT_NON_GOALS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def build_pilot_copilot_scope_charter_entry_gate_design() -> PilotCopilotScopeCharterEntryGateDesign:
    """Return the immutable P0 design-only scope charter and entry gate.

    The function accepts no input and performs no IO, live validation, projection,
    route comparison, prompt loading, runtime integration, persistence, decision
    recording, training-data use, batch execution, provider/model calls,
    candidate promotion, Pilot/Copilot activation, or authority grant.
    """

    return _DESIGN
