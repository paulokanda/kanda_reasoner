from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_54_TRAINING_DATA_BOUNDARY_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt54_training_data_boundary_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-54 Training Data Boundary Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-55 Gold Registry Mutation Gate Plan v1"
POS_LABEL = "RSS_MLRT54_TRAINING_DATA_BOUNDARY_DEFINED_NO_DATA_USE"
PREFIX = "rss_mlrt54_training_data_boundary"


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


def test_mlrt54_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt54_documents_training_data_boundary_only() -> None:
    text = read(DOC)
    required = [
        "defines the **training-data boundary**",
        "does **not** create a dataset",
        "does **not** read prompts as training data",
        "does **not** read freeze memory as training data",
        "does **not** read user logs as training data",
        "does **not** label examples",
        "does **not** create gold records",
        "does **not** train, calibrate, score, or improve a model",
        "The critical boundary error budget remains `0`",
        "Training data: any example, record, prompt, freeze entry, user log, routing decision, expected answer, score, label, correction, or gold truth that could change model behavior.",
        "project_freeze_after_update/frozen_features_memory",
        "kanda_prompt_workspace/prompt_library",
        "user conversation logs",
        "candidate output metadata",
        "LAB fixed cases",
        "training_data_boundary_defined = true",
        "training_data_intake_enabled = false",
        "training_data_use_enabled = false",
        "training_dataset_created = false",
        "training_labels_created = false",
        "gold_registry_mutation_enabled = false",
        "prompt_library_training_ingestion_enabled = false",
        "freeze_memory_training_ingestion_enabled = false",
        "user_log_training_ingestion_enabled = false",
        "embedding_training_index_enabled = false",
        "MLRT-55 -> Gold Registry Mutation Gate Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt54_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt54_stub_boundary_still_blocks_training_data_use_and_runtime_authority() -> None:
    module = load_module(SOURCE, "mlrt54_stub_under_training_data_boundary_test")
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


def test_mlrt54_does_not_create_training_data_or_gold_positive_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "training data may be used now",
        "training data intake is enabled",
        "dataset creation is enabled",
        "labels are created",
        "gold data is created",
        "gold registry mutation is enabled",
        "prompt library may be ingested for training",
        "freeze memory may be ingested for training",
        "user logs may be ingested for training",
        "embedding training index is enabled",
        "model training is enabled",
        "model calibration is enabled",
        "route authority is granted",
        "Pilot is enabled",
        "Copilot is enabled",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not claim candidate reliability",
        "data readiness",
        "training readiness",
        "training_data_intake_enabled = false",
        "training_dataset_created = false",
        "training_labels_created = false",
        "gold_registry_mutation_enabled = false",
        "prompt_library_training_ingestion_enabled = false",
        "freeze_memory_training_ingestion_enabled = false",
        "user_log_training_ingestion_enabled = false",
        "embedding_training_index_enabled = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt54_manifest_records_training_data_boundary_without_unlocking_data_use() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        "training_data_boundary_defined",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "training_dataset_created",
        "training_labels_created",
        "gold_data_created",
        "gold_registry_mutation_enabled",
        "prompt_library_training_ingestion_enabled",
        "freeze_memory_training_ingestion_enabled",
        "user_log_training_ingestion_enabled",
        "embedding_training_index_enabled",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_training_data_boundary_defined": true' in manifest
    false_flags = [
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "training_dataset_created",
        "training_labels_created",
        "gold_data_created",
        "gold_registry_mutation_enabled",
        "prompt_library_training_ingestion_enabled",
        "freeze_memory_training_ingestion_enabled",
        "user_log_training_ingestion_enabled",
        "embedding_training_index_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "candidate_execution_enabled",
        "case_scoring_enabled",
        "route_authority_granted",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]
    for flag in false_flags:
        assert f'"{PREFIX}_{flag}": false' in manifest


def test_mlrt54_readme_references_training_data_boundary_only_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "training-data boundary planning only" in readme
    assert "No training data is ingested, labeled, embedded, indexed, persisted, or used" in readme
    assert "No dataset, gold record, training label, calibration corpus, route authority, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt54_files_exist()
    test_mlrt54_documents_training_data_boundary_only()
    test_mlrt54_only_allowed_python_surfaces_exist()
    test_mlrt54_stub_boundary_still_blocks_training_data_use_and_runtime_authority()
    test_mlrt54_does_not_create_training_data_or_gold_positive_claims()
    test_mlrt54_manifest_records_training_data_boundary_without_unlocking_data_use()
    test_mlrt54_readme_references_training_data_boundary_only_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-54 Training Data Boundary Plan v1, "
        "defined the future training-data boundary after MLRT-53 freeze; no dataset creation, "
        "no training-data use, no project prompt/freeze/user-log ingestion, no model training, "
        "no model calibration, no model improvement, no gold or registry mutation, no dry run, "
        "no candidate execution, no case scoring, no route comparison, no report generation, "
        "no route authority, no prompt loading, no provider calls, no embeddings, no persistence, "
        "no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT54_TRAINING_DATA_BOUNDARY_PLAN_V1_VALIDATION_OK")
