from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_96_MAXIMUM_OPTIMIZED_FREEZE_EXPOSURE_STATUS_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_95_MAXIMUM_OPTIMIZED_FREEZE_EXPOSURE_STATUS_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt96_maximum_optimized_freeze_exposure_status_recovery_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-96 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt96_maximum_optimized_freeze_exposure_status_recovery_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
PREV_FEATURE_ID = 'rss_mlrt95_maximum_optimized_freeze_exposure_status_recovery_controlled_offline_ml_prompt_selection_test_suite_v1'
POS_LABEL = 'RSS_MLRT96_FREEZE_EXPOSURE_STATUS_RECOVERY_RESULT_REVIEW_ACCEPTED_FOR_NEXT_OFFLINE_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-97 Maximum-Optimized Preview-Versus-Write Boundary Controlled Offline ML Prompt-Selection Test Suite v1'
CONTRACT_SUMMARY = 'MLRT-96 Maximum-Optimized Freeze-Exposure Status Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-95 64-case maximum-optimized freeze-exposure status recovery in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-95 freeze; preserved that MLRT-95 passed 64/64 freeze-exposure status recovery cases across eight balanced audit families with 32/32 freeze-exposure recovery pairs represented, two deliberately status-recovered-versus-status-gap variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 794/794 cases across sixteen real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved the distinction between LOCAL FREEZE WRITE OK as written freeze-entry evidence and FREEZE_MEMORY_STATUS OK as refreshed exposure evidence, including omitted, delayed, truncated, separate-upload, stale-status, and wrong-feature status cases without false blockers or unsafe route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized preview-versus-write boundary offline suite to test cases where preview-only evidence, writable preview blocks, local write evidence, refreshed exposure status, and human confirmation requirements are confused, so the system preserves the strict distinction between read-only preview and confirmed write without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT96_MAXIMUM_OPTIMIZED_FREEZE_EXPOSURE_STATUS_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'

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


def test_mlrt96_review_gate_contract_and_manifest() -> None:
    manifest = _manifest()
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt95_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt95_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt95_freeze_exposure_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt95_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt95_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt95_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt95_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt95_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt95_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt95_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 794
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 16
    assert manifest[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert manifest[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    assert manifest[f"{PREFIX}_local_freeze_write_ok_distinction_reviewed"] is True
    assert manifest[f"{PREFIX}_freeze_memory_status_ok_distinction_reviewed"] is True
    assert manifest[f"{PREFIX}_omitted_status_recovery_reviewed"] is True
    assert manifest[f"{PREFIX}_delayed_status_recovery_reviewed"] is True
    assert manifest[f"{PREFIX}_truncated_status_targeted_search_reviewed"] is True
    assert manifest[f"{PREFIX}_separate_upload_status_recovery_reviewed"] is True
    assert manifest[f"{PREFIX}_stale_status_demotion_reviewed"] is True
    assert manifest[f"{PREFIX}_wrong_feature_status_demotion_reviewed"] is True
    assert manifest[f"{PREFIX}_false_blocker_prevention_reviewed"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_preview_versus_write_boundary_offline_suite"

    for suffix in FALSE_SUFFIXES:
        assert manifest[f"{PREFIX}_{suffix}"] is False
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0

    assert FEATURE_ID in doc
    assert CONTRACT_SUMMARY in doc
    assert "794/794" in doc
    assert "16` real test suites" in doc
    assert "LOCAL FREEZE WRITE OK" in doc
    assert "FREEZE_MEMORY_STATUS: OK" in doc
    assert "preview-versus-write boundary" in doc
    assert "Preview Freeze Entry is read-only" in doc
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "MLRT-95" in prev_doc
    assert "64/64 freeze-exposure status recovery cases" in prev_doc


def test_mlrt96_boundary_and_source_surface_preservation() -> None:
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
    test_mlrt96_review_gate_contract_and_manifest()
    test_mlrt96_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt96_maximum_optimized_freeze_exposure_status_recovery_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
