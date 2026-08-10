# project-path: kanda_reasoner_app/engineering_safety/complete_review_contract.py
"""Immutable public result contract for Complete Engineering Review."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "CompleteEngineeringReviewItem",
    "CompleteEngineeringReviewResult",
]


@dataclass(frozen=True, slots=True)
class CompleteEngineeringReviewItem:
    """One immutable Complete Engineering Review capability outcome."""

    index: int
    total: int
    section: str
    label: str
    command_name: str
    outcome: str
    assessment: str
    assessment_reason: str
    status_code: int | None
    stdout: str
    stderr: str


@dataclass(frozen=True, slots=True)
class CompleteEngineeringReviewResult:
    """One Project-bound Complete Engineering Review result."""

    project_root: str
    items: tuple[CompleteEngineeringReviewItem, ...]
    overall: str
    passed: int
    failed: int
    completed: int
    cancelled: bool
    total: int
    assessment_counts: tuple[tuple[str, int], ...]
    rendered_log: str

    def assessment_count(self, name: str) -> int:
        """Return one immutable assessment count by name."""
        wanted = str(name).strip()
        for key, value in self.assessment_counts:
            if key == wanted:
                return int(value)
        return 0
