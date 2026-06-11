"""Coordinate Tab 1 advisory AI review requests."""

from __future__ import annotations

from .adapter import Tab1AIReviewAdapter
from .models import Tab1AIReviewRequest, Tab1AIReviewResult

__all__ = ["build_tab1_ai_review_request", "run_tab1_ai_review"]


def build_tab1_ai_review_request(
    *,
    audit_text: str,
    project_root: str = "",
    model_name: str = "",
) -> Tab1AIReviewRequest:
    """Build a read-only Tab 1 AI review request."""
    return Tab1AIReviewRequest(
        audit_text=str(audit_text or ""),
        project_root=str(project_root or ""),
        model_name=str(model_name or ""),
    )


def run_tab1_ai_review(
    request: Tab1AIReviewRequest,
    adapter: Tab1AIReviewAdapter | None = None,
) -> Tab1AIReviewResult:
    """Run one advisory AI review using the supplied or default adapter."""
    active_adapter = adapter or Tab1AIReviewAdapter()
    return active_adapter.review(request)
