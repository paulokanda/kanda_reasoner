from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
REVIEW_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_FINAL_SAFETY_GATE_READINESS_V1.md"
IMPL_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_V1.md"
PREV_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_CONTRACT_RESULT_REVIEW_GATE_V1.md"

FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_result_review_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1"
PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_implementation_result_review_gate_v1_"
REVIEWED_PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_implementation_v1_"
FORBIDDEN_REVIEW_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'mounted_panel_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'mlrt_113_created']
FORBIDDEN_IMPLEMENTATION_FLAGS = [
    "real_ml_enabled", "adapter_execution_enabled", "candidate_execution_enabled",
    "provider_calls_enabled", "network_calls_enabled", "api_keys_enabled",
    "embeddings_enabled", "vector_store_enabled", "persistence_enabled",
    "report_persistence_enabled", "prompt_loading_enabled",
    "prompt_registry_mutation_enabled", "prompt_library_read_enabled",
    "freeze_memory_read_enabled", "freeze_memory_write_enabled",
    "router_canon_read_enabled", "runtime_shadow_mode_enabled",
    "actual_runtime_panel_activation_enabled", "runtime_panel_activation_enabled",
    "renderer_activation_enabled", "mounted_panel_enabled",
    "runtime_ui_mutation_enabled", "runtime_telemetry_surface_wired",
    "router_prompt_logic_modified", "router_final_selection_modified",
    "route_influence_enabled", "route_authority_enabled", "router_calls_enabled",
    "advisor_calls_enabled", "advisory_rankings_enabled", "prompt_rankings_enabled",
    "free_text_route_advice_enabled", "free_text_explanations_enabled",
    "training_enabled", "calibration_enabled", "model_improvement_enabled",
    "runtime_pilot_behavior_enabled", "runtime_copilot_decision_behavior_enabled",
    "mlrt_113_created",
]


def test_phase9_runtime_activation_implementation_review_gate_accepts_envelope_builder_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
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
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 9 Read-Only Advisory Panel Runtime Activation Final Safety Gate v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_reviewed_phase9_runtime_activation_implementation_still_blocks_runtime_ui_and_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[REVIEWED_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEWED_PREFIX + "runtime_activation_envelope_builder_enabled"] is True
    assert data[REVIEWED_PREFIX + "phase8_panel_view_model_input_only"] is True
    assert data[REVIEWED_PREFIX + "feature_flag_required"] is True
    assert data[REVIEWED_PREFIX + "feature_flag_default_enabled"] is False
    assert data[REVIEWED_PREFIX + "default_off_behavior"] == "disabled_noop"
    assert data[REVIEWED_PREFIX + "missing_view_model_behavior"] == "fail_open"
    assert data[REVIEWED_PREFIX + "unsafe_view_model_behavior"] == "blocked_fail_open"
    assert data[REVIEWED_PREFIX + "renderer_neutral"] is True
    assert data[REVIEWED_PREFIX + "route_authority_enabled"] is False
    for flag in FORBIDDEN_REVIEW_FLAGS:
        assert data[PREFIX + flag] is False, flag
    for flag in FORBIDDEN_IMPLEMENTATION_FLAGS:
        assert data[REVIEWED_PREFIX + flag] is False, flag


def test_review_docs_preserve_phase9_final_safety_gate_scope() -> None:
    review = REVIEW_DOC.read_text(encoding="utf-8")
    next_doc = NEXT_DOC.read_text(encoding="utf-8")
    impl_doc = IMPL_DOC.read_text(encoding="utf-8")
    assert PREV_DOC.exists()
    assert "guarded in-memory activation envelope builder" in review
    assert "not a renderer" in review
    assert "no renderer activation" in review
    assert "no mounted panel" in review
    assert "no runtime telemetry surface wiring" in review
    assert "no route authority" in review
    assert "final safety gate" in next_doc
    assert "must not render a real UI" in next_doc
    assert "not a runtime UI mutation" in impl_doc


if __name__ == "__main__":
    test_phase9_runtime_activation_implementation_review_gate_accepts_envelope_builder_only()
    test_reviewed_phase9_runtime_activation_implementation_still_blocks_runtime_ui_and_authority()
    test_review_docs_preserve_phase9_final_safety_gate_scope()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation implementation result review gate")
