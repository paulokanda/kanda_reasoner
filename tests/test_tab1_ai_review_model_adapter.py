"""Tests for Tab 1 advisory AI review model adapter."""

from __future__ import annotations

from kanda_reasoner_app.manage_architecture.ai_review.adapter import (
    Tab1AIReviewAdapter,
)
from kanda_reasoner_app.manage_architecture.ai_review.models import (
    ADVISORY_BANNER,
    Tab1AIReviewRequest,
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
        return "1. Advisory summary\nThe audit has one warning."


def test_adapter_uses_available_model_and_forces_advisory_banner() -> None:
    """Adapter calls the shared model path and formats advisory output."""
    adapter = Tab1AIReviewAdapter(
        registry_factory=lambda: FakeRegistry(["qwen2.5-coder:7b"]),
        ai_factory=FakeAI,
    )
    request = Tab1AIReviewRequest(
        audit_text="WARNING MIXED_RESPONSIBILITY_FILE path.py :: warning",
        project_root=r"E:\developer_tools",
    )

    result = adapter.review(request)

    assert result.success is True
    assert result.model_name == "qwen2.5-coder:7b"
    assert FakeAI.last_model == "qwen2.5-coder:7b"
    assert result.text.startswith(ADVISORY_BANNER)
    assert "Deterministic First Check remains" in result.text


def test_adapter_returns_safe_result_when_no_models_are_available() -> None:
    """No-model state returns a safe unavailable result."""
    adapter = Tab1AIReviewAdapter(
        registry_factory=lambda: FakeRegistry([]),
        ai_factory=FakeAI,
    )
    request = Tab1AIReviewRequest(audit_text="WARNING CODE file.py :: warning")

    result = adapter.review(request)

    assert result.success is False
    assert "No local Ollama model" in result.error_message


def test_adapter_rejects_empty_audit_text_without_model_call() -> None:
    """Empty audit text returns a clear user-facing error."""
    adapter = Tab1AIReviewAdapter(
        registry_factory=lambda: FakeRegistry(["qwen2.5-coder:7b"]),
        ai_factory=FakeAI,
    )
    request = Tab1AIReviewRequest(audit_text="")

    result = adapter.review(request)

    assert result.success is False
    assert "No Tab 1 audit output" in result.error_message


if __name__ == "__main__":
    test_adapter_uses_available_model_and_forces_advisory_banner()
    test_adapter_returns_safe_result_when_no_models_are_available()
    test_adapter_rejects_empty_audit_text_without_model_call()
    print("Tab 1 AI review model adapter tests passed.")
