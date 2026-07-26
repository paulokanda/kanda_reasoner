# project-path: kanda_reasoner_app/web_ai_stream_runtime.py
"""Streaming transport and non-stream recovery for KANDA web gateways."""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from threading import Event
from typing import Callable, Iterable, Mapping, Sequence

from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ChatUsage,
    GatewayProfile,
    ProviderAuthenticationError,
    ProviderCancelledError,
    ProviderConfigurationError,
    ProviderConnectionError,
    ProviderError,
    ProviderResponseError,
    ProviderTimeoutError,
)
from kanda_reasoner_app.web_ai_response_normalization import (
    extract_choice_content,
    response_content_type,
    safe_stream_diagnostics,
)

__all__ = ["execute_stream_chat_completion"]

UrlOpenCallable = Callable[..., object]
TokenCallback = Callable[[str], None]
UsageLoader = Callable[[Mapping[str, object]], ChatUsage]
PayloadErrorChecker = Callable[[Mapping[str, object]], None]
HttpErrorFactory = Callable[[urllib.error.HTTPError], ProviderError]
NonStreamRequest = Callable[..., ChatResult]

MAX_SSE_LINE_BYTES = 2 * 1024 * 1024
MAX_STREAM_CONTENT_BYTES = 8 * 1024 * 1024


def _sse_payloads(
    response: object,
    cancel_event: Event | None,
    payload_error_checker: PayloadErrorChecker,
) -> Iterable[Mapping[str, object]]:
    """Yield bounded JSON objects from an SSE response."""
    iterator = getattr(response, "__iter__", None)
    if not callable(iterator):
        raise ProviderResponseError("Streaming response is not iterable.")
    for raw_line in response:
        if cancel_event is not None and cancel_event.is_set():
            raise ProviderCancelledError("Request cancelled by user.")
        raw_bytes = bytes(raw_line)
        if len(raw_bytes) > MAX_SSE_LINE_BYTES:
            raise ProviderResponseError("Gateway SSE line exceeded the byte limit.")
        line = raw_bytes.decode("utf-8", errors="replace").strip()
        if not line or line.startswith(":") or not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        try:
            payload = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ProviderResponseError("Gateway returned malformed SSE JSON.") from exc
        if not isinstance(payload, dict):
            raise ProviderResponseError("Gateway SSE event must be a JSON object.")
        payload_error_checker(payload)
        yield payload


def _fallback_result(
    *,
    profile: GatewayProfile,
    clean_model: str,
    messages: Sequence[Mapping[str, str]],
    api_key: str,
    request_id: str,
    timeout_seconds: float,
    max_tokens: int,
    temperature: float,
    active_opener: UrlOpenCallable,
    non_stream_request: NonStreamRequest,
    stream_content_type: str,
    sse_events: int,
    choice_events: int,
    text_chunks: int,
    finish_reason: str,
) -> ChatResult:
    """Retry once without streaming and retain safe transport provenance."""
    try:
        fallback = non_stream_request(
            profile,
            clean_model,
            messages,
            api_key,
            request_id=request_id,
            timeout_seconds=timeout_seconds,
            max_tokens=max_tokens,
            temperature=temperature,
            opener=active_opener,
        )
    except ProviderCancelledError:
        raise
    except ProviderError as exc:
        fallback_status = exc.__class__.__name__ + ": " + str(exc)
        diagnostics = safe_stream_diagnostics(
            content_type=stream_content_type,
            sse_events=sse_events,
            choice_events=choice_events,
            text_chunks=text_chunks,
            finish_reason=finish_reason,
            fallback_status="failed " + fallback_status,
        )
        raise exc.__class__(
            "Gateway stream returned no usable content and the automatic "
            "non-streaming retry failed. " + diagnostics
        ) from exc

    metadata = dict(fallback.raw_metadata)
    metadata["kanda_transport"] = {
        "mode": "non_stream_fallback",
        "stream_content_type": stream_content_type,
        "stream_sse_events": sse_events,
        "stream_choice_events": choice_events,
        "stream_text_chunks": text_chunks,
        "stream_finish_reason": finish_reason,
    }
    return ChatResult(
        request_id=fallback.request_id,
        gateway_id=fallback.gateway_id,
        requested_model=fallback.requested_model,
        returned_model=fallback.returned_model,
        content=fallback.content,
        finish_reason=fallback.finish_reason,
        response_id=fallback.response_id,
        usage=fallback.usage,
        raw_metadata=metadata,
    )


