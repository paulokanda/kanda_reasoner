from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_66_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_65_FIRST_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST.md"
FEATURE_ID = "rss_mlrt66_controlled_offline_ml_prompt_selection_test_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-66 Controlled Offline ML Prompt-Selection Test Result Review Gate v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE_REL = "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_PREFIX = "rss_mlrt65_first_controlled_offline_ml_prompt_selection_test"
PREFIX = "rss_mlrt66_controlled_offline_ml_prompt_selection_test_result_review_gate"
NEXT_TITLE = "Routing Signal Scorer MLRT-67 Second Controlled Offline ML Prompt-Selection Test v1"
POS_LABEL = "RSS_MLRT66_FIRST_TEST_RESULT_REVIEW_ACCEPTED_NON_RUNTIME_NON_AUTHORITATIVE"


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


def build_review_gate_decision() -> dict[str, object]:
    manifest = json.loads(read(MANIFEST))
    assert manifest[f"{PREV_PREFIX}_first_controlled_offline_ml_prompt_selection_test_executed_by_validation"] is True
    assert manifest[f"{PREV_PREFIX}_first_controlled_offline_ml_prompt_selection_test_passed_in_sandbox"] is True
    assert manifest[f"{PREV_PREFIX}_steps_to_start_testing"] == 0
    assert manifest[f"{PREV_PREFIX}_prompt_selection_cases_evaluated_in_memory"] == 3
    assert manifest[f"{PREV_PREFIX}_prompt_selection_cases_passed"] == 3
    for previous_forbidden in [
        "runtime_route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "result_persistence_enabled",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "gold_registry_write_enabled",
        "registry_mutation_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]:
        assert manifest[f"{PREV_PREFIX}_{previous_forbidden}"] is False
    return {
        "feature_id": FEATURE_ID,
        "review_scope": "mlrt65_first_controlled_offline_prompt_selection_result",
        "first_test_reviewed": True,
        "first_test_accepted_for_offline_continuation": True,
        "first_test_accepted_for_runtime_use": False,
        "first_test_accepted_as_reliability_claim": False,
        "first_test_accepted_as_maturity_claim": False,
        "first_test_accepted_as_model_improvement": False,
        "testing_started": True,
        "steps_to_start_testing": 0,
        "next_action": "second_controlled_offline_prompt_selection_test",
        "non_runtime": True,
        "non_authoritative": True,
        "route_authority_granted": False,
        "runtime_router_modified": False,
        "prompt_loading_performed": False,
        "provider_call_performed": False,
        "embedding_call_performed": False,
        "result_persisted": False,
        "training_data_created": False,
        "gold_registry_mutated": False,
        "runtime_pilot_enabled": False,
        "copilot_enabled": False,
    }


def test_mlrt66_files_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert MANIFEST.exists()
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()
    assert PREV_DOC.exists()


def test_mlrt66_reviews_mlrt65_result_without_runtime_authority() -> None:
    before = file_snapshot()
    decision = build_review_gate_decision()
    after = file_snapshot()
    assert before == after
    assert decision["first_test_reviewed"] is True
    assert decision["first_test_accepted_for_offline_continuation"] is True
    assert decision["testing_started"] is True
    assert decision["steps_to_start_testing"] == 0
    assert decision["next_action"] == "second_controlled_offline_prompt_selection_test"
    assert decision["non_runtime"] is True
    assert decision["non_authoritative"] is True
    for forbidden_flag in [
        "first_test_accepted_for_runtime_use",
        "first_test_accepted_as_reliability_claim",
        "first_test_accepted_as_maturity_claim",
        "first_test_accepted_as_model_improvement",
        "route_authority_granted",
        "runtime_router_modified",
        "prompt_loading_performed",
        "provider_call_performed",
        "embedding_call_performed",
        "result_persisted",
        "training_data_created",
        "gold_registry_mutated",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]:
        assert decision[forbidden_flag] is False


def test_mlrt66_preserves_doc_contract_and_count() -> None:
    text = read(DOC)
    required = [
        "ML must be tested for helping prompt selection in router prompt logic",
        "testing has already started",
        "0 steps to start testing",
        "MLRT-65 started testing",
        "acceptable only as a narrow validation result for continuing offline tests",
        "mlrt65_cases_evaluated_in_memory = 3",
        "mlrt65_cases_passed = 3",
        "first_controlled_offline_prompt_selection_test_result_accepted_for_offline_continuation = true",
        "first_controlled_offline_prompt_selection_test_result_accepted_for_runtime_use = false",
        "first_controlled_offline_prompt_selection_test_result_accepted_as_reliability_claim = false",
        "first_controlled_offline_prompt_selection_test_result_accepted_as_maturity_claim = false",
        "first_controlled_offline_prompt_selection_test_result_accepted_as_model_improvement = false",
        "next_action = second_controlled_offline_prompt_selection_test",
        "runtime_result_use_authorized = false",
        "route_authority_enabled = false",
        "router_prompt_logic_modified = false",
        "prompt_loading_enabled = false",
        "provider_calls_enabled = false",
        "embeddings_enabled = false",
        "result_persistence_enabled = false",
        "report_file_created = false",
        "persistent_case_files_created = false",
        "training_data_intake_enabled = false",
        "training_data_use_enabled = false",
        "model_training_started = false",
        "model_calibration_started = false",
        "model_improvement_started = false",
        "reliability_claim_created = false",
        "maturity_claim_created = false",
        "production_readiness_claim_created = false",
        "runtime_pilot_enabled = false",
        "copilot_enabled = false",
        SOURCE_REL,
        LAB_HARNESS_REL,
        LAB_RUNNER_REL,
        LAB_SELF_GATE_REL,
        POS_LABEL,
        NEXT_TITLE,
    ]
    for item in required:
        assert item in text


def test_mlrt66_only_allowed_python_surfaces_exist() -> None:
    mlrt_py_files = sorted(p.relative_to(MLRT).as_posix() for p in MLRT.rglob("*.py"))
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py_files = sorted(p.name for p in LAB.rglob("*.py"))
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt66_stub_boundary_still_blocks_runtime_use() -> None:
    module = load_module(SOURCE, "mlrt66_stub_under_result_review_gate")
    assert module.assert_static_non_runtime_boundary() is True
    contract = module.get_stub_contract()
    assert contract["critical_boundary_error_budget"] == 0
    for flag in [
        "runtime_route_authority_enabled",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "batch_mode_enabled",
        "activation_enabled",
        "field_testing_enabled",
        "training_data_use_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]:
        assert contract[flag] is False


def test_mlrt66_manifest_records_review_gate_without_unlocking_runtime() -> None:
    manifest = read(MANIFEST)
    for item in [FEATURE_ID, FEATURE_TITLE, SOURCE_REL, LAB_HARNESS_REL, LAB_RUNNER_REL, LAB_SELF_GATE_REL, POS_LABEL, NEXT_TITLE]:
        assert item in manifest
    assert f'"{PREFIX}_first_controlled_offline_test_result_reviewed": true' in manifest
    assert f'"{PREFIX}_first_controlled_offline_test_result_accepted_for_offline_continuation": true' in manifest
    assert f'"{PREFIX}_testing_started": true' in manifest
    assert f'"{PREFIX}_steps_to_start_testing": 0' in manifest
    assert f'"{PREFIX}_next_action": "second_controlled_offline_prompt_selection_test"' in manifest
    for flag in [
        "first_controlled_offline_test_result_accepted_for_runtime_use",
        "first_controlled_offline_test_result_accepted_as_reliability_claim",
        "first_controlled_offline_test_result_accepted_as_maturity_claim",
        "first_controlled_offline_test_result_accepted_as_model_improvement",
        "runtime_result_use_authorized",
        "runtime_route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "result_persistence_enabled",
        "report_file_created",
        "persistent_case_files_created",
        "persistent_dataset_created",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "reliability_claim_created",
        "maturity_claim_created",
        "production_readiness_claim_created",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ]:
        assert f'"{PREFIX}_{flag}": false' in manifest


def test_mlrt66_readme_references_review_gate_and_next_test() -> None:
    readme = read(README)
    assert FEATURE_TITLE in readme
    assert FEATURE_ID in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert "result review gate" in readme
    assert "Testing has already started" in readme
    assert "0 steps to start testing" in readme
    assert "No reliability claim, maturity claim, runtime route authority, prompt loading, provider calls, embeddings, persistence, training, calibration, registry mutation, Pilot, or Copilot behavior is enabled" in readme


if __name__ == "__main__":
    test_mlrt66_files_exist()
    test_mlrt66_reviews_mlrt65_result_without_runtime_authority()
    test_mlrt66_preserves_doc_contract_and_count()
    test_mlrt66_only_allowed_python_surfaces_exist()
    test_mlrt66_stub_boundary_still_blocks_runtime_use()
    test_mlrt66_manifest_records_review_gate_without_unlocking_runtime()
    test_mlrt66_readme_references_review_gate_and_next_test()
    print("CONTRACT_TEST_OK: MLRT-66 Controlled Offline ML Prompt-Selection Test Result Review Gate v1, reviewed and accepted the MLRT-65 first controlled offline in-memory prompt-selection test result as a validation-only result after MLRT-65 freeze; preserved that testing has started with 0 steps remaining to start testing; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no reliability claim, no maturity claim, no production-readiness claim, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.")
    print("SANDBOX_RSS_MLRT66_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE_V1_VALIDATION_OK")
