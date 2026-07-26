from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_59_FIRST_CONTROLLED_LEARNING_EXPERIMENT_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt59_first_controlled_learning_experiment_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-59 First Controlled Learning Experiment Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-60 Gold Registry Schema Proposal Plan v1"
POS_LABEL = "RSS_MLRT59_FIRST_CONTROLLED_LEARNING_EXPERIMENT_PLAN_DEFINED_NO_EXPERIMENT"
PREFIX = "rss_mlrt59_first_controlled_learning_experiment_plan"


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


def test_mlrt59_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt59_documents_first_controlled_learning_experiment_plan_only() -> None:
    text = read(DOC)
    required = [
        "defines the **first controlled learning experiment plan**",
        "does **not** create a controlled learning experiment implementation",
        "does **not** create an experiment runner",
        "does **not** create a sandbox workspace",
        "does **not** start or run a learning experiment",
        "does **not** create learning inputs",
        "does **not** create learning outputs",
        "does **not** create learning records or persist learning results",
        "The critical boundary error budget remains `0`",
        "First controlled learning experiment plan: a documented future procedure",
        "Controlled learning experiment: a future non-runtime, non-authoritative rehearsal",
        "Experiment runner: a future runner",
        "Experiment envelope: a future static description",
        "Experiment input: a future non-training, non-gold, non-runtime, non-authoritative input",
        "Experiment output: a future non-authoritative observation",
        "Learning result: a future sandbox-only observation",
        "Model learning: any operation that changes model behavior",
        "Experiment inputs are explicitly non-training, non-gold, non-runtime, non-authoritative, and non-persistent.",
        "Validation proves a future experiment preview cannot write results, persist records, mutate data, train, calibrate, learn, score, compare routes, generate reports, or grant route authority.",
        "first_controlled_learning_experiment_plan_defined = true",
        "controlled_learning_experiment_enabled = false",
        "controlled_learning_experiment_created = false",
        "controlled_learning_experiment_started = false",
        "controlled_learning_experiment_executed = false",
        "experiment_runner_created = false",
        "experiment_envelope_created = false",
        "experiment_inputs_created = false",
        "experiment_outputs_created = false",
        "experiment_records_created = false",
        "experiment_results_persisted = false",
        "learning_sandbox_enabled = false",
        "learning_sandbox_created = false",
        "learning_inputs_created = false",
        "learning_outputs_created = false",
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
        "MLRT-60 -> Gold Registry Schema Proposal Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt59_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt59_stub_boundary_still_blocks_experiment_and_training_use() -> None:
    module = load_module(SOURCE, "mlrt59_stub_under_first_controlled_experiment_plan_test")
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


def test_mlrt59_does_not_create_experiment_or_learning_positive_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "controlled learning experiment may run now",
        "controlled learning experiment is enabled",
        "controlled learning experiment is created",
        "controlled learning experiment is started",
        "experiment runner is created",
        "experiment envelope is created",
        "experiment inputs are created",
        "experiment outputs are created",
        "experiment records are created",
        "experiment results are persisted",
        "learning sandbox is enabled",
        "learning sandbox is created",
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
        "must not claim controlled learning experiment readiness",
        "experiment execution readiness",
        "learning sandbox readiness for execution",
        "model learning readiness",
        "controlled_learning_experiment_enabled = false",
        "controlled_learning_experiment_created = false",
        "controlled_learning_experiment_started = false",
        "controlled_learning_experiment_executed = false",
        "experiment_runner_created = false",
        "experiment_inputs_created = false",
        "experiment_outputs_created = false",
        "experiment_records_created = false",
        "experiment_results_persisted = false",
        "model_learning_started = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt59_manifest_records_plan_without_unlocking_experiment() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        "first_controlled_learning_experiment_plan_defined",
        "controlled_learning_experiment_enabled",
        "controlled_learning_experiment_created",
        "controlled_learning_experiment_started",
        "controlled_learning_experiment_executed",
        "experiment_runner_created",
        "experiment_envelope_created",
        "experiment_inputs_created",
        "experiment_outputs_created",
        "experiment_records_created",
        "experiment_results_persisted",
        "learning_sandbox_enabled",
        "learning_sandbox_created",
        "learning_sandbox_runner_created",
        "learning_sandbox_workspace_created",
        "learning_sandbox_executed",
        "learning_inputs_created",
        "learning_outputs_created",
        "learning_records_created",
        "learning_results_persisted",
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
    assert f'"{PREFIX}_first_controlled_learning_experiment_plan_defined": true' in manifest
    false_flags = [
        "controlled_learning_experiment_enabled",
        "controlled_learning_experiment_created",
        "controlled_learning_experiment_started",
        "controlled_learning_experiment_executed",
        "experiment_runner_created",
        "experiment_envelope_created",
        "experiment_inputs_created",
        "experiment_outputs_created",
        "experiment_records_created",
        "experiment_results_persisted",
        "experiment_metrics_applied",
        "learning_sandbox_enabled",
        "learning_sandbox_created",
        "learning_sandbox_runner_created",
        "learning_sandbox_workspace_created",
        "learning_sandbox_executed",
        "learning_inputs_created",
        "learning_outputs_created",
        "learning_records_created",
        "learning_results_persisted",
        "model_learning_started",
        "model_training_started",
        "model_calibration_started",
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


def test_mlrt59_readme_references_experiment_plan_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "first controlled learning experiment planning only" in readme
    assert "No controlled learning experiment implementation, experiment runner, sandbox workspace, learning input, learning output, learning record, or learning result persistence is created" in readme
    assert "No training-data intake, dataset, labels, model training, model calibration, model improvement, offline evaluation run, scoring, route comparison, report generation, gold mutation, route authority, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt59_files_exist()
    test_mlrt59_documents_first_controlled_learning_experiment_plan_only()
    test_mlrt59_only_allowed_python_surfaces_exist()
    test_mlrt59_stub_boundary_still_blocks_experiment_and_training_use()
    test_mlrt59_does_not_create_experiment_or_learning_positive_claims()
    test_mlrt59_manifest_records_plan_without_unlocking_experiment()
    test_mlrt59_readme_references_experiment_plan_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-59 First Controlled Learning Experiment Plan v1, "
        "defined the future first controlled learning experiment plan after MLRT-58 freeze; no controlled learning "
        "experiment implementation, no experiment runner, no sandbox workspace, no learning inputs, no learning outputs, "
        "no learning records, no learning result persistence, no training-data intake, no dataset creation, no label creation, "
        "no model training, no model calibration, no model improvement, no offline evaluation run, no case execution, "
        "no case scoring, no route comparison, no report generation, no gold registry write, no registry mutation, "
        "no route authority, no prompt loading, no provider calls, no embeddings, no persistence, no runtime Pilot, "
        "no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT59_FIRST_CONTROLLED_LEARNING_EXPERIMENT_PLAN_V1_VALIDATION_OK")
