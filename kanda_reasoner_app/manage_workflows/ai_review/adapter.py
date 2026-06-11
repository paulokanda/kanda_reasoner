"""Local model adapter for Tab 2 advisory AI review."""

from __future__ import annotations

import importlib
from typing import Any, Callable

from .formatter import format_tab2_advisory_review_text
from .models import Tab2AIReviewRequest, Tab2AIReviewResult
from .review_message_builder import build_tab2_ai_review_messages

__all__ = ["Tab2AIReviewAdapter"]

MODEL_REGISTRY_MODULE = "kanda_reasoner_app.reasoner_engine.v10_model_registry"
MODEL_REGISTRY_CLASS = "LocalModelRegistry"
LOCAL_AI_MODULE = "kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models"
LOCAL_AI_CLASS = "V9QwenAIModels"


def _load_class(module_name: str, class_name: str) -> type[Any]:
    """Load a class through an explicit late-bound handoff contract."""
    module = importlib.import_module(module_name)
    loaded = getattr(module, class_name)
    if not isinstance(loaded, type):
        raise TypeError(module_name + "." + class_name + " is not a class")
    return loaded


class Tab2AIReviewAdapter:
    """Call the existing local AI runtime for Tab 2 advisory review."""

    def __init__(
        self,
        *,
        registry_factory: Callable[[], Any] | None = None,
        ai_factory: Callable[[], Any] | None = None,
    ) -> None:
        self._registry_factory = registry_factory
        self._ai_factory = ai_factory

    def _make_registry(self) -> Any:
        """Create the late-bound local model registry."""
        if self._registry_factory is not None:
            return self._registry_factory()
        registry_class = _load_class(MODEL_REGISTRY_MODULE, MODEL_REGISTRY_CLASS)
        return registry_class()

    def _make_ai(self) -> Any:
        """Create the late-bound local AI connector."""
        if self._ai_factory is not None:
            return self._ai_factory()
        ai_class = _load_class(LOCAL_AI_MODULE, LOCAL_AI_CLASS)
        return ai_class()

    def list_models(self) -> list[str]:
        """Return available local model names from the shared registry."""
        registry = self._make_registry()
        models = registry.list_models()
        return [str(model).strip() for model in models if str(model).strip()]

    def choose_model(self, requested_model: str = "") -> str:
        """Choose a model for advisory review from request or registry."""
        models = self.list_models()
        requested = str(requested_model or "").strip()
        if requested and requested in models:
            return requested
        if models:
            return models[0]
        return requested

    def review(self, request: Tab2AIReviewRequest) -> Tab2AIReviewResult:
        """Run one advisory review and return a safe result object."""
        if not request.check_output_text.strip():
            return Tab2AIReviewResult(
                success=False,
                text="",
                model_name="",
                error_message="No Tab 2 Check/Correct output is available.",
            )

        model_name = self.choose_model(request.model_name)
        if not model_name:
            return Tab2AIReviewResult(
                success=False,
                text="",
                model_name="",
                error_message=(
                    "No local Ollama model is available. Run Tab 7 Refresh Models "
                    "or install a local Ollama model."
                ),
            )

        messages = build_tab2_ai_review_messages(request)
        try:
            ai = self._make_ai()
            response_text = ai.chat(
                messages,
                model=model_name,
                temperature=0.05,
                max_tokens=1500,
                use_cache=False,
            )
        except Exception as exc:
            return Tab2AIReviewResult(
                success=False,
                text="",
                model_name=model_name,
                error_message="AI review failed: " + str(exc),
            )

        return Tab2AIReviewResult(
            success=True,
            text=format_tab2_advisory_review_text(
                response_text,
                model_name,
                request.review_kind,
            ),
            model_name=model_name,
            error_message="",
        )
