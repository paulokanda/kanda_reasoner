# project-path: tools/validate_project_web_ai_provider_response_recovery_v1.py
"""Validate Project Web AI provider response recovery and diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from threading import Event
from typing import Iterable

FEATURE_ID = "project-web-ai-provider-response-recovery-v1"
TOUCHED_CODE = (
    "kanda_reasoner_app/web_ai_provider_runtime.py",
    "kanda_reasoner_app/web_ai_response_normalization.py",
    "kanda_reasoner_app/web_ai_stream_runtime.py",
    "kanda_reasoner_app/web_ai_model_catalog.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py",
    "tools/validate_project_web_ai_provider_response_recovery_v1.py",
)


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


class _Headers:
    """Minimal HTTP headers fixture."""

    def __init__(self, content_type: str) -> None:
        self._content_type = content_type

    def get(self, key: str, default: str = "") -> str:
        """Return the controlled content type."""
        if str(key).lower() == "content-type":
            return self._content_type
        return default


class _Response:
    """Context-managed streaming or JSON response fixture."""

    def __init__(
        self,
        *,
        lines: Iterable[bytes] = (),
        body: bytes = b"",
        content_type: str = "application/json",
    ) -> None:
        self._lines = tuple(lines)
        self._body = bytes(body)
        self.headers = _Headers(content_type)

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def __iter__(self):
        return iter(self._lines)

    def read(self, maximum: int = -1) -> bytes:
        if maximum < 0:
            return self._body
        return self._body[:maximum]


class _SequencedOpener:
    """Return controlled responses and record request bodies."""

    def __init__(self, responses: Iterable[_Response]) -> None:
        self._responses = list(responses)
        self.bodies: list[dict[str, object]] = []

    def __call__(self, request, **_kwargs):
        raw = bytes(getattr(request, "data", b"") or b"")
        self.bodies.append(json.loads(raw.decode("utf-8")) if raw else {})
        if not self._responses:
            raise AssertionError("unexpected extra provider request")
        return self._responses.pop(0)


def _sse(payload: dict[str, object]) -> bytes:
    """Return one SSE data line."""
    return ("data: " + json.dumps(payload) + "\n").encode("utf-8")


def _validate_normalization(root: Path) -> None:
    """Validate common structured content shapes."""
    from kanda_reasoner_app.web_ai_provider_runtime import request_chat_completion
    from kanda_reasoner_app.web_ai_provider_contracts import get_gateway_profile

    payload = {
        "id": "non-stream-1",
        "model": "example/model",
        "choices": [
            {
                "message": {
                    "content": [
                        {"type": "text", "text": "Hello"},
                        {"type": "output_text", "text": " world"},
                    ]
                },
                "finish_reason": "stop",
            }
        ],
    }
    result = request_chat_completion(
        get_gateway_profile("kilo"),
        "example/model",
        [{"role": "user", "content": "hello"}],
        opener=_SequencedOpener(
            [_Response(body=json.dumps(payload).encode("utf-8"))]
        ),
    )
    require(result.content == "Hello world", "structured content was not normalized")
    print("STRUCTURED_NON_STREAM_CONTENT_NORMALIZED: PASS")

    source = (root / "kanda_reasoner_app/web_ai_response_normalization.py").read_text(
        encoding="utf-8"
    )
    require("output_text" in source, "output_text content shape is unsupported")
    require("Sequence" in source, "content array normalization is missing")
    print("COMMON_PROVIDER_CONTENT_SHAPES: PASS")


def _validate_empty_stream_fallback() -> None:
    """Validate one bounded non-stream fallback after an empty stream."""
    from kanda_reasoner_app.web_ai_provider_contracts import get_gateway_profile
    from kanda_reasoner_app.web_ai_provider_runtime import stream_chat_completion

    stream_lines = (
        _sse(
            {
                "id": "stream-1",
                "model": "example/model",
                "choices": [
                    {
                        "delta": {"reasoning": "hidden reasoning only"},
                        "finish_reason": "stop",
                    }
                ],
            }
        ),
        b"data: [DONE]\n",
    )
    fallback_payload = {
        "id": "fallback-1",
        "model": "example/model",
        "choices": [
            {
                "message": {"content": "Fallback answer"},
                "finish_reason": "stop",
            }
        ],
        "usage": {"total_tokens": 8},
    }
    opener = _SequencedOpener(
        [
            _Response(lines=stream_lines, content_type="text/event-stream"),
            _Response(body=json.dumps(fallback_payload).encode("utf-8")),
        ]
    )
    tokens: list[str] = []
    messages = [{"role": "user", "content": "Can you access files?"}]
    result = stream_chat_completion(
        get_gateway_profile("kilo"),
        "example/model",
        messages,
        request_id="request-1",
        on_token=tokens.append,
        opener=opener,
    )
    require(result.content == "Fallback answer", "fallback content mismatch")
    require(len(opener.bodies) == 2, "fallback request count mismatch")
    require(opener.bodies[0].get("stream") is True, "first request was not streaming")
    require(opener.bodies[1].get("stream") is False, "fallback was not non-streaming")
    require(
        opener.bodies[0].get("messages") == opener.bodies[1].get("messages"),
        "fallback changed the approved messages",
    )
    require(tokens == [], "empty stream emitted phantom text tokens")
    transport = result.raw_metadata.get("kanda_transport", {})
    require(
        isinstance(transport, dict)
        and transport.get("mode") == "non_stream_fallback",
        "fallback transport provenance is missing",
    )
    require(transport.get("stream_sse_events") == 1, "SSE event count mismatch")
    require(transport.get("stream_text_chunks") == 0, "text chunk count mismatch")
    print("EMPTY_STREAM_NON_STREAM_FALLBACK: PASS")
    print("FALLBACK_REUSES_APPROVED_REQUEST: PASS")
    print("FALLBACK_TRANSPORT_PROVENANCE: PASS")


def _validate_failure_diagnostics() -> None:
    """Validate safe actionable diagnostics when fallback also fails."""
    from kanda_reasoner_app.web_ai_provider_contracts import (
        ProviderCancelledError,
        ProviderResponseError,
        get_gateway_profile,
    )
    from kanda_reasoner_app.web_ai_provider_runtime import stream_chat_completion

    empty_stream = _Response(
        lines=(b"data: [DONE]\n",),
        content_type="application/json",
    )
    empty_payload = {
        "id": "fallback-empty",
        "choices": [{"message": {"content": ""}, "finish_reason": "stop"}],
    }
    opener = _SequencedOpener(
        [empty_stream, _Response(body=json.dumps(empty_payload).encode("utf-8"))]
    )
    try:
        stream_chat_completion(
            get_gateway_profile("kilo"),
            "example/model",
            [{"role": "user", "content": "sensitive question"}],
            opener=opener,
        )
    except ProviderResponseError as exc:
        message = str(exc)
    else:
        raise AssertionError("double-empty provider response was accepted")
    require("content_type=application/json" in message, "content type missing")
    require("sse_events=0" in message, "SSE count missing")
    require("non_stream_fallback=failed" in message, "fallback status missing")
    require("sensitive question" not in message, "request content leaked to diagnostics")
    print("EMPTY_STREAM_ACTIONABLE_DIAGNOSTICS: PASS")
    print("PROVIDER_DIAGNOSTICS_REDACT_REQUEST_CONTENT: PASS")

    cancel_event = Event()
    cancel_event.set()
    cancel_opener = _SequencedOpener(
        [_Response(lines=(_sse({"choices": []}),), content_type="text/event-stream")]
    )
    try:
        stream_chat_completion(
            get_gateway_profile("kilo"),
            "example/model",
            [{"role": "user", "content": "cancel"}],
            cancel_event=cancel_event,
            opener=cancel_opener,
        )
    except ProviderCancelledError:
        pass
    else:
        raise AssertionError("cancelled stream was not rejected")
    require(len(cancel_opener.bodies) == 1, "cancelled request started fallback")
    print("CANCELLED_STREAM_DOES_NOT_FALLBACK: PASS")


def _validate_catalog_capabilities() -> None:
    """Validate streaming capability is derived from current metadata."""
    from kanda_reasoner_app.web_ai_model_catalog import fetch_gateway_models
    from kanda_reasoner_app.web_ai_provider_contracts import get_gateway_profile

    payload = {
        "data": [
            {"id": "explicit", "supports_streaming": True},
            {"id": "parameter", "supported_parameters": ["stream"]},
            {"id": "unknown"},
        ]
    }
    models = fetch_gateway_models(
        get_gateway_profile("kilo"),
        opener=_SequencedOpener(
            [_Response(body=json.dumps(payload).encode("utf-8"))]
        ),
    )
    by_id = {model.model_id: model for model in models}
    require(by_id["explicit"].supports_streaming, "explicit capability lost")
    require(by_id["parameter"].supports_streaming, "stream parameter ignored")
    require(not by_id["unknown"].supports_streaming, "unknown model was guessed")
    print("MODEL_STREAMING_CAPABILITY_FROM_METADATA: PASS")


def _validate_boundaries(root: Path) -> None:
    """Validate authority, provenance, compile, and module-size boundaries."""
    runtime = (root / "kanda_reasoner_app/web_ai_provider_runtime.py").read_text(
        encoding="utf-8"
    )
    stream_runtime = (root / "kanda_reasoner_app/web_ai_stream_runtime.py").read_text(
        encoding="utf-8"
    )
    conversations = (
        root
        / "kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py"
    ).read_text(encoding="utf-8")
    require("non_stream_request=request_chat_completion" in runtime, "fallback owner missing")
    require("write_file" not in stream_runtime, "remote write authority was introduced")
    require("subprocess" not in stream_runtime, "remote command authority was introduced")
    require("Transport mode:" in conversations, "transport provenance is not visible")
    print("REMOTE_AI_WRITE_AUTHORITY_UNCHANGED: PASS")
    print("PROJECT_WEB_AI_TRANSPORT_MODE_VISIBLE: PASS")

    for relative in TOUCHED_CODE:
        path = root / relative
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        require(len(source.splitlines()) <= 500, relative + " exceeds 500 lines")
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run focused validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    sys.path.insert(0, str(root))

    _validate_normalization(root)
    _validate_empty_stream_fallback()
    _validate_failure_diagnostics()
    _validate_catalog_capabilities()
    _validate_boundaries(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
