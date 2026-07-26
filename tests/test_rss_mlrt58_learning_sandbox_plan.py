from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_58_LEARNING_SANDBOX_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt58_learning_sandbox_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-58 Learning Sandbox Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-59 First Controlled Learning Experiment Plan v1"
POS_LABEL = "RSS_MLRT58_LEARNING_SANDBOX_PLAN_DEFINED_NO_LEARNING"
PREFIX = "rss_mlrt58_learning_sandbox_plan"


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


def test_mlrt58_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt58_documents_learning_sandbox_plan_only() -> None:
    text = read(DOC)
    required = [
        "defines the **learning sandbox plan**",
        "does **not** create a learning sandbox implementation",
        "does **not** create a sandbox workspace",
        "does **not** create a sandbox runner",
        "does **not** run a learning experiment",
        "does **not** create learning inputs",
        "does **not** create learning outputs",
        "does **not** create learning records or persist learning results",
        "The critical boundary error budget remains `0`",
        "Learning sandbox plan: a documented future procedure",
        "Learning sandbox environment: a future isolated non-runtime, non-authoritative workspace",
        "Learning sandbox runner: a future non-runtime runner",
        "Learning experiment: a future controlled rehearsal",
        "Model learning: any operation that changes model behavior",
        "Learning outputs are explicitly non-training, non-gold, non-runtime, and non-authoritative.",
        "Validation proves the sandbox preview cannot write results, persist records, mutate data, train, calibrate, learn, or grant route authority.",
        "learning_sandbox_plan_defined = true",
        "learning_sandbox_enabled = false",
        "learning_sandbox_created = false",
        "learning_sandbox_runner_created = false",
        "learning_sandbox_workspace_created = false",
        "learning_sandbox_executed = false",
        "learning_experiment_enabled = false",
        "learning_experiment_started = false",
        "learning_inputs_created = false",
        "learning_outputs_created = false",
        "learning_records_created = false",
        "learning_results_persisted = false",
        "model_learning_started = false",
        "model_training_started = false",
        "model_calibration_started = false",
        "model_improvement_started = false",
        "offline_evaluation_run_enabled = false",
        "case_execution_enabled = false",
        "case_scoring_enabled = false",
        "route_comparison_enabled = false",
        "report_generation_enabled = false",
        "gold_registry_mutation_enabled = false",
        "training_data_use_enabled = false",
        "route_authority_enabled = false",
        "MLRT-59 -> First Controlled Learning Experiment Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt58_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt58_stub_boundary_still_blocks_learning_sandbox_and_training_use() -> None:
    module = load_module(SOURCE, "mlrt58_stub_under_learning_sandbox_plan_test")
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


def test_mlrt58_does_not_create_learning_or_sandbox_positive_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "learning sandbox may run now",
        "learning sandbox is enabled",
        "learning sandbox is created",
        "sandbox runner is created",
        "learning experiment is enabled",
        "learning experiment is started",
        "learning inputs are created",
        "learning outputs are created",
        "learning records are created",
        "learning results are persisted",
        "model learning is enabled",
        "model training is enabled",
        "model calibration is enabled",
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
        "must not claim learning sandbox readiness for execution",
        "controlled learning experiment readiness",
        "model learning readiness",
        "learning_sandbox_enabled = false",
        "learning_sandbox_created = false",
        "learning_sandbox_runner_created = false",
        "learning_sandbox_workspace_created = false",
        "learning_experiment_started = false",
        "learning_inputs_created = false",
        "learning_outputs_created = false",
        "learning_records_created = false",
        "learning_results_persisted = false",
        "model_learning_started = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt58_manifest_records_plan_without_unlocking_learning_sandbox() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        "learning_sandbox_plan_defined",
        "learning_sandbox_enabled",
        "learning_sandbox_created",
        "learning_sandbox_runner_created",
        "learning_sandbox_workspace_created",
        "learning_sandbox_executed",
        "learning_experiment_enabled",
        "learning_experiment_started",
        "learning_inputs_created",
        "learning_outputs_created",
        "learning_records_created",
        "learning_results_persisted",
        "learning_metrics_applied",
        "model_learning_started",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
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
    assert f'"{PREFIX}_learning_sandbox_plan_defined": true' in manifest
    false_flags = [
        "learning_sandbox_enabled",
        "learning_sandbox_created",
        "learning_sandbox_runner_created",
        "learning_sandbox_workspace_created",
        "learning_sandbox_executed",
        "learning_experiment_enabled",
        "learning_experiment_started",
        "learning_inputs_created",
        "learning_outputs_created",
        "learning_records_created",
        "learning_results_persisted",
        "learning_metrics_applied",
        "model_learning_started",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "controlled_learning_experiment_started",
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


def test_mlrt58_readme_references_learning_sandbox_plan_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "learning sandbox planning only" in readme
    assert "No learning sandbox implementation, sandbox workspace, sandbox runner, learning experiment, learning input, learning output, learning record, or learning result persistence is created" in readme
    assert "No training-data intake, dataset, labels, model training, model calibration, model improvement, offline evaluation run, scoring, route comparison, report generation, gold mutation, route authority, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt58_files_exist()
    test_mlrt58_documents_learning_sandbox_plan_only()
    test_mlrt58_only_allowed_python_surfaces_exist()
    test_mlrt58_stub_boundary_still_blocks_learning_sandbox_and_training_use()
    test_mlrt58_does_not_create_learning_or_sandbox_positive_claims()
    test_mlrt58_manifest_records_plan_without_unlocking_learning_sandbox()
    test_mlrt58_readme_references_learning_sandbox_plan_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-58 Learning Sandbox Plan v1, "
        "defined the future learning sandbox plan after MLRT-57 freeze; no learning sandbox implementation, "
        "no sandbox workspace, no sandbox runner, no learning experiment, no learning inputs, no learning outputs, "
        "no learning records, no learning result persistence, no training-data intake, no dataset creation, "
        "no label creation, no model training, no model calibration, no model improvement, no offline evaluation run, "
        "no case execution, no case scoring, no route comparison, no report generation, no gold registry write, "
        "no registry mutation, no route authority, no prompt loading, no provider calls, no embeddings, "
        "no persistence, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT58_LEARNING_SANDBOX_PLAN_V1_VALIDATION_OK")
