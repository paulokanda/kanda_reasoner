"""M34 Pilot/Copilot boundary design.

M34 defines the immutable design-only boundary for a possible later Pilot/Copilot
phase review after the Auxiliar/Assistant assistance-readiness chain is frozen.
It does not start Pilot or Copilot behavior, run a pilot, run a copilot, compare
or select routes, select or load prompts, integrate with runtime routing, read or
write files, persist records, record human decisions, mutate gold or registry
state, call providers, use embeddings, promote candidates, activate shadow mode,
or grant authority.

The only public entry point returns a deterministic immutable design record. Any
future M35 bridge-closure/handoff design must be separately governed after M34 is
validated and frozen.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_copilot_boundary_design_v1"
SCHEMA_VERSION: Final[str] = "3.75-pilot-copilot-boundary-design"
DESIGN_KIND: Final[str] = "post_adviser_pilot_copilot_boundary_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M35 - Routing Signal Scorer v3 Post-Adviser to Pilot/Copilot Handoff Closure Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Pilot/Copilot boundary design describes future role limits only. It is not "
    "Pilot behavior, Copilot behavior, route execution, route selection, prompt "
    "selection, prompt loading, runtime routing integration, persistence, human "
    "decision recording, candidate promotion, Assistant activation, Pilot/Copilot "
    "activation, shadow-mode activation, or runtime authority."
)


@dataclass(frozen=True)
class PilotCopilotBoundaryRoleDesign:
    """Immutable description of one future non-runtime Pilot/Copilot role limit."""

    role_id: str
    role_scope: str
    permitted_future_use: str
    prohibited_interpretation: str
    description: str


@dataclass(frozen=True)
class PilotCopilotBoundaryRuleDesign:
    """Immutable description of one Pilot/Copilot boundary rule."""

    rule_id: str
    boundary_group: str
    required_state: str
    blocked_interpretation: str
    description: str


@dataclass(frozen=True)
class PilotCopilotBoundaryDesign:
    """Immutable design-only M34 Pilot/Copilot boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    boundary_design_status: str
    pilot_status: str
    copilot_status: str
    runtime_authority_status: str
    required_prior_milestones: tuple[str, ...]
    future_allowed_boundary_roles: tuple[PilotCopilotBoundaryRoleDesign, ...]
    hard_blocked_authority_rules: tuple[PilotCopilotBoundaryRuleDesign, ...]
    forbidden_pilot_copilot_behaviors: tuple[str, ...]
    boundary_invariants: tuple[str, ...]
    next_allowed_milestone: str
    implementation_gate: str


_REQUIRED_PRIOR_MILESTONES: Final[tuple[str, ...]] = (
    "m18_shadow_mode_boundary_design_frozen",
    "m19_shadow_mode_input_output_contract_design_frozen",
    "m20_shadow_mode_contract_validator_design_frozen",
    "m21_shadow_mode_observation_skeleton_design_frozen",
    "m22_shadow_mode_implementation_gate_design_frozen",
    "m23_non_runtime_shadow_observation_implementation_frozen",
    "m24_shadow_observation_review_evidence_design_frozen",
    "m25_shadow_mode_assistant_boundary_readiness_gate_design_frozen",
    "m26_auxiliar_assistant_boundary_design_frozen",
    "m27_auxiliar_assistant_input_output_contract_design_frozen",
    "m28_auxiliar_assistant_contract_validator_design_frozen",
    "m29_auxiliar_assistant_assistance_skeleton_design_frozen",
    "m30_auxiliar_assistant_implementation_gate_design_frozen",
    "m31_non_runtime_auxiliar_assistant_assistance_implementation_frozen",
    "m32_auxiliar_assistant_assistance_review_evidence_design_frozen",
    "m33_auxiliar_assistant_assistance_readiness_gate_pilot_boundary_design_frozen",
)

_FUTURE_ALLOWED_BOUNDARY_ROLES: Final[tuple[PilotCopilotBoundaryRoleDesign, ...]] = (
    PilotCopilotBoundaryRoleDesign(
        role_id="future_pilot_boundary_reader",
        role_scope="read_only_boundary_context",
        permitted_future_use="may_read_human_supplied_boundary_context_in_a_separately_governed_future_design",
        prohibited_interpretation="must_not_read_project_files_or_runtime_state",
        description="A later design may describe read-only boundary context, but M34 provides no reader or runtime connection.",
    ),
    PilotCopilotBoundaryRoleDesign(
        role_id="future_pilot_question_drafter",
        role_scope="non_authoritative_human_review_questions",
        permitted_future_use="may_draft_questions_for_human_review_after_separate_governance",
        prohibited_interpretation="must_not_decide_routes_prompts_or_approvals",
        description="Future Pilot-support questions remain non-authoritative and cannot select routing or prompts.",
    ),
    PilotCopilotBoundaryRoleDesign(
        role_id="future_copilot_scope_summarizer",
        role_scope="human_review_scope_summary_only",
        permitted_future_use="may_summarize_scope_for_human_review_after_separate_governance",
        prohibited_interpretation="must_not_execute_or_modify_project_state",
        description="Future Copilot-adjacent summaries remain review support only, not execution or write authority.",
    ),
    PilotCopilotBoundaryRoleDesign(
        role_id="future_bridge_closure_reviewer",
        role_scope="post_adviser_bridge_closure_review_only",
        permitted_future_use="may support a future M35 closure design after M34 freeze",
        prohibited_interpretation="must_not_activate_pilot_copilot_or_assistant_behavior",
        description="M35, if created, must remain closure/handoff design and cannot activate any behavior.",
    ),
)

