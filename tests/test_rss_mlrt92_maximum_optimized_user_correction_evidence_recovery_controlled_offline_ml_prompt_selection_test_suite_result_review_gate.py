from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = MLRT / "MLRT_92_MAXIMUM_OPTIMIZED_USER_CORRECTION_EVIDENCE_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
PREV_DOC = MLRT / "MLRT_91_MAXIMUM_OPTIMIZED_USER_CORRECTION_EVIDENCE_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt92_maximum_optimized_user_correction_evidence_recovery_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-92 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt92_maximum_optimized_user_correction_evidence_recovery_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
PREV_FEATURE_ID = 'rss_mlrt91_maximum_optimized_user_correction_evidence_recovery_controlled_offline_ml_prompt_selection_test_suite_v1'
PREV_TITLE = 'Routing Signal Scorer MLRT-91 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite v1'
POS_LABEL = 'RSS_MLRT92_USER_CORRECTION_EVIDENCE_RECOVERY_RESULT_REVIEW_ACCEPTED_FOR_FREEZE_INTAKE_PRECEDENCE_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-93 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite v1'
NEXT_ID = 'rss_mlrt93_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite_v1'
CONTRACT_SUMMARY = 'MLRT-92 Maximum-Optimized User-Correction Evidence Recovery Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-91 64-case maximum-optimized user-correction evidence recovery in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-91 freeze; preserved that MLRT-91 passed 64/64 user-correction evidence recovery cases across eight balanced audit families with 32/32 user-correction evidence recovery pairs represented, two deliberately correction-versus-false-blocker variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 666/666 cases across fourteen real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved the canonical workflow rule that user corrections such as “I said it is always in upload file” require targeted inspection of the uploaded freeze file before blocking progress; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized current-feature freeze-intake precedence offline suite to test exact current-feature selection among placeholder starters, consumed stale sidecars, preview-only blocks, prior MLRT freeze blocks, latest uploaded freeze-write evidence, and next-step hints so the system preserves current feature sequence without granting route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT92_MAXIMUM_OPTIMIZED_USER_CORRECTION_EVIDENCE_RECOVERY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'
NEXT_CORRECTION = 'maximum_optimized_current_feature_freeze_intake_precedence_offline_suite'


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def manifest() -> dict[str, object]:
    return json.loads(read(MANIFEST))


def relative_py_files(base: Path) -> list[str]:
    if not base.exists():
        return []
    return sorted(
        str(path.relative_to(base)).replace(chr(92), "/")
        for path in base.rglob("*.py")
        if "__pycache__" not in path.parts
    )


def test_mlrt92_review_gate_contract() -> None:
    data = manifest()
    doc = read(DOC)
    readme = read(README)
    prev_doc = read(PREV_DOC)

    assert data[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert data[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert data[f"{PREFIX}_previous_suite_feature_id"] == PREV_FEATURE_ID
    assert data[f"{PREFIX}_previous_suite_title"] == PREV_TITLE
    assert data[f"{PREFIX}_positive_validation_state"] == POS_LABEL
    assert data[f"{PREFIX}_next_safe_milestone"] == NEXT_TITLE
    assert data[f"{PREFIX}_next_suite_feature_id"] == NEXT_ID
    assert data[f"{PREFIX}_accepted_for_continued_offline_testing_only"] is True
    assert data[f"{PREFIX}_validation_only_evidence"] is True
    assert data[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert data[f"{PREFIX}_mlrt91_cases_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt91_cases_passed"] == 64
    assert data[f"{PREFIX}_mlrt91_user_correction_pairs_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt91_audit_families_reviewed"] == 8
    assert data[f"{PREFIX}_mlrt91_cases_per_family_reviewed"] == 8
    assert data[f"{PREFIX}_mlrt91_governed_offline_review_only_cases_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt91_containment_no_authority_cases_reviewed"] == 32
    assert data[f"{PREFIX}_mlrt91_unique_case_ids_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt91_unique_user_requests_reviewed"] == 64
    assert data[f"{PREFIX}_mlrt91_forbidden_selected_routes_reviewed"] == 0
    assert data[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 666
    assert data[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 14
    assert data[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert data[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    assert data[f"{PREFIX}_canonical_validation_in_chat_freeze_in_upload_pattern_preserved"] is True
    assert data[f"{PREFIX}_user_correction_upload_file_recovery_reviewed"] is True
    assert data[f"{PREFIX}_long_truncated_upload_search_recovery_reviewed"] is True
    assert data[f"{PREFIX}_generic_pasted_text_filename_recovery_reviewed"] is True
    assert data[f"{PREFIX}_preview_vs_write_recovery_reviewed"] is True
    assert data[f"{PREFIX}_false_blocker_prevention_reviewed"] is True
    assert data[f"{PREFIX}_next_step_sequence_recovery_reviewed"] is True
    assert data[f"{PREFIX}_identified_next_correction"] == NEXT_CORRECTION
    assert data[f"{PREFIX}_ml_signal_ready_for_runtime"] is False
    assert data[f"{PREFIX}_ml_signal_ready_for_route_authority"] is False
    assert data[f"{PREFIX}_ml_signal_ready_for_training"] is False
    assert data[f"{PREFIX}_critical_boundary_error_budget"] == 0

    for flag in BOUNDARY_FALSE_FLAGS:
        assert data[f"{PREFIX}_{flag}"] is False, flag

    assert FEATURE_TITLE in doc
    assert FEATURE_ID in doc
    assert POS_LABEL in doc
    assert PREV_TITLE in doc
    assert NEXT_TITLE in doc
    assert CONTRACT_SUMMARY in doc
    assert "666/666" in doc
    assert "64/64" in doc
    assert "0` new real prompt-selection cases" in doc
    assert "user corrections such as `I said it is always in upload file`" in doc
    assert "current-feature freeze-intake precedence" in doc

    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert PREV_FEATURE_ID in prev_doc
    assert "MLRT-91" in prev_doc
    assert "64" in prev_doc


def test_mlrt92_non_runtime_project_surface() -> None:
    assert DOC.exists(), DOC
    assert PREV_DOC.exists(), PREV_DOC
    assert MANIFEST.exists(), MANIFEST
    assert README.exists(), README

    mlrt_py_files = relative_py_files(MLRT)
    assert mlrt_py_files == ["source_surface/minimal_non_runtime_harness_stub.py"]

    lab_py_files = relative_py_files(LAB)
    assert lab_py_files == [
        "candidate_evaluation_harness_interface.py",
        "deterministic_runner_skeleton.py",
        "lab_self_validation_gate.py",
    ]

    assert not (ROOT / "KANDA_FREEZE_HINT.json").exists()


def main() -> None:
    test_mlrt92_review_gate_contract()
    test_mlrt92_non_runtime_project_surface()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"CONTRACT_TEST_OK: {CONTRACT_SUMMARY}")
    print(SANDBOX_MARKER)


if __name__ == "__main__":
    main()
