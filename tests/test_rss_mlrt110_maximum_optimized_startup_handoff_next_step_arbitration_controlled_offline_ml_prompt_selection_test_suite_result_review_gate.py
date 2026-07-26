from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
DOC = MLRT / "MLRT_110_MAXIMUM_OPTIMIZED_STARTUP_HANDOFF_NEXT_STEP_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_109_MAXIMUM_OPTIMIZED_STARTUP_HANDOFF_NEXT_STEP_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt110_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-110 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt110_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
NEXT_TITLE = 'Routing Signal Scorer MLRT-111 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite v1'
CONTRACT_SUMMARY = 'MLRT-110 Maximum-Optimized Startup Handoff Next-Step Arbitration Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-109 64-case maximum-optimized startup handoff next-step arbitration in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-109 freeze; preserved that MLRT-109 passed 64/64 startup handoff next-step arbitration cases across eight balanced audit families with 32/32 startup handoff next-step arbitration pairs represented, two deliberately current-governed-next-step-versus-stale-or-conflicting-next-step variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 1242/1242 cases across twenty-three real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved arbitration of the current governed next step across first_prompts_to_ai.zip, paste_after_first_prompts_to_ai.md, 09_active_project_freeze_context.md, AI-send instructions, KANDA_FREEZE_HINT planned_next_step, review-gate next correction, latest current-feature freeze ID, and latest FREEZE_MEMORY_STATUS OK exposure, while demoting stale, truncated, wrong-root, wrong-feature, wrong-next-step, consumed-hint, mismatched-review-gate, or project_freeze_ledger handoff evidence without false blockers or unsafe route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next correction as a maximum-optimized freeze-hint consumption binding offline suite to test cases where KANDA_FREEZE_HINT intake records, used markers, planned next step, feature title, freeze ID, validation output, and local freeze write evidence disagree, so the system does not reuse stale or consumed delivery metadata as current authority without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT110_MAXIMUM_OPTIMIZED_STARTUP_HANDOFF_NEXT_STEP_ARBITRATION_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'

BOUNDARY_FALSE_FLAGS = ['route_authority_enabled', 'runtime_route_authority_enabled', 'router_prompt_logic_modified', 'prompt_loading_enabled', 'live_prompt_library_read_enabled', 'live_freeze_memory_read_enabled', 'live_router_canon_read_enabled', 'provider_calls_enabled', 'embeddings_enabled', 'vector_store_enabled', 'network_calls_enabled', 'subprocess_calls_enabled', 'batch_mode_enabled', 'result_persistence_enabled', 'report_persistence_enabled', 'persistent_case_files_created', 'persistent_dataset_created', 'persistent_labels_created', 'training_data_intake_enabled', 'training_data_use_enabled', 'dataset_creation_enabled', 'model_training_started', 'model_calibration_started', 'model_improvement_started', 'gold_registry_created', 'gold_records_created', 'gold_registry_write_enabled', 'registry_mutation_enabled', 'runtime_pilot_enabled', 'copilot_enabled', 'activation_key_enabled', 'field_test_mode_enabled']


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _only_allowed_python_sources() -> None:
    mlrt_py = [p for p in MLRT.rglob("*.py") if "__pycache__" not in p.parts]
    assert len(mlrt_py) == 1
    assert mlrt_py[0].name == "minimal_non_runtime_harness_stub.py"
    lab_root = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "lab_non_runtime_router_evaluation"
    lab_py = [p for p in lab_root.rglob("*.py") if "__pycache__" not in p.parts]
    assert len(lab_py) == 3


def test_mlrt110_review_gate_contract_and_manifest() -> None:
    assert DOC.exists(), DOC
    assert PREV_DOC.exists(), PREV_DOC
    doc = DOC.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    manifest = _manifest()

    assert FEATURE_TITLE in doc
    assert FEATURE_ID in doc
    assert "MLRT-109" in doc
    assert "64/64" in doc
    assert "1242/1242" in doc
    assert "`23` real test suites" in doc
    assert "first_prompts_to_ai.zip" in doc
    assert "paste_after_first_prompts_to_ai.md" in doc
    assert "09_active_project_freeze_context.md" in doc
    assert "KANDA_FREEZE_HINT" in doc
    assert "review-gate next correction" in doc
    assert "consumed-hint" in doc
    assert "project_freeze_ledger" in doc
    assert "validation-only evidence" in doc
    assert NEXT_TITLE in doc
    assert "Freeze-Hint Consumption Binding" in doc

    assert "MLRT-109" in prev_doc
    assert "64/64 startup handoff next-step arbitration cases" in prev_doc
    assert "1242/1242" in prev_doc
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == "rss_mlrt109_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt109_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt109_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt109_startup_handoff_next_step_arbitration_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt109_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt109_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt109_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt109_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt109_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt109_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt109_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 1242
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 23
    assert manifest[f"{PREFIX}_kanda_freeze_hint_planned_next_step_reviewed"] is True
    assert manifest[f"{PREFIX}_review_gate_next_correction_reviewed"] is True
    assert manifest[f"{PREFIX}_consumed_hint_handoff_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "maximum_optimized_freeze_hint_consumption_binding_offline_suite"
    assert manifest[f"{PREFIX}_validation_only_evidence"] is True
    assert manifest[f"{PREFIX}_accepted_for_continued_offline_testing_only"] is True
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0


def test_mlrt110_boundary_and_source_surface_preservation() -> None:
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
    test_mlrt110_review_gate_contract_and_manifest()
    test_mlrt110_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt110_maximum_optimized_startup_handoff_next_step_arbitration_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
