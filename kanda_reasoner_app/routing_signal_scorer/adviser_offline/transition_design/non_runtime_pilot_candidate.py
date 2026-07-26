# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/non_runtime_pilot_candidate.py
"""P8 non-runtime Pilot candidate implementation.

P8 introduces an inert, static Pilot candidate record for future governed
comparison work. The record is non-runtime and non-authoritative. It does not
process input, generate output, compare routes, load prompts, persist records,
read gold or freeze memory, call providers, use embeddings, train from data,
run batch mode, activate Pilot/Copilot behavior, or grant route authority.
"""

from __future__ import annotations


__all__ = [
    'get_non_runtime_pilot_candidate_record',
    'PilotCandidateBoundaryState',
    'PilotCandidateCapabilityDeclaration',
    'PilotCandidateIdentity',
    'PilotCandidateNonRuntimeRecord',
    'PilotCandidatePreconditionDeclaration',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_non_runtime_pilot_candidate_implementation_v1"
SCHEMA_VERSION: Final[str] = "3.85-non-runtime-pilot-candidate-implementation"
DESIGN_KIND: Final[str] = "non_runtime_pilot_candidate_implementation_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P9 - Routing Signal Scorer v3 Non-Runtime Pilot Candidate Contract "
    "Conformance v1, only after P8 validation, freeze, startup freeze context "
    "refresh, and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Non-Runtime Pilot Candidate Implementation v1 defines only an inert, "
    "static candidate record. It is not a Pilot runtime, not a Copilot, not a "
    "router, not a prompt loader, not a persistence writer, not training data, "
    "not batch mode, and not authority. Human governance and the real router "
    "remain authoritative."
)
NON_RUNTIME_RULE: Final[str] = (
    "A non-runtime candidate is only a static representation of future Pilot "
    "candidate boundaries. It cannot evaluate user requests, compare live routes, "
    "or produce recommendations."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "The candidate remains untrusted for disagreement evidence until a later "
    "governed milestone proves reproduction of frozen router/canon outcomes."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
OPT_IN_PER_INVOCATION_REQUIRED: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
CANDIDATE_RUNTIME_STATUS: Final[str] = "not_runtime"
CANDIDATE_AUTHORITY_STATUS: Final[str] = "not_authoritative"
CANDIDATE_MATURITY_STATUS: Final[str] = "immature_non_runtime_candidate"
FIELD_TEST_STATUS: Final[str] = "not_allowed_in_p8"
DEFINITIVE_ENABLEMENT_STATUS: Final[str] = "not_allowed_in_p8"


@dataclass(frozen=True)
class PilotCandidateIdentity:
    """Immutable identity for the static non-runtime candidate."""

    candidate_id: str
    candidate_label: str
    schema_version: str
    milestone: str
    maturity_status: str
    implementation_scope: str


@dataclass(frozen=True)
class PilotCandidateBoundaryState:
    """Immutable authority and boundary state for the candidate."""

    runtime_status: str
    authority_status: str
    routing_effect: str
    prompt_loading_effect: str
    runtime_effect: str
    activation_effect: str
    storage_status: str
    human_review_mandatory: bool
    opt_in_per_invocation_required: bool
    critical_boundary_error_budget: int
    field_test_status: str
    definitive_enablement_status: str


@dataclass(frozen=True)
class PilotCandidateCapabilityDeclaration:
    """Immutable declaration of an allowed or forbidden capability."""

    capability_id: str
    capability_kind: str
    status: str
    reason: str


@dataclass(frozen=True)
class PilotCandidatePreconditionDeclaration:
    """Immutable declaration of a required predecessor condition."""

    precondition_id: str
    required_state: str
    blocked_if_missing: str


@dataclass(frozen=True)
class PilotCandidateNonRuntimeRecord:
    """Immutable P8 static candidate record.

    The record is intentionally inert. It is a data object containing identity,
    boundary declarations, capability declarations, preconditions, forbidden
    operations, and next-milestone text. It does not evaluate inputs or produce
    routing outputs.
    """

    feature_id: str
    schema_version: str
    design_kind: str
    title: str
    authority_statement: str
    non_runtime_rule: str
    match_before_disagree_rule: str
    identity: PilotCandidateIdentity
    boundary_state: PilotCandidateBoundaryState
    allowed_declarations: tuple[PilotCandidateCapabilityDeclaration, ...]
    forbidden_declarations: tuple[PilotCandidateCapabilityDeclaration, ...]
    required_preconditions: tuple[PilotCandidatePreconditionDeclaration, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_ALLOWED_DECLARATIONS: Final[tuple[PilotCandidateCapabilityDeclaration, ...]] = (
    PilotCandidateCapabilityDeclaration(
        capability_id="static_identity_declaration",
        capability_kind="allowed_static_metadata",
        status="available_in_p8",
        reason="P8 may name a candidate identity without making it callable.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="static_boundary_declaration",
        capability_kind="allowed_static_metadata",
        status="available_in_p8",
        reason="P8 may declare no-authority boundaries as immutable metadata.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="static_capability_map_declaration",
        capability_kind="allowed_static_metadata",
        status="available_in_p8",
        reason="P8 may declare allowed and forbidden capabilities without executing them.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="static_precondition_declaration",
        capability_kind="allowed_static_metadata",
        status="available_in_p8",
        reason="P8 may declare predecessor freeze and governance requirements.",
    ),
)

_FORBIDDEN_DECLARATIONS: Final[tuple[PilotCandidateCapabilityDeclaration, ...]] = (
    PilotCandidateCapabilityDeclaration(
        capability_id="runtime_routing",
        capability_kind="forbidden_behavior",
        status="blocked_in_p8",
        reason="The candidate cannot select, override, or execute routes.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="prompt_loading",
        capability_kind="forbidden_behavior",
        status="blocked_in_p8",
        reason="The candidate cannot select, read, or load prompt assets.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="persistent_recording",
        capability_kind="forbidden_behavior",
        status="blocked_in_p8",
        reason="The candidate cannot write reports, queues, logs, gold, registry, or freeze memory.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="provider_or_embedding_use",
        capability_kind="forbidden_behavior",
        status="blocked_in_p8",
        reason="The candidate cannot call providers, use embeddings, or create vector indexes.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="training_or_batch_use",
        capability_kind="forbidden_behavior",
        status="blocked_in_p8",
        reason="The candidate cannot be used as training data or queried in batch mode.",
    ),
    PilotCandidateCapabilityDeclaration(
        capability_id="field_test_or_definitive_enablement",
        capability_kind="forbidden_behavior",
        status="blocked_in_p8",
        reason="Activation-gate logic belongs to a later governed scope after lab testing and maturity evidence.",
    ),
)

_REQUIRED_PRECONDITIONS: Final[tuple[PilotCandidatePreconditionDeclaration, ...]] = (
    PilotCandidatePreconditionDeclaration(
        precondition_id="m35_bridge_closed_and_frozen",
        required_state="M35 handoff closure frozen with startup freeze context refreshed.",
        blocked_if_missing="Do not create or use the P8 candidate record.",
    ),
    PilotCandidatePreconditionDeclaration(
        precondition_id="rg_pilot_000_router_canon_frozen",
        required_state="RG-PILOT-000 Pilot/Copilot Phase 0 router canon frozen.",
        blocked_if_missing="Do not treat Pilot/Copilot work as routed or safe to continue.",
    ),
    PilotCandidatePreconditionDeclaration(
        precondition_id="p0_through_p7_frozen",
        required_state="P0 through P7 frozen with FREEZE_MEMORY_STATUS OK after P7.",
        blocked_if_missing="Do not advance to P8 candidate implementation.",
    ),
    PilotCandidatePreconditionDeclaration(
        precondition_id="root_drive_staging_installer_canon_frozen",
        required_state="KANDA Patch Delivery Root-Drive ZIP Staging Canon v1 frozen and used.",
        blocked_if_missing="Do not deliver governed patch install instructions.",
    ),
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "evaluate_user_request",
    "process_input",
    "generate_output",
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
    "validate_live_payload",
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

_RECORD: Final[PilotCandidateNonRuntimeRecord] = PilotCandidateNonRuntimeRecord(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    title="Non-Runtime Pilot Candidate Implementation v1",
    authority_statement=AUTHORITY_STATEMENT,
    non_runtime_rule=NON_RUNTIME_RULE,
    match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
    identity=PilotCandidateIdentity(
        candidate_id="pilot_candidate_non_runtime_v1",
        candidate_label="Static non-runtime Pilot candidate",
        schema_version=SCHEMA_VERSION,
        milestone="P8",
        maturity_status=CANDIDATE_MATURITY_STATUS,
        implementation_scope="static_metadata_record_only",
    ),
    boundary_state=PilotCandidateBoundaryState(
        runtime_status=CANDIDATE_RUNTIME_STATUS,
        authority_status=CANDIDATE_AUTHORITY_STATUS,
        routing_effect=ROUTING_EFFECT,
        prompt_loading_effect=PROMPT_LOADING_EFFECT,
        runtime_effect=RUNTIME_EFFECT,
        activation_effect=ACTIVATION_EFFECT,
        storage_status=STORAGE_STATUS,
        human_review_mandatory=HUMAN_REVIEW_MANDATORY,
        opt_in_per_invocation_required=OPT_IN_PER_INVOCATION_REQUIRED,
        critical_boundary_error_budget=CRITICAL_BOUNDARY_ERROR_BUDGET,
        field_test_status=FIELD_TEST_STATUS,
        definitive_enablement_status=DEFINITIVE_ENABLEMENT_STATUS,
    ),
    allowed_declarations=_ALLOWED_DECLARATIONS,
    forbidden_declarations=_FORBIDDEN_DECLARATIONS,
    required_preconditions=_REQUIRED_PRECONDITIONS,
    forbidden_operations=_FORBIDDEN_OPERATIONS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def get_non_runtime_pilot_candidate_record() -> PilotCandidateNonRuntimeRecord:
    """Return the immutable P8 non-runtime candidate record."""

    return _RECORD
