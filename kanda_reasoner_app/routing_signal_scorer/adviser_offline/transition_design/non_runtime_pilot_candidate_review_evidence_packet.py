# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/non_runtime_pilot_candidate_review_evidence_packet.py
"""P11 non-runtime Pilot candidate review evidence packet declaration.

P11 declares the static shape of a future human-review evidence packet for the
non-runtime Pilot candidate after P10 readiness gate freeze. The record is
inert, immutable, and non-authoritative. It does not collect evidence, build
packets from cases, write reports, persist records, start the test lab, activate
field testing, start Copilot, compare routes, load prompts, call providers, use
embeddings, train from output, or grant runtime authority.
"""

from __future__ import annotations


__all__ = [
    'get_non_runtime_pilot_candidate_review_evidence_packet_record',
    'PilotCandidateReviewEvidenceBoundary',
    'PilotCandidateReviewEvidencePacketRecord',
    'PilotCandidateReviewEvidenceSection',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_non_runtime_pilot_candidate_review_evidence_packet_v1"
SCHEMA_VERSION: Final[str] = "3.88-non-runtime-pilot-candidate-review-evidence-packet"
DESIGN_KIND: Final[str] = "non_runtime_pilot_candidate_review_evidence_packet_only"
PILOT_CANDIDATE_SOURCE_MILESTONE: Final[str] = "P8"
CONTRACT_CONFORMANCE_SOURCE_MILESTONE: Final[str] = "P9"
READINESS_GATE_SOURCE_MILESTONE: Final[str] = "P10"
REVIEW_EVIDENCE_PACKET_STATUS: Final[str] = "static_packet_shape_declaration_only"
EVIDENCE_COLLECTION_STATUS: Final[str] = "not_present_in_p11"
PACKET_BUILDER_STATUS: Final[str] = "not_present_in_p11"
PACKET_PERSISTENCE_STATUS: Final[str] = "not_present_in_p11"
HUMAN_DECISION_RECORDING_STATUS: Final[str] = "not_present_in_p11"
LAB_TEST_STATUS: Final[str] = "not_started_in_p11"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P12 - Routing Signal Scorer v3 Pilot Phase Closure / Copilot Boundary "
    "Entry Gate v1, only after P11 validation, freeze, startup freeze context "
    "refresh, and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Non-Runtime Pilot Candidate Review Evidence Packet v1 is a static packet "
    "shape declaration only. It is not an evidence collector, not a packet "
    "builder, not a report writer, not a review queue writer, not a human "
    "decision recorder, not a lab test, not a field test, not a Pilot runtime, "
    "not a Copilot, not a router, not a prompt loader, not persistence, not "
    "training data, not batch mode, and not authority. Human governance and "
    "the real router remain authoritative."
)
PACKET_RULE: Final[str] = (
    "P11 may declare the static evidence sections that a later governed review "
    "artifact must contain, but P11 cannot assemble, collect, persist, score, "
    "approve, or transmit evidence."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "Review evidence remains non-authoritative unless future governed evidence "
    "proves match-before-disagree behavior, zero critical deviations, and no "
    "boundary leaks."
)
ACTIVATION_GATE_DEFERRED_RULE: Final[str] = (
    "Any activation key or maturity on/off behavior remains deferred to a "
    "separate Activation Gate Box after lab testing and maturity evidence."
)
TEST_LAB_WARNING_RULE: Final[str] = (
    "Before any test-lab coding begins, the AI must warn the user explicitly "
    "and wait for confirmation."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
OPT_IN_PER_INVOCATION_REQUIRED: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
FIELD_TEST_STATUS: Final[str] = "not_allowed_in_p11"
DEFINITIVE_ENABLEMENT_STATUS: Final[str] = "not_allowed_in_p11"
COPILOT_STATUS: Final[str] = "not_started_in_p11"
LAB_TEST_CODING_STATUS: Final[str] = "not_started_in_p11"

STATIC_EVIDENCE_SECTIONS: Final[tuple[str, ...]] = (
    "freeze_lineage_p0_through_p10",
    "non_runtime_candidate_identity",
    "contract_conformance_declaration",
    "readiness_gate_criteria_snapshot",
    "unsafe_boundary_preservation_checklist",
    "match_before_disagree_requirement",
    "critical_boundary_error_budget_zero",
    "future_human_review_placeholder",
    "future_lab_warning_requirement",
    "activation_gate_deferred_notice",
)
REQUIRED_PACKET_SOURCE_FREEZES: Final[tuple[str, ...]] = (
    "RG-PILOT-000 router canon freeze with FREEZE_MEMORY_STATUS OK",
    "M35 bridge closure freeze with FREEZE_MEMORY_STATUS OK",
    "P0 scope charter and entry gate freeze with FREEZE_MEMORY_STATUS OK",
    "P1 Pilot boundary freeze with FREEZE_MEMORY_STATUS OK",
    "P2 input/output contract design freeze with FREEZE_MEMORY_STATUS OK",
    "P3 disagreement taxonomy freeze with FREEZE_MEMORY_STATUS OK",
    "P4 reproduction harness design freeze with FREEZE_MEMORY_STATUS OK",
    "P5 simulation skeleton design freeze with FREEZE_MEMORY_STATUS OK",
    "P6 review evidence design freeze with FREEZE_MEMORY_STATUS OK",
    "P7 implementation gate design freeze with FREEZE_MEMORY_STATUS OK",
    "P8 non-runtime Pilot candidate freeze with FREEZE_MEMORY_STATUS OK",
    "P9 contract conformance freeze with FREEZE_MEMORY_STATUS OK",
    "P10 readiness gate freeze with FREEZE_MEMORY_STATUS OK",
)
FORBIDDEN_PACKET_CLAIMS: Final[tuple[str, ...]] = (
    "review_approved",
    "human_decision_recorded",
    "evidence_collected",
    "packet_built_from_live_case",
    "packet_persisted",
    "report_written",
    "review_queue_written",
    "candidate_ready",
    "field_test_enabled",
    "definitive_enablement",
    "pilot_runtime_enabled",
    "copilot_started",
    "lab_test_started",
)
FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "collect_evidence",
    "build_review_packet",
    "assemble_packet",
    "generate_packet",
    "write_packet",
    "write_report",
    "write_review_queue",
    "persist_record",
    "record_human_decision",
    "record_approval",
    "approve_review",
    "mark_ready",
    "evaluate_live_readiness",
    "activate_field_test",
    "activate_definitive_enablement",
    "start_lab_test",
    "create_lab_cases",
    "run_lab_test",
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
class PilotCandidateReviewEvidenceSection:
    """Immutable static evidence section declaration for P11."""

    section_id: str
    required_state: str
    status: str
    failure_policy: str


@dataclass(frozen=True)
class PilotCandidateReviewEvidenceBoundary:
    """Immutable P11 boundary rule."""

    boundary_id: str
    allowed_state: str
    forbidden_claims: tuple[str, ...]


@dataclass(frozen=True)
class PilotCandidateReviewEvidencePacketRecord:
    """Immutable P11 static review evidence packet shape record.

    This record describes section names, required source freezes, no-effect
    constants, forbidden claims, and forbidden operations. It does not assemble
    a packet, collect evidence, persist anything, or grant readiness.
    """

    feature_id: str
    schema_version: str
    design_kind: str
    title: str
    pilot_candidate_source_milestone: str
    contract_conformance_source_milestone: str
    readiness_gate_source_milestone: str
    review_evidence_packet_status: str
    evidence_collection_status: str
    packet_builder_status: str
    packet_persistence_status: str
    human_decision_recording_status: str
    lab_test_status: str
    authority_statement: str
    packet_rule: str
    match_before_disagree_rule: str
    activation_gate_deferred_rule: str
    test_lab_warning_rule: str
    sections: tuple[PilotCandidateReviewEvidenceSection, ...]
    boundary: PilotCandidateReviewEvidenceBoundary
    required_source_freezes: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_SECTIONS: Final[tuple[PilotCandidateReviewEvidenceSection, ...]] = tuple(
    PilotCandidateReviewEvidenceSection(
        section_id=value,
        required_state="static_section_required_for_future_governed_review_artifact",
        status="declared_only_not_populated_in_p11",
        failure_policy="block_progression",
    )
    for value in STATIC_EVIDENCE_SECTIONS
)

_BOUNDARY: Final[PilotCandidateReviewEvidenceBoundary] = PilotCandidateReviewEvidenceBoundary(
    boundary_id="p11_static_review_evidence_packet_boundary",
    allowed_state="static_shape_declaration_only",
    forbidden_claims=FORBIDDEN_PACKET_CLAIMS,
)

_RECORD: Final[PilotCandidateReviewEvidencePacketRecord] = PilotCandidateReviewEvidencePacketRecord(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    title="Non-Runtime Pilot Candidate Review Evidence Packet v1",
    pilot_candidate_source_milestone=PILOT_CANDIDATE_SOURCE_MILESTONE,
    contract_conformance_source_milestone=CONTRACT_CONFORMANCE_SOURCE_MILESTONE,
    readiness_gate_source_milestone=READINESS_GATE_SOURCE_MILESTONE,
    review_evidence_packet_status=REVIEW_EVIDENCE_PACKET_STATUS,
    evidence_collection_status=EVIDENCE_COLLECTION_STATUS,
    packet_builder_status=PACKET_BUILDER_STATUS,
    packet_persistence_status=PACKET_PERSISTENCE_STATUS,
    human_decision_recording_status=HUMAN_DECISION_RECORDING_STATUS,
    lab_test_status=LAB_TEST_STATUS,
    authority_statement=AUTHORITY_STATEMENT,
    packet_rule=PACKET_RULE,
    match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
    activation_gate_deferred_rule=ACTIVATION_GATE_DEFERRED_RULE,
    test_lab_warning_rule=TEST_LAB_WARNING_RULE,
    sections=_SECTIONS,
    boundary=_BOUNDARY,
    required_source_freezes=REQUIRED_PACKET_SOURCE_FREEZES,
    forbidden_operations=FORBIDDEN_OPERATIONS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def get_non_runtime_pilot_candidate_review_evidence_packet_record() -> PilotCandidateReviewEvidencePacketRecord:
    """Return the immutable P11 non-runtime review evidence packet record."""

    return _RECORD
