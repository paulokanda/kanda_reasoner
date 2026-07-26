# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_ui_status.py
"""Pure status projection helpers for the Phase 8 read-only panel UI model.

The functions in this private module convert already-built Phase 7 surface and
payload state into bounded display text. They do not import the public facade,
mutate UI state, call routing services, persist data, or claim route authority.
"""

from __future__ import annotations

from typing import Any

__all__: list[str] = []


def advisory_status(surface: Any, attached_read_only_state: Any) -> str:
    """Return the bounded advisory attachment status text."""
    if surface.attachment_state is attached_read_only_state:
        return "attached_read_only"
    return surface.attachment_state.value.lower()


def boundary_status(payload: Any) -> str:
    """Return the advisory payload boundary status or a missing marker."""
    if payload is None:
        return "not_available"
    return payload.boundary_status.value


def confidence_band(payload: Any) -> str:
    """Map non-authoritative confidence to the existing bounded band text."""
    if payload is None:
        return "not_available"
    value = payload.non_authoritative_confidence
    if value < 0.34:
        return "low_non_authoritative"
    if value < 0.67:
        return "medium_non_authoritative"
    return "high_non_authoritative"


def reason_codes(payload: Any) -> str:
    """Return up to six bounded advisory reason-code values."""
    if payload is None or not payload.advisory_reason_codes:
        return "none"
    return ",".join(code.value for code in payload.advisory_reason_codes[:6])


def guardrail_state(surface: Any) -> str:
    """Return the existing bounded guardrail-state projection."""
    if surface.advisory_display_payload is None:
        return "fail_open_no_payload"
    if surface.failure_state_codes:
        return "fail_open_or_guardrail_notice"
    return "guarded_payload_available"


def disabled_noop_state(surface: Any, disabled_noop_attachment_state: Any) -> str:
    """Return whether the source surface is disabled or read-only enabled."""
    if surface.attachment_state is disabled_noop_attachment_state:
        return "disabled_noop"
    return "enabled_read_only"


def severity(
    kind: Any,
    surface: Any,
    *,
    safety_kinds: frozenset[Any],
    warning_kinds: frozenset[Any],
) -> str:
    """Return the existing section severity using explicit caller-owned sets."""
    if kind in safety_kinds:
        return "safety"
    if surface.failure_state_codes and kind in warning_kinds:
        return "warning"
    return "info"



def build_section_specs(
    surface: Any,
    *,
    kinds: Any,
    attached_read_only_state: Any,
    disabled_noop_state_value: Any,
) -> tuple[tuple[Any, str, str, str], ...]:
    """Build deterministic section specifications without facade imports."""
    payload = surface.advisory_display_payload
    values = (
        (
            kinds.ADVISORY_ROLE_LABEL,
            "Advisory role",
            "Telemetry only; the governed router remains final selector.",
        ),
        (
            kinds.CANONICAL_ROUTE_UNCHANGED_LABEL,
            "Canonical route",
            "Unchanged; panel data does not modify final selection.",
        ),
        (
            kinds.NO_ROUTE_AUTHORITY_LABEL,
            "Route authority",
            "No ML route authority; no override or use-ML-route action.",
        ),
        (
            kinds.ADVISORY_STATUS,
            "Advisory status",
            advisory_status(surface, attached_read_only_state),
        ),
        (
            kinds.BOUNDARY_STATUS,
            "Boundary status",
            boundary_status(payload),
        ),
        (
            kinds.CONFIDENCE_BAND,
            "Confidence band",
            confidence_band(payload),
        ),
        (
            kinds.CONFIDENCE_NOT_CORRECTNESS_LABEL,
            "Confidence meaning",
            "Status only; not route correctness proof.",
        ),
        (
            kinds.REASON_CODES_BOUNDED,
            "Bounded reason codes",
            reason_codes(payload),
        ),
        (
            kinds.GUARDRAIL_STATE,
            "Guardrail state",
            guardrail_state(surface),
        ),
        (
            kinds.DISABLED_NOOP_STATE,
            "Disable/no-op state",
            disabled_noop_state(surface, disabled_noop_state_value),
        ),
        (
            kinds.NON_TRAINING_FEEDBACK_SLOT,
            "Feedback",
            "Optional non-training feedback only.",
        ),
    )
    safety_kinds = frozenset(
        {
            kinds.NO_ROUTE_AUTHORITY_LABEL,
            kinds.CONFIDENCE_NOT_CORRECTNESS_LABEL,
        }
    )
    warning_kinds = frozenset(
        {
            kinds.GUARDRAIL_STATE,
            kinds.ADVISORY_STATUS,
        }
    )
    return tuple(
        (
            kind,
            label,
            value,
            severity(
                kind,
                surface,
                safety_kinds=safety_kinds,
                warning_kinds=warning_kinds,
            ),
        )
        for kind, label, value in values
    )

def build_status_projection_contract_probe() -> dict[str, object]:
    """Return deterministic helper ownership metadata for focused validation."""
    return {
        "kind": "read_only_panel_ui_status_projection",
        "pure_projection": True,
        "imports_public_facade": False,
        "mutates_ui": False,
        "route_authority": False,
    }
