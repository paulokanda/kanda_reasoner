"""Direct public import tests for Tab 2 AI review formatter."""

from __future__ import annotations

from kanda_reasoner_app.manage_workflows.ai_review.formatter import (
    format_tab2_advisory_review_text,
)


def test_formatter_public_contract_adds_advisory_banner() -> None:
    """Formatter output must clearly mark AI guidance as advisory."""
    text = format_tab2_advisory_review_text(
        response_text="review body",
        model_name="qwen3-coder:30b",
        review_kind="check",
    )

    assert text.startswith(
        "ADVISORY AI REVIEW - deterministic Tab 2 Check remains authoritative."
    )
    assert "Model: qwen3-coder:30b" in text
    assert "review body" in text
    assert "This AI review is read-only guidance." in text


if __name__ == "__main__":
    test_formatter_public_contract_adds_advisory_banner()
    print("Tab 2 AI review formatter public contract tests passed.")
