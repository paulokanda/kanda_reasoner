# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/non_runtime_pilot_candidate_readiness_gate.py
"""P10 non-runtime Pilot candidate readiness gate.

P10 declares a static readiness gate for the non-runtime Pilot candidate after
P9 contract conformance freeze. The record is non-runtime, non-authoritative,
and non-executable. It does not evaluate readiness live, process inputs, create
review packets, compare routes, load prompts, persist records, activate a field
test, start Copilot, start a lab test, or grant runtime authority.
"""

from __future__ import annotations


__all__ = [
    'get_non_runtime_pilot_candidate_readiness_gate_record',
    'PilotCandidateReadinessBlocker',
    'PilotCandidateReadinessGateRecord',
    'PilotCandidateReadinessOutcome',
    'PilotCandidateReadinessPrerequisite',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_non_runtime_pilot_candidate_readiness_gate_v1"
SCHEMA_VERSION: Final[str] = "3.87-non-runtime-pilot-candidate-readiness-gate"
DESIGN_KIND: Final[str] = "non_runtime_pilot_candidate_readiness_gate_only"
PILOT_CANDIDATE_SOURCE_MILESTONE: Final[str] = "P8"
CONTRACT_CONFORMANCE_SOURCE_MILESTONE: Final[str] = "P9"
READINESS_GATE_STATUS: Final[str] = "static_gate_criteria_declaration_only"
LIVE_GATE_EVALUATION_STATUS: Final[str] = "not_present_in_p10"
REVIEW_PACKET_STATUS: Final[str] = "not_created_in_p10"
LAB_TEST_STATUS: Final[str] = "not_started_in_p10"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P11 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Review "
    "Evidence Packet v1, only after P10 validation, freeze, startup freeze "
    "context refresh, and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Non-Runtime Pilot Candidate Readiness Gate v1 is a static gate criteria "
    "declaration only. It is not a live gate evaluator, not a readiness "
    "approval, not a review packet, not a lab test, not a field test, not a "
    "Pilot runtime, not a Copilot, not a router, not a prompt loader, not a "
    "persistence writer, not training data, not batch mode, and not authority. "
    "Human governance and the real router remain authoritative."
)
GATE_RULE: Final[str] = (
    "P10 may declare readiness prerequisites, blocker classes, and allowed "
    "non-authoritative gate outcome names, but it cannot evaluate live cases "
    "or approve activation."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "Candidate readiness cannot be claimed until frozen contract conformance, "
    "future review evidence, and reproduction-before-disagreement constraints "
    "remain satisfied."
)
ACTIVATION_GATE_DEFERRED_RULE: Final[str] = (
    "Any activation key or maturity on/off behavior remains deferred to a "
    "separate Activation Gate Box after lab testing and maturity evidence."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
OPT_IN_PER_INVOCATION_REQUIRED: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
FIELD_TEST_STATUS: Final[str] = "not_allowed_in_p10"
DEFINITIVE_ENABLEMENT_STATUS: Final[str] = "not_allowed_in_p10"
COPILOT_STATUS: Final[str] = "not_started_in_p10"
LAB_TEST_CODING_STATUS: Final[str] = "not_started_in_p10"

ALLOWED_GATE_OUTCOMES: Final[tuple[str, ...]] = (
    "blocked",
    "not_blocked_for_separate_governed_review_packet_design",
)
FORBIDDEN_GATE_OUTCOMES: Final[tuple[str, ...]] = (
    "approved",
    "ready",
    "enabled",
    "activated",
    "promoted",
    "runtime_permitted",
    "field_test_enabled",
    "definitive_enablement",
    "copilot_started",
    "lab_test_started",
)

REQUIRED_READINESS_PREREQUISITES: Final[tuple[str, ...]] = (
    "RG-PILOT-000 router canon frozen with FREEZE_MEMORY_STATUS OK",
    "M35 bridge closure frozen with FREEZE_MEMORY_STATUS OK",
    "P0 scope charter and entry gate frozen with FREEZE_MEMORY_STATUS OK",
    "P1 Pilot boundary frozen with FREEZE_MEMORY_STATUS OK",
    "P2 input/output contract design frozen with FREEZE_MEMORY_STATUS OK",
    "P3 disagreement taxonomy frozen with FREEZE_MEMORY_STATUS OK",
    "P4 reproduction harness design frozen with FREEZE_MEMORY_STATUS OK",
    "P5 simulation skeleton design frozen with FREEZE_MEMORY_STATUS OK",
    "P6 review evidence design frozen with FREEZE_MEMORY_STATUS OK",
    "P7 implementation gate design frozen with FREEZE_MEMORY_STATUS OK",
    "P8 non-runtime Pilot candidate frozen with FREEZE_MEMORY_STATUS OK",
    "P9 contract conformance frozen with FREEZE_MEMORY_STATUS OK",
    "KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 frozen and used",
)

BLOCKER_CLASSES: Final[tuple[str, ...]] = (
    "runtime_authority_leak",
    "prompt_loading_leak",
    "persistence_leak",
    "route_authority_leak",
    "copilot_scope_leak",
    "activation_or_field_test_leak",
    "batch_mode_or_training_data_leak",
    "gold_or_registry_mutation_leak",
    "review_or_human_decision_recording_leak",
    "private_reach_in_or_box_boundary_leak",
    "missing_freeze_or_freeze_memory_status_not_ok",
    "missing_future_review_evidence_packet",
    "missing_future_lab_warning_confirmation",
)

FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "evaluate_live_readiness",
    "approve_readiness",
    "mark_ready",
    "enable_candidate",
    "activate_field_test",
    "activate_definitive_enablement",
    "start_lab_test",
    "create_lab_cases",
    "run_lab_test",
    "build_review_packet",
    "collect_evidence",
    "record_human_decision",
    "record_approval",
    "validate_live_payload",
    "process_input",
    "generate_output",
    "transform_payload",
    "project_route",
    "recommend_route",
    "select_route",
    "override_route",
    "execute_route",
    "compare_routes",
    "inspect_runtime_router",
    "load_gold_set",
    "read_freeze_memory",
    "read_prompt_library",
    "select_prompt",
    "load_prompt",
    "persist_record",
    "write_report",
    "write_review_queue",
    "write_gold",
    "write_registry",
    "write_freeze_memory",
    "call_provider",
    "use_embeddings",
    "train_from_output",
    "run_batch_mode",
    "activate_pilot",
    "activate_copilot",
    "activate_limited_shadow_runtime",
    "promote_candidate",
)


