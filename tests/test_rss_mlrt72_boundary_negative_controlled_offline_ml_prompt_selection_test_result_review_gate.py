from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_72_BOUNDARY_NEGATIVE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
LAB_HARNESS = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/candidate_evaluation_harness_interface.py"
LAB_RUNNER = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/deterministic_runner_skeleton.py"
LAB_SELF_GATE = ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation/lab_self_validation_gate.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_71_BOUNDARY_NEGATIVE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
FEATURE_ID = "rss_mlrt72_boundary_negative_controlled_offline_ml_prompt_selection_test_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-72 Boundary-Negative Controlled Offline ML Prompt-Selection Test Result Review Gate v1"
PREFIX = "rss_mlrt72_boundary_negative_controlled_offline_ml_prompt_selection_test_result_review_gate"
PREV_PREFIX = "rss_mlrt71_boundary_negative_controlled_offline_ml_prompt_selection_test_suite"
POS_LABEL = "RSS_MLRT72_BOUNDARY_NEGATIVE_RESULT_REVIEW_ACCEPTED_AND_TEST_VOLUME_ESCALATION_POLICY_SET_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-73 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite v1"
CONTRACT_SUMMARY = 'MLRT-72 Boundary-Negative Controlled Offline ML Prompt-Selection Test Result Review Gate v1, reviewed the MLRT-71 boundary-negative controlled offline in-memory prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-71 freeze; prior controlled offline ML prompt-selection results are 26/26 cases passed across four tests: MLRT-65 3/3 positive, MLRT-67 5/5 harder positive, MLRT-69 10/10 expanded positive, and MLRT-71 8/8 boundary-negative containment cases; web-informed review concluded that increasing test count can improve ML-testing reliability only when the additional tests are representative, statistically meaningful, non-duplicate, boundary-diverse, and not reused until they wear out; MLRT-72 therefore implements a test-volume escalation policy for future ML prompt-selection test-suite ZIPs, requiring larger diverse case suites rather than repeated easy cases, with the next real test suite target set to 24 mixed positive and negative cases; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no reliability claim, no maturity claim, no production-readiness claim, no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'

POLICY_REQUIREMENT_CASES = [
    {"case_id": "mlrt72_google_large_enough", "policy": "future_test_sets_large_enough", "expected": True},
    {"case_id": "mlrt72_google_representative", "policy": "future_test_sets_representative", "expected": True},
    {"case_id": "mlrt72_google_non_duplicate", "policy": "future_test_sets_non_duplicate", "expected": True},
    {"case_id": "mlrt72_google_refresh_worn_sets", "policy": "future_test_sets_refreshed_not_reused_until_worn_out", "expected": True},
    {"case_id": "mlrt72_google_not_easy_repetition", "policy": "repeating_similar_easy_cases_is_insufficient", "expected": True},
    {"case_id": "mlrt72_google_real_world_representative", "policy": "future_cases_represent_real_router_prompt_selection_usage", "expected": True},
    {"case_id": "mlrt72_sklearn_repeated_splits", "policy": "future_validation_should_prefer_multiple_independent_case_groups_when_possible", "expected": True},
    {"case_id": "mlrt72_sklearn_small_sample_warning", "policy": "small_static_case_sets_are_not_reliability_claims", "expected": True},
    {"case_id": "mlrt72_nist_lifecycle_evaluation", "policy": "evaluation_remains_lifecycle_risk_management_not_runtime_authority", "expected": True},
    {"case_id": "mlrt72_google_ml_test_score_breadth", "policy": "ml_testing_should_cover_data_model_infrastructure_and_monitoring_needs_over_time", "expected": True},
    {"case_id": "mlrt72_minimum_future_suite_size", "policy": "minimum_future_real_test_suite_cases_at_least_16", "expected": True},
    {"case_id": "mlrt72_next_suite_target_size", "policy": "next_real_test_suite_target_24_cases", "expected": True},
]


def read(path: Path) -> str:
    assert path.exists(), f"missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def relative_py_files(root: Path) -> list[str]:
    assert root.exists(), f"missing directory: {root}"
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*.py"))


def evaluate_policy_case(case: dict[str, object], data: dict[str, object]) -> dict[str, object]:
    policy = str(case["policy"])
    expected = case["expected"]
    actual_map = {
        "future_test_sets_large_enough": data[f"{PREFIX}_minimum_future_real_test_suite_cases"] >= 16,
        "future_test_sets_representative": data[f"{PREFIX}_next_real_test_suite_case_mix"].find("drift") >= 0,
        "future_test_sets_non_duplicate": data[f"{PREFIX}_future_cases_must_be_non_duplicate"],
        "future_test_sets_refreshed_not_reused_until_worn_out": data[f"{PREFIX}_test_volume_escalation_policy_enabled_for_future_test_suite_zips"],
        "repeating_similar_easy_cases_is_insufficient": data[f"{PREFIX}_repeating_similar_easy_cases_improves_reliability"] is False,
        "future_cases_represent_real_router_prompt_selection_usage": "forbidden" in data[f"{PREFIX}_next_real_test_suite_case_mix"],
        "future_validation_should_prefer_multiple_independent_case_groups_when_possible": data[f"{PREFIX}_cumulative_controlled_offline_test_stages_passed"] >= 4,
        "small_static_case_sets_are_not_reliability_claims": data[f"{PREFIX}_result_accepted_as_reliability_claim"] is False,
        "evaluation_remains_lifecycle_risk_management_not_runtime_authority": data[f"{PREFIX}_runtime_route_authority_enabled"] is False,
        "ml_testing_should_cover_data_model_infrastructure_and_monitoring_needs_over_time": data[f"{PREFIX}_web_check_performed"] is True,
        "minimum_future_real_test_suite_cases_at_least_16": data[f"{PREFIX}_minimum_future_real_test_suite_cases"] >= 16,
        "next_real_test_suite_target_24_cases": data[f"{PREFIX}_next_real_test_suite_target_cases"] == 24,
    }
    actual = actual_map[policy]
    return {"case_id": case["case_id"], "policy": policy, "passed": actual is expected}