_HARD_BLOCKED_AUTHORITY_RULES: Final[tuple[PilotCopilotBoundaryRuleDesign, ...]] = (
    PilotCopilotBoundaryRuleDesign(
        rule_id="boundary_is_not_pilot_activation",
        boundary_group="activation_boundary",
        required_state="pilot_activation_not_granted",
        blocked_interpretation="must_not_start_pilot_behavior_or_pilot_runs",
        description="M34 records limits for a possible later Pilot boundary, but cannot activate Pilot behavior.",
    ),
    PilotCopilotBoundaryRuleDesign(
        rule_id="boundary_is_not_copilot_activation",
        boundary_group="activation_boundary",
        required_state="copilot_activation_not_granted",
        blocked_interpretation="must_not_start_copilot_behavior_or_execution_support",
        description="M34 cannot enable Copilot behavior, execution support, or delegated project changes.",
    ),
    PilotCopilotBoundaryRuleDesign(
        rule_id="boundary_is_not_router_authority",
        boundary_group="runtime_boundary",
        required_state="router_authority_not_granted",
        blocked_interpretation="must_not_compare_select_override_or_execute_routes",
        description="The runtime router remains outside this boundary and receives no authority from M34.",
    ),
    PilotCopilotBoundaryRuleDesign(
        rule_id="boundary_is_not_prompt_loader_authority",
        boundary_group="prompt_boundary",
        required_state="prompt_loader_authority_not_granted",
        blocked_interpretation="must_not_select_or_load_prompts",
        description="M34 cannot choose prompts, load prompts, or create prompt-loading side effects.",
    ),
    PilotCopilotBoundaryRuleDesign(
        rule_id="boundary_is_not_state_or_decision_writer",
        boundary_group="write_boundary",
        required_state="no_project_state_writes_no_decision_recording",
        blocked_interpretation="must_not_persist_records_write_queues_or_record_human_decisions",
        description="M34 is design-only and cannot store evidence, write queues, or record approvals/rejections/overrides.",
    ),
    PilotCopilotBoundaryRuleDesign(
        rule_id="boundary_is_not_candidate_promotion",
        boundary_group="candidate_boundary",
        required_state="candidate_promotion_blocked",
        blocked_interpretation="must_not_promote_enable_or_approve_any_candidate",
        description="M34 cannot move any candidate closer to runtime use or production trust.",
    ),
)

_FORBIDDEN_PILOT_COPILOT_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_pilot_behavior",
    "live_copilot_behavior",
    "callable_pilot_runner",
    "callable_copilot_runner",
    "pilot_activation",
    "copilot_activation",
    "assistant_activation",
    "auxiliar_activation",
    "shadow_mode_activation",
    "pilot_run_execution",
    "copilot_execution_support",
    "route_comparison",
    "route_selection",
    "route_override",
    "route_execution",
    "prompt_selection",
    "prompt_loading",
    "runtime_integration",
    "runtime_router_import",
    "runtime_router_export",
    "router_authority",
    "runtime_state_inspection",
    "source_scanning",
    "case_discovery",
    "file_io",
    "console_io",
    "logging",
    "persistence",
    "report_writing",
    "review_queue_writing",
    "registry_writing",
    "gold_mutation",
    "freeze_writing",
    "human_decision_recording",
    "approval_recording",
    "rejection_recording",
    "override_recording",
    "patch_execution",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
)

_BOUNDARY_INVARIANTS: Final[tuple[str, ...]] = (
    "m34_is_design_only",
    "m34_defines_pilot_copilot_boundary_limits_only",
    "m34_does_not_start_pilot_or_copilot_behavior",
    "m34_does_not_activate_assistant_auxiliar_pilot_copilot_or_shadow_mode",
    "m34_does_not_compare_select_override_or_execute_routes",
    "m34_does_not_select_or_load_prompts",
    "m34_does_not_integrate_runtime_router_or_grant_authority",
    "m34_does_not_read_or_write_project_state",
    "m34_does_not_persist_or_write_reports_or_queues",
    "m34_does_not_record_human_decisions",
    "m34_does_not_mutate_gold_or_registries",
    "m34_does_not_call_providers_or_use_embeddings",
    "candidate_promotion_remains_blocked",
    "shadow_mode_remains_inactive",
    "pilot_copilot_remain_not_started",
    "m35_requires_separate_human_scope_confirmation",
)

_DESIGN_RECORD: Final[PilotCopilotBoundaryDesign] = PilotCopilotBoundaryDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M34",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_pilot_copilot_activation",
    boundary_design_status="static_boundary_limits_only",
    pilot_status="not_started",
    copilot_status="not_started",
    runtime_authority_status="not_granted",
    required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
    future_allowed_boundary_roles=_FUTURE_ALLOWED_BOUNDARY_ROLES,
    hard_blocked_authority_rules=_HARD_BLOCKED_AUTHORITY_RULES,
    forbidden_pilot_copilot_behaviors=_FORBIDDEN_PILOT_COPILOT_BEHAVIORS,
    boundary_invariants=_BOUNDARY_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_separate_m35_scope_confirmation_validation_and_freeze",
)


def build_pilot_copilot_boundary_design() -> PilotCopilotBoundaryDesign:
    """Return the immutable M34 Pilot/Copilot boundary design record."""

    return _DESIGN_RECORD
