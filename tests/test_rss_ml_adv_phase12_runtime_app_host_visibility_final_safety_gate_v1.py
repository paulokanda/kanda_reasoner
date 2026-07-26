from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE12_READ_ONLY_ADVISORY_PANEL_RUNTIME_APP_HOST_VISIBILITY_FINAL_SAFETY_GATE_V1.md"
NEXT_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE12_READ_ONLY_ADVISORY_PANEL_RUNTIME_APP_HOST_VISIBILITY_COMPLETION_HANDOFF_READINESS_V1.md"
IMPLEMENTATION_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE12_READ_ONLY_ADVISORY_PANEL_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_V1.md"
REVIEW_GATE_DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE12_READ_ONLY_ADVISORY_PANEL_RUNTIME_APP_HOST_VISIBILITY_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"

FEATURE_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_final_safety_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_result_review_gate_v1"
PREFIX = "ml_advisory_phase12_read_only_advisory_panel_runtime_app_host_visibility_final_safety_gate_v1_"
IMPL_PREFIX = "ml_advisory_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1_"
REVIEW_PREFIX = "ml_advisory_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_result_review_gate_v1_"
FALSE_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'actual_renderer_mount_enabled', 'mounted_panel_enabled', 'actual_host_binding_enabled', 'host_binding_activation_enabled', 'actual_runtime_app_host_visibility_enabled', 'runtime_app_host_visibility_enabled', 'runtime_app_host_visibility_activation_enabled', 'visibility_activation_enabled', 'mounted_runtime_panel_enabled', 'runtime_panel_mount_side_effects_enabled', 'host_event_subscription_enabled', 'host_callback_registration_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'autonomous_ml_router_enabled', 'visible_ml_integration_complete', 'actual_visible_panel_host_bound', 'mlrt_113_created']


def test_phase12_runtime_app_host_visibility_final_safety_gate_accepts_only_safe_line_for_handoff() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "final_safety_gate_only"] is True
    assert data[PREFIX + "accepted_good_safe_for_completion_handoff_only"] is True
    assert data[PREFIX + "completion_handoff_required_next"] is True
    assert data[PREFIX + "accepted_feature_flag_default_off"] is True
    assert data[PREFIX + "accepted_disabled_noop_path"] is True
    assert data[PREFIX + "accepted_missing_descriptor_fail_open_path"] is True
    assert data[PREFIX + "accepted_unsafe_descriptor_block_path"] is True
    assert data[PREFIX + "accepted_phase11_host_binding_descriptor_lineage_only"] is True
    assert data[PREFIX + "accepted_bounded_runtime_visible_sections"] is True
    assert data[PREFIX + "accepted_read_only_runtime_app_host_visibility_descriptor"] is True
    assert data[PREFIX + "accepted_visible_read_only_panel_descriptor_possible"] is True
    assert data[PREFIX + "accepted_mounted_runtime_panel_descriptor_possible"] is True
    assert data[PREFIX + "accepted_removable_noop_visibility_descriptor"] is True
    assert data[PREFIX + "accepted_route_invariant"] is True
    assert data[PREFIX + "accepted_final_selection_invisible"] is True
    assert data[PREFIX + "accepted_non_training_feedback_slot"] is True
    assert data[PREFIX + "accepted_non_authoritative"] is True
    assert data[PREFIX + "accepted_no_actual_runtime_app_host_visibility_side_effects"] is True
    assert data[PREFIX + "accepted_no_visibility_activation"] is True
    assert data[PREFIX + "accepted_no_mounted_runtime_panel_side_effects"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_host_event_subscription"] is True
    assert data[PREFIX + "accepted_no_host_callback_registration"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Completion Handoff v1"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_phase12_runtime_app_host_visibility_final_safety_gate_updates_prior_state_without_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[IMPL_PREFIX + "feature_id"] == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1"
    assert data[IMPL_PREFIX + "final_safety_gate_completed"] is True
    assert data[IMPL_PREFIX + "final_safety_gate_feature_id"] == FEATURE_ID
    assert data[IMPL_PREFIX + "completion_handoff_required_next"] is True
    assert data[IMPL_PREFIX + "visible_ml_integration_complete"] is False
    assert data[IMPL_PREFIX + "actual_runtime_app_host_visibility_enabled"] is False
    assert data[IMPL_PREFIX + "runtime_app_host_visibility_enabled"] is False
    assert data[IMPL_PREFIX + "visibility_activation_enabled"] is False
    assert data[IMPL_PREFIX + "mounted_runtime_panel_enabled"] is False
    assert data[IMPL_PREFIX + "runtime_panel_mount_side_effects_enabled"] is False
    assert data[IMPL_PREFIX + "runtime_ui_mutation_enabled"] is False
    assert data[REVIEW_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[REVIEW_PREFIX + "final_safety_gate_completed"] is True
    assert data[REVIEW_PREFIX + "final_safety_gate_feature_id"] == FEATURE_ID
    assert data[REVIEW_PREFIX + "completion_handoff_required_next"] is True
    assert data[REVIEW_PREFIX + "visible_ml_integration_complete"] is False
    for flag in FALSE_FLAGS:
        assert data[PREFIX + flag] is False, flag


def test_phase12_runtime_app_host_visibility_final_safety_gate_docs_define_completion_handoff_only() -> None:
    doc_text = DOC.read_text(encoding="utf-8")
    next_text = NEXT_DOC.read_text(encoding="utf-8")
    implementation_text = IMPLEMENTATION_DOC.read_text(encoding="utf-8")
    review_text = REVIEW_GATE_DOC.read_text(encoding="utf-8")
    assert "safe for a separate completion handoff" in doc_text
    assert "not actual runtime app-host visibility side effects" in doc_text
    assert "not route authority" in doc_text
    assert "Completion Handoff v1" in doc_text
    assert "completion handoff must verify" in next_text.lower()
    assert "Runtime UI mutation remains disabled" in next_text
    assert "runtime app-host visibility descriptor" in implementation_text
    assert "Good and safe only for a later governed final safety gate" in review_text


if __name__ == "__main__":
    test_phase12_runtime_app_host_visibility_final_safety_gate_accepts_only_safe_line_for_handoff()
    test_phase12_runtime_app_host_visibility_final_safety_gate_updates_prior_state_without_authority()
    test_phase12_runtime_app_host_visibility_final_safety_gate_docs_define_completion_handoff_only()
    print("VALIDATION OK: phase12 read-only advisory panel runtime app-host visibility final safety gate")
