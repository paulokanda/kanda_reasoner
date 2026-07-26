from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_56_OFFLINE_EVALUATION_PROTOCOL_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt56_offline_evaluation_protocol_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-56 Offline Evaluation Protocol Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-57 Calibration-Only Dry-Run Plan v1"
POS_LABEL = "RSS_MLRT56_OFFLINE_EVALUATION_PROTOCOL_DEFINED_NO_EXECUTION"
PREFIX = "rss_mlrt56_offline_evaluation_protocol"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_snapshot() -> list[str]:
    ignored_parts = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return sorted(
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file() and not any(part in ignored_parts for part in p.parts)
    )


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    import sys
    before = file_snapshot()
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(name, None)
    after = file_snapshot()
    assert before == after
    return module


def test_mlrt56_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt56_documents_offline_evaluation_protocol_only() -> None:
    text = read(DOC)
    required = [
        "defines the **offline evaluation protocol**",
        "does **not** run offline evaluation",
        "does **not** execute candidates",
        "does **not** execute cases",
        "does **not** score cases",
        "does **not** compare routes",
        "does **not** generate reports",
        "does **not** create datasets, labels, gold records, gold registries, mutation proposals, mutation diffs, or registry writes",
        "does **not** train, calibrate, improve, or authorize a model",
        "The critical boundary error budget remains `0`",
        "Offline evaluation protocol: a documented future procedure",
        "Evaluation run: a future controlled invocation of the offline protocol; forbidden in MLRT-56.",
        "Case scoring: future measurement of a case outcome; forbidden in MLRT-56.",
        "Route comparison: future comparison between expected route and candidate route; forbidden in MLRT-56.",
        "Reliability claim: any statement that candidate/router/model behavior is reliable; forbidden in MLRT-56.",
        "Candidate execution remains unavailable until a later explicit execution milestone.",
        "Validation proves preview/protocol checks cannot execute cases or write results.",
        "offline_evaluation_protocol_defined = true",
        "offline_evaluation_case_schema_created = false",
        "offline_evaluation_corpus_created = false",
        "offline_evaluation_cases_created = false",
        "offline_evaluation_runner_created = false",
        "offline_evaluation_run_enabled = false",
        "offline_evaluation_run_executed = false",
        "offline_evaluation_results_created = false",
        "offline_evaluation_results_persisted = false",
        "candidate_execution_enabled = false",
        "case_execution_enabled = false",
        "case_scoring_enabled = false",
        "route_comparison_enabled = false",
        "report_generation_enabled = false",
        "reliability_claim_enabled = false",
        "gold_registry_mutation_enabled = false",
        "training_data_use_enabled = false",
        "route_authority_enabled = false",
        "MLRT-57 -> Calibration-Only Dry-Run Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt56_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt56_stub_boundary_still_blocks_execution_scoring_and_training_use() -> None:
    module = load_module(SOURCE, "mlrt56_stub_under_offline_evaluation_protocol_test")
    assert module.assert_static_non_runtime_boundary() is True
    contract = module.get_stub_contract()
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
    assert contract["critical_boundary_error_budget"] == 0
    for flag in forbidden_flags:
        assert contract[flag] is False


def test_mlrt56_does_not_create_evaluation_execution_positive_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "offline evaluation may run now",
        "offline evaluation is enabled",
        "evaluation cases are created",
        "evaluation corpus is created",
        "evaluation results are created",
        "case scoring is enabled",
        "route comparison is enabled",
        "report generation is enabled",
        "candidate execution is enabled",
        "route authority is granted",
        "Pilot is enabled",
        "Copilot is enabled",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not claim candidate reliability",
        "protocol readiness for execution",
        "evaluation readiness for execution",
        "score readiness",
        "route readiness",
        "offline_evaluation_run_enabled = false",
        "offline_evaluation_run_executed = false",
        "offline_evaluation_results_created = false",
        "case_scoring_enabled = false",
        "route_comparison_enabled = false",
        "report_generation_enabled = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt56_manifest_records_protocol_without_unlocking_execution() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        "offline_evaluation_protocol_defined",
        "offline_evaluation_case_schema_created",
        "offline_evaluation_corpus_created",
        "offline_evaluation_cases_created",
        "offline_evaluation_runner_created",
        "offline_evaluation_run_enabled",
        "offline_evaluation_run_executed",
        "offline_evaluation_results_created",
        "offline_evaluation_results_persisted",
        "case_execution_enabled",
        "case_scoring_enabled",
        "route_comparison_enabled",
        "report_generation_enabled",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_offline_evaluation_protocol_defined": true' in manifest
    false_flags = [
        "offline_evaluation_case_schema_created",
        "offline_evaluation_corpus_created",
        "offline_evaluation_cases_created",
        "offline_evaluation_runner_created",
        "offline_evaluation_run_enabled",
        "offline_evaluation_run_executed",
        "offline_evaluation_results_created",
        "offline_evaluation_results_persisted",
        "case_execution_enabled",
        "case_scoring_enabled",
        "route_comparison_enabled",
        "report_generation_enabled",
        "reliability_claim_enabled",
        "gold_registry_mutation_enabled",
        "gold_registry_mutated",
        "training_data_use_enabled",
        "training_dataset_created",
        "training_labels_created",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "candidate_execution_enabled",
        "route_authority_granted",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]
    for flag in false_flags:
        assert f'"{PREFIX}_{flag}": false' in manifest


def test_mlrt56_readme_references_offline_protocol_only_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "offline evaluation protocol planning only" in readme
    assert "No offline evaluation run, case creation, candidate execution, case scoring, route comparison, report generation, or reliability claim is created" in readme
    assert "No dataset, label, gold mutation, training, calibration, route authority, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt56_files_exist()
    test_mlrt56_documents_offline_evaluation_protocol_only()
    test_mlrt56_only_allowed_python_surfaces_exist()
    test_mlrt56_stub_boundary_still_blocks_execution_scoring_and_training_use()
    test_mlrt56_does_not_create_evaluation_execution_positive_claims()
    test_mlrt56_manifest_records_protocol_without_unlocking_execution()
    test_mlrt56_readme_references_offline_protocol_only_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-56 Offline Evaluation Protocol Plan v1, "
        "defined the future offline evaluation protocol after MLRT-55 freeze; no offline evaluation run, "
        "no case execution, no case scoring, no route comparison, no report generation, no gold registry write, "
        "no registry mutation, no dataset creation, no training-data use, no model training, no model calibration, "
        "no model improvement, no route authority, no prompt loading, no provider calls, no embeddings, "
        "no persistence, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT56_OFFLINE_EVALUATION_PROTOCOL_PLAN_V1_VALIDATION_OK")
