from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import (
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelope,
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelopePolicy,
    ReadOnlyPanelRuntimeActivationEnvelopeState,
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
    build_read_only_advisory_panel_runtime_activation_envelope,
)


def test_phase9_runtime_activation_implementation_import_boundary():
    assert ReadOnlyAdvisoryPanelRuntimeActivationEnvelope.__name__ == "ReadOnlyAdvisoryPanelRuntimeActivationEnvelope"
    assert ReadOnlyAdvisoryPanelRuntimeActivationEnvelopePolicy.__name__ == "ReadOnlyAdvisoryPanelRuntimeActivationPolicy"
    assert ReadOnlyPanelRuntimeActivationEnvelopeState.READY_READ_ONLY_ACTIVATION_ENVELOPE.value == "ready_read_only_activation_envelope"
    probe = build_phase9_read_only_panel_runtime_activation_implementation_probe()
    assert probe.runtime_activation_envelope_ready is True
    assert callable(build_read_only_advisory_panel_runtime_activation_envelope)
    assert probe.actual_runtime_panel_activation_enabled is False
    assert probe.renderer_activation_enabled is False
    assert probe.mounted_panel_enabled is False


if __name__ == "__main__":
    test_phase9_runtime_activation_implementation_import_boundary()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation implementation import boundary")
