# project-path: kanda_reasoner_app/manage_architecture/ai_review/adapter.py
"""Local model adapter for Tab 1 advisory AI review."""

from __future__ import annotations

import importlib
from typing import Any, Callable

from .formatter import format_advisory_review_text
from .models import Tab1AIReviewRequest, Tab1AIReviewResult
from .review_message_builder import build_tab1_ai_review_messages

__all__ = ["AUTO_MODEL_LABEL", "Tab1AIReviewAdapter"]

AUTO_MODEL_LABEL = "Auto (first available Ollama model)"
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


class Tab1AIReviewAdapter:
    """Call the existing local AI runtime for Tab 1 advisory review."""

    def __init__(
        self,
        *,
        registry_factory: Callable[[], Any] | None = None,
        ai_factory: Callable[[], Any] | None = None,
    ) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        registry_factory : Callable[[], Any] | None, optional
            The optional registry factory value.
        ai_factory : Callable[[], Any] | None, optional
            The optional ai factory value.
        """
        
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

    def chat_exact(
        self,
        messages: list[dict[str, str]],
        *,
        model_name: str,
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, str]:
        """Run raw chat with exactly one currently available selected model."""
        selected = str(model_name or "").strip()
        models = self.list_models()
        if not selected or selected not in models:
            raise RuntimeError(
                "Selected Ollama model is not available: "
                + selected
                + ". Refresh AI Models first."
            )
        ai = self._make_ai()
        response_text = ai.chat(
            messages,
            model=selected,
            temperature=temperature,
            max_tokens=max_tokens,
            use_cache=False,
        )
        return str(response_text or ""), selected

    def review(self, request: Tab1AIReviewRequest) -> Tab1AIReviewResult:
        """Run one advisory review and return a safe result object."""
        if not request.audit_text.strip():
            return Tab1AIReviewResult(
                success=False,
                text="",
                model_name="",
                error_message="No Tab 1 audit output is available.",
            )

        model_name = self.choose_model(request.model_name)
        if not model_name:
            return Tab1AIReviewResult(
                success=False,
                text="",
                model_name="",
                error_message=(
                    "No local Ollama model is available. Run Tab 7 Refresh Models "
                    "or install a local Ollama model."
                ),
            )

        messages = build_tab1_ai_review_messages(request)
        try:
            ai = self._make_ai()
            response_text = ai.chat(
                messages,
                model=model_name,
                temperature=0.05,
                max_tokens=1400,
                use_cache=False,
            )
        except Exception as exc:
            return Tab1AIReviewResult(
                success=False,
                text="",
                model_name=model_name,
                error_message="AI review failed: " + str(exc),
            )

        return Tab1AIReviewResult(
            success=True,
            text=format_advisory_review_text(response_text, model_name),
            model_name=model_name,
            error_message="",
        )
