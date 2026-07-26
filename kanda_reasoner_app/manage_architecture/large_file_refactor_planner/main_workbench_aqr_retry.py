# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_aqr_retry.py
"""Bounded retry state for replacing a settling AQR worker generation."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "AQR_RETRY_READY",
    "AQR_RETRY_TIMEOUT",
    "AQR_RETRY_WAIT",
    "AqrStartSettlementGate",
]

AQR_RETRY_WAIT = "WAIT"
AQR_RETRY_READY = "READY"
AQR_RETRY_TIMEOUT = "TIMEOUT"
_DEFAULT_MAX_POLLS = 334


@dataclass
class AqrStartSettlementGate:
    """Track a bounded wait for a stale AQR worker to settle."""

    max_polls: int = _DEFAULT_MAX_POLLS
    pending: bool = False
    polls: int = 0

    def begin(self) -> None:
        """Begin waiting for one previous AQR runtime generation."""
        self.pending = True
        self.polls = 0

    def observe(self, runtime_running: bool) -> str:
        """Return WAIT, READY, or TIMEOUT for the current settlement state."""
        if not self.pending:
            return AQR_RETRY_READY
        if not runtime_running:
            self.reset()
            return AQR_RETRY_READY
        self.polls += 1
        if self.polls >= self.max_polls:
            self.reset()
            return AQR_RETRY_TIMEOUT
        return AQR_RETRY_WAIT

    def reset(self) -> None:
        """Clear pending retry state after start, finish, or timeout."""
        self.pending = False
        self.polls = 0
