# project-path: kanda_reasoner_app/manage_architecture/ai_review/models.py
"""Data contracts for Tab 1 advisory AI review."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "ADVISORY_BANNER",
    "DEFAULT_MAX_AUDIT_CHARS",
    "Tab1AIReviewRequest",
    "Tab1AIReviewResult",
]

ADVISORY_BANNER = (
    "ADVISORY AI REVIEW - deterministic First Check remains authoritative."
)
DEFAULT_MAX_AUDIT_CHARS = 12000


@dataclass(frozen=True)
class Tab1AIReviewRequest:
    """Represent one read-only Tab 1 audit review request."""

    audit_text: str
    project_root: str = ""
    model_name: str = ""
    source_label: str = "Tab 1 First Check output"
    max_audit_chars: int = DEFAULT_MAX_AUDIT_CHARS


@dataclass(frozen=True)
class Tab1AIReviewResult:
    """Represent the advisory result of a Tab 1 AI review."""

    success: bool
    text: str
    model_name: str = ""
    error_message: str = ""
