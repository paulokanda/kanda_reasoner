from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MLRT = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "mlrt_non_runtime_candidate_reliability"
DOC = MLRT / "MLRT_112_MAXIMUM_OPTIMIZED_FREEZE_HINT_CONSUMPTION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE.md"
README = MLRT / "README.md"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
PREV_DOC = MLRT / "MLRT_111_MAXIMUM_OPTIMIZED_FREEZE_HINT_CONSUMPTION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE.md"

FEATURE_ID = 'rss_mlrt112_maximum_optimized_freeze_hint_consumption_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1'
FEATURE_TITLE = 'Routing Signal Scorer MLRT-112 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1'
PREFIX = 'rss_mlrt112_maximum_optimized_freeze_hint_consumption_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate'
NEXT_TITLE = 'Routing Signal Scorer MLRT Consolidation Audit and Coverage Map v1'
CONTRACT_SUMMARY = 'MLRT-112 Maximum-Optimized Freeze-Hint Consumption Binding Controlled Offline ML Prompt-Selection Test Suite Result Review Gate v1, reviewed the MLRT-111 64-case maximum-optimized freeze-hint consumption binding in-memory offline prompt-selection suite result as good and meaningfully stronger but still validation-only evidence after MLRT-111 freeze; preserved that MLRT-111 passed 64/64 freeze-hint consumption binding cases across eight balanced audit families with 32/32 freeze-hint consumption binding pairs represented, two deliberately current-consumption-bound-versus-stale-or-reused-hint variants per pair, 32 governed offline-review-only cases, 32 containment/no-authority cases, 64/64 unique case IDs, 64/64 unique user requests, 0 forbidden selected routes, and cumulative controlled offline prompt-selection coverage of 1306/1306 cases across twenty-four real test suites; accepted the result only for continued offline testing, not as reliability, maturity, production-readiness, training, model-improvement, calibration, or runtime-route-authority evidence; preserved binding of KANDA_FREEZE_HINT consumption to the selected current feature title, feature ID, freeze ID, validation evidence, local freeze write output, used intake marker, planned next step, and delivery-metadata-only status, while demoting stale, unconsumed, already-consumed-for-another-feature, wrong-root, wrong-feature, mismatched-freeze-ID, missing-validation, preview-only, or project_freeze_ledger hint evidence without false blockers or unsafe route authority; preserved the standing rule that future real ML prompt-selection suites use the maximum optimized number of coherent non-duplicate cases; identified the next safe milestone as an MLRT consolidation audit and coverage map rather than another real MLRT expansion, so the system pauses new MLRT growth and audits organization, readability, non-duplication, maintainability, and coverage traceability without false blockers or unsafe route authority; preserved the final goal that ML must be tested for helping prompt selection in router prompt logic; no runtime routing, no route authority, no router prompt logic modification, no prompt loading, no provider calls, no embeddings, no persistence, no report persistence, no training-data intake, no dataset creation, no model training, no model calibration, no model improvement, no gold registry write, no registry mutation, no runtime Pilot, no Copilot behavior, critical boundary error budget zero.'
SANDBOX_MARKER = 'SANDBOX_RSS_MLRT112_MAXIMUM_OPTIMIZED_FREEZE_HINT_CONSUMPTION_BINDING_CONTROLLED_OFFLINE_ML_PROMPT_SELECTION_TEST_SUITE_RESULT_REVIEW_GATE_V1_VALIDATION_OK'

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


def test_mlrt112_review_gate_contract_and_manifest() -> None:
    assert DOC.exists(), DOC
    assert PREV_DOC.exists(), PREV_DOC
    doc = DOC.read_text(encoding="utf-8")
    prev_doc = PREV_DOC.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    manifest = _manifest()

    assert FEATURE_TITLE in doc
    assert FEATURE_ID in doc
    assert "MLRT-111" in doc
    assert "64/64" in doc
    assert "1306/1306" in doc
    assert "`24` real test suites" in doc
    assert "KANDA_FREEZE_HINT" in doc
    assert "used markers" in doc
    assert "local freeze write evidence" in doc
    assert "delivery-metadata-only status" in doc
    assert "already-consumed-for-another-feature" in doc
    assert "mismatched-freeze-ID" in doc
    assert "project_freeze_ledger" in doc
    assert "validation-only evidence" in doc
    assert NEXT_TITLE in doc
    assert "Consolidation Audit and Coverage Map" in doc

    assert "MLRT-111" in prev_doc
    assert "64/64 freeze-hint consumption binding cases" in prev_doc
    assert "1306/1306" in prev_doc
    assert FEATURE_ID in readme
    assert NEXT_TITLE in readme

    assert manifest[f"{PREFIX}_feature_id"] == FEATURE_ID
    assert manifest[f"{PREFIX}_feature_title"] == FEATURE_TITLE
    assert manifest[f"{PREFIX}_previous_suite_feature_id"] == "rss_mlrt111_maximum_optimized_freeze_hint_consumption_binding_controlled_offline_ml_prompt_selection_test_suite_v1"
    assert manifest[f"{PREFIX}_test_suite_real_cases_added"] == 0
    assert manifest[f"{PREFIX}_mlrt111_cases_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt111_cases_passed"] == 64
    assert manifest[f"{PREFIX}_mlrt111_freeze_hint_consumption_binding_pairs_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt111_audit_families_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt111_cases_per_family_reviewed"] == 8
    assert manifest[f"{PREFIX}_mlrt111_governed_offline_review_only_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt111_containment_no_authority_cases_reviewed"] == 32
    assert manifest[f"{PREFIX}_mlrt111_unique_case_ids_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt111_unique_user_requests_reviewed"] == 64
    assert manifest[f"{PREFIX}_mlrt111_forbidden_selected_routes_reviewed"] == 0
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_cases_passed"] == 1306
    assert manifest[f"{PREFIX}_cumulative_controlled_offline_test_stages_reviewed"] == 24
    assert manifest[f"{PREFIX}_kanda_freeze_hint_planned_next_step_reviewed"] is True
    assert manifest[f"{PREFIX}_validation_evidence_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_local_freeze_write_binding_reviewed"] is True
    assert manifest[f"{PREFIX}_already_consumed_for_another_feature_hint_demoted_reviewed"] is True
    assert manifest[f"{PREFIX}_mlrt_expansion_pause_recommended"] is True
    assert manifest[f"{PREFIX}_consolidation_audit_recommended"] is True
    assert manifest[f"{PREFIX}_identified_next_correction"] == "mlrt_consolidation_audit_and_coverage_map"
    assert manifest[f"{PREFIX}_validation_only_evidence"] is True
    assert manifest[f"{PREFIX}_accepted_for_continued_offline_testing_only"] is True
    assert manifest[f"{PREFIX}_critical_boundary_error_budget"] == 0


def test_mlrt112_boundary_and_source_surface_preservation() -> None:
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
    test_mlrt112_review_gate_contract_and_manifest()
    test_mlrt112_boundary_and_source_surface_preservation()
    print("VALIDATION OK: rss_mlrt112_maximum_optimized_freeze_hint_consumption_binding_controlled_offline_ml_prompt_selection_test_suite_result_review_gate_v1")
    print("CONTRACT_TEST_OK: " + CONTRACT_SUMMARY)
    print(SANDBOX_MARKER)
