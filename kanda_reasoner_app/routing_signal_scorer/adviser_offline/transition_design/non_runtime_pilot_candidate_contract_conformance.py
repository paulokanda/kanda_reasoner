# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/non_runtime_pilot_candidate_contract_conformance.py
"""P9 non-runtime Pilot candidate contract conformance.

P9 declares static conformance between the inert P8 non-runtime Pilot candidate
record and the frozen Pilot input/output contract design. The record is
non-runtime and non-authoritative. It does not validate live payloads, process
input, generate output, compare routes, load prompts, persist records, read
gold or freeze memory, call providers, use embeddings, train from data, run
batch mode, activate Pilot/Copilot behavior, or grant route authority.
"""

from __future__ import annotations


__all__ = [
    'get_non_runtime_pilot_candidate_contract_conformance_record',
    'PilotCandidateConformanceInvariant',
    'PilotCandidateConformancePrecondition',
    'PilotCandidateContractConformanceRecord',
    'PilotCandidateContractFieldSet',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_non_runtime_pilot_candidate_contract_conformance_v1"
SCHEMA_VERSION: Final[str] = "3.86-non-runtime-pilot-candidate-contract-conformance"
DESIGN_KIND: Final[str] = "non_runtime_pilot_candidate_contract_conformance_only"
PILOT_CANDIDATE_SOURCE_MILESTONE: Final[str] = "P8"
CONFORMANCE_STATUS: Final[str] = "static_conformance_declaration_only"
LIVE_VALIDATOR_STATUS: Final[str] = "not_present_in_p9"
INPUT_PROCESSING_STATUS: Final[str] = "not_allowed_in_p9"
OUTPUT_GENERATION_STATUS: Final[str] = "not_allowed_in_p9"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P10 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Readiness "
    "Gate v1, only after P9 validation, freeze, startup freeze context refresh, "
    "and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Non-Runtime Pilot Candidate Contract Conformance v1 is a static "
    "conformance declaration only. It is not a live validator, not input "
    "processing, not output generation, not a Pilot runtime, not a Copilot, "
    "not a router, not a prompt loader, not a persistence writer, not training "
    "data, not batch mode, and not authority. Human governance and the real "
    "router remain authoritative."
)
CONFORMANCE_RULE: Final[str] = (
    "P9 may declare which frozen contract fields and invariants a future "
    "non-runtime Pilot candidate must preserve, but it cannot execute live "
    "validation or transform caller payloads."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "Contract conformance is necessary but not sufficient for disagreement "
    "trust; reproduction of frozen router/canon outcomes remains required."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
OPT_IN_PER_INVOCATION_REQUIRED: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
FIELD_TEST_STATUS: Final[str] = "not_allowed_in_p9"
DEFINITIVE_ENABLEMENT_STATUS: Final[str] = "not_allowed_in_p9"

ALLOWED_INPUT_FIELDS: Final[tuple[str, ...]] = (
    "case_id",
    "schema_version",
    "user_request_summary",
    "routing_context_public_summary",
    "task_classification_hints_summary",
    "current_router_outcome_summary",
    "frozen_canon_constraints_summary",
    "known_boundary_flags",
    "caller_generated_timestamp_utc",
)

ALLOWED_OUTPUT_FIELDS: Final[tuple[str, ...]] = (
    "pilot_record_kind",
    "case_id",
    "schema_version",
    "authority_notice",
    "projection_analysis_summary",
    "task_classification_projection_summary",
    "reasoning_summary_for_human_review",
    "boundary_flags_for_human_review",
    "divergence_summary_for_human_review",
    "divergence_type",
    "missing_information_summary",
    "human_review_mandatory",
    "advisory_review_priority",
    "routing_effect",
    "prompt_loading_effect",
    "runtime_effect",
    "activation_effect",
    "storage_status",
)

FORBIDDEN_INPUT_CONCEPTS: Final[tuple[str, ...]] = (
    "raw_prompt_text",
    "prompt_file_path",
    "prompt_group_object",
    "prompt_library_handle",
    "live_router_object",
    "runtime_state_object",
    "provider_model_configuration",
    "executable_file_path",
    "registry_object",
    "gold_set_mutation_handle",
    "callback",
    "callable",
    "training_data_request",
    "batch_mode_request",
    "activation_request",
)

FORBIDDEN_OUTPUT_FIELDS: Final[tuple[str, ...]] = (
    "approved_route",
    "final_route",
    "execute_route",
    "load_prompt",
    "activate_pilot",
    "activate_copilot",
    "promote_candidate",
    "write_gold",
    "write_registry",
    "record_human_decision",
    "persist_report",
    "runtime_authority",
    "confidence",
    "score",
    "probability",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "human_review_completed",
    "promotion_ready",
    "route_override",
    "prompt_to_load",
    "copilot_ready",
    "runtime_enabled",
)

FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
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
    "collect_evidence",
    "build_evidence_packet",
    "record_human_decision",
    "record_approval",
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
    "activate_field_test",
    "activate_definitive_enablement",
    "activate_pilot",
    "activate_copilot",
    "activate_limited_shadow_runtime",
    "promote_candidate",
)


