"""Tests for Tab 1 advisory AI review formatter."""

from __future__ import annotations

from kanda_reasoner_app.manage_architecture.ai_review.formatter import (
    format_advisory_review_text,
)
from kanda_reasoner_app.manage_architecture.ai_review.models import ADVISORY_BANNER


def test_formatter_forces_advisory_banner() -> None:
    """Formatted output always starts with the advisory banner."""
    text = format_advisory_review_text("model body", "qwen2.5-coder:7b")

    assert text.startswith(ADVISORY_BANNER)
    assert "Model: qwen2.5-coder:7b" in text
    assert "model body" in text
    assert "Deterministic First Check remains" in text


if __name__ == "__main__":
    test_formatter_forces_advisory_banner()
    print("Tab 1 AI review formatter tests passed.")
