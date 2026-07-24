# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_openai_compatible_provider_runtime.py
"""OpenAI-compatible local AI docstring provider for Tab 3.

The Tab 3 adapter preserves its frozen provider contract while delegating the
actual OpenAI-compatible HTTP request to KANDA's shared provider runtime.  This
keeps one canonical transport for local-compatible and web-gateway clients.
"""

from __future__ import annotations

from typing import Callable

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
    build_openai_compatible_messages,
    normalize_ai_docstring_output,
)
from kanda_reasoner_app.web_ai_provider_contracts import GatewayProfile, ProviderError
from kanda_reasoner_app.web_ai_provider_runtime import request_chat_completion

__all__ = [
    "AI_OPENAI_COMPATIBLE_PROVIDER_CONTRACT",
    "build_local_openai_compatible_provider",
    "local_openai_compatible_provider_from_owner",
    "local_openai_compatible_profile",
]

AI_OPENAI_COMPATIBLE_PROVIDER_CONTRACT = "tab3_local_openai_compatible_provider_v1"
DEFAULT_TIMEOUT_SECONDS = 45.0
DEFAULT_MAX_TOKENS = 512
DEFAULT_TEMPERATURE = 0.0


def local_openai_compatible_provider_from_owner(
    owner: object,
) -> Callable[[AIProviderRequest], AIProviderResult] | None:
    """Return a local OpenAI-compatible provider from Tab 3 controls."""
    try:
        from kanda_reasoner_app.local_ai_configuration import (
            application_local_ai_configuration,
        )

        snapshot = application_local_ai_configuration().snapshot()
        base_url = snapshot.base_url
        model = snapshot.model_id
    except RuntimeError:
        base_url = _owner_text(
            owner,
            ("_base_url_edit", "ai_base_url_edit", "base_url_edit", "base_url_combo"),
        )
        model = _owner_text(
            owner,
            ("_model_combo", "ai_model_combo", "model_combo", "model_edit"),
        )
    if not base_url or not model:
        return None
    return build_local_openai_compatible_provider(
        base_url=base_url,
        model=model,
        timeout_seconds=_owner_number(
            owner,
            ("_ai_timeout_spin", "timeout_spin"),
            DEFAULT_TIMEOUT_SECONDS,
        ),
        max_tokens=int(
            _owner_number(
                owner,
                ("_ai_max_tokens_spin", "max_tokens_spin"),
                DEFAULT_MAX_TOKENS,
            )
        ),
        temperature=_owner_number(
            owner,
            ("_ai_temperature_spin", "temperature_spin"),
            DEFAULT_TEMPERATURE,
        ),
    )


def local_openai_compatible_profile(base_url: str) -> GatewayProfile:
    """Return a no-auth profile for one configured local endpoint."""
    clean_url = str(base_url or "").strip().rstrip("/")
    suffix = "/chat/completions"
    if clean_url.endswith(suffix):
        clean_url = clean_url[: -len(suffix)]
    return GatewayProfile(
        gateway_id="local_openai_compatible",
        display_name="Local OpenAI-Compatible",
        base_url=clean_url,
        models_path="models",
        chat_path="chat/completions",
        api_key_env="",
        api_key_required=False,
        anonymous_free_allowed=True,
        privacy_summary="Local endpoint configured globally in Config AI.",
    )


def build_local_openai_compatible_provider(
    base_url: str,
    model: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    opener: Callable[..., object] | None = None,
) -> Callable[[AIProviderRequest], AIProviderResult]:
    """Build the frozen Tab 3 provider over the shared transport."""
    clean_base_url = str(base_url or "").strip()
    clean_model = str(model or "").strip()

    def _provider(request: AIProviderRequest) -> AIProviderResult:
        if not clean_base_url:
            return _failed_result("Local AI base URL is empty.")
        if not clean_model:
            return _failed_result("Local AI model is empty.")
        try:
            result = request_chat_completion(
                local_openai_compatible_profile(clean_base_url),
                clean_model,
                build_openai_compatible_messages(request),
                request_id="tab3-docstring",
                timeout_seconds=max(1.0, float(timeout_seconds)),
                max_tokens=max(1, int(max_tokens)),
                temperature=float(temperature),
                opener=opener,
            )
        except (ProviderError, OSError, TimeoutError, ValueError, TypeError) as exc:
            return _failed_result("Local AI request failed: " + exc.__class__.__name__)
        body = normalize_ai_docstring_output(result.content)
        if not body:
            return _failed_result("Local AI returned no usable docstring.")
        return AIProviderResult(
            provider_name="local_openai_compatible",
            success=True,
            docstring_body=body,
            status="ai_draft_generated",
            error_message="",
            used_fallback=False,
        )

    return _provider


def _failed_result(message: str) -> AIProviderResult:
    """Return one failed provider result for fallback handling."""
    return AIProviderResult(
        provider_name="local_openai_compatible",
        success=False,
        docstring_body="",
        status=message,
        error_message=message,
        used_fallback=False,
    )


def _owner_text(owner: object, names: tuple[str, ...]) -> str:
    """Return text/currentText from the first matching owner widget."""
    for name in names:
        widget = getattr(owner, name, None)
        if widget is None:
            continue
        for method_name in ("currentText", "text"):
            method = getattr(widget, method_name, None)
            if not callable(method):
                continue
            try:
                value = str(method() or "").strip()
            except Exception:
                value = ""
            if value:
                return value
    return ""


def _owner_number(owner: object, names: tuple[str, ...], default: float) -> float:
    """Return a numeric value from the first matching owner widget."""
    for name in names:
        widget = getattr(owner, name, None)
        if widget is None:
            continue
        value_method = getattr(widget, "value", None)
        if callable(value_method):
            try:
                return float(value_method())
            except (TypeError, ValueError):
                pass
        text_method = getattr(widget, "text", None)
        if callable(text_method):
            try:
                return float(str(text_method()).strip())
            except (TypeError, ValueError):
                pass
    return float(default)
