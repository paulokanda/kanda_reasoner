# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_boundary_design.py
"""P1 Pilot boundary design.

P1 defines the immutable design-only boundary for what a future Pilot may become
after P0 scope-charter freeze. It does not start Pilot, implement projection,
execute comparison, select or load prompts, integrate runtime routing, persist
records, record human decisions, use outputs for training data, run batch mode,
activate Copilot, start limited shadow runtime, call providers, use embeddings,
promote candidates, or grant authority.
"""

from __future__ import annotations


__all__ = [
    'build_pilot_boundary_design',
    'PilotBoundaryDesign',
    'PilotBoundaryEvidenceRuleDesign',
    'PilotBoundaryRoleDesign',
    'PilotBoundaryRuleDesign',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_boundary_design_v1"
SCHEMA_VERSION: Final[str] = "3.78-pilot-boundary-design"
DESIGN_KIND: Final[str] = "pilot_boundary_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P2 - Routing Signal Scorer v3 Pilot Input Output Contract and Validator Design v1, only after "
    "P1 validation, freeze, startup freeze context refresh, and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot Boundary Design v1 describes future Pilot role limits only. It does not start Pilot, "
    "does not implement projection, does not compare routes, does not load prompts, does not "
    "persist output, does not use output as training data, does not run batch mode, does not "
    "activate Copilot or limited shadow runtime, and does not grant runtime authority. Human "
    "governance and the real router remain authoritative."
)


@dataclass(frozen=True)
class PilotBoundaryRoleDesign:
    """Immutable description of one possible later Pilot role limit."""

    role_id: str
    role_scope: str
    permitted_future_use: str
    required_prior_gate: str
    prohibited_interpretation: str
    description: str


@dataclass(frozen=True)
class PilotBoundaryRuleDesign:
    """Immutable description of one Pilot boundary rule."""

    rule_id: str
    boundary_group: str
    required_state: str
    blocked_interpretation: str
    description: str


@dataclass(frozen=True)
class PilotBoundaryEvidenceRuleDesign:
    """Immutable description of one evidence constraint before later Pilot work."""

    evidence_rule_id: str
    required_before: str
    required_evidence: str
    blocked_progression: str
    description: str


