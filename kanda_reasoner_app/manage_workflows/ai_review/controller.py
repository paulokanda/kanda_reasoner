# project-path: kanda_reasoner_app/manage_workflows/ai_review/controller.py
"""Controller helpers for Tab 2 advisory AI review."""

from __future__ import annotations

from .adapter import Tab2AIReviewAdapter
from .models import Tab2AIReviewRequest, Tab2AIReviewResult

__all__ = [
    "build_tab2_ai_review_request",
    "run_tab2_ai_review",
]


def build_tab2_ai_review_request(
    *,
    review_kind: str,
    check_output_text: str,
    project_root: str = "",
    model_name: str = "",
    mode_label: str = "",
) -> Tab2AIReviewRequest:
    """Build one read-only Tab 2 AI review request."""
    return Tab2AIReviewRequest(
        review_kind=str(review_kind or "check"),
        check_output_text=str(check_output_text or ""),
        project_root=str(project_root or ""),
        model_name=str(model_name or ""),
        mode_label=str(mode_label or ""),
    )


def run_tab2_ai_review(
    request: Tab2AIReviewRequest,
    adapter: Tab2AIReviewAdapter | None = None,
) -> Tab2AIReviewResult:
    """Run one Tab 2 advisory AI review through the local adapter."""
    active_adapter = adapter or Tab2AIReviewAdapter()
    return active_adapter.review(request)
