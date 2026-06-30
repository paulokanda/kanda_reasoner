# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_boundary_design.py
"""Design-only M26 Auxiliar/Assistant boundary design.

M26 defines the safe boundary for a possible later Auxiliar/Assistant phase. It
is a static design record only. It does not start Assistant behavior, activate
shadow mode, inspect runtime state, evaluate readiness, compare routes, select
prompts, write files, persist evidence, record human decisions, promote
candidates, or grant authority.

The only public entry point returns a deterministic immutable design record. Any
future Auxiliar/Assistant contract or behavior remains separately governed and
must be introduced only by later validated and frozen milestones.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_auxiliar_assistant_boundary_design_v1"
SCHEMA_VERSION: Final[str] = "3.67-auxiliar-assistant-boundary-design"
DESIGN_KIND: Final[str] = "post_adviser_auxiliar_assistant_boundary_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M27 - Routing Signal Scorer v3 Auxiliar/Assistant Input Output Contract Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Auxiliar/Assistant boundary design describes future Assistant-phase limits only. "
    "It is not Assistant behavior and has no routing effect, no prompt-loading effect, "
    "no persistence effect, no review-decision effect, no candidate-promotion effect, "
    "no shadow-mode activation effect, no runtime authority, and no Copilot/Pilot behavior."
)


@dataclass(frozen=True)
class AuxiliarAssistantRoleBoundaryDesign:
    """Immutable description of one future allowed role boundary."""

    role_id: str
    allowed_scope: str
    required_human_control: str
    forbidden_interpretation: str
    description: str


@dataclass(frozen=True)
class AuxiliarAssistantAuthorityBoundaryDesign:
    """Immutable description of one authority boundary rule."""

    boundary_id: str
    boundary_group: str
    required_state: str
    forbidden_state: str
    description: str


@dataclass(frozen=True)
class AuxiliarAssistantBoundaryDesign:
    """Immutable design-only M26 Assistant boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    assistant_boundary_design_status: str
    assistant_behavior_status: str
    shadow_mode_status: str
    runtime_authority_status: str
    required_prior_milestones: tuple[str, ...]
    future_allowed_role_boundaries: tuple[AuxiliarAssistantRoleBoundaryDesign, ...]
    authority_boundary_rules: tuple[AuxiliarAssistantAuthorityBoundaryDesign, ...]
    forbidden_assistant_boundary_behaviors: tuple[str, ...]
    assistant_boundary_invariants: tuple[str, ...]
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
    "m25_assistant_boundary_readiness_gate_design_frozen",
)

_FUTURE_ALLOWED_ROLE_BOUNDARIES: Final[tuple[AuxiliarAssistantRoleBoundaryDesign, ...]] = (
    AuxiliarAssistantRoleBoundaryDesign(
        role_id="future_non_authoritative_comparison_reader",
        allowed_scope="may_later_summarize_shadow_observation_vs_current_router_evidence_for_human_review_only",
        required_human_control="human_review_remains_required_before_any_governed_change",
        forbidden_interpretation="must_not_choose_route_or_prompt_or_override_router",
        description="A later Assistant may only help a human read evidence; it may not become the routing authority.",
    ),
    AuxiliarAssistantRoleBoundaryDesign(
        role_id="future_boundary_question_drafter",
        allowed_scope="may_later_draft_questions_for_human_review_of_ambiguous_boundary_cases",
        required_human_control="human_must_answer_or_confirm_any_governed_boundary_decision",
        forbidden_interpretation="must_not_record_human_decision_or_confirm_freeze",
        description="A later Assistant may help formulate review questions but cannot record or infer the human decision.",
    ),
    AuxiliarAssistantRoleBoundaryDesign(
        role_id="future_safety_summary_assistant",
        allowed_scope="may_later_summarize_non_authoritative_safety_flags_from_validated_in_memory_evidence",
        required_human_control="human_keeps_final_interpretation_and_patch_scope_authority",
        forbidden_interpretation="must_not_promote_candidate_or_claim_assistant_prepared",
        description="A later Assistant may explain safety flags but cannot turn them into promotion or activation authority.",
    ),
    AuxiliarAssistantRoleBoundaryDesign(
        role_id="future_next_step_clarifier",
        allowed_scope="may_later_explain_the_next_governed_milestone_and_required_validation_evidence",
        required_human_control="human_explicit_confirmation_required_for_each_governed_step",
        forbidden_interpretation="must_not_run_patch_or_start_background_work",
        description="A later Assistant may clarify process boundaries but cannot execute governed transitions by itself.",
    ),
)

