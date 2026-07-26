from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_74_INCREASED_VOLUME_MIXED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md"
MANIFEST = ROOT / "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
SOURCE = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_73_INCREASED_VOLUME_MIXED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"
FEATURE_ID = "rss_mlrt74_increased_volume_mixed_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-74 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1"
PREFIX = "rss_mlrt74_increased_volume_mixed_controlled_offline_ml_prompt_selection_test_suite_result_review_gate"
PREV_PREFIX = "rss_mlrt73_increased_volume_mixed_controlled_offline_ml_prompt_selection_test_suite"
POS_LABEL = "RSS_MLRT74_64_CASE_RESULT_REVIEW_ACCEPTED_AND_EXPECTED_ANSWER_COMPARISON_CONFIRMED_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-75 Maximum-Optimized Adversarial Controlled Offline ML Prompt-Selection Test Suite v1"
CONTRACT_SUMMARY = "MLRT-74 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-73 64-case optimized mixed in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-73 freeze; confirmed the user's understanding that offline ML prompt-selection testing works by creating fixed cases with known expected outcomes, running or representing the candidate ML answer, and comparing proposed candidate output against the expected answer key to determine pass/fail; preserved that MLRT-73 passed 64/64 optimized mixed cases across eight balanced audit families and cumulative controlled offline prompt-selection coverage is 90/90 cases across five real test suites; accepted this result for continued offline testing only, not as reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the future rule that real test-suite ZIPs use the maximum optimized number of coherent non-duplicate cases rather than repetitive filler; identified the next correction as a new maximum-optimized adversarial/edge offline suite, still in-memory, non-runtime, and non-authoritative; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."

FORBIDDEN_FALSE_SUFFIXES = (
    "result_accepted_as_reliability_claim",
    "result_accepted_as_maturity_claim",
    "result_accepted_as_production_readiness_claim",
    "result_accepted_as_model_improvement_claim",
    "ml_signal_ready_for_runtime",
    "ml_signal_ready_for_training",
    "ml_signal_ready_for_route_authority",
    "runtime_route_authority_enabled",
    "route_authority_enabled",
    "router_prompt_logic_modified",
    "prompt_loading_enabled",
    "live_prompt_library_read_enabled",
    "provider_calls_enabled",
    "embeddings_enabled",
    "vector_store_enabled",
    "result_persistence_enabled",
    "report_file_created",
    "persistent_case_files_created",
    "persistent_dataset_created",
    "persistent_labels_created",
    "training_data_intake_enabled",
    "training_data_use_enabled",
    "dataset_creation_enabled",
    "model_training_started",
    "model_calibration_started",
    "model_improvement_started",
    "gold_registry_created",
    "gold_records_created",
    "gold_registry_write_enabled",
    "registry_mutation_enabled",
    "runtime_pilot_enabled",
    "copilot_enabled",
    "activation_key_enabled",
    "field_test_mode_enabled",
    "python_source_files_created_under_mlrt_box",
    "source_modified_by_mlrt74",
)


def read(path: Path) -> str:
    assert path.exists(), f"missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def relative_py_files(root: Path) -> list[str]:
    assert root.exists(), f"missing directory: {root}"
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*.py"))


def test_mlrt74_files_and_previous_mlrt73_result_exist() -> None:
    for path in (DOC, README, MANIFEST, SOURCE, PREV_DOC):
        assert path.exists(), f"missing expected file: {path}"
    previous = read(PREV_DOC)
    assert "MLRT-73 Increased-Volume Mixed Controlled Offline ML Prompt-Selection Test Suite" in previous
    data = manifest()
    assert data[f"{PREV_PREFIX}_feature_id"] == "rss_mlrt73_increased_volume_mixed_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert data[f"{PREV_PREFIX}_optimized_cases_evaluated_in_memory"] == 64
    assert data[f"{PREV_PREFIX}_optimized_cases_passed"] == 64
    assert data[f"{PREV_PREFIX}_audit_families_count"] == 8
    assert data[f"{PREV_PREFIX}_cases_per_audit_family"] == 8
    assert data[f"{PREV_PREFIX}_cumulative_controlled_offline_cases_passed"] == 90


