"""Contract tests for LAB-6 Deterministic Runner Skeleton v1."""

from __future__ import annotations

from dataclasses import is_dataclass
import importlib.util
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_BOX = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MODULE_PATH = LAB_BOX / "deterministic_runner_skeleton.py"
CONTRACT_DOC = LAB_BOX / "LAB_DETERMINISTIC_RUNNER_SKELETON.md"
MANIFEST = PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FEATURE_ID = "routing_signal_scorer_v3_ml_lab_deterministic_runner_skeleton_v1"
ALLOWED_LAB_PYTHON_FILES = [
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py",
    "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_lab_python_files_are_allowed_for_current_milestone() -> None:
    """Allow only governed LAB Python files introduced up to LAB-7."""
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    allowed_after_lab6 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"]
    allowed_after_lab7 = ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py", "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"]
    allowed_after_lab10 = ['kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py', 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py']
    assert python_files in ([], allowed_after_lab6, allowed_after_lab7, allowed_after_lab10)


def _load_module():
    spec = importlib.util.spec_from_file_location("lab6_deterministic_runner_skeleton", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_lab6_files_exist_and_lab_python_surface_is_exactly_allowed_skeleton() -> None:
    assert MODULE_PATH.is_file()
    assert CONTRACT_DOC.is_file()
    python_files = sorted(path.relative_to(PROJECT_ROOT).as_posix() for path in LAB_BOX.rglob("*.py"))
    assert set(python_files).issubset(set(ALLOWED_LAB_PYTHON_FILES))
    assert 'kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py' in python_files


def test_lab6_doc_declares_non_runtime_skeleton_scope() -> None:
    text = _read(CONTRACT_DOC)
    assert FEATURE_ID in text
    for phrase in (
        "first non-runtime deterministic runner skeleton",
        "non-authoritative `NOT_EVALUATED` run-plan records",
        "does not create actual fixtures",
        "does not create a corpus",
        "does not execute candidate evaluation",
        "does not create a runner"  # historical phrase must not appear as claim for LAB-6
    ):
        if phrase == "does not create a runner":
            assert phrase not in text
        else:
            assert phrase in text, phrase
    for phrase in (
        "does not create actual fixtures",
        "does not create a corpus",
        "does not execute candidate evaluation",
        "does not score candidates",
        "does not compare routes",
        "does not authorize continuing ML implementation",
    ):
        assert phrase in text, phrase


def test_lab6_module_imports_only_safe_standard_library_modules() -> None:
    source = _read(MODULE_PATH)
    forbidden_tokens = (
        "import requests",
        "from requests",
        "urllib",
        "httpx",
        "import socket",
        "import subprocess",
        "subprocess.",
        "import asyncio",
        "asyncio.",
        "PySide6",
        "open(",
        "Path(",
        "project_freeze_after_update",
        "kanda_prompt_workspace",
        "prompt_loader",
        "routing_signal_scorer.adviser_offline",
    )
    for token in forbidden_tokens:
        assert token not in source, token
    allowed_import_lines = {
        "from __future__ import annotations",
        "from dataclasses import dataclass",
        "import hashlib",
        "import json",
        "from types import MappingProxyType",
        "from typing import Final, Mapping",
    }
    import_lines = {line.strip() for line in source.splitlines() if line.startswith("import ") or line.startswith("from ")}
    assert import_lines == allowed_import_lines


def test_lab6_contract_record_is_immutable_non_authoritative_and_zero_authority() -> None:
    module = _load_module()
    record = module.get_lab6_deterministic_runner_skeleton_record()
    assert is_dataclass(record)
    assert record.feature_id == FEATURE_ID
    assert record.schema_version == "lab-6-deterministic-runner-skeleton"
    assert record.design_kind == "non_runtime_deterministic_runner_skeleton_only"
    assert record.outcome == "NOT_EVALUATED"
    assert record.storage_status == "in_memory_only"
    assert record.routing_effect == "none"
    assert record.prompt_loading_effect == "none"
    assert record.runtime_effect == "none"
    assert record.activation_effect == "none"
    assert record.critical_boundary_error_budget == 0
    assert "caller_supplied_fixture_manifest_metadata" in record.allowed_input_kinds
    for forbidden in (
        "load_prompt",
        "read_live_prompt_library",
        "read_live_freeze_memory",
        "read_live_router_canon",
        "execute_candidate_evaluation",
        "score_candidate_output",
        "compare_routes",
        "select_route",
        "call_provider",
        "call_embedding_model",
        "persist_ml_decision",
        "activate_pilot",
        "activate_copilot",
        "enable_field_test",
        "runtime_pilot_behavior",
        "copilot_behavior",
    ):
        assert forbidden in record.forbidden_operations


def test_lab6_canonicalization_and_hash_helpers_are_deterministic_and_in_memory() -> None:
    module = _load_module()
    first = {"b": 2, "a": {"z": 1}}
    second = {"a": {"z": 1}, "b": 2}
    canonical_first = module.canonicalize_json_like_metadata(first)
    canonical_second = module.canonicalize_json_like_metadata(second)
    assert canonical_first == canonical_second
    assert canonical_first == '{"a":{"z":1},"b":2}'
    assert module.compute_sha256_for_text("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_lab6_run_plan_is_not_evaluated_and_cannot_grant_authority() -> None:
    module = _load_module()
    plan = module.build_not_evaluated_run_plan(
        lab_run_id="lab-run-demo",
        candidate_output_reference="candidate-output-demo",
        test_case_reference="case-demo",
        fixture_set_version="fixture-set-demo",
        fixture_manifest_hash="0" * 64,
    )
    assert is_dataclass(plan)
    assert plan.outcome == "NOT_EVALUATED"
    assert plan.non_authoritative is True
    assert plan.candidate_evaluation_executed is False
    assert plan.route_authority_granted is False
    assert plan.prompt_loading_performed is False
    assert plan.provider_call_performed is False
    assert plan.embedding_call_performed is False
    assert plan.persistence_performed is False
    assert plan.activation_performed is False
    assert plan.field_test_performed is False
    assert plan.runtime_pilot_behavior_performed is False
    assert plan.copilot_behavior_performed is False
    assert plan.next_required_gate == "LAB-7 Lab Self-Validation Gate"


def test_lab6_read_only_mapping_cannot_be_mutated() -> None:
    module = _load_module()
    plan = module.build_not_evaluated_run_plan(
        lab_run_id="lab-run-demo",
        candidate_output_reference="candidate-output-demo",
        test_case_reference="case-demo",
        fixture_set_version="fixture-set-demo",
        fixture_manifest_hash="0" * 64,
    )
    view = module.as_read_only_mapping(plan)
    assert view["outcome"] == "NOT_EVALUATED"
    try:
        view["outcome"] = "PASS"  # type: ignore[index]
    except TypeError:
        pass
    else:  # pragma: no cover
        raise AssertionError("LAB-6 run-plan mapping must be read-only")


def test_lab6_no_forbidden_authority_fields_are_exposed_by_run_plan() -> None:
    module = _load_module()
    record = module.get_lab6_deterministic_runner_skeleton_record()
    plan = module.build_not_evaluated_run_plan(
        lab_run_id="lab-run-demo",
        candidate_output_reference="candidate-output-demo",
        test_case_reference="case-demo",
        fixture_set_version="fixture-set-demo",
        fixture_manifest_hash="0" * 64,
    )
    plan_keys = set(plan.__dict__)
    for field in record.forbidden_authority_fields:
        assert field not in plan_keys, field


def test_lab6_manifest_metadata_declares_non_runtime_runner_boundary() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["ml_lab_deterministic_runner_skeleton_feature_id"] == FEATURE_ID
    assert data["ml_lab_deterministic_runner_skeleton_contains_lab_python_modules"] is True
    assert data["ml_lab_deterministic_runner_skeleton_allowed_python_modules"] == ["kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"]
    assert data["ml_lab_deterministic_runner_skeleton_contains_actual_fixtures"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_hash_manifest_data"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_corpus"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_executable_candidate_evaluation"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_executable_scoring_engine"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_candidate_harness"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_live_prompt_library_reads"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_live_freeze_memory_reads"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_live_router_canon_reads"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_runtime_router_imports"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_prompt_loading"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_persistence"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_provider_calls"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_embeddings"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_network_calls"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_subprocess_calls"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_batch_mode"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_activation_key"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_field_test_mode"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_runtime_pilot"] is False
    assert data["ml_lab_deterministic_runner_skeleton_contains_copilot_behavior"] is False
    assert data["ml_lab_deterministic_runner_skeleton_storage_status"] == "in_memory_only"
    assert data["ml_lab_deterministic_runner_skeleton_output_outcome"] == "NOT_EVALUATED"
    assert data["ml_lab_deterministic_runner_skeleton_critical_boundary_error_budget"] == 0
    assert "LAB-7 Lab Self-Validation Gate" in data["ml_lab_deterministic_runner_skeleton_next_safe_milestone"]


if __name__ == "__main__":
    test_lab6_files_exist_and_lab_python_surface_is_exactly_allowed_skeleton()
    test_lab6_doc_declares_non_runtime_skeleton_scope()
    test_lab6_module_imports_only_safe_standard_library_modules()
    test_lab6_contract_record_is_immutable_non_authoritative_and_zero_authority()
    test_lab6_canonicalization_and_hash_helpers_are_deterministic_and_in_memory()
    test_lab6_run_plan_is_not_evaluated_and_cannot_grant_authority()
    test_lab6_read_only_mapping_cannot_be_mutated()
    test_lab6_no_forbidden_authority_fields_are_exposed_by_run_plan()
    test_lab6_manifest_metadata_declares_non_runtime_runner_boundary()
    print(
        "CONTRACT_TEST_OK: LAB-6 ML LAB Deterministic Runner Skeleton v1, "
        "immutable governed non-runtime deterministic runner skeleton after LAB-5 freeze with FREEZE_MEMORY_STATUS OK, "
        "adds first allowed LAB Python skeleton file, pure in-memory caller-supplied metadata only, NOT_EVALUATED output only, "
        "read-only non-authoritative run-plan records, deterministic canonicalization and SHA-256 text hash helpers, no live prompt-library reads, "
        "no live freeze-memory reads, no live router-canon reads, no runtime router imports, no fixture file reads, no actual fixtures, no hash manifest data files, "
        "no corpus, no candidate evaluation, no route comparison, no route authority, no scoring engine, no metrics engine, no candidate harness, no report persistence, "
        "no prompt loading, no provider calls, no embeddings, no network calls, no subprocess calls, no batch mode, no persistent ML decisions, no activation key, "
        "no field-test mode, no runtime Pilot, no Copilot behavior, zero critical boundary doctrine preserved, ML implementation continuation remains blocked until LAB/test fulfills its mission and ML router prompt logic reliability is validated, LAB-7 Lab Self-Validation Gate next"
    )
