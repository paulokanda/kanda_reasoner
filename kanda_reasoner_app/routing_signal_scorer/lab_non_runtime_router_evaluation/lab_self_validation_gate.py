# project-path: kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py
"""Non-runtime self-validation gate for the KANDA ML LAB.

This module evaluates caller-supplied, in-memory self-validation control facts.
It does not run candidate evaluations, compare routes, load prompts, read live project
state, write reports, persist decisions, call providers, use embeddings, activate
Pilot/Copilot, or field-test anything.
"""

from __future__ import annotations


__all__ = [
    'build_all_controls_true',
    'evaluate_lab_self_validation_gate',
    'get_lab7_self_validation_gate_record',
    'Lab7SelfValidationGateRecord',
    'Lab7SelfValidationResult',
]
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Mapping

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_ml_lab_self_validation_gate_v1"
FEATURE_TITLE: Final[str] = "Routing Signal Scorer v3 ML LAB Self-Validation Gate v1"
SCHEMA_VERSION: Final[str] = "lab-7-self-validation-gate"
DESIGN_KIND: Final[str] = "non_runtime_in_memory_self_validation_gate_only"
OUTCOME_PASS: Final[str] = "LAB_SELF_VALIDATION_PASS"
OUTCOME_LAB_INVALID: Final[str] = "LAB_INVALID"
OUTCOME_NOT_EVALUATED: Final[str] = "NOT_EVALUATED"
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
NEXT_SAFE_MILESTONE: Final[str] = "LAB-8 Alpha Corpus Seed"

REQUIRED_SELF_VALIDATION_CONTROLS: Final[tuple[str, ...]] = (
    "gold_vs_gold_control_passed",
    "wrong_route_control_failed_as_expected",
    "missing_prompt_control_failed_as_expected",
    "forbidden_action_control_critical_failed_as_expected",
    "fixture_hash_mismatch_control_lab_invalid_as_expected",
    "skipped_match_before_disagree_control_critical_failed_as_expected",
    "zero_critical_boundary_error_budget_enforced",
    "lab6_runner_outputs_not_evaluated_only",
    "no_live_project_reads_confirmed",
    "no_authority_fields_confirmed",
    "candidate_evaluation_blocked_until_self_validation_passed",
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
    "score_candidate_output",
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


@dataclass(frozen=True)
class Lab7SelfValidationGateRecord:
    """Immutable public contract record for the LAB-7 self-validation gate."""

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
    required_self_validation_controls: tuple[str, ...]
    forbidden_authority_fields: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    next_safe_milestone: str


@dataclass(frozen=True)
class Lab7SelfValidationResult:
    """Non-authoritative in-memory self-validation result."""

    lab_self_validation_id: str
    outcome: str
    gate_passed: bool
    missing_controls: tuple[str, ...]
    false_controls: tuple[str, ...]
    candidate_evaluation_executed: bool
    candidate_evaluation_allowed_by_this_gate: bool
    route_authority_granted: bool
    prompt_loading_performed: bool
    provider_call_performed: bool
    embedding_call_performed: bool
    persistence_performed: bool
    activation_performed: bool
    field_test_performed: bool
    runtime_pilot_behavior_performed: bool
    copilot_behavior_performed: bool
    next_safe_milestone: str
    reason: str


def get_lab7_self_validation_gate_record() -> Lab7SelfValidationGateRecord:
    """Return the immutable LAB-7 self-validation gate contract."""

    return Lab7SelfValidationGateRecord(
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
        required_self_validation_controls=REQUIRED_SELF_VALIDATION_CONTROLS,
        forbidden_authority_fields=FORBIDDEN_AUTHORITY_FIELDS,
        forbidden_operations=FORBIDDEN_OPERATIONS,
        next_safe_milestone=NEXT_SAFE_MILESTONE,
    )


def evaluate_lab_self_validation_gate(
    *,
    lab_self_validation_id: str,
    control_results: Mapping[str, bool],
) -> Lab7SelfValidationResult:
    """Evaluate caller-supplied self-validation control facts in memory only.

    This function performs no file I/O, no project-state reads, no candidate
    evaluation, no route comparison, no provider calls, and no persistence.
    """

    missing = tuple(name for name in REQUIRED_SELF_VALIDATION_CONTROLS if name not in control_results)
    false = tuple(name for name in REQUIRED_SELF_VALIDATION_CONTROLS if name in control_results and control_results[name] is not True)
    passed = not missing and not false
    outcome = OUTCOME_PASS if passed else OUTCOME_LAB_INVALID
    reason = (
        "All required LAB self-validation controls are caller-confirmed true; proceed only to the next governed LAB milestone."
        if passed
        else "LAB self-validation controls are missing or false; candidate evaluation remains blocked."
    )
    return Lab7SelfValidationResult(
        lab_self_validation_id=lab_self_validation_id,
        outcome=outcome,
        gate_passed=passed,
        missing_controls=missing,
        false_controls=false,
        candidate_evaluation_executed=False,
        candidate_evaluation_allowed_by_this_gate=False,
        route_authority_granted=False,
        prompt_loading_performed=False,
        provider_call_performed=False,
        embedding_call_performed=False,
        persistence_performed=False,
        activation_performed=False,
        field_test_performed=False,
        runtime_pilot_behavior_performed=False,
        copilot_behavior_performed=False,
        next_safe_milestone=NEXT_SAFE_MILESTONE,
        reason=reason,
    )


def build_all_controls_true() -> Mapping[str, bool]:
    """Return a read-only in-memory control set useful for self-tests."""

    return MappingProxyType({name: True for name in REQUIRED_SELF_VALIDATION_CONTROLS})


def as_read_only_mapping(result: Lab7SelfValidationResult) -> Mapping[str, object]:
    """Return a read-only mapping view of a LAB-7 self-validation result."""

    return MappingProxyType(result.__dict__.copy())
