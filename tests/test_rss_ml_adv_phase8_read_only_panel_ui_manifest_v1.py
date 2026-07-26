import json
from pathlib import Path

PREFIX = "ml_advisory_phase8_read_only_advisory_panel_ui_contract_v1_"


def test_phase8_panel_ui_manifest_gates():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_v1"
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase7_read_only_advisory_surface_wiring_completion_handoff_v1"
    assert manifest[PREFIX + "panel_track_started"] is True
    assert manifest[PREFIX + "contract_only"] is True
    assert manifest[PREFIX + "visible_panel_implementation_enabled"] is False
    assert manifest[PREFIX + "runtime_panel_activation_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wired"] is False
    assert manifest[PREFIX + "requires_surface_envelope_input"] is True
    assert manifest[PREFIX + "requires_canonical_route_unchanged_label"] is True
    assert manifest[PREFIX + "requires_advisory_role_label"] is True
    assert manifest[PREFIX + "requires_non_training_feedback_slot"] is True
    assert "canonical_route_unchanged_label" in manifest[PREFIX + "allowed_panel_sections"]
    assert "route_override_button" in manifest[PREFIX + "forbidden_panel_capabilities"]
    assert "free_text_route_advice" in manifest[PREFIX + "forbidden_panel_capabilities"]
    assert manifest[PREFIX + "governed_router_remains_final_selector"] is True
    assert manifest[PREFIX + "ml_advisory_signal_telemetry_only"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "route_influence_enabled"] is False
    assert manifest[PREFIX + "route_authority_enabled"] is False
    assert manifest[PREFIX + "router_calls_enabled"] is False
    assert manifest[PREFIX + "advisor_calls_enabled"] is False
    assert manifest[PREFIX + "adapter_execution_enabled"] is False
    assert manifest[PREFIX + "provider_calls_enabled"] is False
    assert manifest[PREFIX + "persistence_enabled"] is False
    assert manifest[PREFIX + "prompt_library_read_enabled"] is False
    assert manifest[PREFIX + "router_canon_read_enabled"] is False
    assert manifest[PREFIX + "advisory_rankings_enabled"] is False
    assert manifest[PREFIX + "free_text_route_advice_enabled"] is False
    assert manifest[PREFIX + "free_text_explanations_enabled"] is False
    assert manifest[PREFIX + "runtime_copilot_decision_behavior_enabled"] is False
    assert manifest[PREFIX + "mlrt_113_created"] is False
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0


if __name__ == "__main__":
    test_phase8_panel_ui_manifest_gates()
    print("VALIDATION OK: phase8 read-only advisory panel UI manifest gates")
