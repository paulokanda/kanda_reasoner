# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_assistant_boundary_readiness_gate_design.py
"""Design-only M25 shadow-mode readiness gate for Assistant boundary review.

M25 defines static criteria for deciding whether a later M26 Assistant boundary
review may even be designed. It does not execute a gate, read observations,
inspect freeze memory, scan source files, transform evidence, activate shadow
mode, start Auxiliar/Assistant behavior, integrate with runtime routing, load
prompts, persist anything, or grant authority.

The only public entry point returns a deterministic immutable design record. Any
future M26 Assistant boundary design must be separately governed after M25 is
validated and frozen.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_shadow_mode_assistant_boundary_readiness_gate_design_v1"
SCHEMA_VERSION: Final[str] = "3.66-shadow-mode-assistant-boundary-readiness-gate-design"
DESIGN_KIND: Final[str] = "post_adviser_shadow_mode_assistant_boundary_readiness_gate_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M26 - Routing Signal Scorer v3 Auxiliar/Assistant Boundary Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Shadow-mode readiness gate design describes future prerequisites for an Assistant boundary review only. "
    "It is not a live readiness gate and has no routing effect, no prompt-loading effect, no persistence effect, "
    "no review-decision effect, no candidate-promotion effect, no shadow-mode activation effect, no runtime authority, "
    "and no Auxiliar/Assistant behavior."
)


@dataclass(frozen=True)
class AssistantBoundaryReadinessCriterionDesign:
    """Immutable description of one future M26 boundary-review prerequisite."""

    criterion_id: str
    evidence_source: str
    required_status: str
    blocked_status: str
    description: str


@dataclass(frozen=True)
class AssistantBoundaryReadinessBoundaryDesign:
    """Immutable description of one M25 authority boundary rule."""

    boundary_id: str
    boundary_group: str
    required_state: str
    forbidden_interpretation: str
    description: str


@dataclass(frozen=True)
class ShadowModeAssistantBoundaryReadinessGateDesign:
    """Immutable design-only M25 readiness gate record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    readiness_gate_design_status: str
    live_gate_execution_status: str
    assistant_boundary_status: str
    runtime_authority_status: str
    required_prior_milestones: tuple[str, ...]
    future_boundary_review_prerequisites: tuple[AssistantBoundaryReadinessCriterionDesign, ...]
    boundary_review_safety_rules: tuple[AssistantBoundaryReadinessBoundaryDesign, ...]
    forbidden_readiness_gate_behaviors: tuple[str, ...]
    readiness_gate_invariants: tuple[str, ...]
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
)

_FUTURE_BOUNDARY_REVIEW_PREREQUISITES: Final[tuple[AssistantBoundaryReadinessCriterionDesign, ...]] = (
    AssistantBoundaryReadinessCriterionDesign(
        criterion_id="m24_review_evidence_design_frozen",
        evidence_source="project_freeze_after_update_frozen_memory_summary_to_be_reviewed_later",
        required_status="m24_freeze_confirmed_and_freeze_memory_status_ok_before_m26_scope_review",
        blocked_status="blocked_if_m24_validation_or_freeze_context_is_missing",
        description="A later M26 design review may not start unless M24 is locally validated, frozen, and exposed in startup context.",
    ),
    AssistantBoundaryReadinessCriterionDesign(
        criterion_id="shadow_mode_remains_inactive",
        evidence_source="human_supplied_project_state_summary_to_be_reviewed_later",
        required_status="shadow_mode_not_active",
        blocked_status="blocked_if_any_runtime_shadow_activation_is_claimed",
        description="M25 does not permit active shadow mode; M26 may only design a boundary if shadow mode remains inactive.",
    ),
    AssistantBoundaryReadinessCriterionDesign(
        criterion_id="auxiliar_assistant_remains_not_started",
        evidence_source="human_supplied_project_state_summary_to_be_reviewed_later",
        required_status="auxiliar_assistant_not_started",
        blocked_status="blocked_if_assistant_behavior_exists_or_is_requested_for_activation",
        description="A later Assistant boundary design cannot start from an already-started Assistant behavior path.",
    ),
    AssistantBoundaryReadinessCriterionDesign(
        criterion_id="runtime_authority_remains_not_granted",
        evidence_source="human_supplied_project_state_summary_to_be_reviewed_later",
        required_status="runtime_router_authority_not_granted",
        blocked_status="blocked_if_router_authority_or_prompt_loading_authority_is_requested",
        description="The real router and prompt-loader must remain outside M25 and M26 authority.",
    ),
    AssistantBoundaryReadinessCriterionDesign(
        criterion_id="m26_scope_requires_explicit_human_confirmation",
        evidence_source="future_user_instruction_before_m26_patch",
        required_status="separate_human_confirmation_for_m26_scope_required",
        blocked_status="blocked_if_confirmation_is_implicit_or_inferred",
        description="M26 must not be generated merely because M25 exists; the human must explicitly confirm the M26 scope.",
    ),
    AssistantBoundaryReadinessCriterionDesign(
        criterion_id="no_persistence_or_review_decision_bridge",
        evidence_source="future_patch_scope_review",
        required_status="no_persistence_no_review_queue_writer_no_human_decision_recorder",
        blocked_status="blocked_if_m26_would_write_evidence_or_decisions",
        description="M26 may design a boundary only; it must not add storage, review-queue writing, or human decision recording.",
    ),
)

