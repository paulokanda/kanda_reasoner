from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ML_DIR = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ML_DIR / "ML_ADVISORY_PHASE12_READ_ONLY_ADVISORY_PANEL_RUNTIME_APP_HOST_VISIBILITY_COMPLETION_HANDOFF_V1.md"
NEXT_DOC = ML_DIR / "ML_ADVISORY_PHASE13_READ_ONLY_ADVISORY_PANEL_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT_READINESS_V1.md"
FINAL_DOC = ML_DIR / "ML_ADVISORY_PHASE12_READ_ONLY_ADVISORY_PANEL_RUNTIME_APP_HOST_VISIBILITY_FINAL_SAFETY_GATE_V1.md"
PREFIX = "ml_advisory_phase12_read_only_advisory_panel_runtime_app_host_visibility_completion_handoff_v1_"
FINAL_PREFIX = "ml_advisory_phase12_read_only_advisory_panel_runtime_app_host_visibility_final_safety_gate_v1_"
IMPL_PREFIX = "ml_advisory_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1_"
REQUIRED_FALSE = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'actual_renderer_mount_enabled', 'mounted_panel_enabled', 'actual_host_binding_enabled', 'host_binding_activation_enabled', 'actual_runtime_app_host_visibility_enabled', 'runtime_app_host_visibility_enabled', 'runtime_app_host_visibility_activation_enabled', 'visibility_activation_enabled', 'mounted_runtime_panel_enabled', 'runtime_panel_mount_side_effects_enabled', 'host_event_subscription_enabled', 'host_callback_registration_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'autonomous_ml_router_enabled', 'visible_ml_integration_complete', 'actual_visible_panel_host_bound', 'mlrt_113_created']


def test_phase12_runtime_app_host_visibility_completion_handoff_closes_descriptor_line_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_completion_handoff_v1"
    assert data[PREFIX + "feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Completion Handoff v1"
    assert data[PREFIX + "completion_handoff_only"] is True
    assert data[PREFIX + "phase12_runtime_app_host_visibility_descriptor_line_closed"] is True
    assert data[PREFIX + "safe_for_phase13_passive_visibility_activation_contract_only"] is True
    assert data[PREFIX + "runtime_app_host_visibility_descriptor_line_complete"] is True
    assert data[PREFIX + "runtime_app_host_visibility_descriptor_in_memory_only"] is True
    assert data[PREFIX + "runtime_app_host_visibility_descriptor_read_only"] is True
    assert data[PREFIX + "runtime_app_host_visibility_descriptor_removable_noop"] is True
    assert data[PREFIX + "phase11_host_binding_descriptor_lineage_only"] is True
    assert data[PREFIX + "bounded_runtime_visible_sections_only"] is True
    assert data[PREFIX + "feature_flag_required"] is True
    assert data[PREFIX + "feature_flag_default_enabled"] is False
    assert data[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert data[PREFIX + "missing_descriptor_behavior"] == "fail_open"
    assert data[PREFIX + "unsafe_descriptor_behavior"] == "blocked_fail_open"
    assert data[PREFIX + "visible_ml_integration_complete"] is False
    assert data[PREFIX + "actual_runtime_app_host_visibility_enabled"] is False
    assert data[PREFIX + "visibility_activation_enabled"] is False
    assert data[PREFIX + "mounted_runtime_panel_enabled"] is False
    assert data[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert data[PREFIX + "runtime_telemetry_surface_wired"] is False
    assert data[PREFIX + "route_influence_enabled"] is False
    assert data[PREFIX + "route_authority_enabled"] is False
    assert data[PREFIX + "critical_boundary_error_budget"] == 0
    assert data[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract v1"
    for flag in REQUIRED_FALSE:
        assert data[PREFIX + flag] is False, flag


def test_phase12_runtime_app_host_visibility_completion_handoff_marks_prior_line_without_authority() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[FINAL_PREFIX + "phase12_runtime_app_host_visibility_completion_handoff_completed"] is True
    assert data[FINAL_PREFIX + "phase12_runtime_app_host_visibility_completion_handoff_feature_id"] == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_completion_handoff_v1"
    assert data[FINAL_PREFIX + "phase12_runtime_app_host_visibility_descriptor_line_closed"] is True
    assert data[FINAL_PREFIX + "visible_ml_integration_complete"] is False
    assert data[FINAL_PREFIX + "passive_visibility_activation_contract_required_next"] is True
    assert data[FINAL_PREFIX + "actual_runtime_app_host_visibility_enabled"] is False
    assert data[FINAL_PREFIX + "visibility_activation_enabled"] is False
    assert data[FINAL_PREFIX + "mounted_runtime_panel_enabled"] is False
    assert data[FINAL_PREFIX + "runtime_ui_mutation_enabled"] is False
    assert data[FINAL_PREFIX + "runtime_telemetry_surface_wired"] is False
    assert data[FINAL_PREFIX + "route_influence_enabled"] is False
    assert data[FINAL_PREFIX + "route_authority_enabled"] is False
    assert data[IMPL_PREFIX + "phase12_runtime_app_host_visibility_completion_handoff_completed"] is True
    assert data[IMPL_PREFIX + "visible_ml_integration_complete"] is False
    assert data[IMPL_PREFIX + "route_authority_enabled"] is False


def test_phase12_runtime_app_host_visibility_completion_handoff_docs_define_next_contract_only() -> None:
    doc_text = DOC.read_text(encoding="utf-8")
    next_text = NEXT_DOC.read_text(encoding="utf-8")
    final_text = FINAL_DOC.read_text(encoding="utf-8")
    assert "closes the Phase 12 runtime app-host visibility descriptor line" in doc_text
    assert "not actual runtime app-host visibility side effects" in doc_text
    assert "No route authority" in doc_text
    assert "No visible ML integration completion claim" in doc_text
    assert "Phase 13 Read-Only Advisory Panel Passive Visibility Activation Contract" in doc_text
    assert "passive app-host visibility activation" in next_text
    assert "No route influence or route authority" in next_text
    assert "safe for a separate completion handoff" in final_text


if __name__ == "__main__":
    test_phase12_runtime_app_host_visibility_completion_handoff_closes_descriptor_line_only()
    test_phase12_runtime_app_host_visibility_completion_handoff_marks_prior_line_without_authority()
    test_phase12_runtime_app_host_visibility_completion_handoff_docs_define_next_contract_only()
    print("VALIDATION OK: phase12 read-only advisory panel runtime app-host visibility completion handoff")
