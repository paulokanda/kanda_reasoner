"""Design-only M30 Auxiliar/Assistant implementation gate design.

M30 defines static implementation-gate requirements that must be satisfied before
any later non-runtime Auxiliar/Assistant assistance implementation may be
considered. It is a design record only. It does not run a gate, inspect runtime
state, read freeze memory, process input, generate output, build assistance,
compare routes, select routes, select prompts, write files, persist evidence,
record human decisions, call providers, use embeddings, activate shadow mode,
start Assistant behavior, promote candidates, or grant runtime authority.

The only public entry point returns a deterministic immutable gate-design record.
Any executable gate evaluation or assistance implementation belongs to a later
separately governed milestone after explicit human confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_auxiliar_assistant_implementation_gate_design_v1"
SCHEMA_VERSION: Final[str] = "3.71-auxiliar-assistant-implementation-gate-design"
DESIGN_KIND: Final[str] = "post_adviser_auxiliar_assistant_implementation_gate_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M31 - Routing Signal Scorer v3 Non Runtime Auxiliar/Assistant Assistance Implementation v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Auxiliar/Assistant implementation gate design describes future "
    "pre-implementation gate limits only. It is not a live gate, not an "
    "implementation permission grant, not Assistant activation, not Auxiliar "
    "behavior, and has no routing effect, no route-selection effect, no "
    "prompt-loading effect, no persistence effect, no human-decision effect, "
    "no candidate-promotion effect, no shadow-mode activation effect, no "
    "runtime authority, and no Copilot/Pilot behavior."
)


@dataclass(frozen=True)
class AuxiliarAssistantImplementationGateCriterionDesign:
    """Immutable description of one future implementation-gate criterion."""

    criterion_id: str
    criterion_group: str
    required_status: str
    blocking_failure: str
    description: str


@dataclass(frozen=True)
class AuxiliarAssistantImplementationGateOutcomeDesign:
    """Immutable description of one allowed future implementation-gate outcome."""

    outcome_id: str
    meaning: str
    allowed_use: str
    blocked_interpretation: str


@dataclass(frozen=True)
class AuxiliarAssistantImplementationGateDesign:
    """Immutable design-only M30 Auxiliar/Assistant implementation gate record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    gate_design_status: str
    live_gate_execution_status: str
    assistance_implementation_status: str
    assistant_behavior_status: str
    shadow_mode_status: str
    runtime_authority_status: str
    required_preconditions: tuple[str, ...]
    allowed_gate_outcomes: tuple[AuxiliarAssistantImplementationGateOutcomeDesign, ...]
    required_frozen_milestone_criteria: tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]
    critical_boundary_failure_criteria: tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]
    human_review_criteria: tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]
    later_m31_constraints: tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]
    forbidden_gate_behaviors: tuple[str, ...]
    gate_invariants: tuple[str, ...]
    next_allowed_milestone: str
    implementation_gate: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
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
    "m29_auxiliar_assistant_assistance_skeleton_design_frozen",
    "freezememory_status_ok_before_later_m31_implementation",
    "explicit_human_confirmation_required_before_m31_implementation",
)

_ALLOWED_GATE_OUTCOMES: Final[tuple[AuxiliarAssistantImplementationGateOutcomeDesign, ...]] = (
    AuxiliarAssistantImplementationGateOutcomeDesign(
        outcome_id="blocked",
        meaning="A future gate evaluation would stop movement toward M31 until the blocking issue is resolved.",
        allowed_use="May be used only as non-authoritative design evidence for human review.",
        blocked_interpretation="Must not be interpreted as permission to implement, activate Assistant behavior, route, load prompts, persist, or promote candidates.",
    ),
    AuxiliarAssistantImplementationGateOutcomeDesign(
        outcome_id="not_blocked_for_separate_human_review",
        meaning="A future gate evaluation would have found no designed blocker, but still requires separate human review before any M31 patch.",
        allowed_use="May only allow a separate human-reviewed M31 scope discussion.",
        blocked_interpretation="Must not be interpreted as automatic implementation approval, Assistant activation, shadow-mode activation, or runtime authority.",
    ),
)

