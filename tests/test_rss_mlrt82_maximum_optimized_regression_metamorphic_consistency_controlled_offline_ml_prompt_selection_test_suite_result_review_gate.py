from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = MLRT / "MLRT_82_MAXIMUM_OPTIMIZED_REGRESSION_METAMORPHIC_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
PREV_DOC = MLRT / "MLRT_81_MAXIMUM_OPTIMIZED_REGRESSION_METAMORPHIC_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = "rss_mlrt82_maximum_optimized_regression_metamorphic_consistency_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1"
FEATURE_TITLE = "Routing Signal Scorer MLRT-82 Maximum-Optimized Regression Metamorphic Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1"
PREFIX = "rss_mlrt82_maximum_optimized_regression_metamorphic_consistency_controlled_offline_ml_prompt_selection_test_suite_result_review_gate"
PREV_FEATURE_ID = "rss_mlrt81_maximum_optimized_regression_metamorphic_consistency_controlled_offline_ml_prompt_selection_test_suite_v1"
POS_LABEL = "RSS_MLRT82_METAMORPHIC_CONSISTENCY_RESULT_REVIEW_ACCEPTED_FOR_SEMANTIC_COLLISION_DISAMBIGUATION_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE"
NEXT_TITLE = "Routing Signal Scorer MLRT-83 Maximum-Optimized Semantic Collision Disambiguation Controlled Offline ML Prompt-Selection Test Suite v1"
CONTRACT_SUMMARY = 'MLRT-82 Maximum-Optimized Regression Metamorphic Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-81 64-case maximum-optimized regression metamorphic consistency in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-81 freeze; preserved that MLRT-81 passed 64/64 metamorphic consistency cases across eight balanced audit families with 32/32 meaning-preserving metamorphic pairs represented, two transformation variants per pair, 32 governed offline-review-only stable cases, 32 containment/no-authority stable cases, and cumulative controlled offline prompt-selection coverage of 346/346 cases across nine real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, or runtime-route-authority evidence; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized semantic collision disambiguation offline suite to test superficially similar or overlapping user requests that must still preserve distinct governed route selection or containment; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'

BOUNDARY_FALSE_FLAGS = [
    "route_authority_enabled",
    "runtime_route_authority_enabled",
    "router_prompt_logic_modified",
    "prompt_loading_enabled",
    "live_prompt_library_read_enabled",
    "live_freeze_memory_read_enabled",
    "live_router_canon_read_enabled",
    "provider_calls_enabled",
    "embeddings_enabled",
    "vector_store_enabled",
    "network_calls_enabled",
    "subprocess_calls_enabled",
    "batch_mode_enabled",
    "result_persistence_enabled",
    "report_persistence_enabled",
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
    "field_test_mode_enabled"
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(read(MANIFEST))


def relative_py_files(base: Path) -> list[str]:
    if not base.exists():
        return []
    return sorted(str(path.relative_to(base)).replace("\\", "/") for path in base.rglob("*.py"))


def test_mlrt82_files_and_prerequisites_exist() -> None:
    assert DOC.exists()
    assert README.exists()
    assert PREV_DOC.exists()
    assert (MLRT / "source_surface" / "minimal_non_runtime_harness_stub.py").exists()
    assert (LAB / "candidate_evaluation_harness_interface.py").exists()
    assert (LAB / "deterministic_runner_skeleton.py").exists()
    assert (LAB / "lab_self_validation_gate.py").exists()


def test_mlrt82_manifest_reviews_mlrt81_without_claiming_runtime() -> None:
    data = manifest()
    assert data[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert data[f"{PREFIX}_previous_suite_feature_id"] == PREV_FEATURE_ID
    assert data[f"{PREFIX}_previous_suite_freeze_required_before_install"] is True
    assert data[f"{PREFIX}_mlrt81_result_reviewed"] is True
    assert data[f"{PREFIX}_mlrt81_regression_metamorphic_consistency_cases_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt81_regression_metamorphic_consistency_cases_passed"] == 64
    assert data[f"{PREFIX}_mlrt81_audit_families_reviewed"] == 8
    assert data[f"{PREFIX}_mlrt81_cases_per_family_reviewed"] == 8
    assert data[f"{PREFIX}_mlrt81_metamorphic_pairs_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt81_metamorphic_pairs_passed"] == 32
    assert data[f"{PREFIX}_mlrt81_transformation_variants_per_pair_reviewed"] == 2
    assert data[f"{PREFIX}_mlrt81_unique_case_ids_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt81_unique_user_requests_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt81_governed_offline_review_only_stable_cases_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt81_containment_no_authority_stable_cases_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt81_forbidden_selected_routes_reviewed"] == 0
    assert data[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 346
    assert data[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 9
    assert data[f"{PREFIX}_review_gate_new_real_cases_added"] == 0
    assert data[f"{PREFIX}_regression_metamorphic_consistency_result_reviewed"] is True
    assert data[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert data[f"{PREFIX}_non_duplicate_case_protection_confirmed"] is True
    assert data[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    assert data[f"{PREFIX}_accepted_for_continued_offline_testing_only"] is True
    assert data[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_semantic_collision_disambiguation_offline_suite"
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


def test_mlrt82_documentation_records_review_result_and_next_correction() -> None:
    doc = read(DOC)
    readme = read(README)
    for text in (doc, readme):
        assert FEATURE_ID in text
        assert FEATURE_TITLE in text
        assert "64/64" in text
        assert "346/346" in text
        assert "validation-only" in text
        assert "semantic collision" in text.lower()
        assert POS_LABEL in text
        assert NEXT_TITLE in text
    assert "32/32" in doc
    assert "0 new real prompt-selection cases" in doc
    assert "continued offline testing" in doc
    assert "meaning-preserving" in doc


def test_mlrt82_preserves_exact_python_source_surface() -> None:
    assert relative_py_files(MLRT) == ["source_surface/minimal_non_runtime_harness_stub.py"]
    assert relative_py_files(LAB) == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def main() -> None:
    test_mlrt82_files_and_prerequisites_exist()
    test_mlrt82_manifest_reviews_mlrt81_without_claiming_runtime()
    test_mlrt82_documentation_records_review_result_and_next_correction()
    test_mlrt82_preserves_exact_python_source_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print("SANDBOX_RSS_MLRT82_MAXIMUM_OPTIMIZED_REGRESSION_METAMORPHIC_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK")


if __name__ == "__main__":
    main()
