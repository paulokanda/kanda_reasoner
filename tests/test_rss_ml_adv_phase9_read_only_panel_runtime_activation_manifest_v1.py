import json
from pathlib import Path

PREFIX = "ml_advisory_phase9_read_only_advisory_panel_runtime_activation_contract_v1_"


def test_phase9_runtime_activation_manifest_gates():
    manifest = json.loads(Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json").read_text(encoding="utf-8"))
    assert manifest[PREFIX + "feature_id"] == "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_v1"
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase8_read_only_advisory_panel_ui_completion_handoff_v1"
    assert manifest[PREFIX + "contract_only"] is True
    assert manifest[PREFIX + "runtime_visible_panel_track_started"] is True
    assert manifest[PREFIX + "actual_runtime_panel_activation_enabled"] is False
    assert manifest[PREFIX + "renderer_activation_enabled"] is False
    assert manifest[PREFIX + "mounted_panel_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wired"] is False
    assert manifest[PREFIX + "requires_phase8_panel_view_model_input"] is True
    assert manifest[PREFIX + "requires_explicit_feature_flag"] is True
    assert manifest[PREFIX + "feature_flag_default_enabled"] is False
    assert manifest[PREFIX + "requires_disable_noop_control"] is True
    assert manifest[PREFIX + "requires_fail_open_on_missing_view_model"] is True
    assert manifest[PREFIX + "renderer_adapter_separate_future_contract_required"] is True
    assert "canonical_route_unchanged_label" in manifest[PREFIX + "required_safe_labels"]
    assert "route_override_button" in manifest[PREFIX + "forbidden_capabilities"]
    assert "runtime_copilot_decision_behavior" in manifest[PREFIX + "forbidden_capabilities"]
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
    assert manifest[PREFIX + "prompt_loading_enabled"] is False
    assert manifest[PREFIX + "prompt_library_read_enabled"] is False
    assert manifest[PREFIX + "freeze_memory_read_enabled"] is False
    assert manifest[PREFIX + "router_canon_read_enabled"] is False
    assert manifest[PREFIX + "advisory_rankings_enabled"] is False
    assert manifest[PREFIX + "free_text_route_advice_enabled"] is False
    assert manifest[PREFIX + "free_text_explanations_enabled"] is False
    assert manifest[PREFIX + "runtime_copilot_decision_behavior_enabled"] is False
    assert manifest[PREFIX + "mlrt_113_created"] is False
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0


if __name__ == "__main__":
    test_phase9_runtime_activation_manifest_gates()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation manifest gates")
