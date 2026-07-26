from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_ui import (
    ReadOnlyAdvisoryPanelUIPolicy,
    ReadOnlyAdvisoryPanelUIState,
    ReadOnlyPanelRenderMode,
    ReadOnlyPanelSectionKind,
    build_phase8_read_only_advisory_panel_ui_probe,
    build_read_only_advisory_panel_view_model,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_surface_wiring import (
    ReadOnlySurfaceAttachmentState,
    build_phase7_read_only_surface_wiring_probe,
)

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_IMPLEMENTATION_V1.md")
BOUNDARY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_IMPLEMENTATION_BOUNDARY_MODEL_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_IMPLEMENTATION_RESULT_REVIEW_READINESS_V1.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_CONTRACT_RESULT_REVIEW_GATE_V1.md")


def _policy(enabled=True):
    return ReadOnlyAdvisoryPanelUIPolicy(
        panel_id="phase8_panel",
        panel_label="Phase 8 Advisory Panel",
        source_review_feature_id="rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1",
        enabled=enabled,
    )


def test_phase8_panel_view_model_probe_is_safe():
    model = build_phase8_read_only_advisory_panel_ui_probe()
    assert model.feature_id == "rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_v1"
    assert model.state is ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY
    assert model.render_mode is ReadOnlyPanelRenderMode.VIEW_MODEL_READY
    assert model.source_attachment_state is ReadOnlySurfaceAttachmentState.ATTACHED_READ_ONLY
    assert model.canonical_result_id == "synthetic_canonical_result_001"
    assert model.read_only is True
    assert model.telemetry_only is True
    assert model.renderer_neutral is True
    assert model.in_memory_only is True
    assert model.route_invariant is True
    assert model.final_selection_invisible is True
    assert model.non_authoritative is True
    assert model.runtime_panel_activation_enabled is False
    assert model.runtime_ui_mutation_enabled is False
    assert model.runtime_telemetry_surface_wired is False
    assert model.route_influence_enabled is False
    assert model.route_authority_enabled is False
    assert model.route_override_button_enabled is False
    assert model.use_ml_route_button_enabled is False
    assert model.prompt_ranking_enabled is False
    assert model.free_text_route_advice_enabled is False
    assert model.free_text_explanations_enabled is False
    assert model.runtime_copilot_decision_behavior_enabled is False
    kinds = {section.kind for section in model.sections}
    assert ReadOnlyPanelSectionKind.ADVISORY_ROLE_LABEL in kinds
    assert ReadOnlyPanelSectionKind.CANONICAL_ROUTE_UNCHANGED_LABEL in kinds
    assert ReadOnlyPanelSectionKind.NO_ROUTE_AUTHORITY_LABEL in kinds
    assert ReadOnlyPanelSectionKind.CONFIDENCE_NOT_CORRECTNESS_LABEL in kinds
    for section in model.sections:
        assert section.read_only is True
        assert section.action_enabled is False
        assert section.route_authority_enabled is False
        assert section.route_influence_enabled is False
        assert section.free_text_route_advice is False
        assert len(section.value) <= 240


def test_phase8_panel_view_model_consumes_phase7_envelope_without_route_change():
    surface = build_phase7_read_only_surface_wiring_probe()
    before = surface.canonical_snapshot_before
    after = surface.canonical_snapshot_after
    assert before == after
    model = build_read_only_advisory_panel_view_model(_policy(), surface)
    assert model.canonical_result_id == before.canonical_result_id
    assert model.canonical_dispatch_label == before.canonical_dispatch_label
    assert model.final_selection_hash == before.final_selection_hash
    assert model.route_invariant is True
    assert model.final_selection_invisible is True
    assert model.route_authority_enabled is False


def test_phase8_panel_view_model_fail_open_paths():
    invalid = build_read_only_advisory_panel_view_model(_policy(), object())
    assert invalid.state is ReadOnlyAdvisoryPanelUIState.FAIL_OPEN_NO_SURFACE
    assert invalid.render_mode is ReadOnlyPanelRenderMode.FAIL_OPEN_NO_SURFACE
    assert invalid.source_surface_id is None
    assert invalid.route_authority_enabled is False
    assert invalid.runtime_panel_activation_enabled is False
    assert "missing_or_invalid_surface_envelope" in invalid.failure_state_codes

    disabled = build_read_only_advisory_panel_view_model(_policy(enabled=False), build_phase7_read_only_surface_wiring_probe())
    assert disabled.state is ReadOnlyAdvisoryPanelUIState.DISABLED_NOOP
    assert disabled.render_mode is ReadOnlyPanelRenderMode.DISABLED_NOOP
    assert disabled.route_authority_enabled is False
    assert disabled.runtime_ui_mutation_enabled is False
    assert "disabled_noop" in disabled.failure_state_codes


def test_phase8_panel_ui_docs_and_boundaries():
    text = DOC.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_v1" in text
    assert "Routing Signal Scorer ML Advisory-Signal Phase 8 Read-Only Advisory Panel UI Contract Result Review Gate v1" in text
    assert "renderer-neutral" in text
    assert "does not render UI" in text
    assert "must not" in text
    assert "route authority" in text
    assert "Phase 7 read-only advisory surface envelope" in boundary
    assert "not a renderer" in boundary
    assert "no runtime panel activation" in readiness
    assert PREV.exists()


if __name__ == "__main__":
    test_phase8_panel_view_model_probe_is_safe()
    test_phase8_panel_view_model_consumes_phase7_envelope_without_route_change()
    test_phase8_panel_view_model_fail_open_paths()
    test_phase8_panel_ui_docs_and_boundaries()
    print("VALIDATION OK: phase8 read-only advisory panel UI implementation")
