# project-path: tools/validate_project_web_ai_bare_tool_request_interception_v1.py
"""Validate interception of exact bare Project Web AI tool requests."""

from __future__ import annotations

import argparse
import json
import py_compile
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_engine import project_web_ai_agent_runtime
from kanda_reasoner_app.reasoner_engine.project_web_ai_agent_protocol import (
    ProjectAgentProtocolError,
    parse_agent_tool_request,
)
from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ChatUsage,
    GatewayProfile,
    ProjectWebAIRequestIdentity,
)

FEATURE_ID = "project-web-ai-bare-tool-request-interception-v1"
TOUCHED = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_protocol.py",
    "tools/validate_project_web_ai_bare_tool_request_interception_v1.py",
)


def require(condition: object, marker: str) -> None:
    """Raise one focused assertion or print its success marker."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _request_identity(root: Path) -> ProjectWebAIRequestIdentity:
    """Return one exact disposable Project request identity."""
    identity = resolve_project_tool_boundary_identity(root)
    return ProjectWebAIRequestIdentity(
        request_id="bare-tool-request-1",
        session_id="session-1",
        project_id=identity.active_project_id,
        project_slug=identity.active_project_slug,
        project_root_fingerprint=identity.active_project_root_fingerprint,
        support_root=str(identity.active_project_support_root),
        snapshot_id="snapshot-1",
        context_hash="context-1",
        gateway_id="fixture",
        model_id="fixture-model",
        privacy_approval_id="approval-1",
        created_at_utc="2026-07-23T00:00:00+00:00",
        project_epoch=1,
    )


def _profile() -> GatewayProfile:
    """Return one deterministic provider profile."""
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


def _result(content: str, call_number: int) -> ChatResult:
    """Return one deterministic provider result."""
    return ChatResult(
        request_id="bare-tool-request-1",
        gateway_id="fixture",
        requested_model="fixture-model",
        returned_model="fixture-model",
        content=content,
        finish_reason="stop",
        response_id="response-" + str(call_number),
        usage=ChatUsage(
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            cost_usd=None,
            provider_name="fixture-provider",
        ),
        raw_metadata={},
    )


def validate_protocol() -> None:
    """Validate exact bare JSON recovery and non-executable ambiguity guards."""
    bare = json.dumps(
        {
            "tool": "search_project_text",
            "arguments": {
                "query": "ProviderResponseError",
                "include": ["*.py"],
                "maximum_results": 20,
            },
        },
        separators=(",", ":"),
    )
    request = parse_agent_tool_request(bare)
    require(request is not None, "BARE_TOOL_REQUEST_INTERCEPTED")
    require(request.tool == "search_project_text", "BARE_TOOL_NAME_PRESERVED")
    require(
        request.arguments.get("query") == "ProviderResponseError",
        "BARE_TOOL_ARGUMENTS_PRESERVED",
    )

    marker = (
        "KANDA_PROJECT_TOOL_REQUEST_BEGIN\n"
        + bare
        + "\nKANDA_PROJECT_TOOL_REQUEST_END"
    )
    marker_request = parse_agent_tool_request(marker)
    require(marker_request == request, "MARKER_PROTOCOL_PRESERVED")

    require(
        parse_agent_tool_request('{"answer":"normal JSON final answer"}') is None,
        "ARBITRARY_JSON_REMAINS_FINAL_ANSWER",
    )
    require(
        parse_agent_tool_request("```json\n" + bare + "\n```") is None,
        "FENCED_JSON_NOT_EXECUTED",
    )
    require(
        parse_agent_tool_request("Please run this: " + bare) is None,
        "PROSE_WRAPPED_JSON_NOT_EXECUTED",
    )
    require(
        parse_agent_tool_request('{"tool":"search_project_text"}') is None,
        "PARTIAL_TOOL_SHAPE_NOT_EXECUTED",
    )

    try:
        parse_agent_tool_request(
            '{"tool":"write_project_file","arguments":{"path":"x.py"}}'
        )
    except ProjectAgentProtocolError:
        print("BARE_UNSUPPORTED_TOOL_REJECTED: PASS")
    else:
        raise AssertionError("BARE_UNSUPPORTED_TOOL_REJECTED")


def validate_runtime_interception() -> None:
    """Validate that bare JSON is executed and never committed as final content."""
    with tempfile.TemporaryDirectory() as temp_text:
        root = Path(temp_text)
        (root / "app").mkdir()
        (root / "app" / "main.py").write_text(
            "class ProviderResponseError(RuntimeError):\n    pass\n",
            encoding="utf-8",
        )
        bare = json.dumps(
            {
                "tool": "search_project_text",
                "arguments": {
                    "query": "ProviderResponseError",
                    "include": ["*.py", "**/*.py"],
                    "maximum_results": 20,
                },
            },
            separators=(",", ":"),
        )
        responses = [bare, "I inspected app/main.py and found the class."]
        calls: list[list[dict[str, str]]] = []
        original = project_web_ai_agent_runtime.request_chat_completion

        def fake_request(*args, **_kwargs):
            calls.append([dict(item) for item in args[2]])
            return _result(responses[len(calls) - 1], len(calls))

        project_web_ai_agent_runtime.request_chat_completion = fake_request
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                [
                    {"role": "system", "content": "Base contract"},
                    {"role": "user", "content": "Find the provider error."},
                ],
                "",
                project_root=str(root),
                request_identity=_request_identity(root),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original

        require(len(calls) == 2, "BARE_TOOL_REQUEST_EXECUTED_ONCE")
        require(
            "KANDA_PROJECT_TOOL_RESULT_BEGIN" in calls[1][-1]["content"],
            "BARE_TOOL_RESULT_RETURNED_TO_MODEL",
        )
        require(result.content != bare, "RAW_BARE_TOOL_JSON_NOT_COMMITTED")
        require(
            result.content.startswith("I inspected app/main.py"),
            "FINAL_ANSWER_AFTER_BARE_TOOL_EXECUTION",
        )
        agent = result.raw_metadata.get("kanda_project_agent", {})
        require(agent.get("tool_rounds") == 1, "BARE_TOOL_PROVENANCE_RECORDED")
        require(agent.get("write_authority") is False, "REMOTE_AI_WRITE_AUTHORITY_UNCHANGED")
        require(agent.get("shell_authority") is False, "REMOTE_AI_SHELL_AUTHORITY_UNCHANGED")


def validate_source_contract(root: Path) -> None:
    """Validate focused source, compile, size, and frozen boundary preservation."""
    protocol = (root / TOUCHED[0]).read_text(encoding="utf-8")
    runtime = (
        root
        / "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py"
    ).read_text(encoding="utf-8")
    boundary = (
        root
        / "kanda_reasoner_app/reasoner_engine/project_web_ai_boundary_context.py"
    ).read_text(encoding="utf-8")
    require(
        "_parse_bare_tool_request" in protocol
        and 'set(payload) != {"tool", "arguments"}' in protocol,
        "BARE_TOOL_EXACT_SHAPE_GUARD_PRESENT",
    )
    require(
        "ProjectAgentBoundaryContext.from_request" in runtime
        and "active_project_support_root" in boundary,
        "FROZEN_DYNAMIC_PROJECT_BOUNDARY_PRESERVED",
    )
    forbidden = ("write_text(", "write_bytes(", "subprocess", "os.system", "Popen(")
    require(
        not any(token in protocol for token in forbidden),
        "BARE_TOOL_FIX_ADDS_NO_WRITE_OR_SHELL_AUTHORITY",
    )
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "TOUCHED_SOURCE_MODULES_MAX_500_LINES " + relative,
        )
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run all focused validation gates."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_protocol()
    validate_runtime_interception()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
