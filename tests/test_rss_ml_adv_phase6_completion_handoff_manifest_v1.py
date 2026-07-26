import json
from pathlib import Path


FEATURE_ID = "rss_ml_adv_phase6_guarded_runtime_advisory_display_completion_handoff_v1"
PREFIX = "ml_advisory_phase6_guarded_runtime_advisory_display_completion_handoff_v1_"


def test_phase6_completion_handoff_manifest_gates():
    manifest = json.loads(
        Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json")
        .read_text(encoding="utf-8")
    )
    assert manifest[PREFIX + "feature_id"] == FEATURE_ID
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase6_guarded_runtime_advisory_display_final_safety_gate_v1"
    assert manifest[PREFIX + "completion_handoff_only"] is True
    assert manifest[PREFIX + "phase6_display_path_completed"] is True
    assert manifest[PREFIX + "safe_completed_state"] == "bounded_in_memory_read_only_telemetry_payload_builder_only"
    assert manifest[PREFIX + "governed_router_remains_final_selector"] is True
    assert manifest[PREFIX + "ml_advisory_signal_telemetry_only"] is True
    assert manifest[PREFIX + "manual_prompt_code_hint_classification_help_only"] is True
    assert manifest[PREFIX + "governed_prompt_intake_only_safe_door"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "in_memory_only"] is True
    assert manifest[PREFIX + "bounded"] is True
    assert manifest[PREFIX + "fail_open"] is True
    assert manifest[PREFIX + "removable_noop"] is True
    assert manifest[PREFIX + "final_selection_invisible"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "route_authority_enabled"] is False
    assert manifest[PREFIX + "router_prompt_logic_modified"] is False
    assert manifest[PREFIX + "router_final_selection_modified"] is False
    assert manifest[PREFIX + "runtime_advisory_panel_enabled"] is False
    assert manifest[PREFIX + "runtime_ui_mutation_enabled"] is False
    assert manifest[PREFIX + "runtime_telemetry_surface_wired"] is False
    assert manifest[PREFIX + "runtime_copilot_decision_behavior_enabled"] is False
    assert manifest[PREFIX + "real_ml_enabled"] is False
    assert manifest[PREFIX + "adapter_execution_enabled"] is False
    assert manifest[PREFIX + "provider_calls_enabled"] is False
    assert manifest[PREFIX + "mlrt_113_created"] is False
    assert manifest[PREFIX + "critical_boundary_error_budget"] == 0


if __name__ == "__main__":
    test_phase6_completion_handoff_manifest_gates()
    print("VALIDATION OK: phase6 guarded runtime advisory display completion handoff manifest gates")
