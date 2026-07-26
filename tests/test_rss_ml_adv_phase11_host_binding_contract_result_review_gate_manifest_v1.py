from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "box_manifest.json"
README = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "README.md"
PREFIX = "ml_advisory_phase11_read_only_advisory_panel_host_binding_contract_result_review_gate_v1_"
REQUIRED_FALSE = ['real_ml_enabled', 'adapter_execution_enabled', 'candidate_execution_enabled', 'provider_calls_enabled', 'network_calls_enabled', 'api_keys_enabled', 'embeddings_enabled', 'vector_store_enabled', 'persistence_enabled', 'report_persistence_enabled', 'prompt_loading_enabled', 'prompt_registry_mutation_enabled', 'prompt_library_read_enabled', 'freeze_memory_read_enabled', 'freeze_memory_write_enabled', 'router_canon_read_enabled', 'runtime_shadow_mode_enabled', 'actual_runtime_panel_activation_enabled', 'runtime_panel_activation_enabled', 'renderer_activation_enabled', 'actual_renderer_mount_enabled', 'mounted_panel_enabled', 'actual_host_binding_enabled', 'host_binding_activation_enabled', 'runtime_app_host_visibility_enabled', 'mounted_runtime_panel_enabled', 'host_event_subscription_enabled', 'host_callback_registration_enabled', 'runtime_ui_mutation_enabled', 'runtime_telemetry_surface_wired', 'runtime_telemetry_surface_wiring_enabled', 'router_prompt_logic_modified', 'router_final_selection_modified', 'final_selection_hook_enabled', 'prompt_selection_hook_enabled', 'route_influence_enabled', 'route_authority_enabled', 'router_calls_enabled', 'advisor_calls_enabled', 'advisory_rankings_enabled', 'prompt_rankings_enabled', 'route_override_button_enabled', 'use_ml_route_button_enabled', 'best_route_claim_enabled', 'free_text_route_advice_enabled', 'free_text_explanations_enabled', 'training_enabled', 'calibration_enabled', 'model_improvement_enabled', 'runtime_pilot_behavior_enabled', 'runtime_copilot_decision_behavior_enabled', 'autonomous_ml_router_enabled', 'visible_ml_integration_complete', 'actual_visible_panel_host_bound', 'mlrt_113_created']


def test_phase11_host_binding_contract_result_review_gate_manifest_gates() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data[PREFIX + "status"] == "review_gate_only_accepts_phase11_host_binding_contract_for_implementation_no_actual_host_binding_no_ui_mutation_no_route_authority"
    assert data[PREFIX + "contract_result_review_gate_only"] is True
    assert data[PREFIX + "review_gate_only"] is True
    assert data[PREFIX + "read_only"] is True
    assert data[PREFIX + "telemetry_only"] is True
    assert data[PREFIX + "in_memory_only"] is True
    assert data[PREFIX + "bounded"] is True
    assert data[PREFIX + "fail_open"] is True
    assert data[PREFIX + "removable_noop"] is True
    assert data[PREFIX + "route_invariant"] is True
    assert data[PREFIX + "final_selection_invisible"] is True
    assert data[PREFIX + "non_authoritative"] is True
    assert data[PREFIX + "feature_flag_required"] is True
    assert data[PREFIX + "feature_flag_default_enabled"] is False
    assert data[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert data[PREFIX + "missing_descriptor_behavior"] == "fail_open"
    assert data[PREFIX + "unsafe_descriptor_behavior"] == "blocked_fail_open"
    assert data[PREFIX + "actual_host_binding_enabled"] is False
    assert data[PREFIX + "runtime_app_host_visibility_enabled"] is False
    assert data[PREFIX + "visible_ml_integration_complete"] is False
    for flag in REQUIRED_FALSE:
        assert data[PREFIX + flag] is False, flag


def test_readme_records_phase11_host_binding_contract_result_review_gate() -> None:
    text = README.read_text(encoding="utf-8")
    assert "Phase 11 read-only advisory panel host binding contract result review gate" in text
    assert "not an actual host binding implementation" in text
    assert "does not bind into the app host" in text
    assert "Implementation v1" in text


if __name__ == "__main__":
    test_phase11_host_binding_contract_result_review_gate_manifest_gates()
    test_readme_records_phase11_host_binding_contract_result_review_gate()
    print("VALIDATION OK: phase11 read-only advisory panel host binding contract result review gate manifest gates")
