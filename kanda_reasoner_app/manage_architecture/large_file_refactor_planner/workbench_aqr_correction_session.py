"""Retain unresolved AQR correction authority across candidate generations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = [
    "AQRCorrectionSession",
    "activate_aqr_correction_session",
    "clear_aqr_correction_session",
    "current_aqr_correction_session",
    "note_aqr_correction_candidate",
]

_SESSION_ATTR = "_large_file_refactor_workbench_aqr_correction_session"


@dataclass(frozen=True)
class AQRCorrectionSession:
    """Immutable unresolved blocker context retained until a fresh AQR passes."""

    context: Any
    source_identity_hash: str
    candidate_generation: int = 0
    last_route: str = ""


def current_aqr_correction_session(window: object) -> AQRCorrectionSession | None:
    """Return the current unresolved AQR correction session, if any."""
    value = getattr(window, _SESSION_ATTR, None)
    return value if isinstance(value, AQRCorrectionSession) else None


def activate_aqr_correction_session(window: object, context: Any) -> AQRCorrectionSession:
    """Create or refresh unresolved AQR blocker authority from terminal evidence."""
    previous = current_aqr_correction_session(window)
    session = AQRCorrectionSession(
        context=context,
        source_identity_hash=str(
            getattr(window, "_large_file_refactor_workbench_aqr_identity_hash", "") or ""
        ),
        candidate_generation=(previous.candidate_generation if previous else 0),
        last_route=(previous.last_route if previous else ""),
    )
    setattr(window, _SESSION_ATTR, session)
    return session


def note_aqr_correction_candidate(window: object, route: str) -> None:
    """Record a candidate generation without retiring unresolved blocker authority."""
    current = current_aqr_correction_session(window)
    if current is None:
        return
    setattr(
        window,
        _SESSION_ATTR,
        AQRCorrectionSession(
            context=current.context,
            source_identity_hash=current.source_identity_hash,
            candidate_generation=current.candidate_generation + 1,
            last_route=str(route),
        ),
    )


def clear_aqr_correction_session(window: object) -> None:
    """Retire blocker authority only after fresh AQR success or explicit card reset."""
    setattr(window, _SESSION_ATTR, None)
