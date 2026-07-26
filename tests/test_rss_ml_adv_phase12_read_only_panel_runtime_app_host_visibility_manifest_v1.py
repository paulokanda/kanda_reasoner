import json
from pathlib import Path


PREFIX = "ml_advisory_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract_v1_"


def test_phase12_runtime_app_host_visibility_contract_manifest_gates():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract_v1"
    assert manifest[PREFIX + "feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 12 Read-Only Advisory Panel Runtime App-Host Visibility Contract v1"
    assert manifest[PREFIX + "status"] == "contract_only_future_runtime_app_host_visibility_boundary"
    assert manifest[PREFIX + "source_completion_handoff_feature_id"] == "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_completion_handoff_v1"
    assert manifest[PREFIX + "source_host_binding_implementation_id"] == "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_implementation_v1"
    assert manifest[PREFIX + "phase11_host_binding_descriptor_input_required"] is True
    assert manifest[PREFIX + "feature_flag_required"] is True
    assert manifest[PREFIX + "feature_flag_default_enabled"] is False
    assert manifest[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert manifest[PREFIX + "missing_descriptor_behavior"] == "fail_open"
    assert manifest[PREFIX + "unsafe_descriptor_behavior"] == "blocked_fail_open"
    assert manifest[PREFIX + "runtime_visibility_input_bounded_required"] is True
    assert manifest[PREFIX + "runtime_visibility_output_bounded_required"] is True
    assert manifest[PREFIX + "removable_noop"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "actual_runtime_app_host_visibility_enabled"] is False
    assert manifest[PREFIX + "runtime_app_host_visibility_activation_enabled"] is False
    assert manifest[PREFIX + "mounted_runtime_panel_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wired"] is False
    assert manifest[PREFIX + "host_event_subscription_enabled"] is False
    assert manifest[PREFIX + "host_callback_registration_enabled"] is False
    assert manifest[PREFIX + "route_authority_enabled"] is False
    assert manifest[PREFIX + "router_calls_enabled"] is False
    assert manifest[PREFIX + "advisor_calls_enabled"] is False
    assert manifest[PREFIX + "provider_calls_enabled"] is False
    assert manifest[PREFIX + "persistence_enabled"] is False
    assert manifest[PREFIX + "runtime_copilot_decision_behavior_enabled"] is False
    assert manifest[PREFIX + "autonomous_ml_router_enabled"] is False
    assert manifest[PREFIX + "mlrt_113_created"] is False
    assert manifest[PREFIX + "visible_ml_integration_complete"] is False
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0


if __name__ == "__main__":
    test_phase12_runtime_app_host_visibility_contract_manifest_gates()
    print("VALIDATION OK: phase12 read-only advisory panel runtime app-host visibility contract manifest gates")
