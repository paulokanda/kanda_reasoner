# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_review_evidence_design.py
"""P6 Pilot review evidence design.

P6 defines static review-evidence vocabulary for a future, non-authoritative,
opt-in, ephemeral Pilot review packet. It is a design-only artifact. It does not
collect evidence, read project memory, inspect routers, compare routes, generate
reports, write queues, persist records, record human decisions, or grant
Pilot/Copilot authority.
"""

from __future__ import annotations


__all__ = [
    'get_pilot_review_evidence_design',
    'PilotReviewEvidenceDesign',
    'PilotReviewEvidenceFieldDesign',
    'PilotReviewEvidenceSectionDesign',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_review_evidence_design_v1"
SCHEMA_VERSION: Final[str] = "3.83-pilot-review-evidence-design"
DESIGN_KIND: Final[str] = "pilot_review_evidence_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P7 - Routing Signal Scorer v3 Pilot Implementation Gate Design v1, only "
    "after P6 validation, freeze, startup freeze context refresh, and "
    "FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot Review Evidence Design v1 defines only static review-evidence "
    "vocabulary for future human review support. It does not collect evidence, "
    "read freeze memory, read the prompt library, inspect runtime routers, compare "
    "routes, calculate metrics, generate reports, write queues, persist records, "
    "record human decisions, train models, run batch mode, activate Limited Shadow "
    "Runtime, or grant Pilot/Copilot authority."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "Any future review-evidence packet that mentions disagreement or taxonomy "
    "language must first reference frozen-router reproduction evidence from a later "
    "governed harness implementation; without that evidence, disagreement language "
    "remains untrusted and fail-closed."
)
HUMAN_REVIEW_RULE: Final[str] = (
    "Human review is mandatory, but the evidence packet is not approval, not a "
    "decision record, and not a substitute for the authoritative router."
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
class PilotReviewEvidenceFieldDesign:
    """Immutable design record for one future review-evidence field."""

    field_id: str
    display_name: str
    design_purpose: str
    allowed_future_content: str
    inert_p6_status: str
    required_prior_evidence: str
    forbidden_interpretation: str


@dataclass(frozen=True)
class PilotReviewEvidenceSectionDesign:
    """Immutable design record for one future review-evidence packet section."""

    section_id: str
    sequence_label: str
    design_purpose: str
    required_fields: tuple[str, ...]
    fail_closed_condition: str
    human_review_visibility: str


@dataclass(frozen=True)
class PilotReviewEvidenceDesign:
    """Immutable design-only P6 review-evidence boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    match_before_disagree_rule: str
    human_review_rule: str
    design_status: str
    evidence_collection_status: str
    evidence_packet_generation_status: str
    live_validation_status: str
    input_processing_status: str
    output_generation_status: str
    route_comparison_status: str
    projection_status: str
    report_generation_status: str
    review_queue_status: str
    human_decision_recording_status: str
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
    evidence_fields: tuple[PilotReviewEvidenceFieldDesign, ...]
    evidence_sections: tuple[PilotReviewEvidenceSectionDesign, ...]
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
    "kanda_patch_delivery_root_drive_staging_canon_frozen",
    "startup_freeze_context_refreshed_after_p5",
    "freeze_memory_status_ok_after_p5",
    "human_request_explicitly_targets_p6_design_only_review_evidence",
)

_EVIDENCE_FIELDS: Final[tuple[PilotReviewEvidenceFieldDesign, ...]] = (
    PilotReviewEvidenceFieldDesign(
        field_id="case_local_opt_in_trace",
        display_name="Case-local opt-in trace",
        design_purpose="Name the future evidence that a Pilot review packet was explicitly requested for this case only.",
        allowed_future_content="Primitive, caller-supplied opt-in summary under a later governed implementation scope.",
        inert_p6_status="No opt-in evidence is collected in P6; field design only.",
        required_prior_evidence="P5 simulation skeleton design freeze and later implementation gate.",
        forbidden_interpretation="Not a durable consent record, not batch permission, and not runtime activation.",
    ),
    PilotReviewEvidenceFieldDesign(
        field_id="contract_boundary_trace",
        display_name="Contract boundary trace",
        design_purpose="Reserve future evidence that the P2 contract boundary shaped the packet.",
        allowed_future_content="Human-readable reference to primitive input/output contract constraints.",
        inert_p6_status="No contract validation is performed in P6; field design only.",
        required_prior_evidence="P2 contract design and later validator implementation gate.",
        forbidden_interpretation="Not live validation, not input processing, and not output approval.",
    ),
    PilotReviewEvidenceFieldDesign(
        field_id="frozen_router_reproduction_trace",
        display_name="Frozen-router reproduction trace",
        design_purpose="Reserve future evidence that match-before-disagree was satisfied before taxonomy language is trusted.",
        allowed_future_content="Exact-match reproduction summary from a separately governed future harness implementation.",
        inert_p6_status="No reproduction evidence is collected in P6; field design only.",
        required_prior_evidence="P4 harness design and later governed harness implementation.",
        forbidden_interpretation="Not a harness run, not gold loading, not route comparison, and not certification.",
    ),
    PilotReviewEvidenceFieldDesign(
        field_id="taxonomy_language_trace",
        display_name="Taxonomy language trace",
        design_purpose="Reserve future descriptive P3 taxonomy vocabulary after reproduction evidence exists.",
        allowed_future_content="Non-recommendation, descriptive disagreement language for human review only.",
        inert_p6_status="No taxonomy label is generated in P6; field design only.",
        required_prior_evidence="Frozen-router reproduction trace and P3 taxonomy traceability.",
        forbidden_interpretation="Not disagreement detection, not scoring, not recommendation, and not route authority.",
    ),
    PilotReviewEvidenceFieldDesign(
        field_id="simulation_skeleton_trace",
        display_name="Simulation skeleton trace",
        design_purpose="Reserve future evidence that any review packet follows P5 stage ordering.",
        allowed_future_content="Human-readable stage-order summary produced under a later governed implementation gate.",
        inert_p6_status="No simulation stage output is generated in P6; field design only.",
        required_prior_evidence="P5 simulation skeleton design freeze.",
        forbidden_interpretation="Not simulation execution, not callable simulator output, and not a report.",
    ),
    PilotReviewEvidenceFieldDesign(
        field_id="critical_boundary_blocker_trace",
        display_name="Critical boundary blocker trace",
        design_purpose="Reserve future fail-closed evidence for authority, persistence, prompt-loading, or runtime conflicts.",
        allowed_future_content="Human-readable blocker names and boundary conflict descriptions.",
        inert_p6_status="No blocker is detected or enforced in P6; field design only.",
        required_prior_evidence="Zero critical boundary error budget remains active.",
        forbidden_interpretation="Not automated repair, not continuation permission, and not authority grant.",
    ),
    PilotReviewEvidenceFieldDesign(
        field_id="human_review_note_trace",
        display_name="Human review note trace",
        design_purpose="Reserve future non-approving human review support language.",
        allowed_future_content="Human-readable review note draft under a later governed milestone.",
        inert_p6_status="No note is written, persisted, queued, or recorded in P6; field design only.",
        required_prior_evidence="All previous review-evidence fields and no critical boundary conflicts.",
        forbidden_interpretation="Not approval, not a decision record, not persistence, and not routing authority.",
    ),
)

_EVIDENCE_SECTIONS: Final[tuple[PilotReviewEvidenceSectionDesign, ...]] = (
    PilotReviewEvidenceSectionDesign(
        section_id="section_1_scope_and_opt_in",
        sequence_label="1",
        design_purpose="Future evidence begins with explicit scope and case-local opt-in boundaries.",
        required_fields=("case_local_opt_in_trace", "contract_boundary_trace"),
        fail_closed_condition="Missing explicit opt-in or contract boundary trace blocks packet use.",
        human_review_visibility="Human reviewer must see why the packet is case-local and non-authoritative.",
    ),
    PilotReviewEvidenceSectionDesign(
        section_id="section_2_reproduction_before_taxonomy",
        sequence_label="2",
        design_purpose="Reproduction before taxonomy: future evidence must show reproduction before any disagreement taxonomy language is trusted.",
        required_fields=("frozen_router_reproduction_trace", "taxonomy_language_trace"),
        fail_closed_condition="Missing reproduction trace blocks taxonomy language trust.",
        human_review_visibility="Human reviewer must see that disagreement language is descriptive only.",
    ),
    PilotReviewEvidenceSectionDesign(
        section_id="section_3_simulation_skeleton_traceability",
        sequence_label="3",
        design_purpose="Future evidence must trace to P5 ordering without running a simulator in P6.",
        required_fields=("simulation_skeleton_trace",),
        fail_closed_condition="Missing simulation skeleton traceability blocks packet completion.",
        human_review_visibility="Human reviewer must see that any future skeleton output is review support only.",
    ),
    PilotReviewEvidenceSectionDesign(
        section_id="section_4_boundary_and_human_review",
        sequence_label="4",
        design_purpose="Future evidence ends with fail-closed boundary blockers and non-approving human review support.",
        required_fields=("critical_boundary_blocker_trace", "human_review_note_trace"),
        fail_closed_condition="Any critical boundary conflict blocks review packet completion.",
        human_review_visibility="Human reviewer remains mandatory and the packet never records a final decision.",
    ),
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "collect_evidence",
    "build_evidence_packet",
    "generate_review_packet",
    "validate_live_payload",
    "process_input",
    "generate_output",
    "run_simulation",
    "execute_simulation_stage",
    "load_gold_set",
    "read_freeze_memory",
    "read_prompt_library",
    "inspect_runtime_router",
    "compare_routes",
    "calculate_metric",
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
    "persist_evidence_packet",
    "record_human_decision",
    "approve_route",
    "train_from_review_evidence",
    "run_batch_mode",
    "activate_limited_shadow_runtime",
    "promote_candidate",
    "call_provider",
    "use_embeddings",
)


def get_pilot_review_evidence_design() -> PilotReviewEvidenceDesign:
    """Return the immutable P6 review evidence design record."""

    return PilotReviewEvidenceDesign(
        feature_id=FEATURE_ID,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        milestone="P6",
        title="Pilot Review Evidence Design v1",
        authority_statement=AUTHORITY_STATEMENT,
        match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
        human_review_rule=HUMAN_REVIEW_RULE,
        design_status="design_only",
        evidence_collection_status="not_implemented_design_only",
        evidence_packet_generation_status="not_implemented",
        live_validation_status="not_implemented",
        input_processing_status="not_implemented",
        output_generation_status="not_implemented",
        route_comparison_status="not_implemented",
        projection_status="not_implemented",
        report_generation_status="not_implemented",
        review_queue_status="not_implemented",
        human_decision_recording_status="not_implemented",
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
        evidence_fields=_EVIDENCE_FIELDS,
        evidence_sections=_EVIDENCE_SECTIONS,
        forbidden_operations=_FORBIDDEN_OPERATIONS,
        next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    )
