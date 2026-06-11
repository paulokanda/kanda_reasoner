"""OpenAI-compatible local AI docstring provider for Tab 3."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Callable

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
    build_openai_compatible_messages,
    normalize_ai_docstring_output,
)

__all__ = [
    "AI_OPENAI_COMPATIBLE_PROVIDER_CONTRACT",
    "build_local_openai_compatible_provider",
    "local_openai_compatible_provider_from_owner",
]

AI_OPENAI_COMPATIBLE_PROVIDER_CONTRACT = "tab3_local_openai_compatible_provider_v1"
DEFAULT_TIMEOUT_SECONDS = 45.0
DEFAULT_MAX_TOKENS = 512
DEFAULT_TEMPERATURE = 0.0
UrlOpenCallable = Callable[..., object]


def local_openai_compatible_provider_from_owner(owner: object) -> Callable[[AIProviderRequest], AIProviderResult] | None:
    """Return a local OpenAI-compatible provider from Tab 3 Local AI controls."""
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
        timeout_seconds=_owner_number(owner, ("_ai_timeout_spin", "timeout_spin"), DEFAULT_TIMEOUT_SECONDS),
        max_tokens=int(_owner_number(owner, ("_ai_max_tokens_spin", "max_tokens_spin"), DEFAULT_MAX_TOKENS)),
        temperature=_owner_number(owner, ("_ai_temperature_spin", "temperature_spin"), DEFAULT_TEMPERATURE),
    )


def build_local_openai_compatible_provider(
    base_url: str,
    model: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    opener: UrlOpenCallable | None = None,
) -> Callable[[AIProviderRequest], AIProviderResult]:
    """Build a provider callable for one OpenAI-compatible chat endpoint."""
    clean_base_url = str(base_url or "").strip()
    clean_model = str(model or "").strip()
    active_opener = opener or urllib.request.urlopen

    def _provider(request: AIProviderRequest) -> AIProviderResult:
        if not clean_base_url:
            return _failed_result("Local AI base URL is empty.")
        if not clean_model:
            return _failed_result("Local AI model is empty.")
        payload = {
            "model": clean_model,
            "messages": build_openai_compatible_messages(request),
            "temperature": float(temperature),
            "max_tokens": max(1, int(max_tokens)),
        }
        try:
            text = _post_chat_completion(
                clean_base_url,
                payload,
                active_opener,
                max(1.0, float(timeout_seconds)),
            )
        except (
            OSError,
            TimeoutError,
            ValueError,
            urllib.error.URLError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ) as exc:
            return _failed_result("Local AI request failed: " + exc.__class__.__name__)
        body = normalize_ai_docstring_output(text)
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


def _post_chat_completion(
    base_url: str,
    payload: dict,
    opener: UrlOpenCallable,
    timeout_seconds: float,
) -> str:
    """Post one chat-completions request and return the message content."""
    url = _chat_completions_url(base_url)
    data = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with opener(request, timeout=timeout_seconds) as response:
        raw = response.read().decode("utf-8", errors="replace")
    body = json.loads(raw)
    return _extract_chat_content(body)


def _extract_chat_content(body: dict) -> str:
    """Extract chat content from common OpenAI-compatible response shapes."""
    choices = body.get("choices") or []
    if not choices:
        return ""
    first = choices[0]
    if not isinstance(first, dict):
        return ""
    message = first.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if content is not None:
            return str(content).strip()
    text = first.get("text")
    if text is not None:
        return str(text).strip()
    return ""


def _chat_completions_url(base_url: str) -> str:
    """Return a chat-completions URL from a base endpoint."""
    url = str(base_url or "").strip().rstrip("/")
    if not url:
        return ""
    if url.endswith("/chat/completions"):
        return url
    return url + "/chat/completions"


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
