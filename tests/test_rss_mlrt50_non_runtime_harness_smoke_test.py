from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_50_NON_RUNTIME_HARNESS_SMOKE_TEST.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
FEATURE_ID = "rss_mlrt50_non_runtime_harness_smoke_test_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-50 Non-Runtime Harness Smoke Test v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-51 Candidate Evaluation Harness Self-Test v1"
POS_LABEL = "RSS_MLRT50_NON_RUNTIME_HARNESS_SMOKE_TEST_PASSED_STUB_STILL_INERT"
PREFIX = "rss_mlrt50_non_runtime_harness_smoke_test"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_snapshot() -> list[str]:
    return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())


def load_source_module():
    spec = importlib.util.spec_from_file_location("mlrt50_non_runtime_harness_smoke_source_import", SOURCE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    before = file_snapshot()
    spec.loader.exec_module(module)
    after = file_snapshot()
    assert before == after
    return module


def smoke_call_contracts(module):
    before = file_snapshot()
    first = dict(module.get_stub_contract())
    assert module.assert_static_non_runtime_boundary() is True
    second = dict(module.get_stub_contract())
    assert module.assert_static_non_runtime_boundary() is True
    after = file_snapshot()
    assert before == after
    assert first == second
    return first


def test_mlrt50_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()


def test_mlrt50_documents_non_runtime_smoke_test_only() -> None:
    text = read(DOC)
    required = [
        "first non-runtime smoke test",
        "smoke test of the inert stub contract only",
        "not a dry run",
        "not candidate execution",
        "not case scoring",
        "not route comparison",
        "not report generation",
        "not reliability validation",
        "not Item 5 training/learning governance",
        "The critical boundary error budget remains `0`",
        SOURCE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt50_only_one_mlrt_python_source_file_exists() -> None:
    py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]


def test_mlrt50_import_and_public_contract_smoke_calls_are_side_effect_free() -> None:
    module = load_source_module()
    contract = smoke_call_contracts(module)
    assert module.FEATURE_ID == "rss_mlrt48_controlled_minimal_source_creation_v1"
    assert module.CRITICAL_BOUNDARY_ERROR_BUDGET == 0
    assert contract["source_file_created"] is True
    assert contract["static_source_surface_only"] is True
    assert contract["import_safe"] is True
    assert contract["critical_boundary_error_budget"] == 0


def test_mlrt50_all_forbidden_capability_flags_remain_false() -> None:
    contract = smoke_call_contracts(load_source_module())
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


def test_mlrt50_does_not_start_dry_run_candidate_training_or_item5() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "dry run is executed",
        "candidate execution is enabled",
        "case scoring is enabled",
        "route authority is granted",
        "Item 5 has started",
        "reliability is validated",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not modify the source file",
        "must not claim validated candidate reliability",
        "not a dry run",
        "not candidate execution",
        "not Item 5 training/learning governance",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt50_manifest_records_smoke_test_without_unlocking_runtime() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        "non_runtime_harness_smoke_test",
        "smoke_test_executed",
        "source_modified_by_mlrt50",
        "dry_run_executed",
        "candidate_executed",
        "item5_training_governance_started",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_smoke_test_executed": true' in manifest
    assert f'"{PREFIX}_source_modified_by_mlrt50": false' in manifest
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


def test_mlrt50_readme_references_smoke_test_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "non-runtime smoke test" in readme
    assert "Item 5 remains blocked" in readme


if __name__ == "__main__":
    test_mlrt50_files_exist()
    test_mlrt50_documents_non_runtime_smoke_test_only()
    test_mlrt50_only_one_mlrt_python_source_file_exists()
    test_mlrt50_import_and_public_contract_smoke_calls_are_side_effect_free()
    test_mlrt50_all_forbidden_capability_flags_remain_false()
    test_mlrt50_does_not_start_dry_run_candidate_training_or_item5()
    test_mlrt50_manifest_records_smoke_test_without_unlocking_runtime()
    test_lab_python_surface_remains_exactly_three_files()
    test_mlrt50_readme_references_smoke_test_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-50 Non-Runtime Harness Smoke Test v1, "
        "smoke-tested the inert MLRT harness stub by import and public contract calls only; "
        "no source modification, no dry run, no candidate execution, no case scoring, no route authority, "
        "no prompt loading, no provider calls, no embeddings, no persistence, no training-data use, no Item 5 start, "
        "no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT50_NON_RUNTIME_HARNESS_SMOKE_TEST_V1_VALIDATION_OK")
