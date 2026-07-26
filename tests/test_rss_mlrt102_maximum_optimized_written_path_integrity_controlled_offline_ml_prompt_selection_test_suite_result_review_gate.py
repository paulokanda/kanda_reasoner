from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_102_MAXIMUM_OPTIMIZED_WRITTEN_PATH_INTEGRITY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_101_MAXIMUM_OPTIMIZED_WRITTEN_PATH_INTEGRITY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt102_maximum_optimized_written_path_integrity_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-102 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt102_maximum_optimized_written_path_integrity_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
PREV_FEATURE_ID = 'rss_mlrt101_maximum_optimized_written_path_integrity_controlled_offline_ml_prompt_selection_test_suite_v1'
POS_LABEL = 'RSS_MLRT102_WRITTEN_PATH_INTEGRITY_RESULT_REVIEW_ACCEPTED_FOR_NEXT_OFFLINE_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-103 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite v1'
CONTRACT_SUMMARY = 'MLRT-102 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-101 64-case maximum-optimized written-path integrity in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-101 freeze; preserved that MLRT-101 passed 64/64 written-path integrity cases across eight balanced audit families with 32/32 written-path integrity pairs represented, two deliberately selected-project-frozen-memory-paths-versus-missing-or-wrong-path variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 986/986 cases across nineteen real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of freeze completion to selected-project written paths under project_freeze_after_update/frozen_features_memory, including matching entries freeze file, freeze_index.json, project_frozen_implemented_steps.md, exact project root, exact current freeze ID, and refreshed FREEZE_MEMORY_STATUS OK, while demoting missing, truncated, stale, project_freeze_ledger, wrong-root, missing-index, missing-implemented-steps, missing-entries, or mismatched-freeze-ID path evidence without false blockers or unsafe route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized freeze-index consistency offline suite to test cases where freeze_index.json counts, entry files, active/non-superseded entries, project_frozen_implemented_steps.md, AI-send exposure, and latest current-feature freeze IDs disagree, so the system binds current freeze memory exposure to selected-project index consistency without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT102_MAXIMUM_OPTIMIZED_WRITTEN_PATH_INTEGRITY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'
FALSE_SUFFIXES = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _only_allowed_python_sources() -> None:
    mlrt_py = [path.relative_to(ROOT).as_posix() for path in MLRT.rglob("*.py") if "__pycache__" not in path.parts]
    assert mlrt_py == ["kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py = sorted(path.name for path in LAB.rglob("*.py") if "__pycache__" not in path.parts)
    assert lab_py == ["candidate_evaluation_harness_interface.py", "deterministic_runner_skeleton.py", "lab_self_validation_gate.py"]


def test_mlrt102_review_gate_contract_and_manifest() -> None:
    manifest = _manifest()
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt101_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt101_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt101_written_path_integrity_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt101_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt101_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt101_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt101_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt101_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt101_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt101_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 986
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 19
    assert manifest[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert manifest[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    for suffix in [
        "selected_project_written_paths_reviewed", "matching_entries_freeze_file_reviewed",
        "freeze_index_json_path_reviewed", "project_frozen_implemented_steps_path_reviewed",
        "exact_project_root_path_reviewed", "exact_current_freeze_id_path_binding_reviewed",
        "freeze_memory_status_ok_path_exposure_reviewed", "missing_paths_demoted_reviewed",
        "truncated_paths_demoted_reviewed", "stale_paths_demoted_reviewed",
        "project_freeze_ledger_paths_demoted_reviewed", "wrong_root_paths_demoted_reviewed",
        "missing_index_path_demoted_reviewed", "missing_implemented_steps_path_demoted_reviewed",
        "missing_entries_path_demoted_reviewed", "mismatched_freeze_id_path_demoted_reviewed",
        "false_blocker_prevention_reviewed",
    ]:
        assert manifest[f"{PREFIX}_{suffix}"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_freeze_index_consistency_offline_suite"
    for suffix in FALSE_SUFFIXES:
        assert manifest[f"{PREFIX}_{suffix}"] is False
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0

    assert FEATURE_ID in doc
    assert CONTRACT_SUMMARY in doc
    assert "986/986" in doc
    assert "19` real test suites" in doc
    assert "written-path integrity" in doc
    assert "freeze_index.json" in doc
    assert "project_frozen_implemented_steps.md" in doc
    assert "project_freeze_ledger" in doc
    assert "freeze-index consistency" in doc
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "MLRT-101" in prev_doc
    assert "64/64 written-path integrity cases" in prev_doc


def test_mlrt102_boundary_and_source_surface_preservation() -> None:
    _only_allowed_python_sources()
    manifest = _manifest()
    forbidden_runtime_tokens = ["openai", "anthropic", "urllib", "socket", "pickle", "fit(", "train(", "vector_store", "runtime_pilot"]
    combined = DOC.read_text(encoding="utf-8").lower()
    for token in forbidden_runtime_tokens:
        assert token not in combined
    assert manifest[f"{PREFIX}_ml_signal_ready_for_runtime"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_route_authority"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_training"] is False


if __name__ == "__main__":
    test_mlrt102_review_gate_contract_and_manifest()
    test_mlrt102_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt102_maximum_optimized_written_path_integrity_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
