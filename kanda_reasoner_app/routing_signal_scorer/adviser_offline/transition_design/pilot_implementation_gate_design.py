# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_implementation_gate_design.py
"""P7 Pilot implementation gate design.

P7 defines static fail-closed gate conditions for a future, separately governed,
non-runtime Pilot candidate implementation milestone. It is a design-only
artifact. It does not evaluate a gate, approve work, create a Pilot, process
input, generate output, compare routes, load prompts, persist records, or grant
runtime authority.
"""

from __future__ import annotations


__all__ = [
    'get_pilot_implementation_gate_design',
    'PilotImplementationGateConditionDesign',
    'PilotImplementationGateDesign',
    'PilotImplementationGateStageDesign',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_implementation_gate_design_v1"
SCHEMA_VERSION: Final[str] = "3.84-pilot-implementation-gate-design"
DESIGN_KIND: Final[str] = "pilot_implementation_gate_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P8 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Implementation v1, "
    "only after P7 validation, freeze, startup freeze context refresh, and "
    "FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot Implementation Gate Design v1 defines only static preconditions and "
    "fail-closed gate language for a future non-runtime Pilot candidate. It does "
    "not evaluate a gate, approve implementation, create Pilot behavior, process "
    "input, generate output, compare routes, load prompts, persist records, run "
    "batch mode, activate Limited Shadow Runtime, or grant runtime authority."
)
GATE_SCOPE_STATEMENT: Final[str] = (
    "P7 is not the Pilot implementation. It is the final design-only gate before "
    "any later non-runtime Pilot candidate implementation may be considered."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "Any later implementation candidate must reproduce frozen router/canon "
    "outcomes before disagreement or taxonomy evidence can be trusted. If "
    "reproduction evidence is absent, the gate remains closed."
)
HUMAN_REVIEW_RULE: Final[str] = (
    "Human review is mandatory for any future Pilot candidate, but P7 records no "
    "human decision; human review is not approval and does not grant authority."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
OPT_IN_PER_INVOCATION_REQUIRED: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
GATE_DEFAULT_STATE: Final[str] = "closed_design_only"
IMPLEMENTATION_AUTHORIZATION_STATUS: Final[str] = "not_granted"


@dataclass(frozen=True)
class PilotImplementationGateConditionDesign:
    """Immutable design record for one future gate condition."""

    condition_id: str
    design_purpose: str
    required_evidence: str
    blocked_when_missing: str
    forbidden_shortcut: str


@dataclass(frozen=True)
class PilotImplementationGateStageDesign:
    """Immutable design record for one future gate stage."""

    stage_id: str
    sequence_label: str
    design_purpose: str
    required_conditions: tuple[str, ...]
    fail_closed_rule: str
    next_stage_if_later_satisfied: str


@dataclass(frozen=True)
class PilotImplementationGateDesign:
    """Immutable design-only P7 gate boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    gate_scope_statement: str
    match_before_disagree_rule: str
    human_review_rule: str
    design_status: str
    gate_evaluation_status: str
    implementation_authorization_status: str
    pilot_candidate_creation_status: str
    callable_pilot_status: str
    live_validation_status: str
    input_processing_status: str
    output_generation_status: str
    evidence_collection_status: str
    evidence_packet_generation_status: str
    simulation_execution_status: str
    reproduction_harness_execution_status: str
    route_comparison_status: str
    metric_calculation_status: str
    disagreement_trust_status: str
    prompt_loading_authority_status: str
    persistence_authority_status: str
    training_data_use_status: str
    batch_mode_status: str
    limited_shadow_runtime_status: str
    runtime_authority_status: str
    storage_status: str
    human_review_mandatory: bool
    opt_in_per_invocation_required: bool
    critical_boundary_error_budget: int
    gate_default_state: str
    required_preconditions: tuple[str, ...]
    gate_conditions: tuple[PilotImplementationGateConditionDesign, ...]
    gate_stages: tuple[PilotImplementationGateStageDesign, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
    "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
    "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
    "p1_pilot_boundary_design_frozen",
    "p2_pilot_input_output_contract_validator_design_frozen",
    "p3_pilot_disagreement_taxonomy_design_frozen",
    "p4_pilot_gold_frozen_router_reproduction_harness_design_frozen",
    "p5_pilot_simulation_skeleton_design_frozen",
    "p6_pilot_review_evidence_design_frozen",
    "kanda_patch_delivery_root_drive_staging_canon_frozen",
    "startup_freeze_context_refreshed_after_p6",
    "freeze_memory_status_ok_after_p6",
    "human_request_explicitly_targets_p7_design_only_implementation_gate",
)

_GATE_CONDITIONS: Final[tuple[PilotImplementationGateConditionDesign, ...]] = (
    PilotImplementationGateConditionDesign(
        condition_id="prior_freeze_chain_complete",
        design_purpose="Require the entire M35/RG-PILOT-000/P0-P6 chain before any later candidate can be considered.",
        required_evidence="Freeze records and startup freeze context showing every prior milestone frozen with FREEZE_MEMORY_STATUS OK.",
        blocked_when_missing="The later Pilot candidate implementation path is blocked and remains closed.",
        forbidden_shortcut="Do not infer readiness from source files alone or from an assistant assertion.",
    ),
    PilotImplementationGateConditionDesign(
        condition_id="root_drive_installer_canon_preserved",
        design_purpose="Require the governed installer canon before delivering any later candidate implementation patch.",
        required_evidence="KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 frozen and used in delivery commands.",
        blocked_when_missing="Patch delivery remains blocked until the installer canon is restored.",
        forbidden_shortcut="Do not use Downloads/Desktop-first or non-staged generic installers.",
    ),
    PilotImplementationGateConditionDesign(
        condition_id="scope_is_non_runtime_pilot_candidate_only",
        design_purpose="Limit any later P8 candidate to non-runtime, opt-in, case-local, in-memory-only Pilot behavior.",
        required_evidence="Future P8 scope text explicitly excludes Copilot, runtime router integration, prompt loading, persistence, training-data use, and batch mode.",
        blocked_when_missing="Any broader runtime, Copilot, prompt-loading, or persistent scope is blocked.",
        forbidden_shortcut="Do not treat P7 as authorization for Copilot or runtime activation.",
    ),
    PilotImplementationGateConditionDesign(
        condition_id="match_before_disagree_preserved",
        design_purpose="Keep frozen-router reproduction before disagreement trust as a hard future gate.",
        required_evidence="Future implementation must expose reproduction-before-taxonomy traceability without trusting disagreement first.",
        blocked_when_missing="Disagreement language is blocked from trust and remains descriptive.",
        forbidden_shortcut="Do not promote taxonomy labels, scores, or recommendations before reproduction evidence.",
    ),
    PilotImplementationGateConditionDesign(
        condition_id="critical_boundary_error_budget_zero",
        design_purpose="Block any later candidate that violates authority, prompt loading, persistence, training, batch, or runtime boundaries.",
        required_evidence="Tests for zero critical boundary errors and explicit false runtime flags.",
        blocked_when_missing="Later implementation is blocked and must fail validation.",
        forbidden_shortcut="Do not downgrade critical boundary errors to warnings.",
    ),
    PilotImplementationGateConditionDesign(
        condition_id="human_review_mandatory_not_approval",
        design_purpose="Preserve human review as mandatory visibility without granting approval or decision recording.",
        required_evidence="Future packet text states human review mandatory, not approval, not route authority, and not persistent decision record.",
        blocked_when_missing="Future candidate output is blocked from presenting itself as approved or authoritative.",
        forbidden_shortcut="Do not record approvals, grant route approval automatically, or substitute reviewer visibility for governance.",
    ),
)

_GATE_STAGES: Final[tuple[PilotImplementationGateStageDesign, ...]] = (
    PilotImplementationGateStageDesign(
        stage_id="stage_1_freeze_chain_and_delivery_canon",
        sequence_label="1",
        design_purpose="Confirm prior frozen design and installer canon prerequisites before future implementation scope is considered.",
        required_conditions=("prior_freeze_chain_complete", "root_drive_installer_canon_preserved"),
        fail_closed_rule="If either prerequisite is absent, do not design or deliver a Pilot candidate implementation.",
        next_stage_if_later_satisfied="stage_2_scope_boundary",
    ),
    PilotImplementationGateStageDesign(
        stage_id="stage_2_scope_boundary",
        sequence_label="2",
        design_purpose="Constrain the next milestone to a non-runtime Pilot candidate only.",
        required_conditions=("scope_is_non_runtime_pilot_candidate_only",),
        fail_closed_rule="If Copilot, runtime, persistence, prompt loading, batch, provider, or training scope appears, block.",
        next_stage_if_later_satisfied="stage_3_safety_invariants",
    ),
    PilotImplementationGateStageDesign(
        stage_id="stage_3_safety_invariants",
        sequence_label="3",
        design_purpose="Require match-before-disagree, zero critical boundary errors, and human review visibility.",
        required_conditions=(
            "match_before_disagree_preserved",
            "critical_boundary_error_budget_zero",
            "human_review_mandatory_not_approval",
        ),
        fail_closed_rule="If any invariant is missing or weakened, the future implementation path remains closed.",
        next_stage_if_later_satisfied="P8 may be designed as a separate governed non-runtime Pilot candidate implementation milestone only.",
    ),
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "evaluate_gate",
    "approve_implementation",
    "authorize_pilot",
    "create_pilot_candidate",
    "run_pilot_candidate",
    "activate_pilot",
    "activate_copilot",
    "validate_live_payload",
    "process_input",
    "generate_output",
    "collect_evidence",
    "build_evidence_packet",
    "run_simulation",
    "run_reproduction_harness",
    "load_gold_set",
    "read_freeze_memory",
    "read_prompt_library",
    "inspect_runtime_router",
    "compare_routes",
    "calculate_metric",
    "detect_disagreement",
    "score_disagreement",
    "trust_disagreement",
    "project_route",
    "recommend_route",
    "select_prompt",
    "load_prompt",
    "persist_record",
    "record_human_decision",
    "record_approval",
    "train_from_gate",
    "run_batch_mode",
    "activate_limited_shadow_runtime",
    "promote_candidate",
    "call_provider",
    "use_embeddings",
)

_DESIGN: Final[PilotImplementationGateDesign] = PilotImplementationGateDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="P7",
    title="Pilot Implementation Gate Design v1",
    authority_statement=AUTHORITY_STATEMENT,
    gate_scope_statement=GATE_SCOPE_STATEMENT,
    match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
    human_review_rule=HUMAN_REVIEW_RULE,
    design_status="design_only",
    gate_evaluation_status="not_implemented_design_only",
    implementation_authorization_status=IMPLEMENTATION_AUTHORIZATION_STATUS,
    pilot_candidate_creation_status="not_implemented",
    callable_pilot_status="not_implemented",
    live_validation_status="not_implemented",
    input_processing_status="not_implemented",
    output_generation_status="not_implemented",
    evidence_collection_status="not_implemented",
    evidence_packet_generation_status="not_implemented",
    simulation_execution_status="not_implemented",
    reproduction_harness_execution_status="not_implemented",
    route_comparison_status="not_implemented",
    metric_calculation_status="not_implemented",
    disagreement_trust_status="not_granted",
    prompt_loading_authority_status="not_granted",
    persistence_authority_status="not_granted",
    training_data_use_status="not_granted",
    batch_mode_status="not_implemented",
    limited_shadow_runtime_status="not_implemented",
    runtime_authority_status="not_granted",
    storage_status=STORAGE_STATUS,
    human_review_mandatory=HUMAN_REVIEW_MANDATORY,
    opt_in_per_invocation_required=OPT_IN_PER_INVOCATION_REQUIRED,
    critical_boundary_error_budget=CRITICAL_BOUNDARY_ERROR_BUDGET,
    gate_default_state=GATE_DEFAULT_STATE,
    required_preconditions=_REQUIRED_PRECONDITIONS,
    gate_conditions=_GATE_CONDITIONS,
    gate_stages=_GATE_STAGES,
    forbidden_operations=_FORBIDDEN_OPERATIONS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def get_pilot_implementation_gate_design() -> PilotImplementationGateDesign:
    """Return the immutable P7 design-only gate record."""

    return _DESIGN
