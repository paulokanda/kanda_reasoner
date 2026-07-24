# project-path: kanda_reasoner_app/manage_architecture/ai_review/models.py
"""Data contracts for Audit Project advisory review."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "ADVISORY_BANNER",
    "DEFAULT_MAX_AUDIT_CHARS",
    "HEURISTIC_MODE",
    "LOCAL_AI_MODE",
    "WEB_AI_MODE",
    "Tab1AIReviewRequest",
    "Tab1AIReviewResult",
]

ADVISORY_BANNER = (
    "ADVISORY AUDIT REVIEW - deterministic Project Audit remains authoritative."
)
DEFAULT_MAX_AUDIT_CHARS = 12000
HEURISTIC_MODE = "heuristic"
LOCAL_AI_MODE = "local"
WEB_AI_MODE = "web"


@dataclass(frozen=True, slots=True)
class Tab1AIReviewRequest:
    """Represent one read-only Audit Project review request."""

    audit_text: str
    project_root: str = ""
    model_name: str = ""
    source_label: str = "Project Audit Results"
    max_audit_chars: int = DEFAULT_MAX_AUDIT_CHARS
    provider_mode: str = LOCAL_AI_MODE
    gateway_id: str = ""
    api_key: str = ""
    request_id: str = ""


@dataclass(frozen=True, slots=True)
class Tab1AIReviewResult:
    """Represent the advisory result of one Audit Project review."""

    success: bool
    text: str
    model_name: str = ""
    error_message: str = ""
    provider_mode: str = LOCAL_AI_MODE
    request_id: str = ""
