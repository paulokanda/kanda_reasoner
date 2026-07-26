from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.guarded_runtime_display import (
    build_phase6_guarded_runtime_display_payload_probe,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_surface_wiring import (
    CanonicalDispatchSnapshot,
    ReadOnlyAdvisorySurfaceWiringEnvelope,
    ReadOnlyAdvisorySurfaceWiringPolicy,
    ReadOnlySurfaceAttachmentState,
    build_phase7_read_only_surface_wiring_probe,
    build_read_only_advisory_surface_wiring_envelope,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "ML_ADVISORY_PHASE7_READ_ONLY_ADVISORY_SURFACE_WIRING_IMPLEMENTATION_V1.md"

FEATURE_ID = "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_v1"
SOURCE_REVIEW_ID = "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1"


def _policy(enabled: bool = True) -> ReadOnlyAdvisorySurfaceWiringPolicy:
    return ReadOnlyAdvisorySurfaceWiringPolicy(
        surface_id="test_surface",
        surface_label="test_surface_label",
        source_review_feature_id=SOURCE_REVIEW_ID,
        allowed_surface_section_codes=(
            "canonical_snapshot",
            "advisory_display_payload",
            "attachment_state",
            "failure_state_codes",
            "non_training_feedback_slot",
        ),
        enabled=enabled,
    )


def _snapshot() -> CanonicalDispatchSnapshot:
    return CanonicalDispatchSnapshot(
        canonical_result_id="result_001",
        canonical_dispatch_label="governed_router_completed",
        final_selection_hash="hash_001",
    )


def test_probe_builds_attached_read_only_envelope() -> None:
    envelope = build_phase7_read_only_surface_wiring_probe()
    assert isinstance(envelope, ReadOnlyAdvisorySurfaceWiringEnvelope)
    assert envelope.feature_id == FEATURE_ID
    assert envelope.attachment_state is ReadOnlySurfaceAttachmentState.ATTACHED_READ_ONLY
    assert envelope.canonical_snapshot_before == envelope.canonical_snapshot_after
    assert envelope.advisory_display_payload is not None
    assert envelope.read_only is True
    assert envelope.telemetry_only is True
    assert envelope.route_invariant is True
    assert envelope.final_selection_invisible is True
    assert envelope.non_authoritative is True
    assert envelope.runtime_advisory_panel_enabled is False
    assert envelope.runtime_ui_mutation_enabled is False
    assert envelope.runtime_telemetry_surface_wired is False
    assert envelope.route_authority_enabled is False
    assert envelope.runtime_copilot_decision_behavior_enabled is False


def test_disabled_mode_returns_noop_without_advisory_payload() -> None:
    envelope = build_read_only_advisory_surface_wiring_envelope(
        _policy(enabled=False),
        _snapshot(),
        build_phase6_guarded_runtime_display_payload_probe(),
    )
    assert envelope.attachment_state is ReadOnlySurfaceAttachmentState.DISABLED_NOOP
    assert envelope.advisory_display_payload is None
    assert envelope.failure_state_codes == ("disabled_noop",)
    assert envelope.canonical_snapshot_before == envelope.canonical_snapshot_after


def test_invalid_advisory_payload_fails_open() -> None:
    original = _snapshot()
    envelope = build_read_only_advisory_surface_wiring_envelope(
        _policy(),
        original,
        object(),
    )
    assert envelope.attachment_state is ReadOnlySurfaceAttachmentState.FAIL_OPEN_NO_ADVISORY
    assert envelope.advisory_display_payload is None
    assert envelope.failure_state_codes == ("invalid_advisory_payload",)
    assert envelope.canonical_snapshot_before == original
    assert envelope.canonical_snapshot_after == original


def test_document_records_non_activation_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "does not wire itself into the runtime app, UI, or router" in text
    assert "no runtime telemetry surface" in text
    assert "Disabled, missing, invalid, or rejected advisory data fails open" in text


if __name__ == "__main__":
    test_probe_builds_attached_read_only_envelope()
    test_disabled_mode_returns_noop_without_advisory_payload()
    test_invalid_advisory_payload_fails_open()
    test_document_records_non_activation_boundary()
    print("VALIDATION OK: phase7 read-only advisory surface wiring implementation")
