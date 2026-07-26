from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_48_CONTROLLED_MINIMAL_SOURCE_CREATION.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
FEATURE_ID = "rss_mlrt48_controlled_minimal_source_creation_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-48 Controlled Minimal Source Creation v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-49 Static Boundary Test v1"
POS_LABEL = "RSS_MLRT48_MINIMAL_NON_RUNTIME_SOURCE_CREATED_STATIC_ONLY"
PREFIX = "rss_mlrt48_controlled_minimal_source_creation"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_source_module():
    spec = importlib.util.spec_from_file_location("mlrt48_minimal_non_runtime_harness_stub", SOURCE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    before = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())
    spec.loader.exec_module(module)
    after = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())
    assert before == after
    return module


def test_mlrt48_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()


def test_mlrt48_source_created_at_exact_path() -> None:
    assert SOURCE_REL == SOURCE.relative_to(ROOT).as_posix()
    assert SOURCE.name == "minimal_non_runtime_harness_stub.py"
    assert SOURCE.parent.name == "source_surface"


def test_mlrt48_is_first_controlled_source_creation_not_testing_or_training() -> None:
    text = read(DOC)
    required = [
        "MLRT-48 is the first controlled source-creation milestone",
        "MLRT-48 intentionally ends the plan-only chain",
        "It creates exactly one inert non-runtime Python source file",
        "This is source creation only",
        "not harness testing",
        "not dry-run execution",
        "not candidate execution",
        "not reliability validation",
        "not training",
        "not Item 5 governance",
        "critical boundary error budget remains `0`",
    ]
    for item in required:
        assert item in text


def test_mlrt48_supersedes_zero_python_boundary_by_exactly_one_file() -> None:
    text = read(DOC)
    assert "supersedes the earlier temporary zero-Python-implementation rule" in text
    assert "exactly one permitted file" in text
    assert SOURCE_REL in text
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]


def test_mlrt48_source_has_no_banned_imports_or_side_effect_api() -> None:
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
    ]
    for token in banned:
        assert token not in source


def test_mlrt48_source_import_safe_and_contract_static() -> None:
    module = load_source_module()
    assert module.FEATURE_ID == FEATURE_ID
    assert module.CRITICAL_BOUNDARY_ERROR_BUDGET == 0
    assert module.assert_static_non_runtime_boundary() is True
    contract = module.get_stub_contract()
    assert contract["feature_id"] == FEATURE_ID
    assert contract["source_file_created"] is True
    assert contract["static_source_surface_only"] is True
    assert contract["import_safe"] is True
    assert contract["critical_boundary_error_budget"] == 0


def test_mlrt48_forbidden_capability_flags_are_false() -> None:
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


def test_mlrt48_manifest_records_controlled_source_creation() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        "controlled_minimal_source_creation",
        "python_source_files_created",
        "source_files_created",
        "source_creation_executed",
        "only_allowed_mlrt_python_file",
        "harness_testing_started",
        "item5_training_governance_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_python_source_files_created": true' in manifest
    assert f'"{PREFIX}_source_files_created": true' in manifest
    assert f'"{PREFIX}_source_creation_executed": true' in manifest
    assert f'"{PREFIX}_harness_testing_started": false' in manifest
    assert f'"{PREFIX}_item5_training_governance_started": false' in manifest
    assert f'"{PREFIX}_dry_run_executed": false' in manifest
    assert f'"{PREFIX}_candidate_executed": false' in manifest


def test_lab_python_surface_remains_exactly_three_files() -> None:
    py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt48_readme_references_feature_and_next_test() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert NEXT_TITLE in readme
    assert "first controlled source-creation milestone" in readme
    assert "Item 5 remains blocked" in readme


if __name__ == "__main__":
    test_mlrt48_files_exist()
    test_mlrt48_source_created_at_exact_path()
    test_mlrt48_is_first_controlled_source_creation_not_testing_or_training()
    test_mlrt48_supersedes_zero_python_boundary_by_exactly_one_file()
    test_mlrt48_source_has_no_banned_imports_or_side_effect_api()
    test_mlrt48_source_import_safe_and_contract_static()
    test_mlrt48_forbidden_capability_flags_are_false()
    test_mlrt48_manifest_records_controlled_source_creation()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt48_readme_references_feature_and_next_test()
    print(
        "CONTRACT_TEST_OK: MLRT-48 Controlled Minimal Source Creation v1, "
        "created exactly one inert non-runtime source file at source_surface/minimal_non_runtime_harness_stub.py, "
        "source imports safely, all forbidden capability flags remain false, no dry run, no candidate execution, "
        "no route authority, no prompt loading, no provider calls, no embeddings, no persistence, no training-data use, "
        "no runtime Pilot, no Copilot behavior, critical boundary error budget zero, next safe milestone is static boundary testing."
    )
    print("SANDBOX_RSS_MLRT48_CONTROLLED_MINIMAL_SOURCE_CREATION_V1_VALIDATION_OK")
