"""Tests for Tab 1 advisory AI review controller contract."""

from __future__ import annotations

from kanda_reasoner_app.manage_architecture.ai_review.controller import (
    build_tab1_ai_review_request,
    run_tab1_ai_review,
)
from kanda_reasoner_app.manage_architecture.ai_review.models import (
    Tab1AIReviewResult,
)


class FakeAdapter:
    """Fake review adapter for controller tests."""

    def review(self, request: object) -> Tab1AIReviewResult:
        """Return the audit text in a safe fake result."""
        audit_text = getattr(request, "audit_text", "")
        return Tab1AIReviewResult(success=True, text="reviewed: " + audit_text)


def test_build_request_preserves_audit_and_root() -> None:
    """Request builder preserves caller-provided audit context."""
    request = build_tab1_ai_review_request(
        audit_text="WARNING CODE file.py :: warning",
        project_root=r"E:\developer_tools",
    )

    assert request.audit_text.startswith("WARNING CODE")
    assert request.project_root == r"E:\developer_tools"


def test_run_review_uses_supplied_adapter() -> None:
    """Controller delegates review through the supplied adapter."""
    request = build_tab1_ai_review_request(audit_text="audit text")

    result = run_tab1_ai_review(request, FakeAdapter())

    assert result.success is True
    assert result.text == "reviewed: audit text"


if __name__ == "__main__":
    test_build_request_preserves_audit_and_root()
    test_run_review_uses_supplied_adapter()
    print("Tab 1 AI review controller tests passed.")