_AUTHORITY_BOUNDARY_RULES: Final[tuple[AuxiliarAssistantAuthorityBoundaryDesign, ...]] = (
    AuxiliarAssistantAuthorityBoundaryDesign(
        boundary_id="assistant_boundary_is_not_assistant_activation",
        boundary_group="assistant_activation_boundary",
        required_state="assistant_behavior_not_started",
        forbidden_state="assistant_behavior_active_or_claimed_ready",
        description="M26 only defines a boundary; it does not start Auxiliar, Assistant, Pilot, or Copilot behavior.",
    ),
    AuxiliarAssistantAuthorityBoundaryDesign(
        boundary_id="assistant_boundary_is_not_shadow_activation",
        boundary_group="shadow_mode_boundary",
        required_state="shadow_mode_not_active",
        forbidden_state="shadow_mode_active_or_connected_to_runtime",
        description="M26 does not activate shadow mode or connect shadow observations to routing outcomes.",
    ),
    AuxiliarAssistantAuthorityBoundaryDesign(
        boundary_id="assistant_boundary_is_not_router_authority",
        boundary_group="runtime_boundary",
        required_state="runtime_router_authority_not_granted",
        forbidden_state="route_selection_prompt_loading_or_runtime_router_integration",
        description="The real router and prompt loader remain outside the M26 boundary.",
    ),
    AuxiliarAssistantAuthorityBoundaryDesign(
        boundary_id="assistant_boundary_is_not_decision_recording",
        boundary_group="human_decision_boundary",
        required_state="human_decision_recording_not_implemented",
        forbidden_state="approval_rejection_override_or_freeze_confirmation_recording",
        description="M26 cannot record human decisions, freeze confirmations, approvals, rejections, or overrides.",
    ),
    AuxiliarAssistantAuthorityBoundaryDesign(
        boundary_id="assistant_boundary_is_not_persistence",
        boundary_group="storage_boundary",
        required_state="no_file_io_no_persistence_no_reports_no_review_queue_writes",
        forbidden_state="evidence_storage_report_writer_review_queue_writer_or_registry_writer",
        description="M26 remains a static design record and adds no storage or writer path.",
    ),
)

_FORBIDDEN_ASSISTANT_BOUNDARY_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_assistant",
    "assistant_behavior",
    "auxiliar_behavior",
    "pilot_behavior",
    "copilot_behavior",
    "assistant_activation",
    "shadow_mode_activation",
    "shadow_mode_runtime_connection",
    "readiness_evaluation_execution",
    "review_evidence_building",
    "observation_transformation_execution",
    "route_comparison_execution",
    "route_selection",
    "route_override",
    "prompt_selection",
    "prompt_loading",
    "runtime_router_import",
    "runtime_router_export",
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

_ASSISTANT_BOUNDARY_INVARIANTS: Final[tuple[str, ...]] = (
    "m26_is_design_only",
    "m26_defines_auxiliar_assistant_boundary_limits_only",
    "m26_does_not_start_auxiliar_assistant_or_copilot_behavior",
    "m26_does_not_activate_shadow_mode",
    "m26_does_not_compare_routes_or_select_prompts",
    "m26_does_not_grant_runtime_router_or_prompt_loader_authority",
    "m26_does_not_persist_or_write_project_state",
    "m26_does_not_record_human_decisions",
    "candidate_promotion_remains_blocked",
    "future_assistant_role_must_remain_non_authoritative_human_review_support_only",
    "m27_requires_separate_governed_input_output_contract_design",
)

_ASSISTANT_BOUNDARY_DESIGN: Final[AuxiliarAssistantBoundaryDesign] = AuxiliarAssistantBoundaryDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M26",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_assistant_behavior",
    assistant_boundary_design_status="static_boundary_design_only",
    assistant_behavior_status="not_started",
    shadow_mode_status="not_active",
    runtime_authority_status="not_granted",
    required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
    future_allowed_role_boundaries=_FUTURE_ALLOWED_ROLE_BOUNDARIES,
    authority_boundary_rules=_AUTHORITY_BOUNDARY_RULES,
    forbidden_assistant_boundary_behaviors=_FORBIDDEN_ASSISTANT_BOUNDARY_BEHAVIORS,
    assistant_boundary_invariants=_ASSISTANT_BOUNDARY_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m26_validation_freeze_and_separate_m27_scope_confirmation",
)


__all__ = ["build_auxiliar_assistant_boundary_design"]


def build_auxiliar_assistant_boundary_design() -> AuxiliarAssistantBoundaryDesign:
    """Return the immutable design-only M26 Assistant boundary record.

    The function accepts no observations, review evidence, prompts, candidates,
    runtime state, router objects, freeze files, or human decisions. It performs
    no Assistant behavior, no route comparison, no prompt loading, no runtime
    integration, no file IO, no persistence, no decision recording, no shadow
    activation, and no candidate promotion.
    """

    return _ASSISTANT_BOUNDARY_DESIGN
