import json
from pathlib import Path

PREFIX = "ml_advisory_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_result_review_gate_v1_"
IMPL_PREFIX = "ml_advisory_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_v1_"
CONTRACT_REVIEW_PREFIX = "ml_advisory_phase13_read_only_advisory_panel_passive_visibility_activation_contract_result_review_gate_v1_"


def test_phase13_passive_visibility_activation_implementation_result_review_gate_manifest():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_result_review_gate_v1"
    assert manifest[PREFIX + "feature_title"] == "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Implementation Result Review Gate v1"
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_v1"
    assert manifest[PREFIX + "implementation_result_review_gate_only"] is True
    assert manifest[PREFIX + "review_gate_only"] is True
    assert manifest[PREFIX + "accepted_implementation_only"] is True
    assert manifest[PREFIX + "accepted_good_safe_for_final_safety_gate_only"] is True
    assert manifest[PREFIX + "accepted_feature_flag_default_off"] is True
    assert manifest[PREFIX + "accepted_disabled_noop_path"] is True
    assert manifest[PREFIX + "accepted_missing_descriptor_fail_open_path"] is True
    assert manifest[PREFIX + "accepted_unsafe_descriptor_block_path"] is True
    assert manifest[PREFIX + "accepted_phase12_runtime_app_host_visibility_descriptor_lineage_only"] is True
    assert manifest[PREFIX + "accepted_bounded_passive_visibility_slot_descriptors"] is True
    assert manifest[PREFIX + "accepted_read_only_passive_visibility_activation_descriptor"] is True
    assert manifest[PREFIX + "accepted_read_only_display_only_passive_slots"] is True
    assert manifest[PREFIX + "accepted_removable_noop_activation_descriptor"] is True
    assert manifest[PREFIX + "accepted_route_invariant"] is True
    assert manifest[PREFIX + "accepted_final_selection_invisible"] is True
    assert manifest[PREFIX + "accepted_non_authoritative"] is True
    assert manifest[PREFIX + "feature_flag_default_enabled"] is False
    assert manifest[PREFIX + "actual_passive_visibility_activation_enabled"] is False
    assert manifest[PREFIX + "passive_visibility_slot_registration_enabled"] is False
    assert manifest[PREFIX + "passive_visibility_slot_mutation_enabled"] is False
    assert manifest[PREFIX + "actual_runtime_app_host_visibility_enabled"] is False
    assert manifest[PREFIX + "runtime_app_host_visibility_activation_enabled"] is False
    assert manifest[PREFIX + "mounted_runtime_panel_enabled"] is False
    assert manifest[PREFIX + "runtime_panel_mount_side_effects_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wired"] is False
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
    assert manifest[PREFIX + "planned_next_step"] == "Routing Signal Scorer ML Advisory-Signal Phase 13 Read-Only Advisory Panel Passive Visibility Activation Final Safety Gate v1"
    assert manifest[IMPL_PREFIX + "implementation_result_review_gate_completed"] is True
    assert manifest[IMPL_PREFIX + "implementation_result_review_gate_feature_id"] == "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_implementation_result_review_gate_v1"
    assert manifest[IMPL_PREFIX + "final_safety_gate_required_next"] is True
    assert manifest[IMPL_PREFIX + "actual_passive_visibility_activation_enabled"] is False
    assert manifest[IMPL_PREFIX + "passive_visibility_slot_registration_enabled"] is False
    assert manifest[IMPL_PREFIX + "passive_visibility_slot_mutation_enabled"] is False
    assert manifest[IMPL_PREFIX + "visible_ml_integration_complete"] is False
    assert manifest[CONTRACT_REVIEW_PREFIX + "review_gate_only"] is True


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_implementation_result_review_gate_manifest()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation implementation result review gate manifest gates")
