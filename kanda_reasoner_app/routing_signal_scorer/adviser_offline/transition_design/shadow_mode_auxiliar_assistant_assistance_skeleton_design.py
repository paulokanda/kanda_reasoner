"""Design-only M29 Auxiliar/Assistant assistance skeleton design.

M29 defines static skeleton slots for possible later Auxiliar/Assistant
human-review support. It is a design record only. It does not process input,
generate output, validate live contracts, transform observations, compare routes,
select prompts, write files, persist evidence, record human decisions, call
providers, use embeddings, activate shadow mode, start Assistant behavior,
promote candidates, or grant runtime authority.

The only public entry point returns a deterministic immutable skeleton-design
record. Executable assistance logic remains a later separately governed and
frozen milestone.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_auxiliar_assistant_assistance_skeleton_design_v1"
SCHEMA_VERSION: Final[str] = "3.70-auxiliar-assistant-assistance-skeleton-design"
DESIGN_KIND: Final[str] = "post_adviser_auxiliar_assistant_assistance_skeleton_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M30 - Routing Signal Scorer v3 Auxiliar/Assistant Implementation Gate Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Auxiliar/Assistant assistance skeleton design describes future in-memory "
    "non-authoritative human-review support slots only. It is not live Assistant "
    "behavior, not Auxiliar behavior, not a callable assistance builder, and has "
    "no routing effect, no route-selection effect, no prompt-loading effect, no "
    "persistence effect, no human-decision effect, no candidate-promotion effect, "
    "no shadow-mode activation effect, no runtime authority, and no Copilot/Pilot "
    "behavior."
)


@dataclass(frozen=True)
class AuxiliarAssistantAssistanceSlotDesign:
    """Immutable future assistance skeleton slot description."""

    slot_id: str
    skeleton_side: str
    allowed_status: str
    blocked_use: str
    description: str


@dataclass(frozen=True)
class AuxiliarAssistantAssistanceSkeletonDesign:
    """Immutable design-only M29 Auxiliar/Assistant assistance skeleton record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    skeleton_design_status: str
    live_assistance_status: str
    input_processing_status: str
    output_generation_status: str
    live_validation_status: str
    assistant_behavior_status: str
    shadow_mode_status: str
    runtime_authority_status: str
    required_prior_milestones: tuple[str, ...]
    future_assistance_slots: tuple[AuxiliarAssistantAssistanceSlotDesign, ...]
    required_future_guardrails: tuple[str, ...]
    forbidden_skeleton_behaviors: tuple[str, ...]
    skeleton_invariants: tuple[str, ...]
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
    "m26_auxiliar_assistant_boundary_design_frozen",
    "m27_auxiliar_assistant_input_output_contract_design_frozen",
    "m28_auxiliar_assistant_contract_validator_design_frozen",
)

_FUTURE_ASSISTANCE_SLOTS: Final[tuple[AuxiliarAssistantAssistanceSlotDesign, ...]] = (
    AuxiliarAssistantAssistanceSlotDesign(
        slot_id="future_validated_assistant_input_reference",
        skeleton_side="input_reference",
        allowed_status="future_m28_validated_payload_reference_only",
        blocked_use="no_input_processing_or_case_discovery",
        description="Future assistance skeletons may reference only caller-supplied payloads validated by a later governed M28-style validator implementation.",
    ),
    AuxiliarAssistantAssistanceSlotDesign(
        slot_id="future_validated_assistant_contract_version_reference",
        skeleton_side="contract_reference",
        allowed_status="future_m27_contract_version_reference_only",
        blocked_use="no_schema_mutation_or_contract_selection",
        description="Future assistance skeletons may carry an immutable M27 contract-version reference but must not choose or mutate contracts.",
    ),
    AuxiliarAssistantAssistanceSlotDesign(
        slot_id="future_non_authoritative_assistance_placeholder",
        skeleton_side="assistance_placeholder",
        allowed_status="in_memory_human_review_support_placeholder_only",
        blocked_use="no_recommendation_no_route_no_prompt_no_decision",
        description="Future assistance payloads may reserve one non-authoritative placeholder for human review support with no routing or prompt effect.",
    ),
    AuxiliarAssistantAssistanceSlotDesign(
        slot_id="future_human_review_required_marker",
        skeleton_side="review_marker",
        allowed_status="separate_human_review_required_marker_only",
        blocked_use="no_human_decision_recording_or_approval",
        description="Future skeletons must carry a marker that separate human review is required and must not record the decision itself.",
    ),
    AuxiliarAssistantAssistanceSlotDesign(
        slot_id="future_no_action_taken_authority_marker",
        skeleton_side="authority_marker",
        allowed_status="explicit_no_action_taken_marker_only",
        blocked_use="no_runtime_action_or_activation",
        description="Future skeleton outputs must state that no route, prompt, persistence, activation, or candidate-promotion action was taken.",
    ),
)

