"""Tests for Tab 1 advisory AI review prompt building."""

from __future__ import annotations

from kanda_reasoner_app.manage_architecture.ai_review.models import (
    ADVISORY_BANNER,
    Tab1AIReviewRequest,
)
from kanda_reasoner_app.manage_architecture.ai_review.review_message_builder import (
    TRUNCATION_NOTE,
    build_tab1_ai_review_messages,
    limit_audit_text,
    mark_project_root,
)


def test_project_root_is_marked_in_audit_text() -> None:
    """Absolute project roots are replaced with the project root marker."""
    text = 'ERROR PATH E:\\developer_tools\\ask_' 'ai_project_reasoner' '\\file.py'

    marked = mark_project_root(text, r"E:\developer_tools")

    assert "<PROJECT_ROOT>" in marked
    assert r"E:\developer_tools" not in marked


def test_long_audit_text_is_bounded_with_visible_note() -> None:
    """Long audit text is truncated with an explicit visible note."""
    bounded, truncated = limit_audit_text("A" * 100 + "B" * 100, 80)

    assert truncated is True
    assert len(bounded) <= 80
    assert TRUNCATION_NOTE in bounded


def test_prompt_includes_advisory_authority_contract() -> None:
    """Prompt messages preserve advisory-only authority rules."""
    request = Tab1AIReviewRequest(
        audit_text="WARNING TEST_CODE path.py :: example warning",
        project_root=r"E:\developer_tools",
        max_audit_chars=4000,
    )

    messages = build_tab1_ai_review_messages(request)
    joined = "\n".join(str(message["content"]) for message in messages)

    assert ADVISORY_BANNER in joined
    assert "deterministic First Check remains authoritative" in joined
    assert "Suggested next inspection files" in joined
    assert "WARNING TEST_CODE" in joined


if __name__ == "__main__":
    test_project_root_is_marked_in_audit_text()
    test_long_audit_text_is_bounded_with_visible_note()
    test_prompt_includes_advisory_authority_contract()
    print("Tab 1 AI review prompt builder tests passed.")
