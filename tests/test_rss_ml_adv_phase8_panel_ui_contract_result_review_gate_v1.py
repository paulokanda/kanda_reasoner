from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
REVIEW_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_CONTRACT_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_IMPLEMENTATION_READINESS_V1.md"
CONTRACT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_CONTRACT_V1.md"

FEATURE_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_v1"
PREFIX = "ml_advisory_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1_"
REVIEWED_PREFIX = "ml_advisory_phase8_read_only_advisory_panel_ui_contract_v1_"
FORBIDDEN_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_advisory_panel_enabled', 'runtime_panel_activation_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'visible_panel_implementation_enabled', 'mlrt_113_created']


def test_phase8_panel_ui_contract_review_gate_accepts_contract_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "accepted_ui_contract_only"] is True
    assert data[PREFIX + "accepted_visible_panel_track_contract_only"] is True
    assert data[PREFIX + "accepted_allowed_panel_sections_bounded"] is True
    assert data[PREFIX + "accepted_required_authority_labels"] is True
    assert data[PREFIX + "accepted_surface_envelope_or_guarded_display_payload_input_only"] is True
    assert data[PREFIX + "accepted_non_training_feedback_slot"] is True
    assert data[PREFIX + "accepted_no_runtime_panel_activation"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "accepted_no_router_call"] is True
    assert data[PREFIX + "accepted_no_advisor_call"] is True
    assert data[PREFIX + "accepted_no_adapter_execution"] is True
    assert data[PREFIX + "accepted_no_provider_call"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Implementation v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_reviewed_phase8_contract_still_blocks_runtime_panel_and_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEWED_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEWED_PREFIX + "panel_track_started"] is True
    assert data[REVIEWED_PREFIX + "contract_only"] is True
    assert data[REVIEWED_PREFIX + "requires_surface_envelope_input"] is True
    assert data[REVIEWED_PREFIX + "requires_advisory_role_label"] is True
    assert data[REVIEWED_PREFIX + "requires_canonical_route_unchanged_label"] is True
    assert data[REVIEWED_PREFIX + "runtime_panel_activation_enabled"] is False
    assert data[REVIEWED_PREFIX + "runtime_ui_mutation_enabled"] is False
    assert data[REVIEWED_PREFIX + "runtime_telemetry_surface_wired"] is False
    assert data[REVIEWED_PREFIX + "route_authority_enabled"] is False
    for flag in FORBIDDEN_FLAGS:
        assert data[REVIEWED_PREFIX + flag] is False, flag
        assert data[PREFIX + flag] is False, flag


def test_review_docs_preserve_implementation_readiness_scope() -> None:
    review = REVIEW_DOC.read_text(encoding="utf-8")
    next_doc = NEXT_DOC.read_text(encoding="utf-8")
    contract_doc = CONTRACT_DOC.read_text(encoding="utf-8")
    assert "contract only" in review
    assert "does not activate a panel" in review
    assert "not accept runtime panel activation" in review or "runtime panel activation" in review
    assert "route authority" in review
    assert "renderer-neutral panel view-model builder only" in next_doc
    assert "runtime UI mutation" in next_doc
    assert "Allowed future panel sections" in contract_doc
    assert "Forbidden panel capabilities" in contract_doc


if __name__ == "__main__":
    test_phase8_panel_ui_contract_review_gate_accepts_contract_only()
    test_reviewed_phase8_contract_still_blocks_runtime_panel_and_authority()
    test_review_docs_preserve_implementation_readiness_scope()
    print("VALIDATION OK: phase8 read-only advisory panel UI contract result review gate")
