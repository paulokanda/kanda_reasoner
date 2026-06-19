"""Tests for Tab 2 advisory AI review controller."""

from __future__ import annotations

from kanda_reasoner_app.manage_workflows.ai_review.controller import (
    build_tab2_ai_review_request,
    run_tab2_ai_review,
)
from kanda_reasoner_app.manage_workflows.ai_review.models import (
    Tab2AIReviewRequest,
    Tab2AIReviewResult,
)


class FakeAdapter:
    """Fake adapter that records the request."""

    last_request: Tab2AIReviewRequest | None = None

    def review(self, request: Tab2AIReviewRequest) -> Tab2AIReviewResult:
        """Return a deterministic fake result."""
        FakeAdapter.last_request = request
        return Tab2AIReviewResult(
            success=True,
            text="ADVISORY",
            model_name=request.model_name or "fake-model",
        )


def test_controller_builds_read_only_check_request() -> None:
    """Controller builds a check review request."""
    request = build_tab2_ai_review_request(
        review_kind="check",
        check_output_text="PASS workflow",
        project_root=r"<PROJECT_ROOT>",
        model_name="qwen2.5-coder:7b",
        mode_label="validate",
    )

    assert request.review_kind == "check"
    assert request.check_output_text == "PASS workflow"
    assert request.model_name == "qwen2.5-coder:7b"
    assert request.mode_label == "validate"


def test_controller_runs_adapter_without_correction_write_path() -> None:
    """Controller calls only the adapter review method."""
    request = build_tab2_ai_review_request(
        review_kind="correction_plan",
        check_output_text="DIFF output",
        model_name="qwen3-coder:30b",
    )

    result = run_tab2_ai_review(request, adapter=FakeAdapter())

    assert result.success is True
    assert FakeAdapter.last_request is request
    assert FakeAdapter.last_request.review_kind == "correction_plan"


if __name__ == "__main__":
    test_controller_builds_read_only_check_request()
    test_controller_runs_adapter_without_correction_write_path()
    print("Tab 2 AI review controller tests passed.")
