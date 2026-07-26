from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
REVIEW_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_CONTRACT_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_READINESS_V1.md"
CONTRACT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_CONTRACT_V1.md"

FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_result_review_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_v1"
PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_contract_result_review_gate_v1_"
REVIEWED_PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_contract_v1_"
FORBIDDEN_REVIEW_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_panel_activation_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'renderer_activation_enabled', 'mounted_panel_enabled', 'visible_panel_runtime_enabled', 'mlrt_113_created']
FORBIDDEN_CONTRACT_FLAGS = ['adapter_execution_enabled', 'provider_calls_enabled', 'persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_telemetry_surface_wired', 'runtime_ui_mutation_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'runtime_copilot_decision_behavior_enabled', 'renderer_activation_enabled', 'mounted_panel_enabled', 'mlrt_113_created']


def test_phase9_runtime_activation_contract_review_gate_accepts_contract_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "accepted_runtime_activation_contract_only"] is True
    assert data[PREFIX + "accepted_future_visible_panel_path_only"] is True
    assert data[PREFIX + "accepted_phase8_panel_view_model_input_only"] is True
    assert data[PREFIX + "accepted_explicit_feature_flag"] is True
    assert data[PREFIX + "accepted_default_off_behavior"] is True
    assert data[PREFIX + "accepted_disable_noop_control"] is True
    assert data[PREFIX + "accepted_fail_open_on_missing_or_unsafe_view_model"] is True
    assert data[PREFIX + "accepted_route_invariant_runtime_mount"] is True
    assert data[PREFIX + "accepted_final_selection_invisible_runtime_mount"] is True
    assert data[PREFIX + "accepted_renderer_adapter_separate_future_contract"] is True
    assert data[PREFIX + "accepted_non_training_feedback_slot"] is True
    assert data[PREFIX + "accepted_no_actual_runtime_panel_activation"] is True
    assert data[PREFIX + "accepted_no_renderer_activation"] is True
    assert data[PREFIX + "accepted_no_mounted_panel"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Implementation v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_reviewed_phase9_contract_still_blocks_runtime_and_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEWED_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEWED_PREFIX + "contract_only"] is True
    assert data[REVIEWED_PREFIX + "runtime_visible_panel_track_started"] is True
    assert data[REVIEWED_PREFIX + "requires_phase8_panel_view_model_input"] is True
    assert data[REVIEWED_PREFIX + "requires_explicit_feature_flag"] is True
    assert data[REVIEWED_PREFIX + "feature_flag_default_enabled"] is False
    assert data[REVIEWED_PREFIX + "requires_disable_noop_control"] is True
    assert data[REVIEWED_PREFIX + "requires_fail_open_on_missing_view_model"] is True
    assert data[REVIEWED_PREFIX + "requires_route_invariant_runtime_mount"] is True
    assert data[REVIEWED_PREFIX + "requires_final_selection_invisible_runtime_mount"] is True
    assert data[REVIEWED_PREFIX + "renderer_adapter_separate_future_contract_required"] is True
    assert data[REVIEWED_PREFIX + "route_authority_enabled"] is False
    for flag in FORBIDDEN_REVIEW_FLAGS:
        assert data[PREFIX + flag] is False, flag
    for flag in FORBIDDEN_CONTRACT_FLAGS:
        assert data[REVIEWED_PREFIX + flag] is False, flag


def test_review_docs_preserve_implementation_readiness_scope() -> None:
    review = REVIEW_DOC.read_text(encoding="utf-8")
    next_doc = NEXT_DOC.read_text(encoding="utf-8")
    contract_doc = CONTRACT_DOC.read_text(encoding="utf-8")
    assert "contract only" in review
    assert "does not activate runtime UI" in review
    assert "does not activate a renderer" in review
    assert "does not mount a panel" in review
    assert "route authority" in review
    assert "feature flag required" in next_doc
    assert "default-off behavior required" in next_doc
    assert "no route influence" in next_doc
    assert "no route authority" in next_doc
    assert "contract only" in contract_doc


if __name__ == "__main__":
    test_phase9_runtime_activation_contract_review_gate_accepts_contract_only()
    test_reviewed_phase9_contract_still_blocks_runtime_and_authority()
    test_review_docs_preserve_implementation_readiness_scope()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation contract result review gate")