@dataclass(frozen=True)
class PilotBoundaryDesign:
    """Immutable design-only P1 Pilot boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    design_status: str
    pilot_status: str
    copilot_status: str
    projection_status: str
    runtime_authority_status: str
    prompt_loading_authority_status: str
    persistence_authority_status: str
    training_data_use_status: str
    batch_mode_status: str
    limited_shadow_runtime_status: str
    human_review_status: str
    required_preconditions: tuple[str, ...]
    allowed_future_pilot_roles: tuple[PilotBoundaryRoleDesign, ...]
    hard_blocked_authority_rules: tuple[PilotBoundaryRuleDesign, ...]
    evidence_constraints: tuple[PilotBoundaryEvidenceRuleDesign, ...]
    pilot_boundary_invariants: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    safe_future_contract_language: tuple[str, ...]
    unsafe_contract_language_policy: tuple[str, ...]
    next_allowed_milestone: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
    "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
    "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
    "startup_freeze_context_refreshed_after_p0",
    "freeze_memory_status_ok_after_p0",
    "human_request_explicitly_targets_p1_design_only_pilot_boundary",
)

_ALLOWED_FUTURE_PILOT_ROLES: Final[tuple[PilotBoundaryRoleDesign, ...]] = (
    PilotBoundaryRoleDesign(
        role_id="future_descriptive_projection_analyst",
        role_scope="non_authoritative_case_pattern_projection_only",
        permitted_future_use="may_later_describe_how_frozen_canon_constraints_appear_to_classify_caller_supplied_case_summaries",
        required_prior_gate="p6_implementation_gate_frozen_before_any_callable_projection",
        prohibited_interpretation="must_not_recommend_select_override_or_perform_route_execution",
        description="A later Pilot may only describe a projection after contracts, taxonomy, skeleton, and implementation gate are frozen.",
    ),
    PilotBoundaryRoleDesign(
        role_id="future_frozen_router_reproduction_candidate",
        role_scope="caller_supplied_reproduction_check_only",
        permitted_future_use="may_later_be_compared_against_caller_supplied_frozen_router_or_canon_outcomes",
        required_prior_gate="p4_reproduction_harness_design_then_p8_comparison_implementation",
        prohibited_interpretation="must_not_trust_divergence_before_reproduction_success",
        description="Pilot must first match critical frozen outcomes before divergence evidence can be trusted.",
    ),
    PilotBoundaryRoleDesign(
        role_id="future_boundary_flag_explainer",
        role_scope="human_review_boundary_flag_summary_only",
        permitted_future_use="may_later_explain_caller_supplied_boundary_flags_for_human_review",
        required_prior_gate="p2_contract_and_validator_design_frozen_before_field_use",
        prohibited_interpretation="must_not_load_or_select_prompts_or_inspect_prompt_library_state",
        description="Boundary flag explanations remain non-authoritative and cannot become prompt loading.",
    ),
    PilotBoundaryRoleDesign(
        role_id="future_in_memory_review_note_preparer",
        role_scope="ephemeral_human_review_support_note_only",
        permitted_future_use="may_later_prepare_ephemeral_in_memory_notes_for_human_review",
        required_prior_gate="p9_passive_simulation_evidence_record_design_frozen_before_evidence_notes",
        prohibited_interpretation="must_not_capture_human_decisions_write_queues_or_store_reports",
        description="Human-review support must not become approval, decision recording, or persistence.",
    ),
)

_HARD_BLOCKED_AUTHORITY_RULES: Final[tuple[PilotBoundaryRuleDesign, ...]] = (
    PilotBoundaryRuleDesign(
        rule_id="pilot_is_not_active",
        boundary_group="activation_boundary",
        required_state="pilot_not_started_design_boundary_only",
        blocked_interpretation="must_not_start_run_enable_or_make_pilot_active",
        description="P1 defines future Pilot limits only and cannot start Pilot behavior.",
    ),
    PilotBoundaryRuleDesign(
        rule_id="pilot_is_not_copilot",
        boundary_group="copilot_boundary",
        required_state="copilot_not_started_and_deferred",
        blocked_interpretation="must_not_define_or_make_copilot_active_inside_pilot_boundary",
        description="Copilot remains deferred to P11/P12 after Pilot readiness gates.",
    ),
    PilotBoundaryRuleDesign(
        rule_id="pilot_is_not_router_authority",
        boundary_group="runtime_boundary",
        required_state="router_authority_not_granted",
        blocked_interpretation="must_not_select_override_or_perform_route_execution",
        description="The real router remains authoritative and receives no delegated authority from P1.",
    ),
    PilotBoundaryRuleDesign(
        rule_id="pilot_is_not_prompt_loader",
        boundary_group="prompt_boundary",
        required_state="prompt_loading_authority_not_granted",
        blocked_interpretation="must_not_select_load_scan_or_inspect_prompt_library_contents",
        description="Pilot boundary language must avoid prompt-loading leakage and unsafe prompt-field naming.",
    ),
    PilotBoundaryRuleDesign(
        rule_id="pilot_is_not_state_writer",
        boundary_group="write_boundary",
        required_state="persistence_not_granted",
        blocked_interpretation="must_not_cache_log_serialize_persist_or_write_review_outputs",
        description="Pilot output must remain ephemeral unless a later governed scope explicitly changes it.",
    ),
    PilotBoundaryRuleDesign(
        rule_id="pilot_is_not_training_data_source",
        boundary_group="data_boundary",
        required_state="training_data_use_forbidden",
        blocked_interpretation="must_not_use_pilot_outputs_for_training_calibration_or_gold_expansion",
        description="Pilot output cannot become hidden training data or canon data.",
    ),
    PilotBoundaryRuleDesign(
        rule_id="pilot_is_not_batch_engine",
        boundary_group="execution_boundary",
        required_state="batch_mode_forbidden",
        blocked_interpretation="must_not_generate_bulk_outputs_or_evidence_volume",
        description="Batch mode is blocked to prevent evidence inflation and hidden authority drift.",
    ),
    PilotBoundaryRuleDesign(
        rule_id="human_review_is_mandatory_not_approval",
        boundary_group="human_review_boundary",
        required_state="human_review_mandatory_invariant",
        blocked_interpretation="must_not_make_review_optional_or_record_approval_state",
        description="Future Pilot outputs may require human review, but Pilot cannot complete, record, or replace human judgment.",
    ),
)

_EVIDENCE_CONSTRAINTS: Final[tuple[PilotBoundaryEvidenceRuleDesign, ...]] = (
    PilotBoundaryEvidenceRuleDesign(
        evidence_rule_id="contracts_before_fields",
        required_before="future_input_output_field_use",
        required_evidence="p2_contract_and_validator_design_frozen",
        blocked_progression="must_not_process_inputs_or_generate_outputs_from_p1",
        description="P1 does not define or validate live input/output records.",
    ),
    PilotBoundaryEvidenceRuleDesign(
        evidence_rule_id="taxonomy_before_projection",
        required_before="future_divergence_or_projection_logic",
        required_evidence="p3_divergence_taxonomy_design_frozen",
        blocked_progression="must_not_invent_disagreement_types_during_implementation",
        description="Divergence categories must be explicit before any implementation.",
    ),
    PilotBoundaryEvidenceRuleDesign(
        evidence_rule_id="implementation_gate_before_callable_projection",
        required_before="first_callable_pilot_projection",
        required_evidence="p6_implementation_gate_design_frozen_and_human_signoff",
        blocked_progression="must_not_create_callable_projection_in_p1",
        description="A separate gate is required before any callable Pilot implementation.",
    ),
    PilotBoundaryEvidenceRuleDesign(
        evidence_rule_id="reproduction_before_divergence_trust",
        required_before="using_divergence_as_readiness_evidence",
        required_evidence="p8_reproduction_comparison_passes_critical_cases_with_zero_critical_deviations",
        blocked_progression="must_not_trust_divergence_before_reproduction_success",
        description="Pilot must first match critical frozen outcomes before divergence is useful.",
    ),
)

_PILOT_BOUNDARY_INVARIANTS: Final[tuple[str, ...]] = (
    "p1_is_design_only",
    "p1_defines_pilot_boundary_limits_only",
    "p1_does_not_start_or_enable_pilot",
    "p1_does_not_define_copilot_behavior",
    "p1_does_not_implement_projection_or_comparison",
    "p1_does_not_define_live_contracts_or_validators",
    "p1_does_not_select_load_or_scan_prompts",
    "p1_does_not_integrate_runtime_router_or_grant_authority",
    "p1_does_not_cache_log_serialize_persist_or_write_outputs",
    "p1_does_not_capture_human_decisions_or_review_approvals",
    "p1_does_not_use_outputs_for_training_or_gold_expansion",
    "p1_does_not_run_batch_mode",
    "p1_preserves_p2_as_next_allowed_milestone",
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "live_pilot_behavior",
    "live_copilot_behavior",
    "pilot_activation",
    "copilot_activation",
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
    "input_processing",
    "output_generation",
    "live_validation",
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

_SAFE_FUTURE_CONTRACT_LANGUAGE: Final[tuple[str, ...]] = (
    "routing_context_public_summary",
    "task_classification_hints_summary",
    "task_classification_projection_summary",
    "projection_analysis_summary",
    "boundary_flags_for_human_review",
    "divergence_summary_for_human_review",
    "human_review_mandatory",
    "advisory_review_priority",
    "routing_effect_none_constant",
    "prompt_loading_effect_none_constant",
    "runtime_effect_none_constant",
    "activation_effect_none_constant",
    "storage_status_in_memory_only_constant",
)

_UNSAFE_CONTRACT_LANGUAGE_POLICY: Final[tuple[str, ...]] = (
    "route_like_output_names_remain_forbidden",
    "prompt_group_field_names_remain_forbidden",
    "approval_or_completion_state_names_remain_forbidden",
    "confidence_score_probability_names_remain_forbidden",
    "activation_enablement_promotion_names_remain_forbidden",
)

_DESIGN: Final[PilotBoundaryDesign] = PilotBoundaryDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="P1",
    title="Routing Signal Scorer v3 Pilot Boundary Design v1",
    authority_statement=AUTHORITY_STATEMENT,
    design_status="design_only",
    pilot_status="boundary_design_only_not_started",
    copilot_status="not_started_deferred_to_p11_boundary_charter",
    projection_status="not_implemented_blocked_until_p7_after_p6_gate",
    runtime_authority_status="not_granted",
    prompt_loading_authority_status="not_granted",
    persistence_authority_status="not_granted",
    training_data_use_status="forbidden",
    batch_mode_status="forbidden",
    limited_shadow_runtime_status="out_of_scope_separate_future_governed_scope_required",
    human_review_status="mandatory_not_approval_not_decision_recording",
    required_preconditions=_REQUIRED_PRECONDITIONS,
    allowed_future_pilot_roles=_ALLOWED_FUTURE_PILOT_ROLES,
    hard_blocked_authority_rules=_HARD_BLOCKED_AUTHORITY_RULES,
    evidence_constraints=_EVIDENCE_CONSTRAINTS,
    pilot_boundary_invariants=_PILOT_BOUNDARY_INVARIANTS,
    forbidden_operations=_FORBIDDEN_OPERATIONS,
    safe_future_contract_language=_SAFE_FUTURE_CONTRACT_LANGUAGE,
    unsafe_contract_language_policy=_UNSAFE_CONTRACT_LANGUAGE_POLICY,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def build_pilot_boundary_design() -> PilotBoundaryDesign:
    """Return the immutable P1 design-only Pilot boundary record.

    The function accepts no input and performs no IO, live validation, projection,
    route comparison, prompt loading, runtime integration, persistence, decision
    recording, training-data use, batch execution, provider/model calls,
    candidate promotion, Pilot/Copilot activation, limited shadow runtime, or
    authority grant.
    """

    return _DESIGN
