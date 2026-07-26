from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_62_ROUTER_PROMPT_SELECTION_FIXED_CASE_SET_FORMAT_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_61_ROUTER_PROMPT_SELECTION_OFFLINE_EVALUATION_CASE_SCHEMA_PLAN.md"
FEATURE_ID = "rss_mlrt62_router_prompt_selection_fixed_case_set_format_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-62 Router Prompt Selection Fixed Case Set Format Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-63 Router Prompt Selection Fixed Case Set Static Validation Plan v1"
POS_LABEL = "RSS_MLRT62_PROMPT_SELECTION_FIXED_CASE_SET_FORMAT_PLANNED_NO_CASE_SET_NO_EVALUATION"
PREFIX = "rss_mlrt62_router_prompt_selection_fixed_case_set_format_plan"


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


def test_mlrt62_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()
    assert PREV_DOC.exists()


def test_mlrt62_preserves_prompt_selection_goal_and_countdown() -> None:
    text = read(DOC)
    required = [
        "ML must be tested for helping prompt selection in router prompt logic",
        "router prompt-selection fixed case set format",
        "does **not** create the fixed case set",
        "does **not** create case files",
        "does **not** create labels",
        "does **not** execute cases",
        "does **not** score candidate output",
        "does **not** compare routes",
        "The critical boundary error budget remains `0`",
        "2 steps to the testing harness",
        "3 steps to the first real ML prompt-selection test",
        "case_set_id",
        "case_set_version",
        "case_schema_version",
        "case_set_purpose",
        "case_count",
        "case_index",
        "expected_primary_prompt_groups_index",
        "accepted_alternate_prompt_groups_index",
        "forbidden_prompt_groups_index",
        "boundary_expectation_index",
        "critical_failure_index",
        "human_review_record",
        "provenance_record",
        "checksum_record",
        "freeze_record_reference",
        "router_prompt_selection_fixed_case_set_format_planned = true",
        "prompt_selection_focus_preserved = true",
        "ml_prompt_selection_testing_goal_preserved = true",
        "fixed_case_set_format_created = false",
        "fixed_case_set_file_created = false",
        "fixed_prompt_selection_case_set_created = false",
        "prompt_selection_cases_created = false",
        "prompt_selection_labels_created = false",
        "prompt_selection_candidate_outputs_created = false",
        "prompt_selection_scoring_enabled = false",
        "route_comparison_enabled = false",
        "offline_evaluation_run_enabled = false",
        "case_execution_enabled = false",
        "case_scoring_enabled = false",
        "report_generation_enabled = false",
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
        "MLRT-63 -> Router Prompt Selection Fixed Case Set Static Validation Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt62_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt62_stub_boundary_still_blocks_runtime_use() -> None:
    module = load_module(SOURCE, "mlrt62_stub_under_fixed_case_set_format_plan_test")
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


def test_mlrt62_does_not_create_fixed_cases_or_evaluation_outputs() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "fixed case set is created",
        "case files are created",
        "labels are created",
        "candidate outputs are created",
        "prompt-selection scoring is enabled",
        "route comparison is enabled",
        "offline evaluation is enabled",
        "case scoring is enabled",
        "report generation is enabled",
        "candidate execution is enabled",
        "route authority is granted",
        "Pilot is enabled",
        "Copilot is enabled",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not claim fixed-case readiness",
        "fixed-case-set implementation readiness",
        "validation readiness",
        "evaluation readiness",
        "scoring readiness",
        "prompt-selection reliability",
        "model reliability",
        "candidate reliability",
        "runtime readiness",
        "fixed_case_set_format_created = false",
        "fixed_prompt_selection_case_set_created = false",
        "prompt_selection_cases_created = false",
        "prompt_selection_scoring_enabled = false",
        "route_comparison_enabled = false",
        "route_authority_enabled = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt62_manifest_records_fixed_case_set_format_without_unlocking_testing() -> None:
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
        "router_prompt_selection_fixed_case_set_format_plan_only_no_case_set_no_cases_no_evaluation_no_runtime_authority",
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_router_prompt_selection_fixed_case_set_format_planned": true' in manifest
    assert f'"{PREFIX}_prompt_selection_focus_preserved": true' in manifest
    assert f'"{PREFIX}_ml_prompt_selection_testing_goal_preserved": true' in manifest
    false_flags = [
        "fixed_case_set_format_created",
        "fixed_case_set_file_created",
        "fixed_case_set_validator_created",
        "fixed_prompt_selection_case_set_created",
        "prompt_selection_cases_created",
        "prompt_selection_labels_created",
        "prompt_selection_gold_cases_created",
        "prompt_selection_candidate_outputs_created",
        "prompt_selection_scoring_enabled",
        "offline_evaluation_run_enabled",
        "offline_evaluation_run_executed",
        "case_execution_enabled",
        "case_scoring_enabled",
        "route_comparison_enabled",
        "report_generation_enabled",
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
        "candidate_execution_enabled",
        "route_authority_granted",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]
    for flag in false_flags:
        assert f'"{PREFIX}_{flag}": false' in manifest


def test_mlrt62_readme_references_fixed_case_set_format_focus_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "router prompt-selection fixed case set format planning only" in readme
    assert "2 steps to the testing harness" in readme
    assert "3 steps to the first real ML prompt-selection test" in readme
    assert "No fixed case set, prompt-selection cases, labels, candidate outputs, scoring, route comparison, or report is created" in readme
    assert "No training-data intake, dataset, labels, model training, model calibration, model improvement, controlled learning experiment, persistence, route authority, prompt loading, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt62_files_exist()
    test_mlrt62_preserves_prompt_selection_goal_and_countdown()
    test_mlrt62_only_allowed_python_surfaces_exist()
    test_mlrt62_stub_boundary_still_blocks_runtime_use()
    test_mlrt62_does_not_create_fixed_cases_or_evaluation_outputs()
    test_mlrt62_manifest_records_fixed_case_set_format_without_unlocking_testing()
    test_mlrt62_readme_references_fixed_case_set_format_focus_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-62 Router Prompt Selection Fixed Case Set Format Plan v1, "
        "defined the future fixed case set format plan for router prompt-selection offline evaluation after MLRT-61 freeze; preserved "
        "the final goal that ML must be tested for helping prompt selection in router prompt logic; after this milestone there "
        "are 2 steps to the testing harness and 3 steps to the first real ML prompt-selection test; no fixed case set, no case files, "
        "no prompt-selection cases, no labels, no candidate outputs, no scoring, no route comparison, no report generation, no registry write, "
        "no registry mutation, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, "
        "no controlled learning experiment, no case execution, no route authority, no prompt loading, no provider calls, no embeddings, "
        "no persistence, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT62_ROUTER_PROMPT_SELECTION_FIXED_CASE_SET_FORMAT_PLAN_V1_VALIDATION_OK")
