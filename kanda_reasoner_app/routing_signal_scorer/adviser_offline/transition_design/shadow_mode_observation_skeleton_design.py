"""Design-only M21 shadow-mode observation skeleton design.

M21 defines the shape and safety limits of a future non-runtime observation
skeleton. It does not implement an observation builder, validate live data,
process input, generate output, compare routes, load prompts, call candidates,
write reports, persist records, or start Auxiliar/Assistant behavior.

The only public entry point returns a deterministic immutable skeleton design
record. Any executable observation logic belongs to a later separately governed
milestone after an implementation gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_shadow_mode_observation_skeleton_design_v1"
SCHEMA_VERSION: Final[str] = "3.62-shadow-mode-observation-skeleton-design"
DESIGN_KIND: Final[str] = "post_adviser_shadow_mode_observation_skeleton_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M22 - Routing Signal Scorer v3 Shadow Mode Implementation Gate Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Shadow observation skeleton design describes future non-runtime skeleton limits only. "
    "The real router and human governance keep decision authority. This design has "
    "no observation execution effect, no routing effect, no prompt-loading effect, "
    "no candidate-promotion effect, and no Auxiliar/Assistant behavior."
)


@dataclass(frozen=True)
class SkeletonSlotDesign:
    """Immutable description of one future skeleton slot or guardrail."""

    slot_id: str
    skeleton_side: str
    allowed_status: str
    blocked_use: str
    description: str


@dataclass(frozen=True)
class ShadowModeObservationSkeletonDesign:
    """Immutable design-only M21 observation skeleton record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    skeleton_design_status: str
    live_validation_status: str
    observation_execution_status: str
    runtime_authority_status: str
    required_preconditions: tuple[str, ...]
    future_skeleton_slots: tuple[SkeletonSlotDesign, ...]
    required_future_guardrails: tuple[SkeletonSlotDesign, ...]
    forbidden_skeleton_behaviors: tuple[str, ...]
    skeleton_invariants: tuple[str, ...]
    next_allowed_milestone: str
    implementation_gate: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m18_shadow_mode_boundary_design_frozen",
    "m19_shadow_mode_input_output_contract_design_frozen",
    "m20_shadow_mode_contract_validator_design_frozen",
    "freezememory_status_ok_before_later_observation_implementation",
    "separate_human_review_required_before_later_observation_implementation",
)

_FUTURE_SKELETON_SLOTS: Final[tuple[SkeletonSlotDesign, ...]] = (
    SkeletonSlotDesign(
        slot_id="future_validated_input_reference",
        skeleton_side="future_input_boundary",
        allowed_status="design_reference_only",
        blocked_use="no_live_input_acceptance_in_m21",
        description="A later implementation may receive M20-validated primitive input, but M21 does not accept data.",
    ),
    SkeletonSlotDesign(
        slot_id="future_contract_version_reference",
        skeleton_side="future_input_boundary",
        allowed_status="design_reference_only",
        blocked_use="no_schema_lookup_or_discovery_in_m21",
        description="A later implementation may reference the frozen M19 contract version supplied by the caller.",
    ),
    SkeletonSlotDesign(
        slot_id="future_non_authoritative_observation_placeholder",
        skeleton_side="future_output_boundary",
        allowed_status="design_reference_only",
        blocked_use="no_observation_output_generation_in_m21",
        description="A later implementation may return one in-memory non-authoritative observation, but M21 returns no observation.",
    ),
    SkeletonSlotDesign(
        slot_id="future_separate_human_review_marker",
        skeleton_side="future_review_boundary",
        allowed_status="design_reference_only",
        blocked_use="no_review_queue_or_approval_in_m21",
        description="A later implementation may mark that separate human review is required without implying approval.",
    ),
)

_REQUIRED_FUTURE_GUARDRAILS: Final[tuple[SkeletonSlotDesign, ...]] = (
    SkeletonSlotDesign(
        slot_id="guardrail_router_authority_not_granted",
        skeleton_side="future_guardrail_boundary",
        allowed_status="must_be_false_or_blocked_in_future_implementation",
        blocked_use="no_final_route_decision",
        description="A future skeleton must preserve that real routing authority remains outside shadow mode.",
    ),
    SkeletonSlotDesign(
        slot_id="guardrail_prompt_loading_not_granted",
        skeleton_side="future_guardrail_boundary",
        allowed_status="must_be_false_or_blocked_in_future_implementation",
        blocked_use="no_prompt_selection_or_loading",
        description="A future skeleton must not select, load, or recommend prompts for execution.",
    ),
    SkeletonSlotDesign(
        slot_id="guardrail_project_mutation_not_granted",
        skeleton_side="future_guardrail_boundary",
        allowed_status="must_be_false_or_blocked_in_future_implementation",
        blocked_use="no_freeze_gold_registry_or_patch_write",
        description="A future skeleton must not write freeze memory, gold sets, registries, patches, reports, or project state.",
    ),
    SkeletonSlotDesign(
        slot_id="guardrail_assistant_not_started",
        skeleton_side="future_guardrail_boundary",
        allowed_status="must_remain_not_started",
        blocked_use="no_auxiliar_assistant_behavior",
        description="A future skeleton must not start Auxiliar/Assistant or expose Assistant-facing behavior.",
    ),
)

_FORBIDDEN_SKELETON_BEHAVIORS: Final[tuple[str, ...]] = (
    "callable_observation_entrypoint",
    "live_input_validation_execution",
    "validated_input_processing",
    "observation_generation",
    "route_comparison",
    "candidate_execution",
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
    "patch_execution",
    "runtime_router_import",
    "runtime_router_export",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
    "shadow_mode_activation",
    "assistant_behavior",
)

_SKELETON_INVARIANTS: Final[tuple[str, ...]] = (
    "m21_is_design_only",
    "m21_defines_future_skeleton_limits_only",
    "m21_has_no_callable_observation_entrypoint",
    "m21_does_not_accept_or_process_input",
    "m21_does_not_generate_observation_output",
    "m21_does_not_compare_routes_or_candidates",
    "m21_does_not_persist_or_mutate_project_state",
    "future_skeleton_must_use_m20_validated_caller_supplied_primitives_only",
    "future_skeleton_output_must_remain_in_memory_non_authoritative_evidence_only",
    "m22_gate_design_is_required_before_later_observation_implementation",
)

_OBSERVATION_SKELETON_DESIGN: Final[ShadowModeObservationSkeletonDesign] = ShadowModeObservationSkeletonDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M21",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_observation_execution",
    skeleton_design_status="static_skeleton_design_only_no_observation_function",
    live_validation_status="not_implemented",
    observation_execution_status="not_implemented",
    runtime_authority_status="not_granted",
    required_preconditions=_REQUIRED_PRECONDITIONS,
    future_skeleton_slots=_FUTURE_SKELETON_SLOTS,
    required_future_guardrails=_REQUIRED_FUTURE_GUARDRAILS,
    forbidden_skeleton_behaviors=_FORBIDDEN_SKELETON_BEHAVIORS,
    skeleton_invariants=_SKELETON_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m21_validation_freeze_and_separate_human_review",
)


__all__ = ["build_shadow_mode_observation_skeleton_design"]


def build_shadow_mode_observation_skeleton_design() -> ShadowModeObservationSkeletonDesign:
    """Return the immutable design-only M21 observation skeleton record.

    The function accepts no input data and performs no validation, observation,
    route comparison, output generation, or authority logic. Executable
    observation behavior must be separately governed later.
    """

    return _OBSERVATION_SKELETON_DESIGN
