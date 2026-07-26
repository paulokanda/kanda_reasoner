# project-path: kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py
"""Non-runtime candidate evaluation harness interface for the KANDA ML LAB.

This module defines an in-memory interface envelope for future candidate evaluation.
It does not evaluate candidates, execute cases, compare routes, score outputs, load
prompts, read live project state, persist reports, call providers, use embeddings,
activate Pilot/Copilot, or field-test anything.
"""

from __future__ import annotations


__all__ = [
    'build_not_evaluated_candidate_harness_envelope',
    'canonicalize_candidate_output_metadata',
    'compute_candidate_output_metadata_hash',
    'find_forbidden_authority_fields',
    'get_lab10_candidate_harness_interface_record',
    'Lab10CandidateHarnessEnvelope',
    'Lab10CandidateHarnessInterfaceRecord',
]
from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Final, Mapping

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_ml_lab_candidate_evaluation_harness_interface_v1"
FEATURE_TITLE: Final[str] = "Routing Signal Scorer v3 ML LAB Candidate Evaluation Harness Interface v1"
SCHEMA_VERSION: Final[str] = "lab-10-candidate-evaluation-harness-interface"
DESIGN_KIND: Final[str] = "non_runtime_candidate_evaluation_harness_interface_only"
OUTCOME_NOT_EVALUATED: Final[str] = "NOT_EVALUATED"
OUTCOME_INTERFACE_REJECTED: Final[str] = "HARNESS_INTERFACE_REJECTED"
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
NEXT_SAFE_MILESTONE: Final[str] = "LAB-11 Corpus V1 Expansion"

REQUIRED_INTERFACE_INPUTS: Final[tuple[str, ...]] = (
    "lab_run_id",
    "candidate_id",
    "candidate_version",
    "candidate_output_reference",
    "candidate_output_metadata",
    "test_case_reference",
    "corpus_version",
    "fixture_manifest_hash",
    "self_validation_status",
)

REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "LAB-7 self-validation gate frozen and passing",
    "LAB-8 alpha corpus or later governed corpus available as static non-authoritative data",
    "LAB-9 offline observability/report contract frozen",
    "candidate output wrapped as non_authoritative_evaluation_record",
    "fixture manifest hash supplied by caller",
    "test case reference supplied by caller",
    "no forbidden authority fields in candidate output metadata",
)

FORBIDDEN_AUTHORITY_FIELDS: Final[tuple[str, ...]] = (
    "route_decision",
    "load_prompt",
    "execute_route",
    "approve_readiness",
    "record_human_approval",
    "write_freeze_memory",
    "write_gold_registry",
    "write_prompt_library",
    "write_router_canon",
    "activate_pilot",
    "activate_copilot",
    "enable_field_test",
    "call_provider",
    "call_embedding_model",
    "start_batch_mode",
    "persist_ml_decision",
    "runtime_command",
    "copilot_instruction",
)

FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "evaluate_candidate_output",
    "execute_test_case",
    "score_candidate_output",
    "compare_routes",
    "select_route",
    "execute_route",
    "load_prompt",
    "read_live_prompt_library",
    "read_live_freeze_memory",
    "read_live_router_canon",
    "import_runtime_router",
    "read_fixture_file_from_disk",
    "discover_fixture_files",
    "create_actual_fixture",
    "create_hash_manifest_data_file",
    "create_corpus_case",
    "generate_report",
    "persist_report",
    "write_freeze_memory",
    "write_gold_registry",
    "write_prompt_library",
    "write_router_canon",
    "persist_ml_decision",
    "call_provider",
    "call_embedding_model",
    "network_call",
    "subprocess_call",
    "start_async_execution",
    "start_batch_mode",
    "activate_pilot",
    "activate_copilot",
    "enable_field_test",
    "runtime_pilot_behavior",
    "copilot_behavior",
)


@dataclass(frozen=True)
class Lab10CandidateHarnessInterfaceRecord:
    """Immutable public contract record for the LAB-10 harness interface."""

    feature_id: str
    feature_title: str
    schema_version: str
    design_kind: str
    storage_status: str
    routing_effect: str
    prompt_loading_effect: str
    runtime_effect: str
    activation_effect: str
    critical_boundary_error_budget: int
    required_interface_inputs: tuple[str, ...]
    required_preconditions: tuple[str, ...]
    forbidden_authority_fields: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    next_safe_milestone: str


@dataclass(frozen=True)
class Lab10CandidateHarnessEnvelope:
    """Non-authoritative in-memory interface envelope for future candidate evaluation."""

    lab_run_id: str
    candidate_id: str
    candidate_version: str
    candidate_output_reference: str
    candidate_output_hash: str
    test_case_reference: str
    corpus_version: str
    fixture_manifest_hash: str
    self_validation_status: str
    outcome: str
    reason: str
    forbidden_authority_fields_present: tuple[str, ...]
    non_authoritative: bool
    candidate_evaluation_executed: bool
    candidate_evaluation_allowed_by_this_interface: bool
    case_execution_performed: bool
    case_scoring_performed: bool
    route_comparison_performed: bool
    route_authority_granted: bool
    prompt_loading_performed: bool
    provider_call_performed: bool
    embedding_call_performed: bool
    persistence_performed: bool
    report_generated: bool
    report_persisted: bool
    activation_performed: bool
    field_test_performed: bool
    runtime_pilot_behavior_performed: bool
    copilot_behavior_performed: bool
    next_safe_milestone: str


