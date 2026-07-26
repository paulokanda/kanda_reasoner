# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_simulation_skeleton_design.py
"""P5 Pilot simulation skeleton design.

P5 defines a design-only skeleton for a future, opt-in, ephemeral Pilot simulation
review envelope. It provides static vocabulary for the order of future simulation
slots, but it does not implement a simulator, process inputs, generate outputs,
validate live payloads, compare routes, load prompts, persist records, or grant
Pilot/Copilot authority.
"""

from __future__ import annotations


__all__ = [
    'get_pilot_simulation_skeleton_design',
    'PilotSimulationSkeletonDesign',
    'PilotSimulationSkeletonSlotDesign',
    'PilotSimulationStageDesign',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_simulation_skeleton_design_v1"
SCHEMA_VERSION: Final[str] = "3.82-pilot-simulation-skeleton-design"
DESIGN_KIND: Final[str] = "pilot_simulation_skeleton_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P6 - Routing Signal Scorer v3 Pilot Review Evidence Design v1, only "
    "after P5 validation, freeze, startup freeze context refresh, and "
    "FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot Simulation Skeleton Design v1 defines only a static skeleton for a "
    "future non-authoritative, opt-in, ephemeral Pilot simulation review envelope. "
    "It does not run a simulator, process input, generate output, validate live "
    "payloads, compare routes, calculate scores, load prompts, persist records, "
    "train models, run batch mode, activate Limited Shadow Runtime, or grant "
    "Pilot/Copilot authority."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "Any future simulation skeleton slot that mentions disagreement evidence must "
    "remain inert until frozen-router reproduction has been proven under a later "
    "governed harness implementation."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
OPT_IN_PER_INVOCATION_REQUIRED: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0


@dataclass(frozen=True)
class PilotSimulationSkeletonSlotDesign:
    """Immutable design record for one future simulation skeleton slot."""

    slot_id: str
    display_name: str
    design_purpose: str
    allowed_future_material: str
    inert_placeholder_output: str
    required_gate_before_use: str
    forbidden_operation: str


@dataclass(frozen=True)
class PilotSimulationStageDesign:
    """Immutable design record for the ordering of future simulation stages."""

    stage_id: str
    sequence_label: str
    design_purpose: str
    required_previous_evidence: str
    fail_closed_condition: str
    human_review_requirement: str


@dataclass(frozen=True)
class PilotSimulationSkeletonDesign:
    """Immutable design-only P5 simulation skeleton boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    match_before_disagree_rule: str
    design_status: str
    simulation_status: str
    callable_simulator_status: str
    live_validation_status: str
    input_processing_status: str
    output_generation_status: str
    route_comparison_status: str
    projection_status: str
    report_generation_status: str
    pilot_status: str
    copilot_status: str
    runtime_authority_status: str
    prompt_loading_authority_status: str
    persistence_authority_status: str
    training_data_use_status: str
    batch_mode_status: str
    limited_shadow_runtime_status: str
    storage_status: str
    human_review_mandatory: bool
    opt_in_per_invocation_required: bool
    critical_boundary_error_budget: int
    required_preconditions: tuple[str, ...]
    skeleton_slots: tuple[PilotSimulationSkeletonSlotDesign, ...]
    stage_designs: tuple[PilotSimulationStageDesign, ...]
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
    "kanda_patch_delivery_root_drive_staging_canon_frozen",
    "startup_freeze_context_refreshed_after_p4",
    "freeze_memory_status_ok_after_p4",
    "human_request_explicitly_targets_p5_design_only_simulation_skeleton",
)

_SKELETON_SLOTS: Final[tuple[PilotSimulationSkeletonSlotDesign, ...]] = (
    PilotSimulationSkeletonSlotDesign(
        slot_id="invocation_envelope_placeholder",
        display_name="Invocation envelope placeholder",
        design_purpose="Name the future opt-in per-invocation review envelope without creating it.",
        allowed_future_material="Caller-supplied primitive summary fields under a later governed implementation scope.",
        inert_placeholder_output="No output in P5; placeholder only.",
        required_gate_before_use="A later implementation gate must authorize any envelope construction.",
        forbidden_operation="No live invocation, hidden state lookup, batch intake, or runtime activation.",
    ),
    PilotSimulationSkeletonSlotDesign(
        slot_id="contract_snapshot_placeholder",
        display_name="Contract snapshot placeholder",
        design_purpose="Reserve a future place for P2 contract-shaped evidence without validating it now.",
        allowed_future_material="A human-reviewed summary that claims conformance to the P2 contract design.",
        inert_placeholder_output="No validation result in P5; placeholder only.",
        required_gate_before_use="A later validator implementation gate must authorize live checks.",
        forbidden_operation="No live contract validation, input processing, or output generation.",
    ),
    PilotSimulationSkeletonSlotDesign(
        slot_id="reproduction_evidence_placeholder",
        display_name="Reproduction evidence placeholder",
        design_purpose="Reserve a future place for P4 reproduction evidence before any disagreement trust.",
        allowed_future_material="A separately governed exact-match reproduction evidence summary.",
        inert_placeholder_output="No certification in P5; placeholder only.",
        required_gate_before_use="A later harness implementation gate must prove match-before-disagree.",
        forbidden_operation="No reproduction harness run, gold loading, route comparison, or score calculation.",
    ),
    PilotSimulationSkeletonSlotDesign(
        slot_id="taxonomy_language_placeholder",
        display_name="Taxonomy language placeholder",
        design_purpose="Reserve a future place for descriptive P3 taxonomy language after reproduction evidence.",
        allowed_future_material="Descriptive human-review vocabulary only, never recommendation authority.",
        inert_placeholder_output="No taxonomy label in P5; placeholder only.",
        required_gate_before_use="Reproduction evidence and later review-evidence gate design must exist first.",
        forbidden_operation="No disagreement detection, disagreement scoring, recommendation, or route projection.",
    ),
    PilotSimulationSkeletonSlotDesign(
        slot_id="human_review_packet_placeholder",
        display_name="Human review packet placeholder",
        design_purpose="Reserve a future place for non-approving human review support evidence.",
        allowed_future_material="Human-readable summary fields only under a later evidence design.",
        inert_placeholder_output="No report or queue item in P5; placeholder only.",
        required_gate_before_use="A later review evidence gate milestone must define the packet boundary.",
        forbidden_operation="No report writing, queue writing, persistence, or human decision recording.",
    ),
    PilotSimulationSkeletonSlotDesign(
        slot_id="critical_boundary_blocker_placeholder",
        display_name="Critical boundary blocker placeholder",
        design_purpose="Reserve a future fail-closed place for authority, prompt-loading, persistence, or runtime conflicts.",
        allowed_future_material="Human-reviewed blocker descriptions only.",
        inert_placeholder_output="No automated blocking action in P5; placeholder only.",
        required_gate_before_use="A later implementation gate must define fail-closed handling before use.",
        forbidden_operation="No automated repair, no continuation after critical conflict, and no authority grant.",
    ),
)

_STAGE_DESIGNS: Final[tuple[PilotSimulationStageDesign, ...]] = (
    PilotSimulationStageDesign(
        stage_id="stage_1_opt_in_context_design",
        sequence_label="1",
        design_purpose="Future simulation must begin only from explicit per-invocation opt-in context.",
        required_previous_evidence="P5 design freeze and later implementation gate.",
        fail_closed_condition="Missing explicit opt-in blocks simulation.",
        human_review_requirement="Human reviewer sees that opt-in was explicit and case-local.",
    ),
    PilotSimulationStageDesign(
        stage_id="stage_2_contract_shape_design",
        sequence_label="2",
        design_purpose="Future simulation must remain shaped by the P2 contract before any narrative evidence.",
        required_previous_evidence="Explicit opt-in context and P2 contract traceability.",
        fail_closed_condition="Unknown or authority-like fields block simulation.",
        human_review_requirement="Human reviewer sees any field uncertainty before interpretation.",
    ),
    PilotSimulationStageDesign(
        stage_id="stage_3_reproduction_gate_design",
        sequence_label="3",
        design_purpose="Future simulation must require reproduction evidence before disagreement language is trusted.",
        required_previous_evidence="P4 match-before-disagree evidence from a later governed harness implementation.",
        fail_closed_condition="Absent exact match blocks disagreement trust.",
        human_review_requirement="Human reviewer confirms match evidence before taxonomy language is considered.",
    ),
    PilotSimulationStageDesign(
        stage_id="stage_4_taxonomy_language_design",
        sequence_label="4",
        design_purpose="Future simulation may only use descriptive taxonomy language after required evidence.",
        required_previous_evidence="Reproduction evidence and P3 taxonomy traceability.",
        fail_closed_condition="Any recommendation-like wording blocks use.",
        human_review_requirement="Human reviewer treats taxonomy language as review support, not approval.",
    ),
    PilotSimulationStageDesign(
        stage_id="stage_5_review_packet_design",
        sequence_label="5",
        design_purpose="Future simulation ends as non-authoritative human review support only.",
        required_previous_evidence="All previous stage evidence and zero critical boundary conflicts.",
        fail_closed_condition="Any non-none effect or authority drift blocks and invalidates the packet.",
        human_review_requirement="Human reviewer remains mandatory and no automatic approval is implied.",
    ),
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "run_simulation",
    "execute_simulation_stage",
    "build_simulation_record",
    "validate_live_payload",
    "process_input",
    "generate_output",
    "transform_observation",
    "load_gold_set",
    "read_freeze_memory",
    "read_prompt_library",
    "inspect_runtime_router",
    "compare_routes",
    "calculate_score",
    "certify_reproduction",
    "trust_disagreement_label",
    "detect_disagreement",
    "score_disagreement",
    "project_route",
    "recommend_route",
    "select_route",
    "select_prompt",
    "load_prompt",
    "write_report",
    "write_review_queue",
    "persist_simulation_record",
    "record_human_decision",
    "train_from_simulation",
    "run_batch_mode",
    "activate_limited_shadow_runtime",
    "promote_candidate",
    "call_provider",
    "use_embeddings",
)


def get_pilot_simulation_skeleton_design() -> PilotSimulationSkeletonDesign:
    """Return the immutable P5 simulation skeleton design record."""

    return PilotSimulationSkeletonDesign(
        feature_id=FEATURE_ID,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        milestone="P5",
        title="Pilot Simulation Skeleton Design v1",
        authority_statement=AUTHORITY_STATEMENT,
        match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
        design_status="design_only",
        simulation_status="not_implemented_design_only",
        callable_simulator_status="not_implemented",
        live_validation_status="not_implemented",
        input_processing_status="not_implemented",
        output_generation_status="not_implemented",
        route_comparison_status="not_implemented",
        projection_status="not_implemented",
        report_generation_status="not_implemented",
        pilot_status="not_implemented",
        copilot_status="not_implemented",
        runtime_authority_status="not_granted",
        prompt_loading_authority_status="not_granted",
        persistence_authority_status="not_granted",
        training_data_use_status="forbidden",
        batch_mode_status="forbidden",
        limited_shadow_runtime_status="forbidden",
        storage_status=STORAGE_STATUS,
        human_review_mandatory=HUMAN_REVIEW_MANDATORY,
        opt_in_per_invocation_required=OPT_IN_PER_INVOCATION_REQUIRED,
        critical_boundary_error_budget=CRITICAL_BOUNDARY_ERROR_BUDGET,
        required_preconditions=_REQUIRED_PRECONDITIONS,
        skeleton_slots=_SKELETON_SLOTS,
        stage_designs=_STAGE_DESIGNS,
        forbidden_operations=_FORBIDDEN_OPERATIONS,
        next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    )
