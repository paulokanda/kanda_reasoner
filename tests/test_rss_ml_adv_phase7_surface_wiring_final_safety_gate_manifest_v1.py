import json
from pathlib import Path


FEATURE_ID = "rss_ml_adv_phase7_read_only_advisory_surface_wiring_final_safety_gate_v1"
PREFIX = "ml_advisory_phase7_read_only_advisory_surface_wiring_final_safety_gate_v1_"


def test_phase7_read_only_surface_wiring_final_safety_manifest_gates():
    manifest = json.loads(
        Path("kanda_reasoner_app/routing_signal_scorer/box_manifest.json")
        .read_text(encoding="utf-8")
    )
    assert manifest[PREFIX + "feature_id"] == FEATURE_ID
    assert manifest[PREFIX + "reviewed_feature_id"] == "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_result_review_gate_v1"
    assert manifest[PREFIX + "surface_envelope_reviewed"] is True
    assert manifest[PREFIX + "surface_envelope_locked_read_only"] is True
    assert manifest[PREFIX + "surface_envelope_locked_telemetry_only"] is True
    assert manifest[PREFIX + "surface_envelope_locked_in_memory"] is True
    assert manifest[PREFIX + "surface_envelope_locked_bounded"] is True
    assert manifest[PREFIX + "surface_envelope_locked_fail_open"] is True
    assert manifest[PREFIX + "surface_envelope_locked_removable_noop"] is True
    assert manifest[PREFIX + "surface_envelope_locked_final_selection_invisible"] is True
    assert manifest[PREFIX + "surface_envelope_locked_route_invariant"] is True
    assert manifest[PREFIX + "surface_envelope_locked_non_authoritative"] is True
    assert manifest[PREFIX + "canonical_dispatch_snapshot_copied_unchanged"] is True
    assert manifest[PREFIX + "already_built_guarded_display_payload_only"] is True
    assert manifest[PREFIX + "separate_telemetry_surface_field_only"] is True
    assert manifest[PREFIX + "completion_handoff_required_before_panel_contract"] is True
    assert manifest[PREFIX + "route_invariant"] is True
    assert manifest[PREFIX + "read_only"] is True
    assert manifest[PREFIX + "telemetry_only"] is True
    assert manifest[PREFIX + "fail_open"] is True
    assert manifest[PREFIX + "non_authoritative"] is True
    assert manifest[PREFIX + "route_influence_enabled"] is False
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
    test_phase7_read_only_surface_wiring_final_safety_manifest_gates()
    print("VALIDATION OK: phase7 read-only advisory surface wiring final safety gate manifest gates")
