"""Tests for Tab 2 advisory AI review prompt builders."""

from __future__ import annotations

from kanda_reasoner_app.manage_workflows.ai_review.models import (
    Tab2AIReviewRequest,
)
from kanda_reasoner_app.manage_workflows.ai_review.review_message_builder import (
    build_tab2_ai_review_messages,
    limit_text_for_model,
)


def test_check_prompt_preserves_deterministic_authority() -> None:
    """AI Review Check prompt keeps Tab 2 Check authoritative."""
    request = Tab2AIReviewRequest(
        review_kind="check",
        check_output_text="FAIL workflow step mismatch",
        mode_label="validate",
    )

    messages = build_tab2_ai_review_messages(request)
    combined = "\n".join(message["content"] for message in messages)

    assert "deterministic Check output" in combined
    assert "Highest risks first" in combined
    assert "deterministic" in combined
    assert "Do not suggest automatic writes" in combined


def test_correction_prompt_is_read_only() -> None:
    """Correction Plan prompt forbids writes and Correct execution."""
    request = Tab2AIReviewRequest(
        review_kind="correction_plan",
        check_output_text="Diff shows workflow manifest changes",
        mode_label="diff",
    )

    messages = build_tab2_ai_review_messages(request)
    combined = "\n".join(message["content"] for message in messages)

    assert "read-only advisory correction plan" in combined
    assert "Do not apply corrections" in combined
    assert "do not run Correct" in combined
    assert "do not create a patch" in combined


def test_prompt_text_is_bounded_with_notice() -> None:
    """Long Tab 2 output is truncated with an explicit notice."""
    text = "x" * 5000

    limited = limit_text_for_model(text, 1200)

    assert len(limited) <= 1200
    assert "Input truncated" in limited


if __name__ == "__main__":
    test_check_prompt_preserves_deterministic_authority()
    test_correction_prompt_is_read_only()
    test_prompt_text_is_bounded_with_notice()
    print("Tab 2 AI review prompt builder tests passed.")
