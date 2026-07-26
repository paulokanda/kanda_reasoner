"""Pure lifecycle models and status helpers for Main Workbench orchestration."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "AQR_READY_DECISIONS",
    "AQR_TERMINAL_STATUSES",
    "MAIN_WORKBENCH_CANCELLED",
    "MAIN_WORKBENCH_FAILED",
    "MAIN_WORKBENCH_READY",
    "MAIN_WORKBENCH_STALE",
    "MAIN_WORKBENCH_WEB_AI_BLOCKED",
    "MainWorkbenchControllerState",
    "aqr_is_ready",
    "aqr_is_terminal",
    "result_blockers",
]

MAIN_WORKBENCH_READY = "READY_FOR_WEB_AI"
MAIN_WORKBENCH_WEB_AI_BLOCKED = "WEB_AI_REQUIRED_WITH_BLOCKERS"
MAIN_WORKBENCH_FAILED = "FAILED_LOCAL_PIPELINE"
MAIN_WORKBENCH_STALE = "STALE_AFTER_EXTERNAL_SOURCE_MUTATION"
MAIN_WORKBENCH_CANCELLED = "CANCELLED"

AQR_READY_DECISIONS = frozenset(
    {
        "PASS",
        "PASS_WITH_WARNINGS",
    }
)

AQR_TERMINAL_STATUSES = frozenset(
    {
        "PASS",
        "PASS_WITH_WARNINGS",
        "BLOCKED",
        "INDETERMINATE",
        "FAILED",
        "TIMED_OUT",
        "CONFIGURATION_ERROR",
        "REVIEW_REQUIRED",
        "ADVISORY_REVIEW_REQUIRED",
        "CANCELLED",
    }
)


@dataclass(frozen=True)
class MainWorkbenchControllerState:
    """Read-only GUI projection for one automatic pipeline generation."""

    generation: int
    running: bool
    cancel_requested: bool
    stage: str
    terminal_status: str
    message: str
    blockers: tuple[str, ...]

    @property
    def packageable(self) -> bool:
        """Return whether the terminal state can produce a Web AI package."""
        return self.terminal_status in {
            MAIN_WORKBENCH_READY,
            MAIN_WORKBENCH_WEB_AI_BLOCKED,
        }

    @property
    def terminal(self) -> bool:
        """Return whether this projection represents a completed generation."""
        return bool(self.terminal_status)

    def to_dict(self) -> dict[str, object]:
        """Return a stable JSON-ready GUI and validation representation."""
        return {
            "generation": self.generation,
            "running": self.running,
            "cancel_requested": self.cancel_requested,
            "stage": self.stage,
            "terminal_status": self.terminal_status,
            "message": self.message,
            "blockers": list(self.blockers),
            "packageable": self.packageable,
            "terminal": self.terminal,
        }


def aqr_is_ready(status: str) -> bool:
    """Return whether AQR authorizes package-ready local evidence."""
    return str(status or "") in AQR_READY_DECISIONS


def aqr_is_terminal(status: str) -> bool:
    """Return whether the guarded AQR worker reached a settled outcome."""
    return str(status or "") in AQR_TERMINAL_STATUSES


def result_blockers(result: object | None) -> tuple[str, ...]:
    """Return typed blocker text without inventing a successful stage state."""
    blockers = [
        str(item)
        for item in tuple(getattr(result, "blockers", ()) or ())
        if str(item)
    ]
    if not blockers:
        status = str(getattr(result, "status", "") or "")
        if status:
            blockers.append("STATUS:" + status)
    return tuple(sorted(set(blockers)))
