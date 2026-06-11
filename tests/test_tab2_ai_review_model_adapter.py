"""Tests for Tab 2 advisory AI review model adapter."""

from __future__ import annotations

from kanda_reasoner_app.manage_workflows.ai_review.adapter import (
    Tab2AIReviewAdapter,
)
from kanda_reasoner_app.manage_workflows.ai_review.models import (
    CHECK_ADVISORY_BANNER,
    CORRECTION_ADVISORY_BANNER,
    Tab2AIReviewRequest,
)


class FakeRegistry:
    """Fake local model registry for adapter tests."""

    def __init__(self, models: list[str]) -> None:
        self._models = models

    def list_models(self) -> list[str]:
        """Return fake local models."""
        return list(self._models)


class FakeAI:
    """Fake local AI connector for adapter tests."""

    last_model = ""
    last_messages: list[dict[str, object]] = []

    def chat(
        self,
        messages: list[dict[str, object]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
    ) -> str:
        """Return a deterministic fake AI response."""
        FakeAI.last_model = str(model or "")
        FakeAI.last_messages = messages
        return "1. Advisory summary\nThe workflow check has one warning."


def test_adapter_formats_check_review_with_advisory_banner() -> None:
    """Adapter calls the shared model path for Check review."""
    adapter = Tab2AIReviewAdapter(
        registry_factory=lambda: FakeRegistry(["qwen2.5-coder:7b"]),
        ai_factory=FakeAI,
    )
    request = Tab2AIReviewRequest(
        review_kind="check",
        check_output_text="WARNING workflow file.py :: warning",
        model_name="qwen2.5-coder:7b",
    )

    result = adapter.review(request)

    assert result.success is True
    assert result.model_name == "qwen2.5-coder:7b"
    assert FakeAI.last_model == "qwen2.5-coder:7b"
    assert result.text.startswith(CHECK_ADVISORY_BANNER)
    assert "read-only guidance" in result.text


def test_adapter_formats_correction_plan_with_advisory_banner() -> None:
    """Adapter formats correction plan as advisory only."""
    adapter = Tab2AIReviewAdapter(
        registry_factory=lambda: FakeRegistry(["qwen3-coder:30b"]),
        ai_factory=FakeAI,
    )
    request = Tab2AIReviewRequest(
        review_kind="correction_plan",
        check_output_text="Diff output here",
    )

    result = adapter.review(request)

    assert result.success is True
    assert result.model_name == "qwen3-coder:30b"
    assert result.text.startswith(CORRECTION_ADVISORY_BANNER)


def test_adapter_returns_safe_result_when_no_models_are_available() -> None:
    """No-model state returns a safe unavailable result."""
    adapter = Tab2AIReviewAdapter(
        registry_factory=lambda: FakeRegistry([]),
        ai_factory=FakeAI,
    )
    request = Tab2AIReviewRequest(
        review_kind="check",
        check_output_text="WARNING CODE file.py :: warning",
    )

    result = adapter.review(request)

    assert result.success is False
    assert "No local Ollama model" in result.error_message


if __name__ == "__main__":
    test_adapter_formats_check_review_with_advisory_banner()
    test_adapter_formats_correction_plan_with_advisory_banner()
    test_adapter_returns_safe_result_when_no_models_are_available()
    print("Tab 2 AI review model adapter tests passed.")
