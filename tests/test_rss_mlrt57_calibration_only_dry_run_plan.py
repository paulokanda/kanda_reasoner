from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_57_CALIBRATION_ONLY_DRY_RUN_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt57_calibration_only_dry_run_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-57 Calibration-Only Dry-Run Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-58 Learning Sandbox Plan v1"
POS_LABEL = "RSS_MLRT57_CALIBRATION_ONLY_DRY_RUN_PLAN_DEFINED_NO_CALIBRATION"
PREFIX = "rss_mlrt57_calibration_only_dry_run_plan"


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


def test_mlrt57_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt57_documents_calibration_only_dry_run_plan_only() -> None:
    text = read(DOC)
    required = [
        "defines the **calibration-only dry-run plan**",
        "does **not** run a calibration dry-run",
        "does **not** create calibration inputs",
        "does **not** create calibration outputs",
        "does **not** create thresholds, parameters, weights, metrics, score transforms, or calibration records",
        "does **not** start model calibration, model training, model improvement, learning, registry mutation, offline evaluation execution",
        "The critical boundary error budget remains `0`",
        "Calibration-only dry-run plan: a documented future procedure",
        "Calibration dry-run: a future non-authoritative rehearsal",
        "Model calibration: any operation that changes model behavior",
        "Calibration outputs are explicitly non-training, non-gold, non-runtime, and non-authoritative.",
        "Validation proves the dry-run preview cannot write results, mutate data, calibrate a model, or grant route authority.",
        "calibration_only_dry_run_plan_defined = true",
        "calibration_only_dry_run_enabled = false",
        "calibration_only_dry_run_executed = false",
        "calibration_dry_run_runner_created = false",
        "calibration_inputs_created = false",
        "calibration_outputs_created = false",
        "calibration_thresholds_created = false",
        "calibration_parameters_created = false",
        "calibration_records_created = false",
        "calibration_results_persisted = false",
        "calibration_metrics_applied = false",
        "model_calibration_started = false",
        "model_calibrated = false",
        "offline_evaluation_run_enabled = false",
        "case_execution_enabled = false",
        "case_scoring_enabled = false",
        "route_comparison_enabled = false",
        "report_generation_enabled = false",
        "gold_registry_mutation_enabled = false",
        "training_data_use_enabled = false",
        "route_authority_enabled = false",
        "MLRT-58 -> Learning Sandbox Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt57_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt57_stub_boundary_still_blocks_dry_run_calibration_and_training_use() -> None:
    module = load_module(SOURCE, "mlrt57_stub_under_calibration_only_dry_run_plan_test")
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


def test_mlrt57_does_not_create_calibration_or_dry_run_positive_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "calibration dry run may run now",
        "calibration dry run is enabled",
        "calibration inputs are created",
        "calibration outputs are created",
        "thresholds are created",
        "parameters are created",
        "model calibration is enabled",
        "model is calibrated",
        "offline evaluation is enabled",
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
        "must not claim model calibration readiness",
        "calibration readiness for execution",
        "threshold readiness",
        "route readiness",
        "calibration_only_dry_run_enabled = false",
        "calibration_only_dry_run_executed = false",
        "calibration_inputs_created = false",
        "calibration_outputs_created = false",
        "model_calibration_started = false",
        "model_calibrated = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt57_manifest_records_plan_without_unlocking_calibration() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        "calibration_only_dry_run_plan_defined",
        "calibration_only_dry_run_enabled",
        "calibration_only_dry_run_executed",
        "calibration_dry_run_runner_created",
        "calibration_inputs_created",
        "calibration_outputs_created",
        "calibration_thresholds_created",
        "calibration_parameters_created",
        "calibration_records_created",
        "calibration_results_persisted",
        "calibration_metrics_applied",
        "model_calibration_started",
        "model_calibrated",
        "offline_evaluation_run_enabled",
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
    assert f'"{PREFIX}_calibration_only_dry_run_plan_defined": true' in manifest
    false_flags = [
        "calibration_only_dry_run_enabled",
        "calibration_only_dry_run_executed",
        "calibration_dry_run_runner_created",
        "calibration_inputs_created",
        "calibration_outputs_created",
        "calibration_thresholds_created",
        "calibration_parameters_created",
        "calibration_records_created",
        "calibration_results_persisted",
        "calibration_metrics_applied",
        "model_calibration_started",
        "model_calibrated",
        "model_training_started",
        "model_improvement_started",
        "offline_evaluation_run_enabled",
        "offline_evaluation_run_executed",
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
        "candidate_execution_enabled",
        "route_authority_granted",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]
    for flag in false_flags:
        assert f'"{PREFIX}_{flag}": false' in manifest


def test_mlrt57_readme_references_calibration_only_plan_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "calibration-only dry-run planning only" in readme
    assert "No calibration dry-run, calibration input, calibration output, threshold, parameter, model calibration, or model update is created" in readme
    assert "No offline evaluation run, case execution, scoring, route comparison, report generation, dataset, gold mutation, training, route authority, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt57_files_exist()
    test_mlrt57_documents_calibration_only_dry_run_plan_only()
    test_mlrt57_only_allowed_python_surfaces_exist()
    test_mlrt57_stub_boundary_still_blocks_dry_run_calibration_and_training_use()
    test_mlrt57_does_not_create_calibration_or_dry_run_positive_claims()
    test_mlrt57_manifest_records_plan_without_unlocking_calibration()
    test_mlrt57_readme_references_calibration_only_plan_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-57 Calibration-Only Dry-Run Plan v1, "
        "defined the future calibration-only dry-run plan after MLRT-56 freeze; no calibration dry run, "
        "no calibration inputs, no calibration outputs, no thresholds, no parameter updates, no model calibration, "
        "no model training, no model improvement, no offline evaluation run, no case execution, no case scoring, "
        "no route comparison, no report generation, no gold registry write, no registry mutation, no dataset creation, "
        "no training-data use, no route authority, no prompt loading, no provider calls, no embeddings, "
        "no persistence, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT57_CALIBRATION_ONLY_DRY_RUN_PLAN_V1_VALIDATION_OK")
