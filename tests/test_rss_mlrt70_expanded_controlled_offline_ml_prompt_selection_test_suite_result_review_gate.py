from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_70_EXPANDED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_69_EXPANDED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
FEATURE_ID = "rss_mlrt70_expanded_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-70 Expanded Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1"
PREV_PREFIX = "rss_mlrt69_expanded_controlled_offline_ml_prompt_selection_test_suite"
PREFIX = "rss_mlrt70_expanded_controlled_offline_ml_prompt_selection_test_suite_result_review_gate"
POS_LABEL = "RSS_MLRT70_EXPANDED_TEST_RESULT_REVIEW_ACCEPTED_FOR_NEGATIVE_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-71 Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite v1"
CONTRACT_SUMMARY = "MLRT-70 Expanded Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-69 expanded controlled offline in-memory prompt-selection suite result as good but still limited validation-only evidence after MLRT-69 freeze; MLRT-65 passed 3/3, MLRT-67 passed 5/5, and MLRT-69 passed 10/10 for cumulative 18/18 controlled offline cases across three tests; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, model-improvement, training, or runtime-route-authority evidence; identified the current weakness that all tested cases are positive/static expected-route matches and the next correction is boundary-negative coverage for rejected/ambiguous/forbidden prompt-selection outputs; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."


def read(path: Path) -> str:
    assert path.exists(), f"missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def relative_py_files(root: Path) -> list[str]:
    assert root.exists(), f"missing directory: {root}"
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*.py"))


def test_mlrt70_files_and_mlrt69_result_exist() -> None:
    for path in (DOC, README, MANIFEST, SOURCE, LAB_HARNESS, LAB_RUNNER, LAB_SELF_GATE, PREV_DOC):
        assert path.exists(), f"missing expected file: {path}"
    previous = read(PREV_DOC)
    assert "MLRT-69 Expanded Controlled Offline ML Prompt-Selection Test Suite" in previous
    data = manifest()
    assert data[f"{PREV_PREFIX}_feature_id"] == "rss_mlrt69_expanded_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert data[f"{PREV_PREFIX}_expanded_cases_evaluated_in_memory"] == 10
    assert data[f"{PREV_PREFIX}_expanded_cases_passed"] == 10
    assert data[f"{PREV_PREFIX}_cumulative_controlled_offline_prompt_selection_cases_passed"] == 18
    assert data[f"{PREV_PREFIX}_ml_signal_good_for_continued_offline_testing"] is True
    assert data[f"{PREV_PREFIX}_ml_signal_ready_for_runtime"] is False
    assert data[f"{PREV_PREFIX}_ml_signal_ready_for_training"] is False
    assert data[f"{PREV_PREFIX}_ml_signal_ready_for_route_authority"] is False


def test_mlrt70_review_interprets_results_as_good_but_limited() -> None:
    data = manifest()
    assert data[f"{PREFIX}_expanded_suite_result_reviewed"] is True
    assert data[f"{PREFIX}_mlrt65_cases_passed"] == 3
    assert data[f"{PREFIX}_mlrt67_cases_passed"] == 5
    assert data[f"{PREFIX}_mlrt69_cases_passed"] == 10
    assert data[f"{PREFIX}_cumulative_controlled_offline_prompt_selection_tests_passed"] == 3
    assert data[f"{PREFIX}_cumulative_controlled_offline_prompt_selection_cases_passed"] == 18
    assert data[f"{PREFIX}_ml_signal_good_for_continued_offline_testing"] is True
    assert data[f"{PREFIX}_result_accepted_for_boundary_negative_testing"] is True
    assert data[f"{PREFIX}_current_weakness"] == "positive_static_expected_route_matches_only"
    assert data[f"{PREFIX}_next_correction"] == "boundary_negative_controlled_offline_prompt_selection_test_suite"
    for key in (
        "ml_signal_ready_for_runtime",
        "ml_signal_ready_for_training",
        "ml_signal_ready_for_route_authority",
        "result_accepted_as_reliability_claim",
        "result_accepted_as_maturity_claim",
        "result_accepted_as_production_readiness_claim",
        "result_accepted_as_model_improvement_claim",
        "runtime_route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "result_persistence_enabled",
        "training_data_intake_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "gold_registry_write_enabled",
        "registry_mutation_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ):
        assert data[f"{PREFIX}_{key}"] is False


def test_mlrt70_documentation_records_summary_and_correction() -> None:
    doc = read(DOC)
    readme = read(README)
    for required in (
        FEATURE_ID,
        FEATURE_TITLE,
        "Status: good direction, but not enough yet.",
        "MLRT-65 first controlled offline test: 3/3 cases passed.",
        "MLRT-67 second harder controlled offline test: 5/5 cases passed.",
        "MLRT-69 expanded controlled offline test suite: 10/10 cases passed.",
        "Cumulative controlled offline prompt-selection coverage: 18/18 cases passed across three tests.",
        "current_weakness = all passed cases are controlled static expected-route matches",
        "next_correction = boundary-negative controlled offline ML prompt-selection test suite",
        "result_accepted_for_negative_boundary_testing = true",
        "ml_signal_ready_for_runtime = false",
        POS_LABEL,
        NEXT_TITLE,
    ):
        assert required in doc
    assert FEATURE_ID in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme


def test_mlrt70_preserves_exact_python_source_surface() -> None:
    mlrt_py = relative_py_files(MLRT)
    assert mlrt_py == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py = relative_py_files(LAB)
    assert lab_py == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def main() -> None:
    test_mlrt70_files_and_mlrt69_result_exist()
    test_mlrt70_review_interprets_results_as_good_but_limited()
    test_mlrt70_documentation_records_summary_and_correction()
    test_mlrt70_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT70_EXPANDED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
