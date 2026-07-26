from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_60_GOLD_REGISTRY_SCHEMA_PROPOSAL_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt60_gold_registry_schema_proposal_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-60 Gold Registry Schema Proposal Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-61 Router Prompt Selection Offline Evaluation Case Schema Plan v1"
POS_LABEL = "RSS_MLRT60_PROMPT_SELECTION_GOLD_SCHEMA_PROPOSAL_DEFINED_NO_SCHEMA_NO_GOLD"
PREFIX = "rss_mlrt60_gold_registry_schema_proposal_plan"


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


def test_mlrt60_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt60_preserves_prompt_selection_goal() -> None:
    text = read(DOC)
    required = [
        "ML must be tested to help prompt selection in router prompt logic",
        "router prompt-selection gold registry schema proposal",
        "define the future fields that a later governed gold registry schema must include so ML/router candidate behavior can eventually be tested against expected prompt-selection outcomes",
        "does **not** create a gold registry implementation",
        "does **not** create a schema file",
        "does **not** create gold records",
        "does **not** create evaluation cases",
        "does **not** run evaluation",
        "does **not** score candidate prompt-selection decisions",
        "does **not** compare routes",
        "The critical boundary error budget remains `0`",
        "case_identity",
        "user_intent_summary",
        "routing_signal_summary",
        "expected_primary_prompt_group",
        "accepted_alternate_prompt_groups",
        "forbidden_prompt_groups",
        "selection_rationale_requirements",
        "boundary_expectations",
        "critical_failure_conditions",
        "human_review_status",
        "provenance_summary",
        "gold_registry_schema_proposal_defined = true",
        "prompt_selection_focus_preserved = true",
        "ml_prompt_selection_testing_goal_preserved = true",
        "gold_registry_schema_created = false",
        "gold_registry_created = false",
        "gold_records_created = false",
        "gold_schema_file_created = false",
        "prompt_selection_gold_cases_created = false",
        "prompt_selection_gold_labels_created = false",
        "prompt_selection_evaluation_cases_created = false",
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
        "MLRT-61 -> Router Prompt Selection Offline Evaluation Case Schema Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt60_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt60_stub_boundary_still_blocks_registry_and_runtime_use() -> None:
    module = load_module(SOURCE, "mlrt60_stub_under_gold_schema_proposal_plan_test")
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


def test_mlrt60_does_not_create_schema_gold_or_prompt_selection_outputs() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "gold registry schema is created",
        "gold registry is created",
        "gold records are created",
        "schema file is created",
        "prompt-selection gold cases are created",
        "prompt-selection labels are created",
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
        "must not claim schema readiness",
        "gold registry readiness",
        "evaluation readiness",
        "scoring readiness",
        "prompt-selection reliability",
        "model reliability",
        "candidate reliability",
        "route readiness",
        "runtime readiness",
        "gold_registry_schema_created = false",
        "gold_registry_created = false",
        "gold_records_created = false",
        "prompt_selection_scoring_enabled = false",
        "route_comparison_enabled = false",
        "route_authority_enabled = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt60_manifest_records_prompt_selection_schema_proposal_without_unlocking_gold() -> None:
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
        "prompt_selection_gold_schema_proposal_only_no_schema_no_gold_no_registry_write_no_runtime_authority",
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_gold_registry_schema_proposal_defined": true' in manifest
    assert f'"{PREFIX}_prompt_selection_focus_preserved": true' in manifest
    assert f'"{PREFIX}_ml_prompt_selection_testing_goal_preserved": true' in manifest
    false_flags = [
        "gold_registry_schema_created",
        "gold_registry_created",
        "gold_records_created",
        "gold_record_labels_created",
        "gold_registry_writer_created",
        "gold_registry_mutation_enabled",
        "gold_registry_mutated",
        "gold_schema_file_created",
        "prompt_selection_gold_cases_created",
        "prompt_selection_gold_labels_created",
        "prompt_selection_evaluation_cases_created",
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


def test_mlrt60_readme_references_prompt_selection_focus_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "router prompt-selection gold registry schema proposal planning only" in readme
    assert "No gold registry schema file, gold registry, gold record, prompt-selection gold case, prompt-selection label, evaluation case, scoring, route comparison, or report is created" in readme
    assert "No training-data intake, dataset, labels, model training, model calibration, model improvement, controlled learning experiment, persistence, route authority, prompt loading, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt60_files_exist()
    test_mlrt60_preserves_prompt_selection_goal()
    test_mlrt60_only_allowed_python_surfaces_exist()
    test_mlrt60_stub_boundary_still_blocks_registry_and_runtime_use()
    test_mlrt60_does_not_create_schema_gold_or_prompt_selection_outputs()
    test_mlrt60_manifest_records_prompt_selection_schema_proposal_without_unlocking_gold()
    test_mlrt60_readme_references_prompt_selection_focus_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-60 Gold Registry Schema Proposal Plan v1, "
        "defined the future router prompt-selection gold registry schema proposal after MLRT-59 freeze; preserved the final "
        "goal that ML must be tested for helping prompt selection in router prompt logic; no gold schema file, no gold registry, "
        "no gold records, no prompt-selection gold cases, no labels, no evaluation cases, no candidate outputs, no scoring, "
        "no route comparison, no report generation, no registry write, no registry mutation, no training-data intake, no dataset "
        "creation, no model training, no model calibration, no model improvement, no controlled learning experiment, no case "
        "execution, no route authority, no prompt loading, no provider calls, no embeddings, no persistence, no runtime Pilot, "
        "no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT60_GOLD_REGISTRY_SCHEMA_PROPOSAL_PLAN_V1_VALIDATION_OK")
