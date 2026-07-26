# project-path: tools/validate_project_web_ai_agent_empty_response_recovery_v1.py
"""Validate bounded empty-response recovery for Project Web AI agent turns."""

from __future__ import annotations

import argparse
import py_compile
import tempfile
from pathlib import Path
from threading import Event

from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.reasoner_engine import project_web_ai_agent_runtime
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ChatUsage,
    GatewayProfile,
    ProviderCancelledError,
    ProviderResponseError,
    ProjectWebAIRequestIdentity,
)

FEATURE_ID = "project-web-ai-agent-empty-response-recovery-v1"
TOUCHED = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py",
    "tools/validate_project_web_ai_agent_empty_response_recovery_v1.py",
)


def require(condition: object, marker: str) -> None:
    """Raise one focused failure or print the marker."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _profile() -> GatewayProfile:
    """Return one local provider fixture."""
    return GatewayProfile(
        gateway_id="fixture",
        display_name="Fixture",
        base_url="https://example.invalid/v1",
        models_path="models",
        chat_path="chat/completions",
        api_key_env="",
        api_key_required=False,
        anonymous_free_allowed=True,
        privacy_summary="fixture",
    )


def _identity(root: Path) -> ProjectWebAIRequestIdentity:
    """Return one exact request identity for the disposable Project."""
    boundary = resolve_project_tool_boundary_identity(root)
    return ProjectWebAIRequestIdentity(
        request_id="request-agent-empty",
        session_id="session-agent-empty",
        project_id=boundary.active_project_id,
        project_slug=boundary.active_project_slug,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        support_root=str(boundary.active_project_support_root),
        snapshot_id="snapshot-agent-empty",
        context_hash="context-agent-empty",
        gateway_id="fixture",
        model_id="fixture-model",
        privacy_approval_id="approval-agent-empty",
        created_at_utc="2026-07-23T00:00:00+00:00",
        project_epoch=3,
    )


def _result(content: str, mode: str = "") -> ChatResult:
    """Return one deterministic provider result."""
    metadata = {}
    if mode:
        metadata["kanda_transport"] = {"mode": mode}
    return ChatResult(
        request_id="request-agent-empty",
        gateway_id="fixture",
        requested_model="fixture-model",
        returned_model="fixture-model",
        content=content,
        finish_reason="stop",
        response_id="response-agent-empty",
        usage=ChatUsage(total_tokens=7, provider_name="fixture-provider"),
        raw_metadata=metadata,
    )


def validate_empty_non_stream_recovers_with_stream() -> None:
    """Prove one alternate-transport retry and preserved request identity."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_empty_") as temp:
        root = Path(temp)
        (root / "main.py").write_text("VALUE = 1\n", encoding="utf-8")
        non_stream_calls: list[object] = []
        stream_calls: list[object] = []
        original_non_stream = project_web_ai_agent_runtime.request_chat_completion
        original_stream = project_web_ai_agent_runtime.stream_chat_completion

        def empty_non_stream(*args, **kwargs):
            non_stream_calls.append((args, kwargs))
            raise ProviderResponseError("Gateway returned an empty response.")

        def successful_stream(*args, **kwargs):
            stream_calls.append((args, kwargs))
            return _result("Recovered agent answer.", "stream")

        project_web_ai_agent_runtime.request_chat_completion = empty_non_stream
        project_web_ai_agent_runtime.stream_chat_completion = successful_stream
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                [{"role": "user", "content": "Inspect the Project."}],
                "",
                project_root=str(root),
                request_identity=_identity(root),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_non_stream
            project_web_ai_agent_runtime.stream_chat_completion = original_stream

        require(len(non_stream_calls) == 1, "AGENT_EMPTY_NON_STREAM_DETECTED")
        require(len(stream_calls) == 1, "AGENT_STREAM_RECOVERY_ATTEMPTED_ONCE")
        non_args, non_kwargs = non_stream_calls[0]
        stream_args, stream_kwargs = stream_calls[0]
        require(non_args[2] == stream_args[2], "AGENT_RECOVERY_REUSES_MESSAGES")
        require(
            non_kwargs["request_id"] == stream_kwargs["request_id"],
            "AGENT_RECOVERY_REUSES_REQUEST_ID",
        )
        require(
            stream_kwargs["allow_non_stream_fallback"] is False,
            "AGENT_RECOVERY_PREVENTS_TRANSPORT_LOOP",
        )
        require(result.content == "Recovered agent answer.", "AGENT_RECOVERY_CONTENT")
        transport = result.raw_metadata.get("kanda_transport", {})
        require(
            transport.get("mode") == "project_agent_stream_recovery",
            "AGENT_STREAM_RECOVERY_PROVENANCE",
        )
        require(
            transport.get("turn_modes")
            == ["stream_recovery_after_empty_non_stream"],
            "AGENT_TURN_TRANSPORT_PROVENANCE",
        )
        agent = result.raw_metadata.get("kanda_project_agent", {})
        require(agent.get("write_authority") is False, "REMOTE_AI_WRITE_AUTHORITY_UNCHANGED")
        require(agent.get("shell_authority") is False, "REMOTE_AI_SHELL_AUTHORITY_UNCHANGED")