@dataclass(frozen=True)
class PilotCandidateReadinessPrerequisite:
    """Immutable static prerequisite for the P10 readiness gate."""

    prerequisite_id: str
    required_state: str
    failure_policy: str


@dataclass(frozen=True)
class PilotCandidateReadinessBlocker:
    """Immutable blocker category for P10."""

    blocker_id: str
    blocker_kind: str
    effect: str


@dataclass(frozen=True)
class PilotCandidateReadinessOutcome:
    """Immutable allowed or forbidden outcome name."""

    outcome_id: str
    status: str
    meaning: str


@dataclass(frozen=True)
class PilotCandidateReadinessGateRecord:
    """Immutable P10 static readiness gate record.

    This record is intentionally inert. It describes gate prerequisites,
    blocker categories, allowed outcome names, forbidden outcome names, and
    fixed no-effect constants. It does not evaluate readiness or activate any
    Pilot/Copilot or lab-test behavior.
    """

    feature_id: str
    schema_version: str
    design_kind: str
    title: str
    pilot_candidate_source_milestone: str
    contract_conformance_source_milestone: str
    readiness_gate_status: str
    live_gate_evaluation_status: str
    review_packet_status: str
    lab_test_status: str
    authority_statement: str
    gate_rule: str
    match_before_disagree_rule: str
    activation_gate_deferred_rule: str
    prerequisites: tuple[PilotCandidateReadinessPrerequisite, ...]
    blockers: tuple[PilotCandidateReadinessBlocker, ...]
    allowed_outcomes: tuple[PilotCandidateReadinessOutcome, ...]
    forbidden_outcomes: tuple[PilotCandidateReadinessOutcome, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_PREREQUISITES: Final[tuple[PilotCandidateReadinessPrerequisite, ...]] = tuple(
    PilotCandidateReadinessPrerequisite(
        prerequisite_id=f"readiness_prerequisite_{index:02d}",
        required_state=value,
        failure_policy="block_progression",
    )
    for index, value in enumerate(REQUIRED_READINESS_PREREQUISITES, start=1)
)

_BLOCKERS: Final[tuple[PilotCandidateReadinessBlocker, ...]] = tuple(
    PilotCandidateReadinessBlocker(
        blocker_id=value,
        blocker_kind="critical_boundary_blocker",
        effect="block_progression",
    )
    for value in BLOCKER_CLASSES
)

_ALLOWED_OUTCOMES: Final[tuple[PilotCandidateReadinessOutcome, ...]] = tuple(
    PilotCandidateReadinessOutcome(
        outcome_id=value,
        status="allowed_static_name_only",
        meaning="May be named by future governed review, but P10 does not compute it.",
    )
    for value in ALLOWED_GATE_OUTCOMES
)

_FORBIDDEN_OUTCOMES: Final[tuple[PilotCandidateReadinessOutcome, ...]] = tuple(
    PilotCandidateReadinessOutcome(
        outcome_id=value,
        status="forbidden_in_p10",
        meaning="Would imply authority, activation, promotion, or lab-test start.",
    )
    for value in FORBIDDEN_GATE_OUTCOMES
)

_RECORD: Final[PilotCandidateReadinessGateRecord] = PilotCandidateReadinessGateRecord(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    title="Non-Runtime Pilot Candidate Readiness Gate v1",
    pilot_candidate_source_milestone=PILOT_CANDIDATE_SOURCE_MILESTONE,
    contract_conformance_source_milestone=CONTRACT_CONFORMANCE_SOURCE_MILESTONE,
    readiness_gate_status=READINESS_GATE_STATUS,
    live_gate_evaluation_status=LIVE_GATE_EVALUATION_STATUS,
    review_packet_status=REVIEW_PACKET_STATUS,
    lab_test_status=LAB_TEST_STATUS,
    authority_statement=AUTHORITY_STATEMENT,
    gate_rule=GATE_RULE,
    match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
    activation_gate_deferred_rule=ACTIVATION_GATE_DEFERRED_RULE,
    prerequisites=_PREREQUISITES,
    blockers=_BLOCKERS,
    allowed_outcomes=_ALLOWED_OUTCOMES,
    forbidden_outcomes=_FORBIDDEN_OUTCOMES,
    forbidden_operations=FORBIDDEN_OPERATIONS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def get_non_runtime_pilot_candidate_readiness_gate_record() -> PilotCandidateReadinessGateRecord:
    """Return the immutable P10 non-runtime readiness gate record."""

    return _RECORD