_REQUIRED_FROZEN_MILESTONE_CRITERIA: Final[tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]] = (
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m18_to_m22_shadow_design_chain_confirmed",
        criterion_group="frozen_milestone_chain",
        required_status="m18_m19_m20_m21_m22_frozen_with_freezememory_ok",
        blocking_failure="early_shadow_design_chain_missing_or_not_confirmed",
        description="The M18-M22 shadow-mode design and gate chain must be frozen before any later Auxiliar/Assistant implementation gate can pass.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m23_to_m25_shadow_transition_chain_confirmed",
        criterion_group="frozen_milestone_chain",
        required_status="m23_m24_m25_frozen_with_freezememory_ok",
        blocking_failure="shadow_transition_chain_missing_or_not_confirmed",
        description="The M23-M25 non-runtime observation, review evidence design, and Assistant-boundary readiness gate chain must be frozen.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m26_auxiliar_assistant_boundary_freeze_confirmed",
        criterion_group="frozen_milestone_chain",
        required_status="m26_frozen_with_freezememory_ok",
        blocking_failure="m26_missing_or_not_confirmed",
        description="M26 Auxiliar/Assistant boundary design must be frozen before any future implementation gate can pass.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m27_auxiliar_assistant_io_contract_freeze_confirmed",
        criterion_group="frozen_milestone_chain",
        required_status="m27_frozen_with_freezememory_ok",
        blocking_failure="m27_missing_or_not_confirmed",
        description="M27 Auxiliar/Assistant input/output contract design must be frozen before any future implementation gate can pass.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m28_auxiliar_assistant_contract_validator_freeze_confirmed",
        criterion_group="frozen_milestone_chain",
        required_status="m28_frozen_with_freezememory_ok",
        blocking_failure="m28_missing_or_not_confirmed",
        description="M28 Auxiliar/Assistant contract validator design must be frozen before any future implementation gate can pass.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m29_auxiliar_assistant_assistance_skeleton_freeze_confirmed",
        criterion_group="frozen_milestone_chain",
        required_status="m29_frozen_with_freezememory_ok",
        blocking_failure="m29_missing_or_not_confirmed",
        description="M29 Auxiliar/Assistant assistance skeleton design must be frozen before any future implementation gate can pass.",
    ),
)

_CRITICAL_BOUNDARY_FAILURE_CRITERIA: Final[tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]] = (
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="runtime_import_boundary_clean",
        criterion_group="critical_boundary_failure",
        required_status="no_runtime_router_prompt_loader_or_app_imports",
        blocking_failure="runtime_or_prompt_loader_coupling_detected",
        description="Any runtime router, prompt loader, or app integration import blocks movement toward M31.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="side_effect_boundary_clean",
        criterion_group="critical_boundary_failure",
        required_status="no_file_io_no_persistence_no_logging_no_console_io",
        blocking_failure="side_effect_or_persistence_detected",
        description="Any file IO, persistence, logging, report writing, review queue writing, or console IO blocks movement toward M31.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="authority_boundary_clean",
        criterion_group="critical_boundary_failure",
        required_status="no_route_prompt_freeze_gold_registry_human_decision_or_candidate_authority",
        blocking_failure="authority_leak_detected",
        description="Any route, prompt, freeze, gold, registry, human-decision, or candidate-promotion authority blocks movement toward M31.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="assistant_activation_boundary_clean",
        criterion_group="critical_boundary_failure",
        required_status="assistant_auxiliar_copilot_and_pilot_behavior_not_started",
        blocking_failure="assistant_or_copilot_behavior_detected",
        description="Any live Assistant, Auxiliar, Copilot, or Pilot behavior blocks movement toward M31.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="future_assistance_scope_boundary_clean",
        criterion_group="critical_boundary_failure",
        required_status="future_m31_scope_is_non_runtime_in_memory_human_review_support_only",
        blocking_failure="future_scope_grants_runtime_authority_or_action",
        description="A later M31 scope must remain non-runtime, in-memory, non-authoritative human-review support only.",
    ),
)

_HUMAN_REVIEW_CRITERIA: Final[tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]] = (
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="human_confirms_m31_scope_separately",
        criterion_group="human_review_boundary",
        required_status="separate_human_confirmation_required",
        blocking_failure="no_separate_human_confirmation",
        description="Even a clean future gate cannot create M31 automatically; a separate human-confirmed patch scope is required.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="validation_evidence_reviewed",
        criterion_group="human_review_boundary",
        required_status="validation_evidence_reviewed_by_human",
        blocking_failure="validation_evidence_missing_or_stale",
        description="Human review must confirm current validation evidence belongs to the exact current feature, not a stale sidecar.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="freeze_context_reviewed",
        criterion_group="human_review_boundary",
        required_status="freezememory_status_ok_and_startup_context_refreshed",
        blocking_failure="freeze_context_not_current",
        description="Human review must confirm project freeze memory is current and startup freeze context is refreshed.",
    ),
)

