import json
from pathlib import Path

PREFIX = "ml_advisory_phase8_read_only_advisory_panel_ui_implementation_v1_"


def test_phase8_panel_ui_implementation_manifest_gates():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_v1"
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1"
    assert manifest[PREFIX + "panel_view_model_builder_enabled"] is True
    assert manifest[PREFIX + "visible_panel_runtime_enabled"] is False
    assert manifest[PREFIX + "runtime_panel_activation_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wired"] is False
    assert manifest[PREFIX + "uses_phase7_surface_envelope_input_only"] is True
    assert manifest[PREFIX + "renderer_neutral"] is True
    assert manifest[PREFIX + "in_memory_only"] is True
    assert manifest[PREFIX + "requires_advisory_role_label"] is True
    assert manifest[PREFIX + "requires_canonical_route_unchanged_label"] is True
    assert manifest[PREFIX + "requires_no_route_authority_label"] is True
    assert manifest[PREFIX + "requires_confidence_not_correctness_label"] is True
    assert "advisory_role_label" in manifest[PREFIX + "allowed_panel_sections"]
    assert "no_route_authority_label" in manifest[PREFIX + "allowed_panel_sections"]
    assert manifest[PREFIX + "governed_router_remains_final_selector"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "route_override_button_enabled"] is False
    assert manifest[PREFIX + "use_ml_route_button_enabled"] is False
    assert manifest[PREFIX + "best_route_claim_enabled"] is False
    assert manifest[PREFIX + "prompt_ranking_enabled"] is False
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
    test_phase8_panel_ui_implementation_manifest_gates()
    print("VALIDATION OK: phase8 read-only advisory panel UI implementation manifest gates")
