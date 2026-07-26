from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_78_MAXIMUM_OPTIMIZED_NEAR_MISS_COUNTERFACTUAL_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
PREV_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_77_MAXIMUM_OPTIMIZED_NEAR_MISS_COUNTERFACTUAL_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = "rss_mlrt78_maximum_optimized_near_miss_counterfactual_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-78 Maximum-Optimized Near-Miss Counterfactual Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1"
PREFIX = "rss_mlrt78_maximum_optimized_near_miss_counterfactual_controlled_offline_ml_prompt_selection_test_suite_result_review_gate"
POS_LABEL = "RSS_MLRT78_NEAR_MISS_COUNTERFACTUAL_RESULT_REVIEW_ACCEPTED_FOR_DIFFERENTIAL_DRIFT_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-79 Maximum-Optimized Differential Drift Controlled Offline ML Prompt-Selection Test Suite v1"
CONTRACT_SUMMARY = "MLRT-78 Maximum-Optimized Near-Miss Counterfactual Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-77 64-case maximum-optimized near-miss counterfactual in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-77 freeze; preserved that MLRT-77 passed 64/64 near-miss counterfactual cases across eight balanced audit families with 32/32 counterfactual pairs represented, 32 governed offline-review-only cases, 32 containment/no-authority cases, and cumulative controlled offline prompt-selection coverage of 218/218 cases across seven real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized differential drift offline suite to test small wording/context shifts that could wrongly change route selection or boundary containment; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero."

BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_enabled', 'model_training_started', 'model_calibration_enabled', 'model_calibration_started', 'model_improvement_enabled', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'gold_record_creation_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'copilot_behavior_enabled', 'activation_key_enabled', 'field_test_mode_enabled', 'runtime_decision_enabled']

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def manifest() -> dict[str, object]:
    return json.loads(read(MANIFEST))

def relative_py_files(base: Path) -> list[str]:
    if not base.exists():
        return []
    return sorted(str(path.relative_to(base)).replace("\\", "/") for path in base.rglob("*.py"))

def test_mlrt78_files_and_prerequisites_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert PREV_DOC.exists()
    assert (MLRT / "source_surface" / "minimal_non_runtime_harness_stub.py").exists()
    assert (LAB / "candidate_evaluation_harness_interface.py").exists()
    assert (LAB / "deterministic_runner_skeleton.py").exists()
    assert (LAB / "lab_self_validation_gate.py").exists()

def test_mlrt78_manifest_reviews_mlrt77_without_claiming_runtime() -> None:
    data = manifest()
    assert data[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert data[f"{PREFIX}_previous_suite_feature_id"] == "rss_mlrt77_maximum_optimized_near_miss_counterfactual_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert data[f"{PREFIX}_previous_suite_freeze_required_before_install"] is True
    assert data[f"{PREFIX}_mlrt77_result_reviewed"] is True
    assert data[f"{PREFIX}_mlrt77_near_miss_cases_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt77_near_miss_cases_passed"] == 64
    assert data[f"{PREFIX}_mlrt77_audit_families_reviewed"] == 8
    assert data[f"{PREFIX}_mlrt77_cases_per_family_reviewed"] == 8
    assert data[f"{PREFIX}_mlrt77_counterfactual_pairs_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt77_counterfactual_pairs_passed"] == 32
    assert data[f"{PREFIX}_mlrt77_unique_case_ids_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt77_unique_user_requests_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt77_governed_offline_review_only_cases_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt77_containment_no_authority_cases_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt77_forbidden_selected_routes_reviewed"] == 0
    assert data[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 218
    assert data[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 7
    assert data[f"{PREFIX}_answer_key_comparison_reviewed"] is True
    assert data[f"{PREFIX}_counterfactual_pairing_reviewed"] is True
    assert data[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert data[f"{PREFIX}_non_duplicate_case_protection_confirmed"] is True
    assert data[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    assert data[f"{PREFIX}_accepted_for_continued_offline_testing_only"] is True
    assert data[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_differential_drift_offline_suite"
    assert data[f"{PREFIX}_next_real_test_suite_target_cases"] == 64
    for suffix in (
        "result_accepted_as_reliability_claim",
        "result_accepted_as_maturity_claim",
        "result_accepted_as_production_readiness_claim",
        "result_accepted_as_model_improvement_claim",
        "ml_signal_ready_for_runtime",
        "ml_signal_ready_for_training",
        "ml_signal_ready_for_route_authority",
    ):
        assert data[f"{PREFIX}_{suffix}"] is False
    for flag in BOUNDARY_FALSE_FLAGS:
        assert data[f"{PREFIX}_{flag}"] is False
    assert data[f"{PREFIX}_critical_boundary_error_budget"] == 0

def test_mlrt78_documentation_records_review_result_and_next_correction() -> None:
    doc = read(DOC)
    readme = read(README)
    for text in (doc, readme):
        assert FEATURE_ID in text
        assert FEATURE_TITLE in text
        assert "64/64" in text
        assert "218/218" in text
        assert "32/32" in doc
        assert "validation-only" in text
        assert "differential drift" in text.lower()
        assert POS_LABEL in text
        assert NEXT_TITLE in text

def test_mlrt78_preserves_exact_python_source_surface() -> None:
    assert relative_py_files(MLRT) == ["source_surface/minimal_non_runtime_harness_stub.py"]
    assert relative_py_files(LAB) == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]

def main() -> None:
    test_mlrt78_files_and_prerequisites_exist()
    test_mlrt78_manifest_reviews_mlrt77_without_claiming_runtime()
    test_mlrt78_documentation_records_review_result_and_next_correction()
    test_mlrt78_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT78_MAXIMUM_OPTIMIZED_NEAR_MISS_COUNTERFACTUAL_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK")

if __name__ == "__main__":
    main()
