from __future__ import annotations

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.boundary_guard import (
    PHASE1A_ALLOWED_CAPABILITIES,
    PHASE1A_FORBIDDEN_CAPABILITIES,
    assert_phase1a_environment_allowed,
)

FEATURE_ID = "rss_ml_advisory_prompt_intake_boundary_v1"


def test_allowed_phase1a_capabilities_pass() -> None:
    assert_phase1a_environment_allowed(set(PHASE1A_ALLOWED_CAPABILITIES))


def test_forbidden_phase1a_capabilities_fail() -> None:
    for capability in PHASE1A_FORBIDDEN_CAPABILITIES:
        try:
            assert_phase1a_environment_allowed({capability})
        except ValueError as exc:
            assert capability in str(exc)
        else:
            raise AssertionError(f"Forbidden capability accepted: {capability}")


def test_unknown_capability_fails_closed() -> None:
    try:
        assert_phase1a_environment_allowed({"new_runtime_mode"})
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown capability was accepted")


if __name__ == "__main__":
    test_allowed_phase1a_capabilities_pass()
    test_forbidden_phase1a_capabilities_fail()
    test_unknown_capability_fails_closed()
    print(f"VALIDATION OK: {FEATURE_ID}")
