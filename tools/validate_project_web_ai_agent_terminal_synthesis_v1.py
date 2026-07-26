# project-path: tools/validate_project_web_ai_agent_terminal_synthesis_v1.py
"""Validate bounded terminal synthesis for Project Web AI read-only agent mode."""

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
    ProjectWebAIRequestIdentity,
    ProviderCancelledError,
    ProviderResponseError,
)

FEATURE_ID = "project-web-ai-agent-terminal-synthesis-v1"
TOUCHED = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_terminal.py",
    "tools/validate_project_web_ai_agent_terminal_synthesis_v1.py",
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


def _identity(root: Path, request_id: str) -> ProjectWebAIRequestIdentity:
    """Return one request identity bound to the disposable Project."""
    boundary = resolve_project_tool_boundary_identity(root)
    return ProjectWebAIRequestIdentity(
        request_id=request_id,
        session_id="session-terminal-synthesis",
        project_id=boundary.active_project_id,
        project_slug=boundary.active_project_slug,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        support_root=str(boundary.active_project_support_root),
        snapshot_id="snapshot-terminal-synthesis",
        context_hash="context-terminal-synthesis",
        gateway_id="fixture",
        model_id="fixture-model",
        privacy_approval_id="approval-terminal-synthesis",
        created_at_utc="2026-07-23T00:00:00+00:00",
        project_epoch=8,
    )


def _result(content: str, response_id: str) -> ChatResult:
    """Return one deterministic provider result."""
    return ChatResult(
        request_id="request-terminal-synthesis",
        gateway_id="fixture",
        requested_model="fixture-model",
        returned_model="fixture-model",
        content=content,
        finish_reason="stop",
        response_id=response_id,
        usage=ChatUsage(total_tokens=5, provider_name="fixture-provider"),
        raw_metadata={},
    )


def _tool_request(query: str) -> str:
    """Return one canonical bare read-only tool request."""
    return (
        '{"tool":"search_project_text","arguments":'
        '{"query":"' + query + '","include":["*.py"],'
        '"maximum_results":5}}'
    )


def _messages() -> list[dict[str, str]]:
    """Return one minimal Inspect Project request."""
    return [
        {"role": "system", "content": "TRUSTED TOOL VERSUS PROJECT BOUNDARY"},
        {
            "role": "user",
            "content": "CURRENT QUESTION\nTrace the exact source flow.",
        },
    ]


def _make_project(root: Path) -> None:
    """Create deterministic searchable source fixtures."""
    for index in range(1, 7):
        (root / ("module_" + str(index) + ".py")).write_text(
            "VALUE_" + str(index) + " = " + str(index) + "\n",
            encoding="utf-8",
        )


def validate_six_reads_then_terminal_answer() -> None:
    """Prove six local reads are followed by one evidence-only answer turn."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_terminal_") as temp:
        root = Path(temp)
        _make_project(root)
        calls: list[list[dict[str, str]]] = []
        responses = [
            _result(_tool_request("VALUE_" + str(index)), "tool-" + str(index))
            for index in range(1, 7)
        ]
        responses.append(_result("Grounded final answer.", "terminal-answer"))
        original_request = project_web_ai_agent_runtime.request_chat_completion

        def provider(*args, **_kwargs):
            calls.append([dict(item) for item in args[2]])
            return responses[len(calls) - 1]

        project_web_ai_agent_runtime.request_chat_completion = provider
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                _messages(),
                "",
                project_root=str(root),
                request_identity=_identity(root, "request-terminal-synthesis"),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request

        require(len(calls) == 7, "AGENT_SIX_READS_PLUS_ONE_SYNTHESIS_TURN")
        require(result.content == "Grounded final answer.", "AGENT_TERMINAL_FINAL_ANSWER")
        agent = result.raw_metadata.get("kanda_project_agent", {})
        context = agent.get("context", {})
        tools = agent.get("tools", [])
        require(len(tools) == 6, "AGENT_MAX_SIX_LOCAL_TOOL_EXECUTIONS")
        require(all(item.get("ok") is True for item in tools), "AGENT_SIX_TOOL_RESULTS_RETAINED")
        require(context.get("terminal_synthesis_used") is True, "AGENT_TERMINAL_SYNTHESIS_USED")
        require(
            context.get("terminal_reason") == "maximum_tool_rounds",
            "AGENT_TERMINAL_REASON_MAXIMUM_ROUNDS",
        )
        terminal_text = "\n".join(
            str(item.get("content") or "") for item in calls[-1]
        )
        require(
            "KANDA TERMINAL SYNTHESIS" in terminal_text,
            "AGENT_TERMINAL_SYNTHESIS_PROMPT_PRESENT",
        )
        require(
            "FINAL ANSWER GROUNDING" in terminal_text,
            "AGENT_GROUNDING_REMINDER_PRESENT",
        )
        require(
            agent.get("write_authority") is False,
            "REMOTE_AI_WRITE_AUTHORITY_UNCHANGED",
        )
        require(
            agent.get("shell_authority") is False,
            "REMOTE_AI_SHELL_AUTHORITY_UNCHANGED",
        )


def validate_duplicate_loop_terminates_without_reexecution() -> None:
    """Prove repeated identical reads execute once and end in synthesis."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_duplicate_") as temp:
        root = Path(temp)
        _make_project(root)
        repeated = _result(_tool_request("VALUE_1"), "duplicate-tool")
        responses = [
            repeated,
            repeated,
            repeated,
            _result("Answer from the first result.", "duplicate-terminal"),
        ]
        calls: list[list[dict[str, str]]] = []
        original_request = project_web_ai_agent_runtime.request_chat_completion

        def provider(*args, **_kwargs):
            calls.append([dict(item) for item in args[2]])
            return responses[len(calls) - 1]

        project_web_ai_agent_runtime.request_chat_completion = provider
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                _messages(),
                "",
                project_root=str(root),
                request_identity=_identity(root, "request-duplicate-synthesis"),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request

        agent = result.raw_metadata.get("kanda_project_agent", {})
        context = agent.get("context", {})
        tools = agent.get("tools", [])
        executed = [item for item in tools if item.get("ok") is True]
        duplicates = [item for item in tools if item.get("duplicate") is True]
        require(len(executed) == 1, "AGENT_DUPLICATE_TOOL_EXECUTED_ONCE")
        require(len(duplicates) == 2, "AGENT_DUPLICATE_REQUESTS_REJECTED")
        require(len(calls) == 4, "AGENT_DUPLICATE_LOOP_BOUNDED")
        require(
            context.get("terminal_reason") == "duplicate_tool_loop",
            "AGENT_DUPLICATE_LOOP_TERMINAL_SYNTHESIS",
        )
        require(
            context.get("duplicate_tool_requests") == 2,
            "AGENT_DUPLICATE_COUNT_PROVENANCE",
        )
        require(
            result.content == "Answer from the first result.",
            "AGENT_DUPLICATE_LOOP_FINAL_ANSWER",
        )


