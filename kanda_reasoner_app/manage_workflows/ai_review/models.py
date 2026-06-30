# project-path: kanda_reasoner_app/manage_workflows/ai_review/models.py
"""Data contracts for Tab 2 advisory AI review."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "CHECK_ADVISORY_BANNER",
    "CORRECTION_ADVISORY_BANNER",
    "Tab2AIReviewRequest",
    "Tab2AIReviewResult",
]

CHECK_ADVISORY_BANNER = (
    "ADVISORY AI REVIEW - deterministic Tab 2 Check remains authoritative."
)
CORRECTION_ADVISORY_BANNER = (
    "ADVISORY AI CORRECTION PLAN - deterministic Tab 2 Correct remains authoritative."
)


@dataclass(frozen=True)
class Tab2AIReviewRequest:
    """Input for one read-only Tab 2 AI review."""

    review_kind: str
    check_output_text: str
    project_root: str = ""
    model_name: str = ""
    mode_label: str = ""
    max_chars: int = 12000


@dataclass(frozen=True)
class Tab2AIReviewResult:
    """Result from one read-only Tab 2 AI review."""

    success: bool
    text: str
    model_name: str
    error_message: str = ""
