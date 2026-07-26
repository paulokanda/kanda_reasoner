from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
REVIEW_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_FINAL_SAFETY_GATE_READINESS_V1.md"
IMPL_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_IMPLEMENTATION_V1.md"

FEATURE_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_result_review_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_v1"
PREFIX = "ml_advisory_phase8_read_only_advisory_panel_ui_implementation_result_review_gate_v1_"
REVIEWED_PREFIX = "ml_advisory_phase8_read_only_advisory_panel_ui_implementation_v1_"
FORBIDDEN_REVIEW_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_panel_activation_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'visible_panel_runtime_enabled', 'mlrt_113_created']
FORBIDDEN_IMPLEMENTATION_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'runtime_panel_activation_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'visible_panel_runtime_enabled', 'mlrt_113_created']


def test_phase8_panel_ui_implementation_review_gate_accepts_view_model_builder_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "accepted_panel_view_model_builder_only"] is True
    assert data[PREFIX + "accepted_renderer_neutral_only"] is True
    assert data[PREFIX + "accepted_phase7_surface_envelope_input_only"] is True
    assert data[PREFIX + "accepted_bounded_typed_sections_only"] is True
    assert data[PREFIX + "accepted_advisory_role_label"] is True
    assert data[PREFIX + "accepted_canonical_route_unchanged_label"] is True
    assert data[PREFIX + "accepted_no_route_authority_label"] is True
    assert data[PREFIX + "accepted_confidence_not_correctness_label"] is True
    assert data[PREFIX + "accepted_disabled_noop_path"] is True
    assert data[PREFIX + "accepted_invalid_surface_fail_open_path"] is True
    assert data[PREFIX + "accepted_non_training_feedback_slot"] is True
    assert data[PREFIX + "accepted_no_renderer"] is True
    assert data[PREFIX + "accepted_no_runtime_panel_activation"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Final Safety Gate v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_reviewed_phase8_panel_ui_implementation_still_blocks_runtime_and_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEWED_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEWED_PREFIX + "panel_view_model_builder_enabled"] is True
    assert data[REVIEWED_PREFIX + "renderer_neutral"] is True
    assert data[REVIEWED_PREFIX + "uses_phase7_surface_envelope_input_only"] is True
    assert data[REVIEWED_PREFIX + "requires_advisory_role_label"] is True
    assert data[REVIEWED_PREFIX + "requires_canonical_route_unchanged_label"] is True
    assert data[REVIEWED_PREFIX + "requires_no_route_authority_label"] is True
    assert data[REVIEWED_PREFIX + "requires_confidence_not_correctness_label"] is True
    assert data[REVIEWED_PREFIX + "route_authority_enabled"] is False
    for flag in FORBIDDEN_REVIEW_FLAGS:
        assert data[PREFIX + flag] is False, flag
    for flag in FORBIDDEN_IMPLEMENTATION_FLAGS:
        assert data[REVIEWED_PREFIX + flag] is False, flag


def test_review_docs_preserve_final_safety_gate_scope() -> None:
    review = REVIEW_DOC.read_text(encoding="utf-8")
    next_doc = NEXT_DOC.read_text(encoding="utf-8")
    impl_doc = IMPL_DOC.read_text(encoding="utf-8")
    assert "renderer-neutral bounded in-memory read-only advisory panel view-model builder" in review
    assert "does not activate a panel" in review
    assert "runtime panel activation" in review
    assert "route authority" in review
    assert "final safety gate" in next_doc
    assert "must not render a real UI" in next_doc
    assert "no runtime panel activation" in next_doc
    assert "does not render UI" in impl_doc


if __name__ == "__main__":
    test_phase8_panel_ui_implementation_review_gate_accepts_view_model_builder_only()
    test_reviewed_phase8_panel_ui_implementation_still_blocks_runtime_and_authority()
    test_review_docs_preserve_final_safety_gate_scope()
    print("VALIDATION OK: phase8 read-only advisory panel UI implementation result review gate")