def validate_terminal_tool_request_fails_closed() -> None:
    """Prove the synthesis turn cannot reopen the local tool phase."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_terminal_reject_") as temp:
        root = Path(temp)
        _make_project(root)
        responses = [
            _result(_tool_request("VALUE_" + str(index)), "tool-" + str(index))
            for index in range(1, 7)
        ]
        responses.append(_result(_tool_request("VALUE_1"), "terminal-tool"))
        calls = 0
        original_request = project_web_ai_agent_runtime.request_chat_completion

        def provider(*_args, **_kwargs):
            nonlocal calls
            response = responses[calls]
            calls += 1
            return response

        project_web_ai_agent_runtime.request_chat_completion = provider
        try:
            try:
                project_web_ai_agent_runtime.run_project_agent_completion(
                    _profile(),
                    "fixture-model",
                    _messages(),
                    "",
                    project_root=str(root),
                    request_identity=_identity(root, "request-terminal-reject"),
                )
            except ProviderResponseError as exc:
                require(
                    "terminal synthesis requested another tool" in str(exc),
                    "AGENT_TERMINAL_TOOL_REQUEST_REJECTED",
                )
            else:
                raise AssertionError("AGENT_TERMINAL_TOOL_REQUEST_REJECTED")
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request


def validate_cancellation_blocks_terminal_turn() -> None:
    """Prove cancellation after the last read prevents synthesis network work."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_terminal_cancel_") as temp:
        root = Path(temp)
        _make_project(root)
        cancel_event = Event()
        calls = 0
        original_request = project_web_ai_agent_runtime.request_chat_completion

        def provider(*_args, **_kwargs):
            nonlocal calls
            calls += 1
            if calls == 6:
                cancel_event.set()
            return _result(_tool_request("VALUE_" + str(calls)), "tool-" + str(calls))

        project_web_ai_agent_runtime.request_chat_completion = provider
        try:
            try:
                project_web_ai_agent_runtime.run_project_agent_completion(
                    _profile(),
                    "fixture-model",
                    _messages(),
                    "",
                    project_root=str(root),
                    request_identity=_identity(root, "request-terminal-cancel"),
                    cancel_event=cancel_event,
                )
            except ProviderCancelledError:
                print("AGENT_TERMINAL_SYNTHESIS_CANCELLATION: PASS")
            else:
                raise AssertionError("AGENT_TERMINAL_SYNTHESIS_CANCELLATION")
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request
        require(calls == 6, "AGENT_CANCELLED_TERMINAL_PROVIDER_CALL_BLOCKED")


def validate_source_contract(root: Path) -> None:
    """Compile touched modules and enforce frozen authority boundaries."""
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "TOUCHED_SOURCE_MODULES_MAX_500_LINES " + relative,
        )
    runtime = (root / TOUCHED[0]).read_text(encoding="utf-8")
    helper = (root / TOUCHED[1]).read_text(encoding="utf-8")
    require(
        "ProjectAgentBoundaryContext.from_request" in runtime
        and '"boundary_identity_bound": True' in runtime,
        "FROZEN_DYNAMIC_PROJECT_BOUNDARY_PRESERVED",
    )
    require(
        "allow_non_stream_fallback=False" in runtime,
        "FROZEN_EMPTY_RESPONSE_RECOVERY_PRESERVED",
    )
    require(
        "parse_agent_tool_request" in runtime,
        "FROZEN_BARE_TOOL_INTERCEPTION_PRESERVED",
    )
    forbidden = (
        "subprocess",
        "os.system",
        "Popen(",
        "write_project_file",
        "write_text(",
        "write_bytes(",
    )
    combined = runtime + helper
    require(
        not any(token in combined for token in forbidden),
        "TERMINAL_SYNTHESIS_ADDS_NO_WRITE_OR_SHELL_AUTHORITY",
    )
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run the focused terminal-synthesis validation suite."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_six_reads_then_terminal_answer()
    validate_duplicate_loop_terminates_without_reexecution()
    validate_terminal_tool_request_fails_closed()
    validate_cancellation_blocks_terminal_turn()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