def validate_non_empty_and_non_eligible_failures() -> None:
    """Prove normal success stays single-request and other failures do not retry."""
    original_non_stream = project_web_ai_agent_runtime.request_chat_completion
    original_stream = project_web_ai_agent_runtime.stream_chat_completion
    stream_calls: list[object] = []

    def good_non_stream(*_args, **_kwargs):
        return _result("Normal answer.")

    def unexpected_stream(*args, **kwargs):
        stream_calls.append((args, kwargs))
        return _result("Unexpected.", "stream")

    project_web_ai_agent_runtime.request_chat_completion = good_non_stream
    project_web_ai_agent_runtime.stream_chat_completion = unexpected_stream
    try:
        result = project_web_ai_agent_runtime._request_agent_turn(
            _profile(),
            "fixture-model",
            [{"role": "user", "content": "Hello"}],
            "",
            request_id="request-normal",
            cancel_event=None,
        )
    finally:
        project_web_ai_agent_runtime.request_chat_completion = original_non_stream
        project_web_ai_agent_runtime.stream_chat_completion = original_stream
    require(result.content == "Normal answer.", "AGENT_NON_EMPTY_SINGLE_REQUEST")
    require(not stream_calls, "AGENT_STREAM_RECOVERY_NOT_USED_FOR_SUCCESS")

    def malformed_non_stream(*_args, **_kwargs):
        raise ProviderResponseError("Gateway returned malformed JSON.")

    project_web_ai_agent_runtime.request_chat_completion = malformed_non_stream
    project_web_ai_agent_runtime.stream_chat_completion = unexpected_stream
    try:
        try:
            project_web_ai_agent_runtime._request_agent_turn(
                _profile(),
                "fixture-model",
                [{"role": "user", "content": "Hello"}],
                "",
                request_id="request-malformed",
                cancel_event=None,
            )
        except ProviderResponseError as exc:
            require("malformed JSON" in str(exc), "AGENT_NON_EMPTY_ERROR_PRESERVED")
        else:
            raise AssertionError("AGENT_NON_EMPTY_ERROR_PRESERVED")
    finally:
        project_web_ai_agent_runtime.request_chat_completion = original_non_stream
        project_web_ai_agent_runtime.stream_chat_completion = original_stream


def validate_cancellation_before_recovery() -> None:
    """Prove cancellation blocks the alternate transport."""
    original_non_stream = project_web_ai_agent_runtime.request_chat_completion
    original_stream = project_web_ai_agent_runtime.stream_chat_completion
    stream_calls: list[object] = []
    cancel_event = Event()
    cancel_event.set()

    def empty_non_stream(*_args, **_kwargs):
        raise ProviderResponseError("Gateway returned an empty response.")

    def unexpected_stream(*args, **kwargs):
        stream_calls.append((args, kwargs))
        return _result("Unexpected.", "stream")

    project_web_ai_agent_runtime.request_chat_completion = empty_non_stream
    project_web_ai_agent_runtime.stream_chat_completion = unexpected_stream
    try:
        try:
            project_web_ai_agent_runtime._request_agent_turn(
                _profile(),
                "fixture-model",
                [{"role": "user", "content": "Cancel"}],
                "",
                request_id="request-cancel",
                cancel_event=cancel_event,
            )
        except ProviderCancelledError:
            print("AGENT_EMPTY_RESPONSE_RECOVERY_CANCELLATION: PASS")
        else:
            raise AssertionError("AGENT_EMPTY_RESPONSE_RECOVERY_CANCELLATION")
    finally:
        project_web_ai_agent_runtime.request_chat_completion = original_non_stream
        project_web_ai_agent_runtime.stream_chat_completion = original_stream
    require(not stream_calls, "AGENT_CANCELLED_RECOVERY_NO_SECOND_REQUEST")


def validate_source_contract(root: Path) -> None:
    """Compile touched modules and preserve frozen boundary restrictions."""
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "TOUCHED_SOURCE_MODULES_MAX_500_LINES " + relative,
        )
    runtime = (root / TOUCHED[0]).read_text(encoding="utf-8")
    require(
        "allow_non_stream_fallback=False" in runtime,
        "AGENT_ALTERNATE_TRANSPORT_LOOP_GUARD",
    )
    require(
        "ProjectAgentBoundaryContext.from_request" in runtime
        and '"boundary_identity_bound": True' in runtime,
        "FROZEN_DYNAMIC_PROJECT_BOUNDARY_PRESERVED",
    )
    forbidden = ("subprocess", "os.system", "Popen(", "write_text(", "write_bytes(")
    require(
        not any(token in runtime for token in forbidden),
        "AGENT_RECOVERY_ADDS_NO_WRITE_OR_SHELL_AUTHORITY",
    )
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run all focused validations."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_empty_non_stream_recovers_with_stream()
    validate_non_empty_and_non_eligible_failures()
    validate_cancellation_before_recovery()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