def get_lab10_candidate_harness_interface_record() -> Lab10CandidateHarnessInterfaceRecord:
    """Return the immutable LAB-10 non-runtime harness interface contract."""

    return Lab10CandidateHarnessInterfaceRecord(
        feature_id=FEATURE_ID,
        feature_title=FEATURE_TITLE,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        storage_status=STORAGE_STATUS,
        routing_effect=ROUTING_EFFECT,
        prompt_loading_effect=PROMPT_LOADING_EFFECT,
        runtime_effect=RUNTIME_EFFECT,
        activation_effect=ACTIVATION_EFFECT,
        critical_boundary_error_budget=CRITICAL_BOUNDARY_ERROR_BUDGET,
        required_interface_inputs=REQUIRED_INTERFACE_INPUTS,
        required_preconditions=REQUIRED_PRECONDITIONS,
        forbidden_authority_fields=FORBIDDEN_AUTHORITY_FIELDS,
        forbidden_operations=FORBIDDEN_OPERATIONS,
        next_safe_milestone=NEXT_SAFE_MILESTONE,
    )


def canonicalize_candidate_output_metadata(candidate_output_metadata: Mapping[str, object]) -> str:
    """Canonicalize caller-supplied candidate metadata deterministically.

    This performs no file I/O, no project-state reads, no prompt loading, and no
    candidate evaluation. It only serializes the mapping supplied by the caller.
    """

    return json.dumps(candidate_output_metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_candidate_output_metadata_hash(candidate_output_metadata: Mapping[str, object]) -> str:
    """Return SHA-256 for caller-supplied candidate metadata."""

    return hashlib.sha256(canonicalize_candidate_output_metadata(candidate_output_metadata).encode("utf-8")).hexdigest()


def find_forbidden_authority_fields(candidate_output_metadata: Mapping[str, object]) -> tuple[str, ...]:
    """Find forbidden top-level authority fields in caller-supplied metadata.

    This is an interface precheck, not candidate evaluation and not route scoring.
    """

    return tuple(field for field in FORBIDDEN_AUTHORITY_FIELDS if field in candidate_output_metadata)


def build_not_evaluated_candidate_harness_envelope(
    *,
    lab_run_id: str,
    candidate_id: str,
    candidate_version: str,
    candidate_output_reference: str,
    candidate_output_metadata: Mapping[str, object],
    test_case_reference: str,
    corpus_version: str,
    fixture_manifest_hash: str,
    self_validation_status: str,
) -> Lab10CandidateHarnessEnvelope:
    """Build a non-authoritative NOT_EVALUATED harness interface envelope.

    The function does not evaluate the candidate, execute or score cases, compare
    routes, load prompts, read fixtures from disk, read live project state, write
    reports, persist decisions, call providers, use embeddings, activate Pilot or
    Copilot, or field-test anything.
    """

    forbidden = find_forbidden_authority_fields(candidate_output_metadata)
    rejected = bool(forbidden)
    outcome = OUTCOME_INTERFACE_REJECTED if rejected else OUTCOME_NOT_EVALUATED
    reason = (
        "Candidate metadata contains forbidden authority fields; future candidate evaluation remains blocked."
        if rejected
        else "LAB-10 defines the candidate harness interface only; candidate evaluation is not executed by this milestone."
    )
    return Lab10CandidateHarnessEnvelope(
        lab_run_id=lab_run_id,
        candidate_id=candidate_id,
        candidate_version=candidate_version,
        candidate_output_reference=candidate_output_reference,
        candidate_output_hash=compute_candidate_output_metadata_hash(candidate_output_metadata),
        test_case_reference=test_case_reference,
        corpus_version=corpus_version,
        fixture_manifest_hash=fixture_manifest_hash,
        self_validation_status=self_validation_status,
        outcome=outcome,
        reason=reason,
        forbidden_authority_fields_present=forbidden,
        non_authoritative=True,
        candidate_evaluation_executed=False,
        candidate_evaluation_allowed_by_this_interface=False,
        case_execution_performed=False,
        case_scoring_performed=False,
        route_comparison_performed=False,
        route_authority_granted=False,
        prompt_loading_performed=False,
        provider_call_performed=False,
        embedding_call_performed=False,
        persistence_performed=False,
        report_generated=False,
        report_persisted=False,
        activation_performed=False,
        field_test_performed=False,
        runtime_pilot_behavior_performed=False,
        copilot_behavior_performed=False,
        next_safe_milestone=NEXT_SAFE_MILESTONE,
    )


def as_read_only_mapping(envelope: Lab10CandidateHarnessEnvelope) -> Mapping[str, object]:
    """Return a read-only mapping view of a LAB-10 envelope."""

    return MappingProxyType(envelope.__dict__.copy())
