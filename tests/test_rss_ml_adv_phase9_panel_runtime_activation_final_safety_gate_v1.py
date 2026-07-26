from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
FINAL_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_FINAL_SAFETY_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_COMPLETION_HANDOFF_READINESS_V1.md"
REVIEW_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
IMPL_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_V1.md"

FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_final_safety_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_result_review_gate_v1"
IMPLEMENTATION_FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1"
PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_final_safety_gate_v1_"
REVIEW_PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_implementation_result_review_gate_v1_"
IMPL_PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_implementation_v1_"
FORBIDDEN_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'mounted_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created']


def test_phase9_runtime_activation_final_safety_gate_closes_dormant_envelope_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "reviewed_implementation_feature_id"] == IMPLEMENTATION_FEATURE_ID
    assert data[PREFIX + "final_safety_gate_only"] is True
    assert data[PREFIX + "phase9_runtime_activation_line_closed_as_dormant_envelope_only"] is True
    assert data[PREFIX + "accepted_runtime_activation_envelope_builder_only"] is True
    assert data[PREFIX + "accepted_guarded_in_memory_envelope_only"] is True
    assert data[PREFIX + "accepted_phase8_panel_view_model_input_only"] is True
    assert data[PREFIX + "accepted_feature_flag_required"] is True
    assert data[PREFIX + "accepted_feature_flag_default_off"] is True
    assert data[PREFIX + "accepted_disabled_noop_path"] is True
    assert data[PREFIX + "accepted_missing_view_model_fail_open_path"] is True
    assert data[PREFIX + "accepted_unsafe_view_model_blocked_fail_open_path"] is True
    assert data[PREFIX + "accepted_route_invariant"] is True
    assert data[PREFIX + "accepted_final_selection_invisible"] is True
    assert data[PREFIX + "accepted_renderer_neutral"] is True
    assert data[PREFIX + "accepted_non_training_feedback_slot"] is True
    assert data[PREFIX + "accepted_non_authoritative"] is True
    assert data[PREFIX + "accepted_no_router_call"] is True
    assert data[PREFIX + "accepted_no_advisor_call"] is True
    assert data[PREFIX + "accepted_no_adapter_execution"] is True
    assert data[PREFIX + "accepted_no_provider_call"] is True
    assert data[PREFIX + "accepted_no_persistence"] is True
    assert data[PREFIX + "accepted_no_prompt_library_read"] is True
    assert data[PREFIX + "accepted_no_freeze_memory_read"] is True
    assert data[PREFIX + "accepted_no_router_canon_read"] is True
    assert data[PREFIX + "accepted_no_renderer_activation"] is True
    assert data[PREFIX + "accepted_no_mounted_panel"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Completion Handoff v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_phase9_runtime_activation_final_safety_gate_preserves_previous_gates() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEW_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEW_PREFIX + "accepted_runtime_activation_envelope_builder_only"] is True
    assert data[REVIEW_PREFIX + "accepted_no_renderer_activation"] is True
    assert data[REVIEW_PREFIX + "accepted_no_mounted_panel"] is True
    assert data[REVIEW_PREFIX + "accepted_no_route_authority"] is True
    assert data[IMPL_PREFIX + "feature_id"] == IMPLEMENTATION_FEATURE_ID
    assert data[IMPL_PREFIX + "runtime_activation_envelope_builder_enabled"] is True
    assert data[IMPL_PREFIX + "feature_flag_required"] is True
    assert data[IMPL_PREFIX + "feature_flag_default_enabled"] is False
    assert data[IMPL_PREFIX + "runtime_panel_activation_enabled"] is False
    assert data[IMPL_PREFIX + "renderer_activation_enabled"] is False
    assert data[IMPL_PREFIX + "mounted_panel_enabled"] is False
    assert data[IMPL_PREFIX + "route_authority_enabled"] is False
    for flag in FORBIDDEN_FLAGS:
        assert data[PREFIX + flag] is False, flag


def test_phase9_runtime_activation_final_safety_docs_block_renderer_and_mount() -> None:
    final_text = FINAL_DOC.read_text(encoding="utf-8")
    next_text = NEXT_DOC.read_text(encoding="utf-8")
    review_text = REVIEW_DOC.read_text(encoding="utf-8")
    impl_text = IMPL_DOC.read_text(encoding="utf-8")
    assert "safe dormant read-only activation-envelope foundation" in final_text
    assert "does not activate a renderer" in final_text
    assert "does not mount a panel" in final_text
    assert "does not wire runtime telemetry surfaces" in final_text
    assert "does not grant route authority" in final_text
    assert "completion handoff only" in final_text
    assert "separate Phase 10 renderer/mount contract" in next_text
    assert "not a renderer" in review_text
    assert "not a runtime UI mutation" in impl_text


if __name__ == "__main__":
    test_phase9_runtime_activation_final_safety_gate_closes_dormant_envelope_only()
    test_phase9_runtime_activation_final_safety_gate_preserves_previous_gates()
    test_phase9_runtime_activation_final_safety_docs_block_renderer_and_mount()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation final safety gate")
