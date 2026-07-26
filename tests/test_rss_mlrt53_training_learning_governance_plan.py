from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_53_TRAINING_LEARNING_GOVERNANCE_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt53_training_learning_governance_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-53 Training Learning Governance Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-54 Training Data Boundary Plan v1"
POS_LABEL = "RSS_MLRT53_ITEM5_GOVERNANCE_STARTED_NO_TRAINING"
PREFIX = "rss_mlrt53_training_learning_governance"


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


def test_mlrt53_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt53_documents_item5_as_governance_only() -> None:
    text = read(DOC)
    required = [
        "starts **Item 5** in the narrow safe sense",
        "governance planning",
        "does **not** start training",
        "does **not** use training data",
        "does **not** calibrate thresholds",
        "does **not** mutate a gold registry",
        "does **not** execute candidates",
        "does **not** run dry-runs",
        "does **not** score cases",
        "does **not** grant route authority",
        "The critical boundary error budget remains `0`",
        "MLRT-54 -> Training Data Boundary Plan",
        "MLRT-55 -> Gold Registry Mutation Gate Plan",
        "MLRT-56 -> Offline Evaluation Protocol Plan",
        "MLRT-57 -> Calibration-Only Dry-Run Plan",
        "MLRT-58 -> Learning Sandbox Plan",
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


def test_mlrt53_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt53_stub_boundary_still_blocks_training_and_runtime_authority() -> None:
    module = load_module(SOURCE, "mlrt53_stub_under_item5_governance_test")
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


def test_mlrt53_does_not_create_training_or_calibration_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "training is started",
        "model training is enabled",
        "model calibration is enabled",
        "training data may be used now",
        "gold registry mutation is enabled",
        "route authority is granted",
        "candidate reliability is validated",
        "Pilot is enabled",
        "Copilot is enabled",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not claim candidate reliability",
        "model_training_started = false",
        "model_calibration_started = false",
        "gold_registry_mutation_enabled = false",
        "route_authority_enabled = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt53_manifest_records_item5_governance_without_unlocking_training() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        "item5_governance_plan_started",
        "training_data_use_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "gold_registry_mutation_enabled",
        "route_authority_granted",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_item5_governance_plan_started": true' in manifest
    assert f'"{PREFIX}_training_data_use_enabled": false' in manifest
    assert f'"{PREFIX}_model_training_started": false' in manifest
    assert f'"{PREFIX}_model_calibration_started": false' in manifest
    assert f'"{PREFIX}_model_improvement_started": false' in manifest
    assert f'"{PREFIX}_gold_registry_mutation_enabled": false' in manifest
    assert f'"{PREFIX}_candidate_execution_enabled": false' in manifest
    assert f'"{PREFIX}_case_scoring_enabled": false' in manifest
    assert f'"{PREFIX}_route_authority_granted": false' in manifest
    assert f'"{PREFIX}_runtime_pilot_enabled": false' in manifest
    assert f'"{PREFIX}_copilot_enabled": false' in manifest


def test_mlrt53_readme_references_governance_only_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "Item 5 governance planning only" in readme
    assert "No training data is used" in readme
    assert "No model training, calibration, model improvement, gold registry mutation, route authority, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt53_files_exist()
    test_mlrt53_documents_item5_as_governance_only()
    test_mlrt53_only_allowed_python_surfaces_exist()
    test_mlrt53_stub_boundary_still_blocks_training_and_runtime_authority()
    test_mlrt53_does_not_create_training_or_calibration_claims()
    test_mlrt53_manifest_records_item5_governance_without_unlocking_training()
    test_mlrt53_readme_references_governance_only_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-53 Training Learning Governance Plan v1, "
        "started Item 5 as governance planning only after MLRT-52 freeze; defined training/learning/calibration boundaries "
        "and future governed milestones; no training data use, no model training, no model calibration, "
        "no model improvement, no gold or registry mutation, no dry run, no candidate execution, no case scoring, "
        "no route comparison, no report generation, no route authority, no prompt loading, no provider calls, "
        "no embeddings, no persistence, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT53_TRAINING_LEARNING_GOVERNANCE_PLAN_V1_VALIDATION_OK")
