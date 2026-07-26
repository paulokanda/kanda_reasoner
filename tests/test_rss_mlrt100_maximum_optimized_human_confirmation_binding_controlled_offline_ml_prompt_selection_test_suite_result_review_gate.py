from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_100_MAXIMUM_OPTIMIZED_HUMAN_CONFIRMATION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_99_MAXIMUM_OPTIMIZED_HUMAN_CONFIRMATION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt100_maximum_optimized_human_confirmation_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-100 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt100_maximum_optimized_human_confirmation_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
PREV_FEATURE_ID = 'rss_mlrt99_maximum_optimized_human_confirmation_binding_controlled_offline_ml_prompt_selection_test_suite_v1'
POS_LABEL = 'RSS_MLRT100_HUMAN_CONFIRMATION_BINDING_RESULT_REVIEW_ACCEPTED_FOR_NEXT_OFFLINE_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-101 Maximum-Optimized Written-Path Integrity Controlled Offline ML Prompt-Selection Test Suite v1'
CONTRACT_SUMMARY = 'MLRT-100 Maximum-Optimized Human-Confirmation Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-99 64-case maximum-optimized human-confirmation binding in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-99 freeze; preserved that MLRT-99 passed 64/64 human-confirmation binding cases across eight balanced audit families with 32/32 human-confirmation binding pairs represented, two deliberately current-bound-confirmation-versus-unbound-or-mismatched-confirmation variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 922/922 cases across eighteen real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of human confirmation to the exact current feature title, exact current freeze ID, explicit Confirm and Write action, matching LOCAL FREEZE WRITE OK block, written frozen_features_memory paths, and refreshed FREEZE_MEMORY_STATUS OK, while demoting implied, stale, mismatched, split, preview-only, wrong-feature, or ambiguous confirmation evidence without false blockers or unsafe route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized written-path integrity offline suite to test cases where written paths are missing, truncated, stale, pointed at project_freeze_ledger, pointed at the wrong project root, missing freeze_index.json, missing project_frozen_implemented_steps.md, missing entries path, or mismatched to the current freeze ID, so the system binds freeze completion to the selected project frozen_features_memory paths without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT100_MAXIMUM_OPTIMIZED_HUMAN_CONFIRMATION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'

FALSE_SUFFIXES = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _only_allowed_python_sources() -> None:
    mlrt_py = [path.relative_to(ROOT).as_posix() for path in MLRT.rglob("*.py") if "__pycache__" not in path.parts]
    assert mlrt_py == ["kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"]

    lab_py = sorted(path.name for path in LAB.rglob("*.py") if "__pycache__" not in path.parts)
    assert lab_py == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]


def test_mlrt100_review_gate_contract_and_manifest() -> None:
    manifest = _manifest()
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt99_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt99_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt99_human_confirmation_binding_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt99_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt99_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt99_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt99_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt99_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt99_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt99_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 922
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 18
    assert manifest[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert manifest[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    assert manifest[f"{PREFIX}_exact_current_feature_title_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_exact_current_freeze_id_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_explicit_confirm_and_write_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_local_freeze_write_ok_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_written_frozen_features_memory_paths_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_freeze_memory_status_ok_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_implied_confirmation_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_stale_confirmation_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_mismatched_title_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_mismatched_freeze_id_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_split_confirmation_recovered_reviewed"] is True
    assert manifest[f"{PREFIX}_preview_only_confirmation_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_wrong_feature_confirmation_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_ambiguous_confirmation_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_false_blocker_prevention_reviewed"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_written_path_integrity_offline_suite"

    for suffix in FALSE_SUFFIXES:
        assert manifest[f"{PREFIX}_{suffix}"] is False
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0

    assert FEATURE_ID in doc
    assert CONTRACT_SUMMARY in doc
    assert "922/922" in doc
    assert "18` real test suites" in doc
    assert "human-confirmation binding" in doc
    assert "Confirm and Write" in doc
    assert "LOCAL FREEZE WRITE OK" in doc
    assert "FREEZE_MEMORY_STATUS: OK" in doc
    assert "written-path integrity" in doc
    assert "project_freeze_ledger" in doc
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "MLRT-99" in prev_doc
    assert "64/64 human-confirmation binding cases" in prev_doc


def test_mlrt100_boundary_and_source_surface_preservation() -> None:
    _only_allowed_python_sources()
    manifest = _manifest()
    forbidden_runtime_tokens = [
        "openai", "anthropic", "urllib", "socket", "pickle",
        "fit(", "train(", "vector_store", "runtime_pilot",
    ]
    combined = DOC.read_text(encoding="utf-8").lower()
    for token in forbidden_runtime_tokens:
        assert token not in combined
    assert manifest[f"{PREFIX}_ml_signal_ready_for_runtime"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_route_authority"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_training"] is False


if __name__ == "__main__":
    test_mlrt100_review_gate_contract_and_manifest()
    test_mlrt100_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt100_maximum_optimized_human_confirmation_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
