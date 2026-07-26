from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
LAB = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
DOC = MLRT / "MLRT_104_MAXIMUM_OPTIMIZED_FREEZE_INDEX_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_103_MAXIMUM_OPTIMIZED_FREEZE_INDEX_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt104_maximum_optimized_freeze_index_consistency_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-104 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt104_maximum_optimized_freeze_index_consistency_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
PREV_FEATURE_ID = 'rss_mlrt103_maximum_optimized_freeze_index_consistency_controlled_offline_ml_prompt_selection_test_suite_v1'
POS_LABEL = 'RSS_MLRT104_FREEZE_INDEX_CONSISTENCY_RESULT_REVIEW_ACCEPTED_FOR_NEXT_OFFLINE_COVERAGE_NON_RUNTIME_NON_AUTHORITATIVE'
NEXT_TITLE = 'Routing Signal Scorer MLRT-105 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite v1'
CONTRACT_SUMMARY = 'MLRT-104 Maximum-Optimized Freeze-Index Consistency Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-103 64-case maximum-optimized freeze-index consistency in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-103 freeze; preserved that MLRT-103 passed 64/64 freeze-index consistency cases across eight balanced audit families with 32/32 freeze-index consistency pairs represented, two deliberately index-consistent-versus-index-inconsistent variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 1050/1050 cases across twenty real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of current freeze memory exposure to selected-project freeze_index.json consistency, including index entry counts, entry file counts, active/non-superseded counts, project_frozen_implemented_steps.md alignment, AI-send exposure alignment, latest current-feature freeze ID coherence, and read-only exposure status, while demoting stale, truncated, wrong-root, wrong-feature, project_freeze_ledger, mismatched-count, missing-entry-file, or mismatched-index evidence without false blockers or unsafe route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized AI-send exposure alignment offline suite to test cases where files_to_send_ai ZIPs, what_to_say_to_ai_freeze_feature.md, startup ZIP refresh, paste-after file refresh, 09_active_project_freeze_context.md, AI compliance refresh, and latest current-feature freeze IDs disagree, so the system binds current freeze memory exposure to AI-send/startup exposure alignment without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT104_MAXIMUM_OPTIMIZED_FREEZE_INDEX_CONSISTENCY_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'
FALSE_SUFFIXES = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _only_allowed_python_sources() -> None:
    mlrt_py = [path.relative_to(ROOT).as_posix() for path in MLRT.rglob("*.py") if "__pycache__" not in path.parts]
    assert mlrt_py == ["kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/source_surface/minimal_non_runtime_harness_stub.py"]
    lab_py = sorted(path.name for path in LAB.rglob("*.py") if "__pycache__" not in path.parts)
    assert lab_py == ["candidate_evaluation_harness_interface.py", "deterministic_runner_skeleton.py", "lab_self_validation_gate.py"]


def test_mlrt104_review_gate_contract_and_manifest() -> None:
    manifest = _manifest()
    doc = DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == PREV_FEATURE_ID
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt103_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt103_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt103_freeze_index_consistency_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt103_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt103_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt103_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt103_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt103_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt103_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt103_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 1050
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 20
    assert manifest[f"{PREFIX}_coverage_protection_confirmed"] is True
    assert manifest[f"{PREFIX}_maximum_optimized_number_policy_preserved"] is True
    for suffix in [
        "freeze_index_json_counts_reviewed", "entry_file_counts_reviewed",
        "active_non_superseded_counts_reviewed", "project_frozen_implemented_steps_alignment_reviewed",
        "ai_send_exposure_alignment_reviewed", "latest_current_feature_freeze_id_coherence_reviewed",
        "read_only_exposure_status_reviewed", "stale_index_evidence_demoted_reviewed",
        "truncated_index_evidence_demoted_reviewed", "wrong_root_index_evidence_demoted_reviewed",
        "wrong_feature_index_evidence_demoted_reviewed", "project_freeze_ledger_index_evidence_demoted_reviewed",
        "mismatched_count_evidence_demoted_reviewed", "missing_entry_file_evidence_demoted_reviewed",
        "mismatched_index_evidence_demoted_reviewed", "false_blocker_prevention_reviewed",
    ]:
        assert manifest[f"{PREFIX}_{suffix}"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_ai_send_exposure_alignment_offline_suite"
    for suffix in FALSE_SUFFIXES:
        assert manifest[f"{PREFIX}_{suffix}"] is False
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0

    assert FEATURE_ID in doc
    assert CONTRACT_SUMMARY in doc
    assert "1050/1050" in doc
    assert "20` real test suites" in doc
    assert "freeze-index consistency" in doc
    assert "freeze_index.json" in doc
    assert "project_frozen_implemented_steps.md" in doc
    assert "project_freeze_ledger" in doc
    assert "freeze-index consistency" in doc
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme
    assert "MLRT-103" in prev_doc
    assert "64/64 freeze-index consistency cases" in prev_doc


def test_mlrt104_boundary_and_source_surface_preservation() -> None:
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
    test_mlrt104_review_gate_contract_and_manifest()
    test_mlrt104_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt104_maximum_optimized_freeze_index_consistency_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