def test_mlrt72_files_and_mlrt71_result_exist() -> None:
    for path in (DOC, README, MANIFEST, SOURCE, LAB_HARNESS, LAB_RUNNER, LAB_SELF_GATE, PREV_DOC):
        assert path.exists(), f"missing expected file: {path}"
    previous = read(PREV_DOC)
    assert "MLRT-71 Boundary-Negative Controlled Offline ML Prompt-Selection Test Suite" in previous
    data = manifest()
    assert data[f"{PREV_PREFIX}_feature_id"] == "rss_mlrt71_boundary_negative_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert data[f"{PREV_PREFIX}_boundary_negative_cases_evaluated_in_memory"] == 8
    assert data[f"{PREV_PREFIX}_boundary_negative_cases_passed"] == 8
    assert data[f"{PREV_PREFIX}_cumulative_controlled_offline_prompt_selection_cases_passed"] == 26


def test_mlrt72_reviews_boundary_negative_result_and_keeps_claim_limited() -> None:
    data = manifest()
    assert data[f"{PREFIX}_previous_result_reviewed"] is True
    assert data[f"{PREFIX}_mlrt65_positive_cases_passed"] == 3
    assert data[f"{PREFIX}_mlrt67_harder_positive_cases_passed"] == 5
    assert data[f"{PREFIX}_mlrt69_expanded_positive_cases_passed"] == 10
    assert data[f"{PREFIX}_mlrt71_boundary_negative_cases_passed"] == 8
    assert data[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 26
    assert data[f"{PREFIX}_ml_signal_good_for_continued_offline_testing"] is True
    assert data[f"{PREFIX}_ml_signal_stronger_after_boundary_negative_tests"] is True
    assert data[f"{PREFIX}_ml_signal_still_limited_validation_only"] is True
    for key in (
        "result_accepted_as_reliability_claim",
        "result_accepted_as_maturity_claim",
        "result_accepted_as_production_readiness_claim",
        "result_accepted_as_model_improvement_claim",
        "ml_signal_ready_for_runtime",
        "ml_signal_ready_for_training",
        "ml_signal_ready_for_route_authority",
        "runtime_route_authority_enabled",
        "router_prompt_logic_modified",
        "prompt_loading_enabled",
        "provider_calls_enabled",
        "embeddings_enabled",
        "result_persistence_enabled",
        "training_data_intake_enabled",
        "dataset_creation_enabled",
        "model_training_started",
        "model_calibration_started",
        "model_improvement_started",
        "gold_registry_write_enabled",
        "registry_mutation_enabled",
        "runtime_pilot_enabled",
        "copilot_enabled",
    ):
        assert data[f"{PREFIX}_{key}"] is False


def test_mlrt72_implements_web_informed_test_volume_policy() -> None:
    data = manifest()
    assert data[f"{PREFIX}_web_check_performed"] is True
    assert data[f"{PREFIX}_more_tests_help_reliability_conditionally"] is True
    assert data[f"{PREFIX}_repeating_similar_easy_cases_improves_reliability"] is False
    assert data[f"{PREFIX}_test_volume_escalation_policy_enabled_for_future_test_suite_zips"] is True
    assert data[f"{PREFIX}_minimum_future_real_test_suite_cases"] == 16
    assert data[f"{PREFIX}_next_real_test_suite_target_cases"] == 24
    assert data[f"{PREFIX}_future_cases_must_be_in_memory_test_local"] is True
    assert data[f"{PREFIX}_future_cases_must_be_non_duplicate"] is True
    assert data[f"{PREFIX}_future_cases_must_be_boundary_diverse"] is True
    results = [evaluate_policy_case(case, data) for case in POLICY_REQUIREMENT_CASES]
    assert len(results) == 12
    assert all(result["passed"] for result in results), results


def test_mlrt72_documentation_records_research_decision_and_next_correction() -> None:
    doc = read(DOC)
    readme = read(README)
    for required in (
        FEATURE_ID,
        FEATURE_TITLE,
        "Status: good direction, stronger than before, but still not runtime-ready.",
        "MLRT-71 boundary-negative controlled offline test suite: 8/8 boundary-negative containment cases passed.",
        "Cumulative controlled offline prompt-selection coverage: 26/26 cases passed across four tests.",
        "More cases can improve confidence when they are large enough, representative, non-duplicate, and closer to real expected usage.",
        "Repeating similar easy positive cases does not materially improve reliability and may overstate confidence.",
        "Minimum future real test-suite size: 16 in-memory cases",
        "Next real test-suite target: 24 in-memory cases.",
        POS_LABEL,
        NEXT_TITLE,
    ):
        assert required in doc
    assert FEATURE_ID in readme
    assert POS_LABEL in readme
    assert NEXT_TITLE in readme


def test_mlrt72_preserves_exact_python_source_surface() -> None:
    mlrt_py = relative_py_files(MLRT)
    assert mlrt_py == ["source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py = relative_py_files(LAB)
    assert lab_py == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def main() -> None:
    test_mlrt72_files_and_mlrt71_result_exist()
    test_mlrt72_reviews_boundary_negative_result_and_keeps_claim_limited()
    test_mlrt72_implements_web_informed_test_volume_policy()
    test_mlrt72_documentation_records_research_decision_and_next_correction()
    test_mlrt72_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT72_BOUNDARY_NEGATIVE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_RESULT_REVIEW_GATE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