_REQUIRED_FUTURE_GUARDRAILS: Final[tuple[str, ...]] = (
    "guardrail_assistance_is_non_authoritative_human_review_support_only",
    "guardrail_router_authority_not_granted",
    "guardrail_prompt_loading_not_granted",
    "guardrail_runtime_integration_not_granted",
    "guardrail_shadow_mode_activation_not_granted",
    "guardrail_assistant_activation_not_granted",
    "guardrail_no_human_decision_recording",
    "guardrail_no_persistence_or_report_writing",
    "guardrail_no_gold_registry_or_review_queue_mutation",
    "guardrail_no_candidate_promotion",
)

_FORBIDDEN_SKELETON_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_assistance_execution",
    "callable_assistance_builder",
    "live_contract_validation_execution",
    "live_input_processing",
    "live_output_generation",
    "assistant_behavior",
    "auxiliar_behavior",
    "copilot_behavior",
    "pilot_behavior",
    "assistant_activation",
    "shadow_mode_activation",
    "observation_transformation",
    "review_evidence_builder",
    "route_comparison_execution",
    "route_selection",
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
    "human_decision_recording",
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
)

_SKELETON_INVARIANTS: Final[tuple[str, ...]] = (
    "m29_is_design_only",
    "m29_defines_auxiliar_assistant_assistance_skeleton_limits_only",
    "m29_has_no_callable_assistance_builder",
    "m29_does_not_validate_live_contracts",
    "m29_does_not_process_input_or_generate_output",
    "m29_does_not_compare_or_select_routes",
    "m29_does_not_select_or_load_prompts",
    "m29_does_not_start_auxiliar_assistant_or_copilot_behavior",
    "m29_does_not_activate_shadow_mode",
    "m29_does_not_grant_runtime_router_or_prompt_loader_authority",
    "m29_does_not_record_human_decisions",
    "m29_does_not_persist_or_mutate_project_state",
    "future_assistance_must_remain_non_authoritative_human_review_support_only",
    "m30_requires_separate_governed_implementation_gate_design",
)

_ASSISTANCE_SKELETON_DESIGN: Final[AuxiliarAssistantAssistanceSkeletonDesign] = AuxiliarAssistantAssistanceSkeletonDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M29",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_live_assistance_execution",
    skeleton_design_status="static_slot_design_only_no_assistance_builder",
    live_assistance_status="not_implemented",
    input_processing_status="not_implemented",
    output_generation_status="not_implemented",
    live_validation_status="not_implemented",
    assistant_behavior_status="not_started",
    shadow_mode_status="not_active",
    runtime_authority_status="not_granted",
    required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
    future_assistance_slots=_FUTURE_ASSISTANCE_SLOTS,
    required_future_guardrails=_REQUIRED_FUTURE_GUARDRAILS,
    forbidden_skeleton_behaviors=_FORBIDDEN_SKELETON_BEHAVIORS,
    skeleton_invariants=_SKELETON_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m29_validation_freeze_and_separate_scope_review",
)


__all__ = ["build_auxiliar_assistant_assistance_skeleton_design"]


def build_auxiliar_assistant_assistance_skeleton_design() -> AuxiliarAssistantAssistanceSkeletonDesign:
    """Return the immutable design-only M29 assistance skeleton record.

    The function accepts no input and performs no validation, I/O, logging,
    persistence, route comparison, prompt loading, Assistant activation, provider
    calls, embedding work, candidate promotion, or runtime integration.
    """

    return _ASSISTANCE_SKELETON_DESIGN