def execute_stream_chat_completion(
    profile: GatewayProfile,
    model_id: str,
    messages: Sequence[Mapping[str, str]],
    api_key: str = "",
    *,
    request_id: str = "",
    cancel_event: Event | None = None,
    on_token: TokenCallback | None = None,
    timeout_seconds: float,
    max_tokens: int,
    temperature: float,
    allow_non_stream_fallback: bool,
    opener: UrlOpenCallable | None,
    usage_loader: UsageLoader,
    payload_error_checker: PayloadErrorChecker,
    http_error_factory: HttpErrorFactory,
    non_stream_request: NonStreamRequest,
) -> ChatResult:
    """Execute a stream and retry once without streaming when it is empty."""
    clean_model = str(model_id or "").strip()
    if not clean_model:
        raise ProviderConfigurationError("A model must be selected.")
    if profile.api_key_required and not str(api_key or "").strip():
        raise ProviderAuthenticationError(profile.display_name + " requires an API key.")

    body = {
        "model": clean_model,
        "messages": [dict(message) for message in messages],
        "stream": True,
        "stream_options": {"include_usage": True},
        "temperature": float(temperature),
        "max_tokens": max(1, int(max_tokens)),
    }
    request = urllib.request.Request(
        profile.chat_url(),
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers=profile.headers(api_key) | {"Accept": "text/event-stream"},
        method="POST",
    )
    active_opener = opener or urllib.request.urlopen
    content_parts: list[str] = []
    content_bytes = 0
    usage = ChatUsage()
    returned_model = clean_model
    finish_reason = ""
    response_id = ""
    last_payload: Mapping[str, object] = {}
    stream_content_type = "unknown"
    sse_events = 0
    choice_events = 0
    text_chunks = 0

    try:
        with active_opener(request, timeout=max(1.0, float(timeout_seconds))) as response:
            stream_content_type = response_content_type(response)
            for payload in _sse_payloads(
                response,
                cancel_event,
                payload_error_checker,
            ):
                sse_events += 1
                last_payload = payload
                response_id = str(payload.get("id") or response_id)
                returned_model = str(payload.get("model") or returned_model)
                current_usage = usage_loader(payload)
                if current_usage.total_tokens or current_usage.cost_usd is not None:
                    usage = current_usage
                choices = payload.get("choices")
                if not isinstance(choices, list) or not choices:
                    continue
                first = choices[0]
                if not isinstance(first, dict):
                    continue
                choice_events += 1
                token = extract_choice_content(first)
                if token:
                    text_chunks += 1
                    content_bytes += len(token.encode("utf-8"))
                    if content_bytes > MAX_STREAM_CONTENT_BYTES:
                        raise ProviderResponseError(
                            "Gateway stream exceeded the content byte limit."
                        )
                    content_parts.append(token)
                    if on_token is not None:
                        on_token(token)
                reason = first.get("finish_reason")
                if reason:
                    finish_reason = str(reason)
                    if finish_reason == "error":
                        raise ProviderResponseError(
                            "Gateway stream ended with an error finish reason."
                        )
    except urllib.error.HTTPError as exc:
        raise http_error_factory(exc) from exc
    except ProviderError:
        raise
    except (socket.timeout, TimeoutError) as exc:
        raise ProviderTimeoutError("Gateway stream timed out.") from exc
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        if isinstance(reason, (socket.timeout, TimeoutError)):
            raise ProviderTimeoutError("Gateway stream timed out.") from exc
        raise ProviderConnectionError("Gateway stream failed: " + str(reason)) from exc
    except OSError as exc:
        raise ProviderConnectionError("Gateway stream failed: " + str(exc)) from exc

    if cancel_event is not None and cancel_event.is_set():
        raise ProviderCancelledError("Request cancelled by user.")
    content = "".join(content_parts)
    if not content.strip():
        if allow_non_stream_fallback:
            return _fallback_result(
                profile=profile,
                clean_model=clean_model,
                messages=messages,
                api_key=api_key,
                request_id=request_id,
                timeout_seconds=timeout_seconds,
                max_tokens=max_tokens,
                temperature=temperature,
                active_opener=active_opener,
                non_stream_request=non_stream_request,
                stream_content_type=stream_content_type,
                sse_events=sse_events,
                choice_events=choice_events,
                text_chunks=text_chunks,
                finish_reason=finish_reason,
            )
        diagnostics = safe_stream_diagnostics(
            content_type=stream_content_type,
            sse_events=sse_events,
            choice_events=choice_events,
            text_chunks=text_chunks,
            finish_reason=finish_reason,
            fallback_status="disabled",
        )
        raise ProviderResponseError(
            "Gateway stream returned no usable content. " + diagnostics
        )

    metadata = dict(last_payload)
    metadata["kanda_transport"] = {
        "mode": "stream",
        "content_type": stream_content_type,
        "sse_events": sse_events,
        "choice_events": choice_events,
        "text_chunks": text_chunks,
    }
    return ChatResult(
        request_id=request_id,
        gateway_id=profile.gateway_id,
        requested_model=clean_model,
        returned_model=returned_model,
        content=content,
        finish_reason=finish_reason,
        response_id=response_id,
        usage=usage,
        raw_metadata=metadata,
    )
