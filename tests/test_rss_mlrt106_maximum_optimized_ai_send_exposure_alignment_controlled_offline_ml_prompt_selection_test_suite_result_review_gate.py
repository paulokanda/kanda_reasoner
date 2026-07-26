from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_106_MAXIMUM_OPTIMIZED_AI_SEND_EXPOSURE_ALIGNMENT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md'
PREV_DOC = ROOT / 'kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/MLRT_105_MAXIMUM_OPTIMIZED_AI_SEND_EXPOSURE_ALIGNMENT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md'
MANIFEST = ROOT / 'kanda_reasoner_app/routing_signal_scorer/box_manifest.json'
README = ROOT / 'kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability/README.md'
FEATURE_ID = 'rss_mlrt106_maximum_optimized_ai_send_exposure_alignment_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-106 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt106_maximum_optimized_ai_send_exposure_alignment_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
NEXT_TITLE = 'Routing Signal Scorer MLRT-107 Maximum-Optimized Startup Freeze-Context Propagation Controlled Offline ML Prompt-Selection Test Suite v1'
CONTRACT_SUMMARY = 'MLRT-106 Maximum-Optimized AI-Send Exposure Alignment Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-105 64-case maximum-optimized AI-send exposure alignment in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-105 freeze; preserved that MLRT-105 passed 64/64 AI-send exposure alignment cases across eight balanced audit families with 32/32 AI-send exposure alignment pairs represented, two deliberately exposure-aligned-versus-exposure-mismatched variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 1114/1114 cases across twenty-one real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of current freeze memory exposure to selected-project AI-send and startup exposure alignment, including files_to_send_ai ZIP refresh, what_to_say_to_ai_freeze_feature.md alignment, startup ZIP refresh (`first_prompts_to_ai.zip`), paste-after file refresh, 09_active_project_freeze_context.md coherence, AI compliance refresh block coherence, and latest current-feature freeze ID alignment, while demoting stale, truncated, wrong-root, wrong-feature, missing-AI-send, missing-startup, mismatched-context, or project_freeze_ledger exposure evidence without false blockers or unsafe route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized startup freeze-context propagation offline suite to test cases where first_prompts_to_ai.zip, paste_after_first_prompts_to_ai.md, 09_active_project_freeze_context.md, AI-send instructions, current freeze IDs, and planned next-step sequencing disagree across startup handoff surfaces, so the system binds the next AI programming session to the selected project current freeze memory without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT106_MAXIMUM_OPTIMIZED_AI_SEND_EXPOSURE_ALIGNMENT_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'

BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _only_allowed_python_sources() -> None:
    mlrt_py = [p for p in (ROOT / "kanda_reasoner_app/routing_signal_scorer/mlrt_non_runtime_candidate_reliability").rglob("*.py") if "__pycache__" not in p.parts]
    assert len(mlrt_py) == 1
    assert mlrt_py[0].as_posix().endswith("source_surface/minimal_non_runtime_harness_stub.py")
    lab_py = [p for p in (ROOT / "kanda_reasoner_app/routing_signal_scorer/lab_non_runtime_router_evaluation").rglob("*.py") if "__pycache__" not in p.parts]
    assert len(lab_py) == 3


def test_mlrt106_review_gate_contract_and_manifest() -> None:
    assert DOC.exists(), DOC
    assert PREV_DOC.exists(), PREV_DOC
    doc = DOC.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    manifest = _manifest()

    assert FEATURE_TITLE in doc
    assert FEATURE_ID in doc
    assert "MLRT-105" in doc
    assert "64/64" in doc
    assert "1114/1114" in doc
    assert "`21` real test suites" in doc
    assert "files_to_send_ai" in doc
    assert "what_to_say_to_ai_freeze_feature.md" in doc
    assert "first_prompts_to_ai.zip" in doc
    assert "paste_after_first_prompts_to_ai.md" in doc
    assert "09_active_project_freeze_context.md" in doc
    assert "AI compliance refresh" in doc
    assert "project_freeze_ledger" in doc
    assert "validation-only evidence" in doc
    assert NEXT_TITLE in doc
    assert "Startup Freeze-Context Propagation" in doc

    assert "MLRT-105" in prev_doc
    assert "64/64 AI-send exposure alignment cases" in prev_doc
    assert "1114/1114" in prev_doc
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == "rss_mlrt105_maximum_optimized_ai_send_exposure_alignment_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt105_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt105_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt105_ai_send_exposure_alignment_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt105_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt105_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt105_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt105_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt105_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt105_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt105_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 1114
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 21
    assert manifest[f"{PREFIX}_files_to_send_ai_zip_refresh_reviewed"] is True
    assert manifest[f"{PREFIX}_what_to_say_to_ai_freeze_feature_alignment_reviewed"] is True
    assert manifest[f"{PREFIX}_startup_zip_refresh_reviewed"] is True
    assert manifest[f"{PREFIX}_paste_after_file_refresh_reviewed"] is True
    assert manifest[f"{PREFIX}_active_project_freeze_context_coherence_reviewed"] is True
    assert manifest[f"{PREFIX}_ai_compliance_refresh_block_coherence_reviewed"] is True
    assert manifest[f"{PREFIX}_latest_current_feature_freeze_id_alignment_reviewed"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_startup_freeze_context_propagation_offline_suite"
    assert manifest[f"{PREFIX}_validation_only_evidence"] is True
    assert manifest[f"{PREFIX}_accepted_for_continued_offline_testing_only"] is True
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0


def test_mlrt106_boundary_and_source_surface_preservation() -> None:
    _only_allowed_python_sources()
    manifest = _manifest()
    forbidden_runtime_tokens = ["openai", "anthropic", "urllib", "socket", "pickle", "fit(", "train(", "vector_store", "runtime_pilot"]
    combined = DOC.read_text(encoding="utf-8").lower()
    for token in forbidden_runtime_tokens:
        assert token not in combined
    assert manifest[f"{PREFIX}_ml_signal_ready_for_runtime"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_route_authority"] is False
    assert manifest[f"{PREFIX}_ml_signal_ready_for_training"] is False
    for flag in BOUNDARY_FALSE_FLAGS:
        assert manifest[f"{PREFIX}_{flag}"] is False, flag


if __name__ == "__main__":
    test_mlrt106_review_gate_contract_and_manifest()
    test_mlrt106_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt106_maximum_optimized_ai_send_exposure_alignment_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