def test_mlrt74_review_accepts_mlrt73_as_good_but_limited() -> None:
    data = manifest()
    assert data[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert data[f"{PREFIX}_previous_result_reviewed"] is True
    assert data[f"{PREFIX}_mlrt73_optimized_cases_passed"] == 64
    assert data[f"{PREFIX}_mlrt73_optimized_cases_evaluated_in_memory"] == 64
    assert data[f"{PREFIX}_mlrt73_audit_families_represented"] == 8
    assert data[f"{PREFIX}_mlrt73_cases_per_family"] == 8
    assert data[f"{PREFIX}_mlrt73_unique_case_ids"] == 64
    assert data[f"{PREFIX}_mlrt73_unique_user_requests"] == 64
    assert data[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 90
    assert data[f"{PREFIX}_cumulative_controlled_offline_test_stages_passed"] == 5
    assert data[f"{PREFIX}_ml_signal_good_for_continued_offline_testing"] is True
    assert data[f"{PREFIX}_ml_signal_stronger_after_64_case_suite"] is True
    assert data[f"{PREFIX}_ml_signal_still_limited_validation_only"] is True


def test_mlrt74_confirms_expected_answer_comparison_model() -> None:
    data = manifest()
    assert data[f"{PREFIX}_expected_answer_key_defined_for_each_test_case"] is True
    assert data[f"{PREFIX}_candidate_output_compared_against_expected_answer_key"] is True
    assert data[f"{PREFIX}_proposed_vs_expected_pass_fail_comparison_confirmed"] is True
    assert data[f"{PREFIX}_known_correct_answer_comparison_model_confirmed"] is True
    assert data[f"{PREFIX}_offline_gold_answer_oracle_is_test_local_only"] is True
    assert data[f"{PREFIX}_expected_answers_created_as_test_local_in_memory_fixtures_only"] is True
    assert data[f"{PREFIX}_gold_answer_oracle_persisted_to_registry"] is False
    assert data[f"{PREFIX}_comparison_result_is_validation_only"] is True
    assert data[f"{PREFIX}_comparison_result_is_not_unseen_generalization_proof"] is True


def test_mlrt74_future_testing_policy_and_next_milestone() -> None:
    data = manifest()
    assert data[f"{PREFIX}_future_real_suites_use_maximum_optimized_cases"] is True
    assert data[f"{PREFIX}_future_real_suites_must_remain_non_duplicate"] is True
    assert data[f"{PREFIX}_future_real_suites_must_remain_boundary_diverse"] is True
    assert data[f"{PREFIX}_future_real_suites_must_remain_statistically_coherent"] is True
    assert data[f"{PREFIX}_future_real_suites_must_not_use_repetitive_filler"] is True
    assert data[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert data[f"{PREFIX}_positive_label"] == POS_LABEL
    assert data[f"{PREFIX}_critical_boundary_error_budget"] == 0


def test_mlrt74_forbidden_boundary_flags_remain_false() -> None:
    data = manifest()
    for suffix in FORBIDDEN_FALSE_SUFFIXES:
        key = f"{PREFIX}_{suffix}"
        assert data[key] is False, f"forbidden flag should be false: {key}"


def test_mlrt74_docs_record_result_summary_and_comparison_doctrine() -> None:
    doc = read(DOC)
    readme = read(README)
    for text in (doc, readme):
        assert FEATURE_TITLE in text
        assert FEATURE_ID in text
        assert "64/64" in text
        assert "90/90" in text
        assert "expected answer" in text.lower()
        assert "candidate" in text.lower()
        assert "validation-only" in text
        assert ("not a reliability" in text.lower() or "not reliability" in text.lower() or "not a proof of reliability" in text.lower())
        assert NEXT_TITLE in text


def test_mlrt74_source_boundaries_are_preserved() -> None:
    assert relative_py_files(MLRT) == ["source_surface/minimal_non_runtime_harness_stub.py"]
    assert relative_py_files(LAB) == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt74_validation_markers() -> None:
    assert FEATURE_ID.endswith("_v1")
    assert POS_LABEL.startswith("RSS_MLRT74_")
    assert "64-case optimized mixed" in CONTRACT_SUMMARY
    assert "known expected outcomes" in CONTRACT_SUMMARY
    assert "validation-only evidence" in CONTRACT_SUMMARY
    assert "no runtime routing" in CONTRACT_SUMMARY
    assert "critical boundary error budget zero" in CONTRACT_SUMMARY


if __name__ == "__main__":
    test_mlrt74_files_and_previous_mlrt73_result_exist()
    test_mlrt74_review_accepts_mlrt73_as_good_but_limited()
    test_mlrt74_confirms_expected_answer_comparison_model()
    test_mlrt74_future_testing_policy_and_next_milestone()
    test_mlrt74_forbidden_boundary_flags_remain_false()
    test_mlrt74_docs_record_result_summary_and_comparison_doctrine()
    test_mlrt74_source_boundaries_are_preserved()
    test_mlrt74_validation_markers()
    print("VALIDATION OK: " + FEATURE_ID)
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print("SANDBOX_RSS_MLRT74_INCREASED_VOLUME_MIXED_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK")
