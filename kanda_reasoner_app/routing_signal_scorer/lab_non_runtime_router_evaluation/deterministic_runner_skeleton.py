# project-path: kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py
"""Non-runtime deterministic runner skeleton for the KANDA ML LAB.

This module is intentionally small, pure, in-memory, and non-authoritative.
It does not load prompts, read live project memory, read fixtures from disk,
score candidates, compare routes, persist reports, call providers, use embeddings,
start batch mode, activate Pilot/Copilot, or field-test anything.
"""

from __future__ import annotations


__all__ = [
    'build_not_evaluated_run_plan',
    'canonicalize_json_like_metadata',
    'compute_sha256_for_text',
    'get_lab6_deterministic_runner_skeleton_record',
    'Lab6DeterministicRunnerSkeletonRecord',
    'Lab6RunPlan',
]
from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Final, Mapping

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1"
FEATURE_TITLE: Final[str] = "Routing Signal Scorer v3 ML LAB Deterministic Runner Skeleton v1"
SCHEMA_VERSION: Final[str] = "lab-6-deterministic-runner-skeleton"
DESIGN_KIND: Final[str] = "non_runtime_deterministic_runner_skeleton_only"
OUTCOME_NOT_EVALUATED: Final[str] = "NOT_EVALUATED"
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"

ALLOWED_INPUT_KINDS: Final[tuple[str, ...]] = (
    "caller_supplied_candidate_output_metadata",
    "caller_supplied_test_case_metadata",
    "caller_supplied_fixture_manifest_metadata",
    "caller_supplied_runner_metadata",
)

FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
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
    "execute_candidate_evaluation",
    "score_candidate_output",
    "compare_routes",
    "select_route",
    "execute_route",
    "approve_readiness",
    "record_human_approval",
    "write_report",
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

HARD_STOP_CONDITIONS: Final[tuple[str, ...]] = (
    "fixture_manifest_missing",
    "fixture_manifest_hash_missing",
    "fixture_set_version_missing",
    "test_case_metadata_missing",
    "candidate_output_metadata_missing",
    "lab_self_validation_not_yet_frozen",
    "candidate_evaluation_requested_before_lab7",
)

NEXT_SAFE_MILESTONE: Final[str] = "LAB-7 Lab Self-Validation Gate"


@dataclass(frozen=True)
class Lab6DeterministicRunnerSkeletonRecord:
    """Immutable public contract record for the LAB-6 runner skeleton."""

    feature_id: str
    feature_title: str
    schema_version: str
    design_kind: str
    outcome: str
    storage_status: str
    routing_effect: str
    prompt_loading_effect: str
    runtime_effect: str
    activation_effect: str
    critical_boundary_error_budget: int
    allowed_input_kinds: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    forbidden_authority_fields: tuple[str, ...]
    hard_stop_conditions: tuple[str, ...]
    next_safe_milestone: str


@dataclass(frozen=True)
class Lab6RunPlan:
    """A non-authoritative NOT_EVALUATED in-memory run-plan record."""

    lab_run_id: str
    candidate_output_reference: str
    test_case_reference: str
    fixture_set_version: str
    fixture_manifest_hash: str
    outcome: str
    reason: str
    non_authoritative: bool
    candidate_evaluation_executed: bool
    route_authority_granted: bool
    prompt_loading_performed: bool
    provider_call_performed: bool
    embedding_call_performed: bool
    persistence_performed: bool
    activation_performed: bool
    field_test_performed: bool
    runtime_pilot_behavior_performed: bool
    copilot_behavior_performed: bool
    next_required_gate: str


def get_lab6_deterministic_runner_skeleton_record() -> Lab6DeterministicRunnerSkeletonRecord:
    """Return the immutable LAB-6 non-runtime runner skeleton contract."""

    return Lab6DeterministicRunnerSkeletonRecord(
        feature_id=FEATURE_ID,
        feature_title=FEATURE_TITLE,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        outcome=OUTCOME_NOT_EVALUATED,
        storage_status=STORAGE_STATUS,
        routing_effect=ROUTING_EFFECT,
        prompt_loading_effect=PROMPT_LOADING_EFFECT,
        runtime_effect=RUNTIME_EFFECT,
        activation_effect=ACTIVATION_EFFECT,
        critical_boundary_error_budget=CRITICAL_BOUNDARY_ERROR_BUDGET,
        allowed_input_kinds=ALLOWED_INPUT_KINDS,
        forbidden_operations=FORBIDDEN_OPERATIONS,
        forbidden_authority_fields=FORBIDDEN_AUTHORITY_FIELDS,
        hard_stop_conditions=HARD_STOP_CONDITIONS,
        next_safe_milestone=NEXT_SAFE_MILESTONE,
    )


def canonicalize_json_like_metadata(metadata: Mapping[str, object]) -> str:
    """Canonicalize caller-supplied metadata deterministically.

    This function performs no file I/O and no live project reads. It only serializes
    the mapping supplied by the caller using stable JSON settings.
    """

    return json.dumps(metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def compute_sha256_for_text(text: str) -> str:
    """Return SHA-256 for caller-supplied text using UTF-8 encoding."""

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_not_evaluated_run_plan(
    *,
    lab_run_id: str,
    candidate_output_reference: str,
    test_case_reference: str,
    fixture_set_version: str,
    fixture_manifest_hash: str,
    reason: str = "LAB-7 self-validation gate is not yet frozen; candidate evaluation is blocked.",
) -> Lab6RunPlan:
    """Build a deterministic, non-authoritative NOT_EVALUATED run plan.

    The function does not inspect files, validate fixtures, score candidates, compare
    routes, write reports, or approve readiness. It records caller-supplied metadata
    so later LAB milestones can use a stable runner surface.
    """

    return Lab6RunPlan(
        lab_run_id=lab_run_id,
        candidate_output_reference=candidate_output_reference,
        test_case_reference=test_case_reference,
        fixture_set_version=fixture_set_version,
        fixture_manifest_hash=fixture_manifest_hash,
        outcome=OUTCOME_NOT_EVALUATED,
        reason=reason,
        non_authoritative=True,
        candidate_evaluation_executed=False,
        route_authority_granted=False,
        prompt_loading_performed=False,
        provider_call_performed=False,
        embedding_call_performed=False,
        persistence_performed=False,
        activation_performed=False,
        field_test_performed=False,
        runtime_pilot_behavior_performed=False,
        copilot_behavior_performed=False,
        next_required_gate=NEXT_SAFE_MILESTONE,
    )


def as_read_only_mapping(record: Lab6RunPlan) -> Mapping[str, object]:
    """Return a read-only mapping view of a LAB-6 run plan."""

    return MappingProxyType(record.__dict__.copy())
