from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_55_GOLD_REGISTRY_MUTATION_GATE_PLAN.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
FEATURE_ID = "rss_mlrt55_gold_registry_mutation_gate_plan_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-55 Gold Registry Mutation Gate Plan v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
NEXT_TITLE = "Routing Signal Scorer MLRT-56 Offline Evaluation Protocol Plan v1"
POS_LABEL = "RSS_MLRT55_GOLD_REGISTRY_MUTATION_GATE_DEFINED_NO_MUTATION"
PREFIX = "rss_mlrt55_gold_registry_mutation_gate"


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


def test_mlrt55_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def test_mlrt55_documents_gold_registry_mutation_gate_only() -> None:
    text = read(DOC)
    required = [
        "defines the **gold registry mutation gate**",
        "does **not** create gold data",
        "does **not** create a registry",
        "does **not** write registry records",
        "does **not** mutate a registry",
        "does **not** create labels, datasets, examples, thresholds, scores, route decisions, or accepted truth",
        "does **not** execute candidates, score cases, train, calibrate, or improve a model",
        "The critical boundary error budget remains `0`",
        "Gold record: a canonical expected output",
        "Gold registry: a governed collection of gold records",
        "Gold mutation: any addition, edit, deletion, supersession, relabeling, migration, normalization, or status change",
        "Mutation write: a committed registry change; forbidden in MLRT-55.",
        "A human authorization record is required before any write.",
        "Validation proves that write behavior remains unavailable until a later explicit write-authorization milestone.",
        "gold_registry_mutation_gate_defined = true",
        "gold_registry_schema_created = false",
        "gold_registry_created = false",
        "gold_record_created = false",
        "gold_mutation_proposal_created = false",
        "gold_mutation_diff_created = false",
        "gold_mutation_write_enabled = false",
        "gold_registry_mutation_enabled = false",
        "gold_registry_mutated = false",
        "human_authorization_record_created = false",
        "training_data_use_enabled = false",
        "candidate_execution_enabled = false",
        "case_scoring_enabled = false",
        "route_authority_enabled = false",
        "MLRT-56 -> Offline Evaluation Protocol Plan",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt55_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt55_stub_boundary_still_blocks_runtime_authority_and_training_use() -> None:
    module = load_module(SOURCE, "mlrt55_stub_under_gold_registry_mutation_gate_test")
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


def test_mlrt55_does_not_create_registry_or_mutation_positive_claims() -> None:
    text = read(DOC)
    forbidden_positive_claims = [
        "gold registry may be mutated now",
        "gold registry mutation is enabled",
        "gold registry writes are enabled",
        "gold records are created",
        "mutation proposals are created",
        "mutation diffs are created",
        "rollback records are created",
        "human authorization records are created",
        "registry readiness is achieved",
        "mutation readiness is achieved",
        "write readiness is achieved",
        "route authority is granted",
        "Pilot is enabled",
        "Copilot is enabled",
    ]
    for claim in forbidden_positive_claims:
        assert claim not in text
    required_negative_claims = [
        "must not claim candidate reliability",
        "registry readiness",
        "mutation readiness",
        "write readiness",
        "gold_registry_schema_created = false",
        "gold_registry_created = false",
        "gold_record_created = false",
        "gold_mutation_proposal_created = false",
        "gold_mutation_diff_created = false",
        "gold_mutation_write_enabled = false",
        "gold_registry_mutation_enabled = false",
        "gold_registry_mutated = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
    ]
    for claim in required_negative_claims:
        assert claim in text


def test_mlrt55_manifest_records_gold_mutation_gate_without_unlocking_writes() -> None:
    manifest = read(MANIFEST)
    required = [
        FEATURE_ID,
        FEATURE_TITLE,
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        "gold_registry_mutation_gate_defined",
        "gold_registry_schema_created",
        "gold_registry_created",
        "gold_record_created",
        "gold_mutation_proposal_created",
        "gold_mutation_diff_created",
        "gold_mutation_write_enabled",
        "gold_registry_mutation_enabled",
        "gold_registry_mutated",
        "gold_rollback_record_created",
        "human_authorization_record_created",
        "critical_boundary_error_budget",
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in manifest
    assert f'"{PREFIX}_gold_registry_mutation_gate_defined": true' in manifest
    false_flags = [
        "gold_registry_schema_created",
        "gold_registry_created",
        "gold_record_created",
        "gold_mutation_proposal_created",
        "gold_mutation_diff_created",
        "gold_mutation_write_enabled",
        "gold_registry_mutation_enabled",
        "gold_registry_mutated",
        "gold_rollback_record_created",
        "human_authorization_record_created",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "training_dataset_created",
        "training_labels_created",
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


def test_mlrt55_readme_references_gold_registry_mutation_gate_only_and_next_milestone() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert SOURCE_REL in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "gold registry mutation gate planning only" in readme
    assert "No gold data, gold registry, mutation proposal, mutation diff, rollback record, registry write, or registry mutation is created" in readme
    assert "No dataset, label, training, calibration, route authority, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt55_files_exist()
    test_mlrt55_documents_gold_registry_mutation_gate_only()
    test_mlrt55_only_allowed_python_surfaces_exist()
    test_mlrt55_stub_boundary_still_blocks_runtime_authority_and_training_use()
    test_mlrt55_does_not_create_registry_or_mutation_positive_claims()
    test_mlrt55_manifest_records_gold_mutation_gate_without_unlocking_writes()
    test_mlrt55_readme_references_gold_registry_mutation_gate_only_and_next_milestone()
    print(
        "CONTRACT_TEST_OK: MLRT-55 Gold Registry Mutation Gate Plan v1, "
        "defined the future gold registry mutation gate after MLRT-54 freeze; no gold data creation, "
        "no gold registry writes, no registry mutation, no dataset creation, no training-data use, "
        "no model training, no model calibration, no model improvement, no dry run, no candidate execution, "
        "no case scoring, no route comparison, no report generation, no route authority, no prompt loading, "
        "no provider calls, no embeddings, no persistence, no runtime Pilot, no Copilot behavior, "
        "critical boundary error budget zero."
    )
    print("SANDBOX_RSS_MLRT55_GOLD_REGISTRY_MUTATION_GATE_PLAN_V1_VALIDATION_OK")
