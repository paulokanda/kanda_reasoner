# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_observation_review_evidence_design.py
"""Design-only M24 shadow observation review evidence design.

M24 defines a static review-evidence envelope for later human review of M23
non-runtime shadow observations. It does not transform live observations,
compare routes, validate inputs, write reports, persist evidence, enqueue review
items, read files, activate shadow mode, start Auxiliar/Assistant behavior, or
grant runtime authority.

The only public entry point returns a deterministic immutable design record. A
future executable review-evidence builder, persistence writer, or review queue
integration must be separately governed later.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_shadow_observation_review_evidence_design_v1"
SCHEMA_VERSION: Final[str] = "3.65-shadow-observation-review-evidence-design"
DESIGN_KIND: Final[str] = "post_adviser_shadow_observation_review_evidence_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M25 - Routing Signal Scorer v3 Shadow Mode Readiness Gate for Assistant Boundary Review v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Shadow observation review evidence design describes future human-review evidence fields only. "
    "The real router and human governance keep decision authority. This design has no routing effect, "
    "no prompt-loading effect, no persistence effect, no review-queue writing effect, no candidate-promotion effect, "
    "no runtime authority, and no Auxiliar/Assistant behavior."
)


@dataclass(frozen=True)
class ReviewEvidenceFieldDesign:
    """Immutable description of one future review evidence field."""

    name: str
    value_kind: str
    source_rule: str
    requirement: str
    description: str


@dataclass(frozen=True)
class ReviewEvidenceBoundaryDesign:
    """Immutable description of one review evidence boundary rule."""

    boundary_id: str
    boundary_group: str
    required_status: str
    blocked_interpretation: str
    description: str


@dataclass(frozen=True)
class ShadowObservationReviewEvidenceDesign:
    """Immutable design-only M24 review evidence record."""

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
    allowed_source_observation_fields: tuple[str, ...]
    future_review_evidence_fields: tuple[ReviewEvidenceFieldDesign, ...]
    review_boundary_rules: tuple[ReviewEvidenceBoundaryDesign, ...]
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
)

_ALLOWED_SOURCE_OBSERVATION_FIELDS: Final[tuple[str, ...]] = (
    "observation_record_kind",
    "routing_case_id",
    "contract_schema_version",
    "authority_notice",
    "route_path_difference_observed",
    "constraint_flags_observed",
    "requires_separate_human_review",
    "human_review_reason_summary",
    "storage_status",
    "routing_effect",
    "prompt_loading_effect",
    "candidate_promotion_effect",
    "runtime_authority",
    "shadow_mode_status",
    "assistant_status",
)

_FUTURE_REVIEW_EVIDENCE_FIELDS: Final[tuple[ReviewEvidenceFieldDesign, ...]] = (
    ReviewEvidenceFieldDesign(
        name="review_evidence_record_kind",
        value_kind="literal_string",
        source_rule="fixed_by_future_builder",
        requirement="required",
        description="Identifies a future human-review evidence envelope without granting authority.",
    ),
    ReviewEvidenceFieldDesign(
        name="routing_case_id",
        value_kind="string",
        source_rule="copied_from_m23_observation",
        requirement="required",
        description="Carries the M23 observation case identifier into future review evidence.",
    ),
    ReviewEvidenceFieldDesign(
        name="source_observation_schema_version",
        value_kind="string",
        source_rule="copied_from_m23_contract_schema_version",
        requirement="required",
        description="Records which non-runtime observation schema produced the source evidence.",
    ),
    ReviewEvidenceFieldDesign(
        name="review_reason_summary",
        value_kind="string",
        source_rule="copied_or_summarized_from_m23_human_review_reason_summary",
        requirement="required",
        description="Preserves why the evidence requires separate human review.",
    ),
    ReviewEvidenceFieldDesign(
        name="constraint_flags_for_review",
        value_kind="tuple_of_strings",
        source_rule="copied_from_m23_constraint_flags_observed",
        requirement="required_empty_tuple_allowed",
        description="Preserves non-authoritative constraint flags for later human review.",
    ),
    ReviewEvidenceFieldDesign(
        name="authority_notice",
        value_kind="string",
        source_rule="copied_from_m23_authority_notice",
        requirement="required",
        description="Keeps the non-authority notice visible in future review evidence.",
    ),
    ReviewEvidenceFieldDesign(
        name="review_storage_design_status",
        value_kind="literal_string",
        source_rule="fixed_by_future_builder",
        requirement="required",
        description="Must state that M24 design does not persist or write review evidence.",
    ),
    ReviewEvidenceFieldDesign(
        name="requires_separate_human_review",
        value_kind="boolean",
        source_rule="fixed_true_or_copied_true_from_m23_observation",
        requirement="required_true",
        description="Keeps human review mandatory and prevents automated approval semantics.",
    ),
    ReviewEvidenceFieldDesign(
        name="routing_effect",
        value_kind="literal_string",
        source_rule="fixed_none_or_copied_none_from_m23_observation",
        requirement="required_none",
        description="Keeps evidence non-authoritative for routing.",
    ),
    ReviewEvidenceFieldDesign(
        name="prompt_loading_effect",
        value_kind="literal_string",
        source_rule="fixed_none_or_copied_none_from_m23_observation",
        requirement="required_none",
        description="Keeps evidence unable to load prompts.",
    ),
    ReviewEvidenceFieldDesign(
        name="candidate_promotion_effect",
        value_kind="literal_string",
        source_rule="fixed_none_or_copied_none_from_m23_observation",
        requirement="required_none",
        description="Keeps evidence unable to promote candidates.",
    ),
)

_REVIEW_BOUNDARY_RULES: Final[tuple[ReviewEvidenceBoundaryDesign, ...]] = (
    ReviewEvidenceBoundaryDesign(
        boundary_id="source_must_be_m23_non_runtime_observation",
        boundary_group="source_evidence_boundary",
        required_status="future_source_must_be_m23_observation_dict_only",
        blocked_interpretation="must_not_accept_runtime_router_objects_prompt_objects_or_live_candidate_objects",
        description="Future review evidence may be derived only from M23-style non-runtime observation dictionaries.",
    ),
    ReviewEvidenceBoundaryDesign(
        boundary_id="review_evidence_is_not_human_decision",
        boundary_group="authority_boundary",
        required_status="human_review_required_not_completed",
        blocked_interpretation="must_not_mean_approval_rejection_override_or_promotion",
        description="Future evidence records may support review, but must not record or imply a human decision.",
    ),
    ReviewEvidenceBoundaryDesign(
        boundary_id="review_evidence_is_not_persistence",
        boundary_group="side_effect_boundary",
        required_status="m24_design_has_no_writer_and_no_storage_target",
        blocked_interpretation="must_not_write_reports_logs_files_queues_registries_or_freeze_memory",
        description="M24 only designs future review evidence fields and must not write them anywhere.",
    ),
    ReviewEvidenceBoundaryDesign(
        boundary_id="review_evidence_is_not_shadow_activation",
        boundary_group="shadow_mode_boundary",
        required_status="shadow_mode_not_active_auxiliar_assistant_not_started",
        blocked_interpretation="must_not_enable_shadow_mode_or_assistant_boundary",
        description="Review evidence design cannot activate shadow mode or begin Auxiliar/Assistant behavior.",
    ),
)

_FORBIDDEN_REVIEW_EVIDENCE_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_review_evidence_builder",
    "observation_transformation_execution",
    "live_input_validation_execution",
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
)

_REVIEW_EVIDENCE_INVARIANTS: Final[tuple[str, ...]] = (
    "m24_is_design_only",
    "m24_defines_future_review_evidence_fields_only",
    "m24_has_no_callable_review_evidence_builder",
    "m24_does_not_transform_live_observations",
    "m24_does_not_persist_or_write_review_evidence",
    "m24_does_not_record_human_decisions",
    "m24_does_not_compare_routes",
    "m24_keeps_shadow_mode_inactive",
    "m24_keeps_auxiliar_assistant_not_started",
    "future_review_evidence_must_remain_non_authoritative",
    "future_m25_readiness_gate_for_assistant_boundary_review_is_required_before_assistant_boundary_design",
)

_REVIEW_EVIDENCE_DESIGN: Final[ShadowObservationReviewEvidenceDesign] = ShadowObservationReviewEvidenceDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M24",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_live_review_evidence_builder",
    evidence_design_status="static_review_evidence_field_design_only",
    live_evidence_builder_status="not_implemented",
    persistence_status="not_implemented",
    runtime_authority_status="not_granted",
    required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
    allowed_source_observation_fields=_ALLOWED_SOURCE_OBSERVATION_FIELDS,
    future_review_evidence_fields=_FUTURE_REVIEW_EVIDENCE_FIELDS,
    review_boundary_rules=_REVIEW_BOUNDARY_RULES,
    forbidden_review_evidence_behaviors=_FORBIDDEN_REVIEW_EVIDENCE_BEHAVIORS,
    review_evidence_invariants=_REVIEW_EVIDENCE_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m24_validation_freeze_and_m25_scope_confirmation",
)


__all__ = ["build_shadow_observation_review_evidence_design"]


def build_shadow_observation_review_evidence_design() -> ShadowObservationReviewEvidenceDesign:
    """Return the immutable design-only M24 review evidence record.

    The function accepts no observation data and performs no review-evidence
    building, validation, transformation, persistence, report writing, queue
    writing, route comparison, runtime integration, or authority logic.
    """

    return _REVIEW_EVIDENCE_DESIGN
