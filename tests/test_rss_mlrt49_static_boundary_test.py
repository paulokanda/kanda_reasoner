from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_49_STATIC_BOUNDARY_TEST.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
FEATURE_ID = "rss_mlrt49_static_boundary_test_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-49 Static Boundary Test v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-50 Non-Runtime Harness Smoke Test v1"
POS_LABEL = "RSS_MLRT49_STATIC_BOUNDARY_TEST_PASSED_SOURCE_STILL_INERT"
PREFIX = "rss_mlrt49_static_boundary_test"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_source_module():
    spec = importlib.util.spec_from_file_location("mlrt49_static_boundary_source_import", SOURCE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    before = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())
    spec.loader.exec_module(module)
    after = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())
    assert before == after
    return module


def test_mlrt49_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()


def test_mlrt49_documents_first_post_source_static_boundary_test() -> None:
    text = read(DOC)
    required = [
        "MLRT-49 is the first post-source testing milestone",
        "static boundary test",
        "starts boundary testing, not candidate execution",
        "The critical boundary error budget remains `0`",
        SOURCE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt49_only_one_mlrt_python_source_file_exists() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]


def test_mlrt49_source_text_has_no_banned_runtime_or_io_api() -> None:
    source = read(SOURCE)
    banned = [
        "import os",
        "import sys",
        "import subprocess",
        "import socket",
        "import requests",
        "import urllib",
        "import pathlib",
        "from pathlib",
        "open(",
        "Path(",
        "write_text",
        "read_text",
        "mkdir",
        "rmdir",
        "unlink",
        "remove(",
        "rename(",
        "replace(",
        "exec(",
        "eval(",
        "compile(",
        "input(",
        "pickle",
        "sqlite",
        "shelve",
        "threading",
        "multiprocessing",
        "asyncio",
        "http",
        "socket",
        "requests",
    ]
    for token in banned:
        assert token not in source


def test_mlrt49_source_import_safe_and_static_boundary_assertion_passes() -> None:
    module = load_source_module()
    assert module.FEATURE_ID == "rss_mlrt48_controlled_minimal_source_creation_v1"
    assert module.CRITICAL_BOUNDARY_ERROR_BUDGET == 0
    assert module.assert_static_non_runtime_boundary() is True
    contract = module.get_stub_contract()
    assert contract["source_file_created"] is True
    assert contract["static_source_surface_only"] is True
    assert contract["import_safe"] is True
    assert contract["critical_boundary_error_budget"] == 0


def test_mlrt49_forbidden_capability_flags_remain_false() -> None:
    contract = load_source_module().get_stub_contract()
    forbidden_flags = [
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
    ]
    for flag in forbidden_flags:
        assert contract[flag] is False


def test_mlrt49_does_not_start_dry_run_candidate_training_or_item5() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "dry run is executed",
        "candidate execution is enabled",
        "route authority is granted",
        "training has started",
        "Item 5 has started",
        "reliability is validated",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "does not execute a dry run",
        "does not execute candidates",
        "does not score cases",
        "does not compare routes",
        "does not generate reports",
        "does not persist outputs",
        "does not use training data",
        "does not train",
        "does not calibrate",
        "does not improve a model",
        "does not start Item 5 governance",
        "does not grant route authority",
        "does not create runtime Pilot or Copilot behavior",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt49_manifest_records_static_boundary_test_without_unlocking_runtime() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        "static_boundary_test",
        "static_boundary_test_executed",
        "source_modified_by_mlrt49",
        "dry_run_executed",
        "candidate_executed",
        "item5_training_governance_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_static_boundary_test_executed": true' in manifest
    assert f'"{PREFIX}_source_modified_by_mlrt49": false' in manifest
    assert f'"{PREFIX}_dry_run_executed": false' in manifest
    assert f'"{PREFIX}_candidate_executed": false' in manifest
    assert f'"{PREFIX}_route_authority_granted": false' in manifest
    assert f'"{PREFIX}_item5_training_governance_started": false' in manifest


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt49_readme_references_static_boundary_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "first post-source static boundary testing milestone" in readme
    assert "Item 5 remains blocked" in readme


if __name__ == "__main__":
    test_mlrt49_files_exist()
    test_mlrt49_documents_first_post_source_static_boundary_test()
    test_mlrt49_only_one_mlrt_python_source_file_exists()
    test_mlrt49_source_text_has_no_banned_runtime_or_io_api()
    test_mlrt49_source_import_safe_and_static_boundary_assertion_passes()
    test_mlrt49_forbidden_capability_flags_remain_false()
    test_mlrt49_does_not_start_dry_run_candidate_training_or_item5()
    test_mlrt49_manifest_records_static_boundary_test_without_unlocking_runtime()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt49_readme_references_static_boundary_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-49 Static Boundary Test v1, "
        "verified exactly one inert non-runtime MLRT source file remains present, import-safe, side-effect-free, "
        "and all forbidden capability flags remain false; no dry run, no candidate execution, no route authority, "
        "no prompt loading, no provider calls, no embeddings, no persistence, no training-data use, no Item 5 start, "
        "no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT49_STATIC_BOUNDARY_TEST_V1_VALIDATION_OK")
