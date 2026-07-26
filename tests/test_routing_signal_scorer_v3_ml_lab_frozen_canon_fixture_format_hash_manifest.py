"""Contract tests for LAB-5 ML LAB Frozen Canon Fixture Format + Hash Manifest v1.

These tests validate a documentation-only fixture-format/hash-manifest design milestone.
They must not import LAB implementation code because LAB-5 is not allowed to create
actual fixtures, manifest data, schema code, validators, corpus, runner, scoring engine,
metrics engine, candidate harness, live readers, import scanners, write guards, provider
adapters, or runtime authority.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_frozen_canon_fixture_format_hash_manifest_v1"
CONTRACT_DOC = LAB_BOX / "LAB_FROZEN_CANON_FIXTURE_FORMAT_HASH_MANIFEST.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"

REQUIRED_FUTURE_FIXTURE_FIELDS = (
    "fixture_id",
    "fixture_version",
    "fixture_schema_version",
    "fixture_kind",
    "fixture_set_version",
    "source_freeze_id",
    "source_feature_id",
    "source_feature_title",
    "source_path",
    "source_snapshot_purpose",
    "source_canon_rule_references",
    "source_content_hash",
    "fixture_content_hash",
    "fixture_hash",
    "hash_algorithm",
    "hash_input_canonicalization",
    "created_at_utc",
    "created_by_process",
    "review_status",
    "reviewed_by_human",
    "human_review_reference",
    "immutability_status",
    "supersedes_fixture_id",
    "superseded_by_fixture_id",
    "allowed_read_scope",
    "forbidden_live_sources",
)

REQUIRED_FUTURE_MANIFEST_FIELDS = (
    "manifest_id",
    "manifest_version",
    "manifest_schema_version",
    "fixture_set_version",
    "corpus_version_reference",
    "canon_version_reference",
    "created_at_utc",
    "hash_algorithm",
    "hash_input_canonicalization",
    "fixture_entries",
    "aggregate_manifest_hash",
    "manifest_review_status",
    "reviewed_by_human",
    "human_review_reference",
    "source_freeze_ids",
    "source_feature_ids",
    "allowed_fixture_roots",
    "forbidden_live_roots",
)

LAB_INVALID_CODES = (
    "fixture_hash_missing",
    "fixture_hash_mismatch",
    "fixture_schema_version_missing",
    "fixture_set_version_missing",
    "fixture_manifest_missing",
    "aggregate_manifest_hash_missing",
    "aggregate_manifest_hash_mismatch",
    "source_freeze_id_missing",
    "canon_version_reference_missing",
    "review_status_missing",
    "review_status_not_approved",
    "hash_algorithm_missing",
    "hash_algorithm_not_sha256",
    "hash_input_canonicalization_missing",
    "fixture_entry_not_listed_in_manifest",
    "manifest_lists_missing_fixture",
    "fixture_mutated_after_review",
    "fixture_path_outside_allowed_fixture_roots",
)

CRITICAL_BOUNDARY_CODES = (
    "live_prompt_library_read_as_fixture",
    "live_freeze_memory_read_as_fixture",
    "live_router_canon_read_as_fixture",
    "runtime_router_object_used_as_fixture",
    "prompt_loader_invoked_for_fixture",
    "provider_call_for_fixture_creation",
    "embedding_call_for_fixture_creation",
    "freeze_memory_mutation",
    "prompt_library_mutation",
    "router_canon_mutation",
    "gold_registry_mutation",
    "startup_pack_mutation",
    "human_approval_record_mutation",
    "activation_state_mutation",
    "field_test_state_mutation",
    "runtime_decision_log_mutation",
    "persistent_ml_decision_storage_mutation",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_lab_python_files_are_allowed_for_current_milestone() -> None:
    """Allow only governed LAB Python files introduced up to LAB-7."""
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    allowed_after_lab6 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"]
    allowed_after_lab7 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py", "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"]
    allowed_after_lab10 = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
    assert python_files in ([], allowed_after_lab6, allowed_after_lab7, allowed_after_lab10)

def test_lab5_contract_doc_exists() -> None:
    assert CONTRACT_DOC.is_file()


def test_lab5_box_remains_documentation_only_with_no_python_modules() -> None:
    assert LAB_BOX.is_dir()
    _assert_lab_python_files_are_allowed_for_current_milestone()


def test_lab5_declares_documentation_only_scope_and_non_claims() -> None:
    text = _read(CONTRACT_DOC)
    assert FEATURE_ID in text
    assert "LAB-5 is documentation/governance design only" in text
    for phrase in (
        "does not create actual fixture files",
        "does not create hash manifest data files",
        "does not create fixture data",
        "does not create a corpus",
        "does not create a runner",
        "does not evaluate a candidate",
        "does not prove ML router prompt logic reliability",
        "does not authorize continuing ML implementation",
    ):
        assert phrase in text, phrase


def test_lab5_declares_static_copied_fixture_doctrine() -> None:
    text = _read(CONTRACT_DOC)
    for phrase in (
        "A LAB fixture is a frozen copied snapshot",
        "A LAB fixture is not a live link",
        "not a prompt loader",
        "not a route authority",
        "not a freeze-memory reader",
        "not a router-canon reader",
        "does not copy source material and does not create fixture files",
    ):
        assert phrase in text, phrase


def test_lab5_declares_future_fixture_record_shape() -> None:
    text = _read(CONTRACT_DOC)
    for field in REQUIRED_FUTURE_FIXTURE_FIELDS:
        assert field in text, field
    for kind in (
        "router_prompt_logic_snapshot",
        "freeze_memory_summary_snapshot",
        "routing_canon_snapshot",
        "prompt_group_index_snapshot",
        "box_boundary_snapshot",
        "patch_delivery_rule_snapshot",
        "validation_marker_snapshot",
        "roadmap_lock_snapshot",
        "known_failure_regression_snapshot",
    ):
        assert kind in text, kind


def test_lab5_declares_future_hash_manifest_record_shape() -> None:
    text = _read(CONTRACT_DOC)
    for field in REQUIRED_FUTURE_MANIFEST_FIELDS:
        assert field in text, field
    assert "A manifest is an integrity record for copied fixtures" in text
    assert "not a live discovery index" in text
    assert "LAB-5 does not create a manifest data file" in text


def test_lab5_declares_hash_algorithm_and_canonicalization_doctrine() -> None:
    text = _read(CONTRACT_DOC)
    for phrase in (
        "SHA-256",
        "UTF-8 text encoding",
        "line-ending normalization rule",
        "field ordering rule",
        "included fields",
        "excluded volatile fields",
        "does not implement hashing code",
    ):
        assert phrase in text, phrase


def test_lab5_declares_static_fixture_read_model_and_forbidden_live_sources() -> None:
    text = _read(CONTRACT_DOC)
    for phrase in (
        "Future LAB evaluation may read only copied, reviewed fixture snapshots",
        "Traceability metadata cannot become an automatic live read instruction",
        "kanda_prompt_workspace/prompt_library",
        "project_freeze_after_update/frozen_features_memory",
        "project_freeze_ledger",
        "runtime router modules",
        "prompt loader modules",
        "provider configuration",
        "embedding/vector stores",
    ):
        assert phrase in text, phrase


def test_lab5_declares_lab_invalid_and_critical_boundary_rules() -> None:
    text = _read(CONTRACT_DOC)
    for code in LAB_INVALID_CODES:
        assert code in text, code
    for code in CRITICAL_BOUNDARY_CODES:
        assert code in text, code
    assert "LAB_INVALID means the LAB is not in a valid state to evaluate the candidate" in text
    assert "critical boundary error budget at zero" in text


def test_lab5_declares_immutability_traceability_and_relationship_to_lab4_lab6() -> None:
    text = _read(CONTRACT_DOC)
    for phrase in (
        "Once a fixture is frozen for a fixture set, it must not be edited in place",
        "Correction requires a new fixture version",
        "A future candidate run must record the fixture set version and manifest hash",
        "source_freeze_id",
        "source_canon_rule_references",
        "human_review_reference",
        "LAB-4 defined the future field `fixture_hash_reference`",
        "LAB-6 may only begin after LAB-5 is locally validated and frozen",
        "LAB-5 itself does not create a runner",
    ):
        assert phrase in text, phrase


def test_lab5_updates_readme_boundary_and_allowed_artifacts() -> None:
    readme = _read(LAB_BOX / "README.md")
    boundary = _read(LAB_BOX / "LAB_PHASE_BOUNDARY.md")
    allowed = _read(LAB_BOX / "LAB_ALLOWED_ARTIFACTS.md")
    for text in (readme, boundary, allowed):
        assert "LAB-5" in text
        assert "Frozen Canon Fixture Format + Hash Manifest" in text
        assert "LAB-6" in text
    assert "actual fixture files" in allowed
    assert "hash manifest data files" in allowed
    assert "live canon readers" in allowed


def test_lab5_manifest_metadata_declares_non_runtime_boundary() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_feature_id"] == FEATURE_ID
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_documentation_only"] is True
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_actual_fixtures"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_hash_manifest_data"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_runner"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_live_canon_readers"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_live_freeze_memory_readers"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_provider_calls"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_embeddings"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_runtime_pilot"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_contains_copilot_behavior"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_hash_algorithm"] == "SHA-256"
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_static_copied_fixtures_only"] is True
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_live_source_reads_allowed"] is False
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_fixture_hash_mismatch_lab_invalid"] is True
    assert data["ml_lab_frozen_canon_fixture_format_hash_manifest_critical_boundary_error_budget"] == 0
    assert "LAB-6 Deterministic Runner Skeleton" in data["ml_lab_frozen_canon_fixture_format_hash_manifest_next_safe_milestone"]


if __name__ == "__main__":
    test_lab5_contract_doc_exists()
    test_lab5_box_remains_documentation_only_with_no_python_modules()
    test_lab5_declares_documentation_only_scope_and_non_claims()
    test_lab5_declares_static_copied_fixture_doctrine()
    test_lab5_declares_future_fixture_record_shape()
    test_lab5_declares_future_hash_manifest_record_shape()
    test_lab5_declares_hash_algorithm_and_canonicalization_doctrine()
    test_lab5_declares_static_fixture_read_model_and_forbidden_live_sources()
    test_lab5_declares_lab_invalid_and_critical_boundary_rules()
    test_lab5_declares_immutability_traceability_and_relationship_to_lab4_lab6()
    test_lab5_updates_readme_boundary_and_allowed_artifacts()
    test_lab5_manifest_metadata_declares_non_runtime_boundary()
    print(
        "CONTRACT_TEST_OK: LAB-5 ML LAB Frozen Canon Fixture Format + Hash Manifest v1, "
        "immutable governed documentation-only fixture-format/hash-manifest design after LAB-4 freeze with FREEZE_MEMORY_STATUS OK, "
        "defines future copied fixture snapshot format, future hash manifest record shape, SHA-256 hash doctrine, "
        "static fixture read model, no live canon coupling, no live freeze-memory coupling, fixture immutability, "
        "fixture traceability, LAB_INVALID handling for hash/manifest/source-review failures, critical boundary rules for live reads or mutations, "
        "roadmap lock, zero critical boundary error budget preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission "
        "and ML router prompt logic reliability is validated, no LAB code, no schema code, no executable validators, no actual fixtures, no hash manifest data files, "
        "no corpus, no runner, no executable scoring engine, no metrics engine, no candidate harness, no live readers, no live detectors, no import scanner, "
        "no write guard, no prompt loading, no persistence, no provider calls, no embeddings, no training-data use, no batch mode, no activation key, "
        "no field-test mode, no runtime Pilot, no Copilot behavior, LAB-6 Deterministic Runner Skeleton next"
    )
