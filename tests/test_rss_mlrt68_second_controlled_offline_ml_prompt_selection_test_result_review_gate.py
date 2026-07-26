from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_68_SECOND_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_67_SECOND_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST.md"
FEATURE_ID = "rss_mlrt68_second_controlled_offline_ml_prompt_selection_test_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-68 Second Controlled Offline ML Prompt-Selection Test Result Review Gate v1"
SOURCE_REL = "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
POS_LABEL = "RSS_MLRT68_SECOND_TEST_RESULT_REVIEW_ACCEPTED_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-69 Expanded Controlled Offline ML Prompt-Selection Test Suite v1"
CONTRACT_SUMMARY = "MLRT-68 Second Controlled Offline ML Prompt-Selection Test Result Review Gate v1, reviewed and accepted the MLRT-67 second controlled offline in-memory prompt-selection test result as validation-only evidence to continue expanded offline prompt-selection testing after MLRT-67 freeze; preserved that testing has already started with 0 steps remaining to start testing; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no reliability claim, no maturity claim, no production-readiness claim, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."
PREFIX = "rss_mlrt68_second_controlled_offline_ml_prompt_selection_test_result_review_gate"


def _read(path: Path) -> str:
    assert path.exists(), f"missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def _manifest() -> dict[str, object]:
    assert MANIFEST.exists(), "box manifest missing"
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _relative_py_files(root: Path) -> list[str]:
    assert root.exists(), f"missing directory: {root}"
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*.py"))


def _review_record() -> dict[str, object]:
    return {
        "feature_id": FEATURE_ID,
        "previous_feature_id": "rss_mlrt67_second_controlled_offline_ml_prompt_selection_test_v1",
        "previous_cases_evaluated_in_memory": 5,
        "previous_cases_passed": 5,
        "testing_started": True,
        "steps_to_start_testing": 0,
        "review_gate_defined": True,
        "accepted_for_expanded_offline_continuation": True,
        "accepted_for_runtime_use": False,
        "accepted_as_reliability_claim": False,
        "accepted_as_maturity_claim": False,
        "accepted_as_model_improvement": False,
        "accepted_as_router_prompt_logic_change": False,
        "route_authority_enabled": False,
        "router_prompt_logic_modified": False,
        "prompt_loading_enabled": False,
        "provider_calls_enabled": False,
        "embeddings_enabled": False,
        "persistence_enabled": False,
        "training_data_intake_enabled": False,
        "training_data_use_enabled": False,
        "dataset_creation_enabled": False,
        "model_training_started": False,
        "model_calibration_started": False,
        "model_improvement_started": False,
        "gold_registry_write_enabled": False,
        "registry_mutation_enabled": False,
        "runtime_pilot_enabled": False,
        "copilot_enabled": False,
        "critical_boundary_error_budget": 0,
        "positive_label": POS_LABEL,
        "next_safe_milestone": NEXT_TITLE,
    }


def test_mlrt68_review_gate_documents_second_test_result_without_runtime_authority() -> None:
    doc = _read(DOC)
    readme = _read(README)
    prev = _read(PREV_DOC)
    manifest = _manifest()

    for required in (
        FEATURE_ID,
        FEATURE_TITLE,
        "ML must be tested for helping prompt selection in router prompt logic",
        "0 steps to start testing",
        "mlrt67_cases_evaluated_in_memory = 5",
        "mlrt67_cases_passed = 5",
        "second_controlled_offline_prompt_selection_test_result_accepted_for_runtime_use = false",
        "second_controlled_offline_prompt_selection_test_result_accepted_as_reliability_claim = false",
        "router_prompt_logic_modified = false",
        "route_authority_enabled = false",
        "prompt_loading_enabled = false",
        "provider_calls_enabled = false",
        "embeddings_enabled = false",
        "training_data_intake_enabled = false",
        "gold_registry_write_enabled = false",
        "registry_mutation_enabled = false",
        POS_LABEL,
        NEXT_TITLE,
    ):
        assert required in doc

    assert "Second Controlled Offline ML Prompt-Selection Test" in prev
    assert FEATURE_ID in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme
    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_status"] == "review_gate_accepts_mlrt67_for_expanded_offline_testing_only_no_runtime_authority"
    assert manifest[f"{PREFIX}_previous_feature_id"] == "rss_mlrt67_second_controlled_offline_ml_prompt_selection_test_v1"
    assert manifest[f"{PREFIX}_previous_cases_passed"] == 5
    assert manifest[f"{PREFIX}_testing_started"] is True
    assert manifest[f"{PREFIX}_steps_to_start_testing"] == 0
    assert manifest[f"{PREFIX}_accepted_for_expanded_offline_continuation"] is True
    for key in (
        "accepted_for_runtime_use",
        "accepted_as_reliability_claim",
        "accepted_as_maturity_claim",
        "accepted_as_model_improvement",
        "accepted_as_router_prompt_logic_change",
        "route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "persistence_enabled",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "gold_registry_write_enabled",
        "registry_mutation_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ):
        assert manifest[f"{PREFIX}_{key}"] is False


def test_mlrt68_review_record_accepts_only_offline_continuation() -> None:
    record = _review_record()
    assert record["previous_cases_evaluated_in_memory"] == 5
    assert record["previous_cases_passed"] == 5
    assert record["testing_started"] is True
    assert record["steps_to_start_testing"] == 0
    assert record["review_gate_defined"] is True
    assert record["accepted_for_expanded_offline_continuation"] is True
    assert record["accepted_for_runtime_use"] is False
    assert record["accepted_as_reliability_claim"] is False
    assert record["accepted_as_maturity_claim"] is False
    assert record["accepted_as_model_improvement"] is False
    assert record["accepted_as_router_prompt_logic_change"] is False
    assert record["critical_boundary_error_budget"] == 0

    forbidden_keys = (
        "route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "persistence_enabled",
        "training_data_intake_enabled",
        "training_data_use_enabled",
        "dataset_creation_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "gold_registry_write_enabled",
        "registry_mutation_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    )
    assert [key for key in forbidden_keys if record[key] is True] == []


def test_mlrt68_preserves_exact_python_source_surface() -> None:
    mlrt_py = _relative_py_files(MLRT)
    assert mlrt_py == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py = _relative_py_files(LAB)
    assert lab_py == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]
    assert SOURCE.exists()
    assert LAB_HARNESS.exists()
    assert LAB_RUNNER.exists()
    assert LAB_SELF_GATE.exists()


def main() -> None:
    test_mlrt68_review_gate_documents_second_test_result_without_runtime_authority()
    test_mlrt68_review_record_accepts_only_offline_continuation()
    test_mlrt68_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT68_SECOND_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