_BOUNDARY_REVIEW_SAFETY_RULES: Final[tuple[AssistantBoundaryReadinessBoundaryDesign, ...]] = (
    AssistantBoundaryReadinessBoundaryDesign(
        boundary_id="readiness_gate_is_not_live_gate",
        boundary_group="execution_boundary",
        required_state="static_design_record_only",
        forbidden_interpretation="must_not_calculate_readiness_or_evaluate_live_evidence",
        description="M25 records future prerequisites but never evaluates whether they are met at runtime.",
    ),
    AssistantBoundaryReadinessBoundaryDesign(
        boundary_id="assistant_boundary_review_is_not_assistant_behavior",
        boundary_group="assistant_boundary",
        required_state="assistant_boundary_review_design_only",
        forbidden_interpretation="must_not_start_auxiliar_assistant_or_copilot_behavior",
        description="Even if M26 is later designed, it remains boundary design, not Assistant behavior.",
    ),
    AssistantBoundaryReadinessBoundaryDesign(
        boundary_id="readiness_gate_is_not_promotion",
        boundary_group="candidate_boundary",
        required_state="candidate_promotion_blocked",
        forbidden_interpretation="must_not_promote_candidate_or_approve_router_use",
        description="M25 cannot move any candidate toward runtime authority or production use.",
    ),
    AssistantBoundaryReadinessBoundaryDesign(
        boundary_id="readiness_gate_is_not_router_integration",
        boundary_group="runtime_boundary",
        required_state="runtime_router_authority_not_granted",
        forbidden_interpretation="must_not_import_export_or_call_runtime_router_or_prompt_loader",
        description="M25 must remain in the adviser-offline transition-design package only.",
    ),
)

_FORBIDDEN_READINESS_GATE_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_readiness_gate",
    "readiness_evaluation_execution",
    "review_evidence_building",
    "review_evidence_validation",
    "observation_transformation_execution",
    "route_comparison",
    "runtime_state_inspection",
    "runtime_router_import",
    "runtime_router_export",
    "prompt_selection",
    "prompt_loading",
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
    "shadow_mode_activation",
    "assistant_behavior",
    "auxiliar_behavior",
    "copilot_behavior",
)

_READINESS_GATE_INVARIANTS: Final[tuple[str, ...]] = (
    "m25_is_design_only",
    "m25_defines_future_m26_boundary_review_prerequisites_only",
    "m25_has_no_live_readiness_gate",
    "m25_does_not_evaluate_live_observations_or_review_evidence",
    "m25_does_not_start_auxiliar_assistant_or_copilot_behavior",
    "m25_does_not_grant_runtime_router_or_prompt_loader_authority",
    "m25_does_not_persist_or_write_project_state",
    "m25_does_not_record_human_decisions",
    "candidate_promotion_remains_blocked",
    "shadow_mode_remains_inactive",
    "m26_requires_separate_human_scope_confirmation",
)

_READINESS_GATE_DESIGN: Final[ShadowModeAssistantBoundaryReadinessGateDesign] = (
    ShadowModeAssistantBoundaryReadinessGateDesign(
        feature_id=FEATURE_ID,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        milestone="M25",
        authority_disclaimer=AUTHORITY_DISCLAIMER,
        lifecycle_status="design_only_no_live_readiness_gate",
        readiness_gate_design_status="static_prerequisite_design_only",
        live_gate_execution_status="not_implemented",
        assistant_boundary_status="not_started_design_review_only_after_m25_freeze_and_confirmation",
        runtime_authority_status="not_granted",
        required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
        future_boundary_review_prerequisites=_FUTURE_BOUNDARY_REVIEW_PREREQUISITES,
        boundary_review_safety_rules=_BOUNDARY_REVIEW_SAFETY_RULES,
        forbidden_readiness_gate_behaviors=_FORBIDDEN_READINESS_GATE_BEHAVIORS,
        readiness_gate_invariants=_READINESS_GATE_INVARIANTS,
        next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
        implementation_gate="blocked_until_m25_validation_freeze_and_explicit_m26_scope_confirmation",
    )
)


__all__ = ["build_shadow_mode_assistant_boundary_readiness_gate_design"]


def build_shadow_mode_assistant_boundary_readiness_gate_design() -> ShadowModeAssistantBoundaryReadinessGateDesign:
    """Return the immutable design-only M25 readiness gate record.

    The function accepts no observations, evidence, runtime state, freeze files,
    prompts, candidates, or router objects. It performs no live gate execution,
    no readiness calculation, no review-evidence building, no persistence, no
    prompt loading, no router integration, no shadow-mode activation, and no
    Auxiliar/Assistant behavior.
    """

    return _READINESS_GATE_DESIGN
