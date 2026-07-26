from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ML_DIR = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal"
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
DOC = ML_DIR / "ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_IMPLEMENTATION_RESULT_REVIEW_GATE_V1.md"
NEXT_DOC = ML_DIR / "ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_FINAL_SAFETY_GATE_READINESS_V1.md"
IMPLEMENTATION_DOC = ML_DIR / "ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_IMPLEMENTATION_V1.md"
CONTRACT_REVIEW_DOC = ML_DIR / "ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_CONTRACT_RESULT_REVIEW_GATE_V1.md"
PREFIX = "ml_advisory_phase11_read_only_advisory_panel_host_binding_implementation_result_review_gate_v1_"
IMPL_PREFIX = "ml_advisory_phase11_read_only_advisory_panel_host_binding_implementation_v1_"
FEATURE_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_implementation_result_review_gate_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_implementation_v1"
FALSE_FLAGS = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'actual_renderer_mount_enabled', 'mounted_panel_enabled', 'actual_host_binding_enabled', 'host_binding_activation_enabled', 'runtime_app_host_visibility_enabled', 'mounted_runtime_panel_enabled', 'host_event_subscription_enabled', 'host_callback_registration_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'autonomous_ml_router_enabled', 'visible_ml_integration_complete', 'actual_visible_panel_host_bound', 'mlrt_113_created']


def test_phase11_host_binding_implementation_result_review_gate_accepts_implementation_only() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "feature_id"] == FEATURE_ID
    assert data[PREFIX + "feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 11 Read-Only Advisory Panel Host Binding Implementation Result Review Gate v1"
    assert data[PREFIX + "reviewed_feature_id"] == REVIEWED_FEATURE_ID
    assert data[PREFIX + "implementation_result_review_gate_only"] is True
    assert data[PREFIX + "review_gate_only"] is True
    assert data[PREFIX + "accepted_implementation_only"] is True
    assert data[PREFIX + "accepted_good_safe_for_final_safety_gate_only"] is True
    assert data[PREFIX + "accepted_feature_flag_default_off"] is True
    assert data[PREFIX + "accepted_phase10_renderer_mount_descriptor_lineage_only"] is True
    assert data[PREFIX + "accepted_bounded_host_bound_sections"] is True
    assert data[PREFIX + "accepted_read_only_host_binding_descriptor"] is True
    assert data[PREFIX + "accepted_runtime_app_host_visibility_descriptor_possible"] is True
    assert data[PREFIX + "accepted_mounted_runtime_panel_descriptor_possible"] is True
    assert data[PREFIX + "accepted_no_actual_host_binding_side_effects"] is True
    assert data[PREFIX + "accepted_no_host_binding_activation"] is True
    assert data[PREFIX + "accepted_no_runtime_ui_mutation"] is True
    assert data[PREFIX + "accepted_no_runtime_telemetry_surface_wiring"] is True
    assert data[PREFIX + "accepted_no_host_event_subscription"] is True
    assert data[PREFIX + "accepted_no_host_callback_registration"] is True
    assert data[PREFIX + "accepted_no_route_influence"] is True
    assert data[PREFIX + "accepted_no_route_authority"] is True
    assert data[PREFIX + "read_only"] is True
    assert data[PREFIX + "in_memory_only"] is True
    assert data[PREFIX + "bounded"] is True
    assert data[PREFIX + "removable_noop"] is True
    assert data[PREFIX + "route_invariant"] is True
    assert data[PREFIX + "final_selection_invisible"] is True
    assert data[PREFIX + "non_authoritative"] is True
    assert data[PREFIX + "feature_flag_default_enabled"] is False
    assert data[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert data[PREFIX + "missing_descriptor_behavior"] == "fail_open"
    assert data[PREFIX + "unsafe_descriptor_behavior"] == "blocked_fail_open"
    assert data[PREFIX + "new_real_prompt_selection_cases_added"] == 0
    assert data[PREFIX + "critical_boundary_error_budget"] == 0


def test_phase11_host_binding_implementation_result_review_gate_preserves_implementation_state() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[IMPL_PREFIX + "feature_id"] == REVIEWED_FEATURE_ID
    assert data[IMPL_PREFIX + "implementation_enabled"] is True
    assert data[IMPL_PREFIX + "feature_flag_default_enabled"] is False
    assert data[IMPL_PREFIX + "phase10_renderer_mount_descriptor_input_required"] is True
    assert data[IMPL_PREFIX + "read_only_host_binding_descriptor_ready_possible"] is True
    assert data[IMPL_PREFIX + "runtime_app_host_visibility_descriptor_ready_possible"] is True
    assert data[IMPL_PREFIX + "mounted_runtime_panel_descriptor_ready_possible"] is True
    assert data[IMPL_PREFIX + "actual_host_binding_enabled"] is False
    assert data[IMPL_PREFIX + "host_binding_activation_enabled"] is False
    assert data[IMPL_PREFIX + "runtime_app_host_visibility_enabled"] is False
    assert data[IMPL_PREFIX + "mounted_runtime_panel_enabled"] is False
    assert data[IMPL_PREFIX + "runtime_ui_mutation_enabled"] is False
    assert data[IMPL_PREFIX + "runtime_telemetry_surface_wired"] is False
    assert data[IMPL_PREFIX + "route_influence_enabled"] is False
    assert data[IMPL_PREFIX + "route_authority_enabled"] is False
    assert data[IMPL_PREFIX + "implementation_result_review_gate_completed"] is True
    assert data[IMPL_PREFIX + "implementation_result_review_gate_feature_id"] == FEATURE_ID
    assert data[IMPL_PREFIX + "final_safety_gate_required_next"] is True
    assert data[IMPL_PREFIX + "visible_ml_integration_complete"] is False
    for flag in FALSE_FLAGS:
        assert data[PREFIX + flag] is False, flag


def test_phase11_host_binding_implementation_result_review_gate_docs_define_final_safety_gate() -> None:
    doc_text = DOC.read_text(encoding="utf-8")
    next_text = NEXT_DOC.read_text(encoding="utf-8")
    implementation_text = IMPLEMENTATION_DOC.read_text(encoding="utf-8")
    contract_review_text = CONTRACT_REVIEW_DOC.read_text(encoding="utf-8")
    assert "accepts the Phase 11 read-only advisory panel host-binding" in doc_text
    assert "not an actual host-binding side-effect approval" in doc_text
    assert "not accepted as complete visible ML integration" in doc_text
    assert "Phase 11 Read-Only Advisory Panel Host Binding Final Safety Gate v1" in doc_text
    assert "The final safety gate must verify" in next_text
    assert "actual host-binding side effects remain disabled" in next_text
    assert "runtime UI mutation remains disabled" in next_text
    assert "host-binding descriptor" in implementation_text
    assert "Phase 11 Read-Only Advisory Panel Host Binding Implementation v1" in contract_review_text


if __name__ == "__main__":
    test_phase11_host_binding_implementation_result_review_gate_accepts_implementation_only()
    test_phase11_host_binding_implementation_result_review_gate_preserves_implementation_state()
    test_phase11_host_binding_implementation_result_review_gate_docs_define_final_safety_gate()
    print("VALIDATION OK: phase11 read-only advisory panel host binding implementation result review gate")
