# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_assistance_review_evidence_design.py
"""M32 Auxiliar/Assistant assistance review evidence design.

M32 defines a static review-evidence envelope for later human review of M31
non-runtime Auxiliar/Assistant assistance records. It does not transform live
assistance, validate live payloads, build review evidence, persist evidence,
write reports, enqueue review items, record human decisions, read files, load
prompts, activate Assistant behavior, activate shadow mode, integrate runtime
routing, or grant router authority.

The only public entry point returns a deterministic immutable design record. A
future executable review-evidence builder, validator, persistence writer, or
review queue integration must be separately governed later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = (
    "routing_signal_scorer_v3_auxiliar_assistant_assistance_review_evidence_design_v1"
)
SCHEMA_VERSION: Final[str] = "3.73-auxiliar-assistant-assistance-review-evidence-design"
DESIGN_KIND: Final[str] = (
    "post_adviser_auxiliar_assistant_assistance_review_evidence_design_only"
)
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M33 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Readiness Gate for Pilot Boundary Review v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Auxiliar/Assistant assistance review evidence design describes future human-review "
    "evidence fields only. The real router and human governance keep decision authority. "
    "This design has no routing effect, no route-selection effect, no prompt-loading effect, "
    "no persistence effect, no review-queue writing effect, no human-decision effect, "
    "no candidate-promotion effect, no shadow-mode activation effect, no Assistant activation "
    "effect, no runtime authority, and no Copilot/Pilot behavior."
)


@dataclass(frozen=True)
class AssistanceReviewEvidenceFieldDesign:
    """Immutable description of one future assistance review evidence field."""

    name: str
    value_kind: str
    source_rule: str
    requirement: str
    description: str


@dataclass(frozen=True)
class AssistanceReviewEvidenceBoundaryDesign:
    """Immutable description of one future assistance review evidence boundary rule."""

    boundary_id: str
    boundary_group: str
    required_status: str
    blocked_interpretation: str
    description: str


@dataclass(frozen=True)
class AuxiliarAssistantAssistanceReviewEvidenceDesign:
    """Immutable design-only M32 assistance review evidence record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    evidence_design_status: str
    live_evidence_builder_status: str
    persistence_status: str
    runtime_authority_status: str
    required_prior_milestones: tuple[str, ...]
    allowed_source_assistance_fields: tuple[str, ...]
    future_review_evidence_fields: tuple[AssistanceReviewEvidenceFieldDesign, ...]
    review_boundary_rules: tuple[AssistanceReviewEvidenceBoundaryDesign, ...]
    forbidden_review_evidence_behaviors: tuple[str, ...]
    review_evidence_invariants: tuple[str, ...]
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
)

_ALLOWED_SOURCE_ASSISTANCE_FIELDS: Final[tuple[str, ...]] = (
    "assistance_record_kind",
    "assistant_case_id",
    "contract_schema_version",
    "authority_notice",
    "human_review_context_summary",
    "boundary_questions_for_human_review",
    "safety_flags_for_human_review",
    "missing_information_summary",
    "requires_separate_human_review",
    "storage_status",
    "routing_effect",
    "prompt_loading_effect",
    "assistant_activation_effect",
)

_FUTURE_REVIEW_EVIDENCE_FIELDS: Final[
    tuple[AssistanceReviewEvidenceFieldDesign, ...]
] = (
    AssistanceReviewEvidenceFieldDesign(
        name="assistance_review_evidence_record_kind",
        value_kind="literal_string",
        source_rule="fixed_by_future_builder",
        requirement="required",
        description="Identifies a future assistance review-evidence envelope without granting authority.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="assistant_case_id",
        value_kind="string",
        source_rule="copied_from_m31_assistance_record",
        requirement="required",
        description="Carries the M31 assistance case identifier into future review evidence.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="source_assistance_schema_version",
        value_kind="string",
        source_rule="copied_from_m31_contract_schema_version",
        requirement="required",
        description="Records which non-runtime assistance schema produced the source record.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="human_review_context_summary",
        value_kind="string",
        source_rule="copied_from_m31_human_review_context_summary",
        requirement="required",
        description="Preserves the non-authoritative review context generated by M31.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="boundary_questions_for_review",
        value_kind="tuple_of_strings",
        source_rule="copied_from_m31_boundary_questions_for_human_review",
        requirement="required_non_empty_tuple",
        description="Preserves human-review questions without converting them into decisions.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="safety_flags_for_review",
        value_kind="tuple_of_strings",
        source_rule="copied_from_m31_safety_flags_for_human_review",
        requirement="required_non_empty_tuple",
        description="Preserves non-authoritative safety flags for later review.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="missing_information_summary",
        value_kind="string",
        source_rule="copied_from_m31_missing_information_summary",
        requirement="required",
        description="Preserves missing-information context for human review only.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="authority_notice",
        value_kind="string",
        source_rule="copied_from_m31_authority_notice",
        requirement="required",
        description="Keeps the non-authority notice visible in future review evidence.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="review_storage_design_status",
        value_kind="literal_string",
        source_rule="fixed_by_future_builder",
        requirement="required",
        description="Must state that M32 design does not persist or write review evidence.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="requires_separate_human_review",
        value_kind="boolean",
        source_rule="fixed_true_or_copied_true_from_m31_assistance_record",
        requirement="required_true",
        description="Keeps human review mandatory and prevents automated approval semantics.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="routing_effect",
        value_kind="literal_string",
        source_rule="fixed_none_or_copied_none_from_m31_assistance_record",
        requirement="required_none",
        description="Keeps evidence non-authoritative for routing.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="prompt_loading_effect",
        value_kind="literal_string",
        source_rule="fixed_none_or_copied_none_from_m31_assistance_record",
        requirement="required_none",
        description="Keeps evidence unable to load prompts.",
    ),
    AssistanceReviewEvidenceFieldDesign(
        name="assistant_activation_effect",
        value_kind="literal_string",
        source_rule="fixed_none_or_copied_none_from_m31_assistance_record",
        requirement="required_none",
        description="Keeps evidence unable to activate Assistant behavior.",
    ),
)

