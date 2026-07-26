# project-path: kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py
"""Minimal non-runtime harness stub for Routing Signal Scorer MLRT-48.

This module is intentionally inert.
It creates no route authority, no dry-run execution, no candidate execution,
no prompt loading, no provider calls, no embeddings, no persistence,
no training-data use, no runtime Pilot behavior, and no Copilot behavior.

The module is a static source surface only. It exists so later governed
milestones can test boundaries before any non-runtime harness behavior is added.
"""

from __future__ import annotations


__all__ = [
    'assert_static_non_runtime_boundary',
    'get_stub_contract',
    'MinimalNonRuntimeHarnessStubContract',
]
from typing import Mapping


FEATURE_ID = "rss_mlrt48_controlled_minimal_source_creation_v1"
SOURCE_STATUS = "controlled_minimal_non_runtime_source_created_static_only"
CRITICAL_BOUNDARY_ERROR_BUDGET = 0


class MinimalNonRuntimeHarnessStubContract:
    """Static namespace for the inert MLRT-48 source surface."""

    feature_id = FEATURE_ID
    source_status = SOURCE_STATUS
    critical_boundary_error_budget = CRITICAL_BOUNDARY_ERROR_BUDGET
    source_file_created = True
    static_source_surface_only = True
    import_safe = True
    runtime_route_authority_enabled = False
    prompt_loading_enabled = False
    provider_calls_enabled = False
    embeddings_enabled = False
    vector_store_enabled = False
    persistence_enabled = False
    batch_mode_enabled = False
    activation_enabled = False
    field_testing_enabled = False
    dry_run_execution_enabled = False
    candidate_execution_enabled = False
    case_scoring_enabled = False
    report_generation_enabled = False
    reliability_claim_enabled = False
    training_data_use_enabled = False
    runtime_pilot_enabled = False
    copilot_enabled = False


def get_stub_contract() -> Mapping[str, object]:
    """Return the static MLRT-48 boundary contract as plain data."""

    contract = MinimalNonRuntimeHarnessStubContract
    return {
        "feature_id": contract.feature_id,
        "source_status": contract.source_status,
        "critical_boundary_error_budget": contract.critical_boundary_error_budget,
        "source_file_created": contract.source_file_created,
        "static_source_surface_only": contract.static_source_surface_only,
        "import_safe": contract.import_safe,
        "runtime_route_authority_enabled": contract.runtime_route_authority_enabled,
        "prompt_loading_enabled": contract.prompt_loading_enabled,
        "provider_calls_enabled": contract.provider_calls_enabled,
        "embeddings_enabled": contract.embeddings_enabled,
        "vector_store_enabled": contract.vector_store_enabled,
        "persistence_enabled": contract.persistence_enabled,
        "batch_mode_enabled": contract.batch_mode_enabled,
        "activation_enabled": contract.activation_enabled,
        "field_testing_enabled": contract.field_testing_enabled,
        "dry_run_execution_enabled": contract.dry_run_execution_enabled,
        "candidate_execution_enabled": contract.candidate_execution_enabled,
        "case_scoring_enabled": contract.case_scoring_enabled,
        "report_generation_enabled": contract.report_generation_enabled,
        "reliability_claim_enabled": contract.reliability_claim_enabled,
        "training_data_use_enabled": contract.training_data_use_enabled,
        "runtime_pilot_enabled": contract.runtime_pilot_enabled,
        "copilot_enabled": contract.copilot_enabled,
    }


def assert_static_non_runtime_boundary() -> bool:
    """Assert that all forbidden ML/router capabilities remain disabled."""

    contract = get_stub_contract()
    forbidden_flags = (
        "runtime_route_authority_enabled",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "batch_mode_enabled",
        "activation_enabled",
        "field_testing_enabled",
        "dry_run_execution_enabled",
        "candidate_execution_enabled",
        "case_scoring_enabled",
        "report_generation_enabled",
        "reliability_claim_enabled",
        "training_data_use_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    )
    enabled = [name for name in forbidden_flags if contract[name] is not False]
    if enabled:
        raise AssertionError(f"MLRT-48 forbidden capabilities enabled: {enabled}")
    if contract["critical_boundary_error_budget"] != 0:
        raise AssertionError("MLRT-48 critical boundary error budget must remain zero")
    return True