@dataclass(frozen=True)
class PilotCandidateContractFieldSet:
    """Immutable declaration of a contract field set."""

    field_set_id: str
    status: str
    allowed_fields: tuple[str, ...]
    forbidden_items: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class PilotCandidateConformanceInvariant:
    """Immutable static conformance invariant."""

    invariant_id: str
    expected_value: str
    conformance_status: str
    failure_policy: str


@dataclass(frozen=True)
class PilotCandidateConformancePrecondition:
    """Immutable predecessor condition for P9."""

    precondition_id: str
    required_state: str
    blocked_if_missing: str


@dataclass(frozen=True)
class PilotCandidateContractConformanceRecord:
    """Immutable P9 static contract conformance record.

    This record is intentionally inert. It describes allowed fields,
    forbidden fields, invariant values, predecessor requirements, and forbidden
    operations. It does not validate live payloads, execute a candidate, or
    create Pilot output.
    """

    feature_id: str
    schema_version: str
    design_kind: str
    title: str
    pilot_candidate_source_milestone: str
    conformance_status: str
    live_validator_status: str
    input_processing_status: str
    output_generation_status: str
    authority_statement: str
    conformance_rule: str
    match_before_disagree_rule: str
    input_field_set: PilotCandidateContractFieldSet
    output_field_set: PilotCandidateContractFieldSet
    invariants: tuple[PilotCandidateConformanceInvariant, ...]
    required_preconditions: tuple[PilotCandidateConformancePrecondition, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_INPUT_FIELD_SET: Final[PilotCandidateContractFieldSet] = PilotCandidateContractFieldSet(
    field_set_id="future_pilot_input_contract_fields",
    status="static_declared_only_no_live_validation",
    allowed_fields=ALLOWED_INPUT_FIELDS,
    forbidden_items=FORBIDDEN_INPUT_CONCEPTS,
    reason="P9 may declare the frozen future input field boundary without processing payloads.",
)

_OUTPUT_FIELD_SET: Final[PilotCandidateContractFieldSet] = PilotCandidateContractFieldSet(
    field_set_id="future_pilot_output_contract_fields",
    status="static_declared_only_no_output_generation",
    allowed_fields=ALLOWED_OUTPUT_FIELDS,
    forbidden_items=FORBIDDEN_OUTPUT_FIELDS,
    reason="P9 may declare the frozen future output field boundary without generating output.",
)

_INVARIANTS: Final[tuple[PilotCandidateConformanceInvariant, ...]] = (
    PilotCandidateConformanceInvariant(
        invariant_id="routing_effect",
        expected_value=ROUTING_EFFECT,
        conformance_status="must_equal_none",
        failure_policy="block_progression",
    ),
    PilotCandidateConformanceInvariant(
        invariant_id="prompt_loading_effect",
        expected_value=PROMPT_LOADING_EFFECT,
        conformance_status="must_equal_none",
        failure_policy="block_progression",
    ),
    PilotCandidateConformanceInvariant(
        invariant_id="runtime_effect",
        expected_value=RUNTIME_EFFECT,
        conformance_status="must_equal_none",
        failure_policy="block_progression",
    ),
    PilotCandidateConformanceInvariant(
        invariant_id="activation_effect",
        expected_value=ACTIVATION_EFFECT,
        conformance_status="must_equal_none",
        failure_policy="block_progression",
    ),
    PilotCandidateConformanceInvariant(
        invariant_id="storage_status",
        expected_value=STORAGE_STATUS,
        conformance_status="must_equal_in_memory_only",
        failure_policy="block_progression",
    ),
    PilotCandidateConformanceInvariant(
        invariant_id="human_review_mandatory",
        expected_value="true",
        conformance_status="must_remain_true",
        failure_policy="block_progression",
    ),
    PilotCandidateConformanceInvariant(
        invariant_id="critical_boundary_error_budget",
        expected_value="zero",
        conformance_status="must_remain_zero",
        failure_policy="block_progression",
    ),
)

_REQUIRED_PRECONDITIONS: Final[tuple[PilotCandidateConformancePrecondition, ...]] = (
    PilotCandidateConformancePrecondition(
        precondition_id="p8_non_runtime_candidate_frozen",
        required_state="P8 Non-Runtime Pilot Candidate Implementation v1 frozen with FREEZE_MEMORY_STATUS OK.",
        blocked_if_missing="Do not create or trust P9 contract conformance.",
    ),
    PilotCandidateConformancePrecondition(
        precondition_id="p2_contract_design_frozen",
        required_state="P2 Pilot Input Output Contract and Validator Design v1 frozen.",
        blocked_if_missing="Do not declare conformance without frozen contract design.",
    ),
    PilotCandidateConformancePrecondition(
        precondition_id="p3_taxonomy_design_frozen",
        required_state="P3 Pilot Disagreement Taxonomy Design v1 frozen.",
        blocked_if_missing="Do not advance toward readiness or disagreement use.",
    ),
    PilotCandidateConformancePrecondition(
        precondition_id="p4_reproduction_harness_design_frozen",
        required_state="P4 reproduction-before-disagreement harness design frozen.",
        blocked_if_missing="Do not trust disagreement or readiness evidence.",
    ),
    PilotCandidateConformancePrecondition(
        precondition_id="root_drive_staging_installer_canon_frozen",
        required_state="KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 frozen and used.",
        blocked_if_missing="Do not deliver governed patch install instructions.",
    ),
)

_RECORD: Final[PilotCandidateContractConformanceRecord] = PilotCandidateContractConformanceRecord(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    title="Non-Runtime Pilot Candidate Contract Conformance v1",
    pilot_candidate_source_milestone=PILOT_CANDIDATE_SOURCE_MILESTONE,
    conformance_status=CONFORMANCE_STATUS,
    live_validator_status=LIVE_VALIDATOR_STATUS,
    input_processing_status=INPUT_PROCESSING_STATUS,
    output_generation_status=OUTPUT_GENERATION_STATUS,
    authority_statement=AUTHORITY_STATEMENT,
    conformance_rule=CONFORMANCE_RULE,
    match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
    input_field_set=_INPUT_FIELD_SET,
    output_field_set=_OUTPUT_FIELD_SET,
    invariants=_INVARIANTS,
    required_preconditions=_REQUIRED_PRECONDITIONS,
    forbidden_operations=FORBIDDEN_OPERATIONS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def get_non_runtime_pilot_candidate_contract_conformance_record() -> PilotCandidateContractConformanceRecord:
    """Return the immutable P9 non-runtime contract conformance record."""

    return _RECORD
