import json
from pathlib import Path

PREFIX = "ml_advisory_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_v1_"
MANIFEST = Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json")


def test_phase13_passive_visibility_activation_implementation_manifest_gates():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_v1"
    assert manifest[PREFIX + "feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation v1"
    assert manifest[PREFIX + "source_contract_result_review_gate_feature_id"] == "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_contract_result_review_gate_v1"
    assert manifest[PREFIX + "source_runtime_app_host_visibility_implementation_feature_id"] == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_implementation_v1"
    assert manifest[PREFIX + "implementation_status"] == "feature_flagged_default_off_read_only_passive_visibility_activation_descriptor_builder"
    assert manifest[PREFIX + "feature_flag_required"] is True
    assert manifest[PREFIX + "feature_flag_default_enabled"] is False
    assert manifest[PREFIX + "default_off_behavior"] == "disabled_noop"
    assert manifest[PREFIX + "missing_descriptor_behavior"] == "fail_open"
    assert manifest[PREFIX + "unsafe_descriptor_behavior"] == "blocked_fail_open"
    assert manifest[PREFIX + "read_only_passive_visibility_activation_descriptor_builder_enabled"] is True
    assert manifest[PREFIX + "passive_visibility_activation_descriptor_ready"] is True
    assert manifest[PREFIX + "passive_visibility_slot_descriptor_ready"] is True
    assert manifest[PREFIX + "actual_passive_visibility_activation_enabled"] is False
    assert manifest[PREFIX + "passive_visibility_slot_registration_enabled"] is False
    assert manifest[PREFIX + "passive_visibility_slot_mutation_enabled"] is False
    assert manifest[PREFIX + "actual_runtime_app_host_visibility_enabled"] is False
    assert manifest[PREFIX + "visibility_activation_enabled"] is False
    assert manifest[PREFIX + "mounted_runtime_panel_enabled"] is False
    assert manifest[PREFIX + "runtime_panel_mount_side_effects_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wiring_enabled"] is False
    assert manifest[PREFIX + "host_event_subscription_enabled"] is False
    assert manifest[PREFIX + "host_callback_registration_enabled"] is False
    assert manifest[PREFIX + "route_influence_enabled"] is False
    assert manifest[PREFIX + "route_authority_enabled"] is False
    assert manifest[PREFIX + "router_calls_enabled"] is False
    assert manifest[PREFIX + "advisor_calls_enabled"] is False
    assert manifest[PREFIX + "provider_calls_enabled"] is False
    assert manifest[PREFIX + "persistence_enabled"] is False
    assert manifest[PREFIX + "runtime_copilot_decision_behavior_enabled"] is False
    assert manifest[PREFIX + "autonomous_ml_router_enabled"] is False
    assert manifest[PREFIX + "visible_ml_integration_complete"] is False
    assert manifest[PREFIX + "mlrt_113_created"] is False
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0
    assert manifest[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation Result Review Gate v1"


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_implementation_manifest_gates()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation implementation manifest gates")
