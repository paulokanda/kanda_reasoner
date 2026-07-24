# project-path: kanda_reasoner_app/manage_architecture/ai_review/controller.py
"""Coordinate Audit Project advisory review requests."""

from __future__ import annotations

from .adapter import Tab1AIReviewAdapter
from .heuristic import review_audit_with_heuristic
from .models import (
    HEURISTIC_MODE,
    LOCAL_AI_MODE,
    Tab1AIReviewRequest,
    Tab1AIReviewResult,
    WEB_AI_MODE,
)
from .web_adapter import Tab1WebAIReviewAdapter

__all__ = ["build_tab1_ai_review_request", "run_tab1_ai_review"]


def build_tab1_ai_review_request(
    *,
    audit_text: str,
    project_root: str = "",
    model_name: str = "",
    provider_mode: str = LOCAL_AI_MODE,
    gateway_id: str = "",
    api_key: str = "",
    request_id: str = "",
) -> Tab1AIReviewRequest:
    """Build one read-only Audit Project review request."""
    return Tab1AIReviewRequest(
        audit_text=str(audit_text or ""),
        project_root=str(project_root or ""),
        model_name=str(model_name or ""),
        provider_mode=str(provider_mode or LOCAL_AI_MODE),
        gateway_id=str(gateway_id or ""),
        api_key=str(api_key or ""),
        request_id=str(request_id or ""),
    )


def run_tab1_ai_review(
    request: Tab1AIReviewRequest,
    adapter: Tab1AIReviewAdapter | None = None,
    web_adapter: Tab1WebAIReviewAdapter | None = None,
) -> Tab1AIReviewResult:
    """Dispatch one advisory review through the selected workflow mode."""
    mode = str(request.provider_mode or LOCAL_AI_MODE).strip().lower()
    if mode == HEURISTIC_MODE:
        return review_audit_with_heuristic(request)
    if mode == WEB_AI_MODE:
        return (web_adapter or Tab1WebAIReviewAdapter()).review(request)
    return (adapter or Tab1AIReviewAdapter()).review(request)