_LATER_M31_CONSTRAINTS: Final[tuple[AuxiliarAssistantImplementationGateCriterionDesign, ...]] = (
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m31_may_be_non_runtime_only",
        criterion_group="later_m31_constraint",
        required_status="pure_in_memory_non_runtime_only",
        blocking_failure="runtime_execution_or_app_integration_planned",
        description="A later M31 patch may only be pure in-memory and must not run inside the real router or app runtime.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m31_may_use_validated_primitives_only",
        criterion_group="later_m31_constraint",
        required_status="m28_validated_caller_supplied_primitives_only",
        blocking_failure="live_objects_or_discovery_planned",
        description="A later M31 patch may only use caller-supplied primitive data validated by a separately governed validator implementation.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m31_must_follow_m29_skeleton_slots",
        criterion_group="later_m31_constraint",
        required_status="m29_skeleton_slots_preserved_without_authority_expansion",
        blocking_failure="assistance_skeleton_expands_authority_or_actions",
        description="A later M31 patch must stay within the M29 skeleton slots and must not add route, prompt, persistence, human-decision, or promotion effects.",
    ),
    AuxiliarAssistantImplementationGateCriterionDesign(
        criterion_id="m31_may_return_one_non_authoritative_assistance_record",
        criterion_group="later_m31_constraint",
        required_status="single_in_memory_non_authoritative_human_review_support_record_only",
        blocking_failure="persistence_report_queue_decision_or_authority_planned",
        description="A later M31 patch may only return one in-memory non-authoritative assistance record and must not persist, report, queue, or decide anything.",
    ),
)

_FORBIDDEN_GATE_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_implementation_gate_execution",
    "callable_gate_entrypoint",
    "automatic_scope_confirmation",
    "implementation_permission_grant",
    "runtime_state_inspection",
    "freeze_memory_reading",
    "source_scanning",
    "case_discovery",
    "live_assistance_execution",
    "callable_assistance_builder",
    "live_contract_validation_execution",
    "input_processing",
    "output_generation",
    "observation_transformation",
    "review_evidence_builder",
    "route_comparison",
    "route_selection",
    "prompt_selection",
    "prompt_loading",
    "assistant_behavior",
    "auxiliar_behavior",
    "copilot_behavior",
    "pilot_behavior",
    "assistant_activation",
    "shadow_mode_activation",
    "runtime_router_import",
    "runtime_router_export",
    "runtime_integration",
    "router_authority",
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
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
)

_GATE_INVARIANTS: Final[tuple[str, ...]] = (
    "m30_is_design_only",
    "m30_defines_auxiliar_assistant_implementation_gate_limits_only",
    "m30_has_no_callable_gate_entrypoint",
    "m30_does_not_evaluate_live_project_state",
    "m30_does_not_read_freeze_memory_or_source_files",
    "m30_does_not_authorize_m31_by_itself",
    "m30_does_not_implement_assistance_logic",
    "m30_does_not_process_input_or_generate_output",
    "m30_does_not_compare_or_select_routes",
    "m30_does_not_select_or_load_prompts",
    "m30_does_not_start_auxiliar_assistant_or_copilot_behavior",
    "m30_does_not_activate_shadow_mode",
    "m30_does_not_grant_runtime_router_or_prompt_loader_authority",
    "m30_does_not_record_human_decisions",
    "m30_does_not_persist_or_mutate_project_state",
    "future_m31_requires_separate_human_confirmation_after_m30_freeze",
)

_IMPLEMENTATION_GATE_DESIGN: Final[AuxiliarAssistantImplementationGateDesign] = AuxiliarAssistantImplementationGateDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M30",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_live_implementation_gate_execution",
    gate_design_status="static_gate_design_only_no_callable_gate_entrypoint",
    live_gate_execution_status="not_implemented",
    assistance_implementation_status="not_implemented",
    assistant_behavior_status="not_started",
    shadow_mode_status="not_active",
    runtime_authority_status="not_granted",
    required_preconditions=_REQUIRED_PRECONDITIONS,
    allowed_gate_outcomes=_ALLOWED_GATE_OUTCOMES,
    required_frozen_milestone_criteria=_REQUIRED_FROZEN_MILESTONE_CRITERIA,
    critical_boundary_failure_criteria=_CRITICAL_BOUNDARY_FAILURE_CRITERIA,
    human_review_criteria=_HUMAN_REVIEW_CRITERIA,
    later_m31_constraints=_LATER_M31_CONSTRAINTS,
    forbidden_gate_behaviors=_FORBIDDEN_GATE_BEHAVIORS,
    gate_invariants=_GATE_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m30_validation_freeze_and_separate_scope_review",
)


__all__ = ["build_auxiliar_assistant_implementation_gate_design"]


def build_auxiliar_assistant_implementation_gate_design() -> AuxiliarAssistantImplementationGateDesign:
    """Return the immutable design-only M30 implementation gate record.

    The function accepts no input and performs no live gate evaluation, source
    scanning, freeze-memory reading, validation, I/O, logging, persistence,
    assistance building, route comparison, prompt loading, Assistant activation,
    provider calls, embedding work, candidate promotion, or runtime integration.
    """

    return _IMPLEMENTATION_GATE_DESIGN