_REVIEW_BOUNDARY_RULES: Final[tuple[AssistanceReviewEvidenceBoundaryDesign, ...]] = (
    AssistanceReviewEvidenceBoundaryDesign(
        boundary_id="source_must_be_m31_non_runtime_assistance",
        boundary_group="source_evidence_boundary",
        required_status="future_source_must_be_m31_assistance_dict_only",
        blocked_interpretation="must_not_accept_runtime_router_prompt_objects_live_assistant_objects_or_live_candidate_objects",
        description="Future review evidence may be derived only from M31-style in-memory assistance dictionaries.",
    ),
    AssistanceReviewEvidenceBoundaryDesign(
        boundary_id="assistance_review_evidence_is_not_human_decision",
        boundary_group="authority_boundary",
        required_status="human_review_required_not_completed",
        blocked_interpretation="must_not_mean_approval_rejection_override_route_selection_prompt_selection_or_promotion",
        description="Future evidence may support review, but must not record or imply a human decision.",
    ),
    AssistanceReviewEvidenceBoundaryDesign(
        boundary_id="assistance_review_evidence_is_not_persistence",
        boundary_group="side_effect_boundary",
        required_status="m32_design_has_no_writer_and_no_storage_target",
        blocked_interpretation="must_not_write_reports_logs_files_queues_registries_or_freeze_memory",
        description="M32 only designs future review evidence fields and must not write them anywhere.",
    ),
    AssistanceReviewEvidenceBoundaryDesign(
        boundary_id="assistance_review_evidence_is_not_assistant_activation",
        boundary_group="assistant_boundary",
        required_status="auxiliar_assistant_not_started_pilot_copilot_not_started",
        blocked_interpretation="must_not_enable_assistant_auxiliar_pilot_copilot_or_shadow_mode_behavior",
        description="Review evidence design cannot activate Assistant, Auxiliar, Pilot/Copilot, or shadow mode.",
    ),
)

_FORBIDDEN_REVIEW_EVIDENCE_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_review_evidence_builder",
    "assistance_transformation_execution",
    "live_input_validation_execution",
    "live_assistance_execution",
    "route_comparison",
    "route_selection",
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
    "assistant_activation",
    "assistant_behavior",
    "auxiliar_behavior",
    "copilot_behavior",
    "pilot_behavior",
)

_REVIEW_EVIDENCE_INVARIANTS: Final[tuple[str, ...]] = (
    "m32_is_design_only",
    "m32_has_no_live_review_evidence_builder",
    "m32_does_not_transform_or_validate_live_m31_assistance_records",
    "m32_does_not_persist_write_enqueue_or_report_review_evidence",
    "m32_does_not_record_human_decisions_or_decision_outcomes",
    "m32_does_not_select_routes_or_prompts",
    "m32_does_not_start_auxiliar_assistant_or_pilot_copilot_behavior",
    "m32_does_not_activate_shadow_mode_or_assistant_behavior",
    "m32_does_not_grant_runtime_router_or_prompt_loader_authority",
    "candidate_promotion_remains_blocked",
    "shadow_mode_remains_inactive",
    "assistant_auxiliar_pilot_copilot_remain_not_started",
    "m33_requires_separate_human_scope_confirmation",
)

_REVIEW_EVIDENCE_DESIGN: Final[AuxiliarAssistantAssistanceReviewEvidenceDesign] = (
    AuxiliarAssistantAssistanceReviewEvidenceDesign(
        feature_id=FEATURE_ID,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        milestone="M32",
        authority_disclaimer=AUTHORITY_DISCLAIMER,
        lifecycle_status="post_adviser_auxiliar_assistant_assistance_review_evidence_design_only",
        evidence_design_status="future_evidence_fields_only_no_live_builder",
        live_evidence_builder_status="not_implemented",
        persistence_status="not_implemented_no_storage_target",
        runtime_authority_status="not_granted",
        required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
        allowed_source_assistance_fields=_ALLOWED_SOURCE_ASSISTANCE_FIELDS,
        future_review_evidence_fields=_FUTURE_REVIEW_EVIDENCE_FIELDS,
        review_boundary_rules=_REVIEW_BOUNDARY_RULES,
        forbidden_review_evidence_behaviors=_FORBIDDEN_REVIEW_EVIDENCE_BEHAVIORS,
        review_evidence_invariants=_REVIEW_EVIDENCE_INVARIANTS,
        next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
        implementation_gate="blocked_until_separate_m33_scope_confirmation_validation_and_freeze",
    )
)


def build_auxiliar_assistant_assistance_review_evidence_design() -> AuxiliarAssistantAssistanceReviewEvidenceDesign:
    """Return the immutable M32 assistance review evidence design record."""

    return _REVIEW_EVIDENCE_DESIGN


__all__ = [
    "AssistanceReviewEvidenceBoundaryDesign",
    "AssistanceReviewEvidenceFieldDesign",
    "AuxiliarAssistantAssistanceReviewEvidenceDesign",
    "build_auxiliar_assistant_assistance_review_evidence_design",
]
