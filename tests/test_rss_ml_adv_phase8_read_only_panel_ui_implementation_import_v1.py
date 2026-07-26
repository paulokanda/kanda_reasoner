from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    DEFAULT_ALLOWED_SECTION_KINDS,
    ReadOnlyAdvisoryPanelSection,
    ReadOnlyAdvisoryPanelUIState,
    ReadOnlyAdvisoryPanelUIPolicy,
    ReadOnlyAdvisoryPanelViewModel,
    ReadOnlyPanelRenderMode,
    ReadOnlyPanelSectionKind,
    build_phase8_read_only_advisory_panel_ui_probe,
    build_read_only_advisory_panel_view_model,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_surface_wiring import build_phase7_read_only_surface_wiring_probe


def test_phase8_panel_ui_import_boundary():
    model = build_phase8_read_only_advisory_panel_ui_probe()
    assert isinstance(model, ReadOnlyAdvisoryPanelViewModel)
    assert isinstance(ReadOnlyAdvisoryPanelUIPolicy(panel_id="x", panel_label="x", source_review_feature_id="rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1"), ReadOnlyAdvisoryPanelUIPolicy)
    assert model.state is ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY
    assert model.render_mode is ReadOnlyPanelRenderMode.VIEW_MODEL_READY
    assert ReadOnlyPanelSectionKind.ADVISORY_ROLE_LABEL in DEFAULT_ALLOWED_SECTION_KINDS
    section = model.sections[0]
    assert isinstance(section, ReadOnlyAdvisoryPanelSection)
    assert section.action_enabled is False
    surface = build_phase7_read_only_surface_wiring_probe()
    model2 = build_read_only_advisory_panel_view_model(
        ReadOnlyAdvisoryPanelUIPolicy(panel_id="x", panel_label="x", source_review_feature_id="rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1"),
        surface,
    )
    assert model2.route_authority_enabled is False


if __name__ == "__main__":
    test_phase8_panel_ui_import_boundary()
    print("VALIDATION OK: phase8 read-only advisory panel UI implementation import boundary")
