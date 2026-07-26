from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_64_ROUTER_PROMPT_SELECTION_NON_RUNTIME_OFFLINE_EVALUATION_HARNESS_PLAN.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_63_ROUTER_PROMPT_SELECTION_FIXED_CASE_SET_STATIC_VALIDATION_PLAN.md"
FEATURE_ID = "rss_mlrt64_router_prompt_selection_non_runtime_offline_evaluation_harness_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-64 Router Prompt Selection Non-Runtime Offline Evaluation Harness Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-65 First Controlled Offline ML Prompt-Selection Test v1"
POS_LABEL = "RSS_MLRT64_PROMPT_SELECTION_OFFLINE_EVALUATION_HARNESS_PLANNED_NO_HARNESS_NO_EXECUTION"
PREFIX = "rss_mlrt64_router_prompt_selection_non_runtime_offline_evaluation_harness_plan"


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


def test_mlrt64_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()
    assert PREV_DOC.exists()


def test_mlrt64_preserves_prompt_selection_goal_and_countdown() -> None:
    text = read(DOC)
    required = [
        "ML must be tested for helping prompt selection in router prompt logic",
        "router prompt-selection non-runtime offline evaluation harness plan",
        "does **not** implement the harness",
        "does **not** create a runner",
        "does **not** create fixed cases",
        "does **not** create labels",
        "does **not** execute a candidate",
        "does **not** score cases",
        "does **not** compare routes",
        "The critical boundary error budget remains `0`",
        "0 remaining planning steps to the testing-harness gate",
        "1 step to the first real controlled ML prompt-selection test",
        "harness_identity_gate",
        "fixed_case_set_gate",
        "candidate_output_envelope_gate",
        "expected_route_label_gate",
        "accepted_alternate_route_gate",
        "forbidden_route_gate",
        "boundary_failure_gate",
        "read_only_result_gate",
        "no_learning_gate",
        "no_authority_gate",
        "human_review_gate",
        "router_prompt_selection_non_runtime_offline_evaluation_harness_planned = true",
        "prompt_selection_focus_preserved = true",
        "ml_prompt_selection_testing_goal_preserved = true",
        "testing_harness_gate_planned = true",
        "remaining_planning_steps_to_testing_harness_gate = 0",
        "remaining_steps_to_first_real_ml_prompt_selection_test = 1",
        "offline_evaluation_harness_created = false",
        "offline_evaluation_harness_source_created = false",
        "offline_evaluation_runner_created = false",
        "offline_evaluation_run_enabled = false",
        "offline_evaluation_run_executed = false",
        "fixed_case_set_created = false",
        "prompt_selection_cases_created = false",
        "prompt_selection_labels_created = false",
        "candidate_output_envelope_created = false",
        "candidate_execution_enabled = false",
        "candidate_output_created = false",
        "expected_route_comparison_enabled = false",
        "prompt_selection_scoring_enabled = false",
        "case_execution_enabled = false",
        "case_scoring_enabled = false",
        "route_comparison_enabled = false",
        "report_generation_enabled = false",
        "result_persistence_enabled = false",
        "training_data_use_enabled = false",
        "model_learning_started = false",
        "model_training_started = false",
        "model_calibration_started = false",
        "model_improvement_started = false",
        "controlled_learning_experiment_started = false",
        "persistence_enabled = false",
        "route_authority_enabled = false",
        "prompt_loading_enabled = false",
        "provider_calls_enabled = false",
        "embeddings_enabled = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
        "MLRT-65 -> First Controlled Offline ML Prompt-Selection Test",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt64_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt64_stub_boundary_still_blocks_runtime_use() -> None:
    module = load_module(SOURCE, "mlrt64_stub_under_harness_plan_test")
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


def test_mlrt64_does_not_create_harness_cases_or_evaluation_outputs() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "harness is implemented",
        "offline evaluation harness is created",
        "runner is created",
        "fixed case set is created",
        "case files are created",
        "labels are created",
        "candidate outputs are created",
        "prompt-selection scoring is enabled",
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
        "must not claim that a harness exists",
        "an offline evaluation ran",
        "prompt-selection testing started",
        "prompt-selection accuracy was measured",
        "model reliability was validated",
        "candidate reliability was validated",
        "runtime routing is allowed",
        "offline_evaluation_harness_created = false",
        "offline_evaluation_harness_source_created = false",
        "offline_evaluation_run_enabled = false",
        "offline_evaluation_run_executed = false",
        "fixed_case_set_created = false",
        "prompt_selection_cases_created = false",
        "candidate_execution_enabled = false",
        "candidate_output_created = false",
        "prompt_selection_scoring_enabled = false",
        "route_comparison_enabled = false",
        "route_authority_enabled = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt64_manifest_records_harness_plan_without_unlocking_testing() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
        "router_prompt_selection_non_runtime_offline_evaluation_harness_plan_only_no_harness_no_execution_no_runtime_authority",
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_router_prompt_selection_non_runtime_offline_evaluation_harness_planned": true' in manifest
    assert f'"{PREFIX}_prompt_selection_focus_preserved": true' in manifest
    assert f'"{PREFIX}_ml_prompt_selection_testing_goal_preserved": true' in manifest
    assert f'"{PREFIX}_testing_harness_gate_planned": true' in manifest
    assert f'"{PREFIX}_remaining_planning_steps_to_testing_harness_gate": 0' in manifest
    assert f'"{PREFIX}_remaining_steps_to_first_real_ml_prompt_selection_test": 1' in manifest
    false_flags = [
        "offline_evaluation_harness_created",
        "offline_evaluation_harness_source_created",
        "offline_evaluation_runner_created",
        "offline_evaluation_run_enabled",
        "offline_evaluation_run_executed",
        "fixed_case_set_created",
        "fixed_case_set_file_created",
        "prompt_selection_cases_created",
        "prompt_selection_labels_created",
        "candidate_output_envelope_created",
        "candidate_execution_enabled",
        "candidate_output_created",
        "expected_route_comparison_enabled",
        "prompt_selection_scoring_enabled",
        "case_execution_enabled",
        "case_scoring_enabled",
        "route_comparison_enabled",
        "report_generation_enabled",
        "result_persistence_enabled",
        "reliability_claim_enabled",
        "training_data_use_enabled",
        "training_data_intake_enabled",
        "training_dataset_created",
        "training_labels_created",
        "model_learning_started",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "controlled_learning_experiment_started",
        "learning_sandbox_enabled",
        "persistence_enabled",
        "route_authority_granted",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]
    for flag in false_flags:
        assert f'"{PREFIX}_{flag}": false' in manifest


def test_mlrt64_readme_references_harness_gate_focus_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "router prompt-selection non-runtime offline evaluation harness planning only" in readme
    assert "0 remaining planning steps to the testing-harness gate" in readme
    assert "1 step to the first real controlled ML prompt-selection test" in readme
    assert "No offline evaluation harness, runner, fixed case set, prompt-selection cases, labels, candidate outputs, scoring, route comparison, or report is created" in readme
    assert "No training-data intake, dataset, labels, model training, model calibration, model improvement, controlled learning experiment, persistence, route authority, prompt loading, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt64_files_exist()
    test_mlrt64_preserves_prompt_selection_goal_and_countdown()
    test_mlrt64_only_allowed_python_surfaces_exist()
    test_mlrt64_stub_boundary_still_blocks_runtime_use()
    test_mlrt64_does_not_create_harness_cases_or_evaluation_outputs()
    test_mlrt64_manifest_records_harness_plan_without_unlocking_testing()
    test_mlrt64_readme_references_harness_gate_focus_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-64 Router Prompt Selection Non-Runtime Offline Evaluation Harness Plan v1, "
        "defined the future non-runtime offline evaluation harness plan for router prompt-selection after MLRT-63 freeze; preserved "
        "the final goal that ML must be tested for helping prompt selection in router prompt logic; after this milestone there are "
        "0 remaining planning steps to the testing-harness gate and 1 step to the first real controlled ML prompt-selection test; no offline evaluation harness, "
        "no harness source, no runner, no offline evaluation run, no fixed case set, no case files, no prompt-selection cases, no labels, "
        "no candidate outputs, no scoring, no route comparison, no report generation, no registry write, no registry mutation, no training-data intake, "
        "no dataset creation, no model training, no model calibration, no model improvement, no controlled learning experiment, no case execution, "
        "no route authority, no prompt loading, no provider calls, no embeddings, no persistence, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT64_ROUTER_PROMPT_SELECTION_NON_RUNTIME_OFFLINE_EVALUATION_HARNESS_PLAN_V1_VALIDATION_OK")
