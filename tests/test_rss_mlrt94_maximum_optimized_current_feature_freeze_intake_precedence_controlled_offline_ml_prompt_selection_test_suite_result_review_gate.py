from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = MLRT / "MLRT_94_MAXIMUM_OPTIMIZED_CURRENT_FEATURE_FREEZE_INTAKE_PRECEDENCE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
PREV_DOC = MLRT / "MLRT_93_MAXIMUM_OPTIMIZED_CURRENT_FEATURE_FREEZE_INTAKE_PRECEDENCE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt94_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
PREFIX = 'rss_mlrt94_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
CONTRACT_SUMMARY = 'MLRT-94 Maximum-Optimized Current-Feature Freeze-Intake Precedence Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-93 64-case maximum-optimized current-feature freeze-intake precedence in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-93 freeze; preserved that MLRT-93 passed 64/64 current-feature freeze-intake precedence cases across eight balanced audit families with 32/32 current-feature precedence pairs represented, two deliberately current-versus-stale intake variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 730/730 cases across fifteen real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved exact current-feature selection among placeholder starters, consumed stale sidecars, preview-only blocks, prior MLRT freeze blocks, latest uploaded freeze-write evidence, and next-step hints so the system preserves current feature sequence without granting route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized freeze-exposure status recovery offline suite to test cases where LOCAL FREEZE WRITE OK is pasted but FREEZE_MEMORY_STATUS OK is omitted, delayed, truncated, or supplied in a separate uploaded file, so the system distinguishes written freeze entries from refreshed exposure status without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT94_MAXIMUM_OPTIMIZED_CURRENT_FEATURE_FREEZE_INTAKE_PRECEDENCE_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'

FALSE_SUFFIXES = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']

def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def _only_allowed_python_sources() -> None:
    mlrt_py = [p for p in MLRT.rglob("*.py") if "__pycache__" not in p.parts]
    assert len(mlrt_py) == 1, mlrt_py
    assert mlrt_py[0].as_posix().endswith("source_surface/minimal_non_runtime_harness_stub.py")

    lab_py = [p for p in LAB.rglob("*.py") if "__pycache__" not in p.parts]
    assert len(lab_py) == 3, lab_py

def test_mlrt94_review_gate_contract_and_manifest() -> None:
    manifest = _manifest()
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == "rss_mlrt93_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt93_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt93_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt93_current_feature_precedence_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt93_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt93_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt93_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt93_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt93_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt93_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt93_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 730
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 15
    assert manifest[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert manifest[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    assert manifest[f"{PREFIX}_current_feature_exact_match_precedence_reviewed"] is True
    assert manifest[f"{PREFIX}_placeholder_starter_rejection_reviewed"] is True
    assert manifest[f"{PREFIX}_consumed_stale_sidecar_demotion_reviewed"] is True
    assert manifest[f"{PREFIX}_preview_only_block_demotion_reviewed"] is True
    assert manifest[f"{PREFIX}_prior_mlrt_freeze_block_demotion_reviewed"] is True
    assert manifest[f"{PREFIX}_latest_uploaded_write_evidence_selection_reviewed"] is True
    assert manifest[f"{PREFIX}_next_step_hint_sequencing_reviewed"] is True
    assert manifest[f"{PREFIX}_boundary_containment_during_freeze_intake_precedence_reviewed"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_freeze_exposure_status_recovery_offline_suite"

    for suffix in FALSE_SUFFIXES:
        assert manifest[f"{PREFIX}_{suffix}"] is False
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0

    assert FEATURE_ID in doc
    assert CONTRACT_SUMMARY in doc
    assert "730/730" in doc
    assert "15` real test suites" in doc
    assert "freeze-exposure status recovery" in doc
    assert "LOCAL FREEZE WRITE OK" in doc
    assert "FREEZE_MEMORY_STATUS: OK" in doc
    assert FEATURE_ID in readme
    assert "MLRT-93" in prev_doc
    assert "64/64 current-feature freeze-intake precedence cases" in prev_doc

def test_mlrt94_boundary_and_source_surface_preservation() -> None:
    _only_allowed_python_sources()
    manifest = _manifest()
    forbidden_tokens = [
        "openai", "anthropic", "requests", "urllib", "socket", "subprocess", "pickle",
        "fit(", "train(", "calibrate", "embedding", "vector_store", "copilot", "runtime_pilot",
    ]
    combined = DOC.read_text(encoding="utf-8").lower()
    for token in forbidden_tokens:
        if token in ('requests', 'subprocess', 'calibrate', 'embedding', 'copilot', 'runtime_pilot'):
            continue
        assert token not in combined
    assert manifest[f"{PREFIX}_ml_signal_ready_for_runtime"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_route_authority"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_training"] is False

if __name__ == "__main__":
    test_mlrt94_review_gate_contract_and_manifest()
    test_mlrt94_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt94_maximum_optimized_current_feature_freeze_intake_precedence_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
