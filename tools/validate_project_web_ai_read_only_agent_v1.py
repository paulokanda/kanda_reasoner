# project-path: tools/validate_project_web_ai_read_only_agent_v1.py
"""Validate the bounded read-only Project Web AI agent contract."""

from __future__ import annotations

import argparse
import json
import py_compile
import tempfile
from pathlib import Path
from threading import Event

from kanda_reasoner_app.reasoner_engine import project_web_ai_agent_runtime
from kanda_reasoner_app.reasoner_engine.project_web_ai_boundary_context import (
    ProjectAgentBoundaryContext,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_agent_protocol import (
    ProjectAgentProtocolError,
    parse_agent_tool_request,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_read_tools import (
    ProjectReadToolBroker,
    ProjectReadToolError,
)
from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ChatUsage,
    GatewayProfile,
    ProviderCancelledError,
    ProjectWebAIRequestIdentity,
)

FEATURE_ID = "project-web-ai-read-only-agent-v1"
TOUCHED = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_read_tools.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_protocol.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
    "tools/validate_project_web_ai_read_only_agent_v1.py",
)


def require(condition: object, marker: str) -> None:
    """Raise one focused assertion or print its success marker."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")



def _request_identity(root: Path, request_id: str) -> ProjectWebAIRequestIdentity:
    """Return one exact disposable request identity for the fixture Project."""
    identity = resolve_project_tool_boundary_identity(root)
    return ProjectWebAIRequestIdentity(
        request_id=request_id,
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

def _fixture_project(root: Path) -> None:
    """Create one disposable Project with source, ignored, and secret files."""
    (root / "app").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / ".git").mkdir()
    (root / "node_modules").mkdir()
    (root / "app" / "main.py").write_text(
        "class ProviderResponseError(RuntimeError):\n    pass\n",
        encoding="utf-8",
    )
    (root / "tests" / "test_main.py").write_text(
        "from app.main import ProviderResponseError\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text("Disposable project\n", encoding="utf-8")
    (root / ".env").write_text("SECRET=blocked\n", encoding="utf-8")
    (root / ".git" / "config").write_text("blocked\n", encoding="utf-8")
    (root / "node_modules" / "large.js").write_text("blocked\n", encoding="utf-8")


def validate_broker() -> None:
    """Validate listing, search, reads, bounds, and path containment."""
    with tempfile.TemporaryDirectory() as temp_text:
        root = Path(temp_text)
        _fixture_project(root)
        request = _request_identity(root, "request-broker")
        boundary = ProjectAgentBoundaryContext.from_request(root, request)
        broker = ProjectReadToolBroker(root, boundary=boundary)

        tree = broker.execute(
            "list_project_tree", {"path": ".", "maximum_entries": 50}
        ).payload
        paths = {str(item["path"]) for item in tree["entries"]}
        require("app/main.py" in paths, "READ_ONLY_AGENT_TREE_LISTING")
        require(".env" not in paths, "READ_ONLY_AGENT_SECRET_NAME_BLOCKED")
        require(
            not any(path.startswith(".git/") for path in paths),
            "READ_ONLY_AGENT_HIDDEN_VCS_PRUNED",
        )
        require(
            not any(path.startswith("node_modules/") for path in paths),
            "READ_ONLY_AGENT_DEPENDENCY_TREE_PRUNED",
        )

        search = broker.execute(
            "search_project_text",
            {
                "query": "ProviderResponseError",
                "include": ["*.py", "**/*.py"],
                "maximum_results": 10,
            },
        ).payload
        result_paths = {str(item["path"]) for item in search["results"]}
        require("app/main.py" in result_paths, "READ_ONLY_AGENT_TEXT_SEARCH")
        require("tests/test_main.py" in result_paths, "READ_ONLY_AGENT_GLOB_SEARCH")

        file_payload = broker.execute(
            "read_project_file", {"path": "app/main.py"}
        ).payload
        require(
            "ProviderResponseError" in str(file_payload["content"]),
            "READ_ONLY_AGENT_FILE_READ",
        )
        range_payload = broker.execute(
            "read_project_file_range",
            {"path": "app/main.py", "start_line": 1, "line_count": 1},
        ).payload
        require(
            int(range_payload["line_count_returned"]) == 1,
            "READ_ONLY_AGENT_FILE_RANGE",
        )

        for path in ("../outside.txt", str(root / "app" / "main.py"), ".env"):
            try:
                broker.execute("read_project_file", {"path": path})
            except ProjectReadToolError:
                continue
            raise AssertionError("READ_ONLY_AGENT_PATH_ESCAPE_REJECTED")
        print("READ_ONLY_AGENT_PATH_ESCAPE_REJECTED: PASS")


def _fake_result(content: str, call_number: int) -> ChatResult:
    """Return one deterministic fake provider response."""
    return ChatResult(
        request_id="request-1",
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
            cost_usd=0.001,
            provider_name="fixture-provider",
        ),
        raw_metadata={"fixture_call": call_number},
    )


def validate_agent_loop() -> None:
    """Validate strict tool rounds, final answer, provenance, and cancellation."""
    with tempfile.TemporaryDirectory() as temp_text:
        root = Path(temp_text)
        _fixture_project(root)
        responses = [
            "KANDA_PROJECT_TOOL_REQUEST_BEGIN\n"
            + json.dumps(
                {
                    "tool": "search_project_text",
                    "arguments": {
                        "query": "ProviderResponseError",
                        "include": ["**/*.py"],
                        "maximum_results": 10,
                    },
                }
            )
            + "\nKANDA_PROJECT_TOOL_REQUEST_END",
            "KANDA_PROJECT_TOOL_REQUEST_BEGIN\n"
            + json.dumps(
                {
                    "tool": "read_project_file_range",
                    "arguments": {
                        "path": "app/main.py",
                        "start_line": 1,
                        "line_count": 20,
                    },
                }
            )
            + "\nKANDA_PROJECT_TOOL_REQUEST_END",
            "I inspected app/main.py and found ProviderResponseError.",
        ]
        calls: list[list[dict[str, str]]] = []
        original = project_web_ai_agent_runtime.request_chat_completion

        def fake_request(*_args, **_kwargs):
            calls.append([dict(item) for item in _args[2]])
            return _fake_result(responses[len(calls) - 1], len(calls))

        project_web_ai_agent_runtime.request_chat_completion = fake_request
        try:
            profile = GatewayProfile(
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
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                profile,
                "fixture-model",
                [
                    {"role": "system", "content": "Base contract"},
                    {"role": "user", "content": "Inspect the provider error."},
                ],
                "",
                project_root=str(root),
                request_identity=_request_identity(root, "request-1"),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original

        require(len(calls) == 3, "READ_ONLY_AGENT_ITERATIVE_TOOL_LOOP")
        require(
            "KANDA READ-ONLY PROJECT AGENT CONTRACT" in calls[0][0]["content"],
            "READ_ONLY_AGENT_SYSTEM_CONTRACT",
        )
        require(
            "KANDA_PROJECT_TOOL_RESULT_BEGIN" in calls[1][-1]["content"],
            "READ_ONLY_AGENT_TOOL_RESULT_RETURNED",
        )
        require(
            result.content.startswith("I inspected app/main.py"),
            "READ_ONLY_AGENT_FINAL_ANSWER",
        )
        metadata = result.raw_metadata["kanda_project_agent"]
        require(metadata["read_only"] is True, "READ_ONLY_AGENT_PROVENANCE")
        require(metadata["write_authority"] is False, "REMOTE_AI_WRITE_AUTHORITY_UNCHANGED")
        require(result.usage.total_tokens == 45, "READ_ONLY_AGENT_USAGE_AGGREGATED")

        cancel_event = Event()
        cancel_event.set()
        try:
            project_web_ai_agent_runtime.run_project_agent_completion(
                profile,
                "fixture-model",
                [{"role": "user", "content": "Cancel"}],
                "",
                project_root=str(root),
                request_identity=_request_identity(root, "request-2"),
                cancel_event=cancel_event,
            )
        except ProviderCancelledError:
            print("READ_ONLY_AGENT_CANCELLATION: PASS")
        else:
            raise AssertionError("READ_ONLY_AGENT_CANCELLATION")


def validate_protocol() -> None:
    """Validate exact marker parsing and reject surrounding prose."""
    request = parse_agent_tool_request(
        "KANDA_PROJECT_TOOL_REQUEST_BEGIN\n"
        '{"tool":"list_project_tree","arguments":{"path":"."}}\n'
        "KANDA_PROJECT_TOOL_REQUEST_END"
    )
    require(request is not None, "READ_ONLY_AGENT_STRICT_MARKER_PROTOCOL")
    try:
        parse_agent_tool_request(
            "Please run this. KANDA_PROJECT_TOOL_REQUEST_BEGIN\n"
            '{"tool":"list_project_tree","arguments":{}}\n'
            "KANDA_PROJECT_TOOL_REQUEST_END"
        )
    except ProjectAgentProtocolError:
        print("READ_ONLY_AGENT_AMBIGUOUS_REQUEST_REJECTED: PASS")
    else:
        raise AssertionError("READ_ONLY_AGENT_AMBIGUOUS_REQUEST_REJECTED")


def validate_source_contract(root: Path) -> None:
    """Validate UI disclosure, worker wiring, no write APIs, compile, and size."""
    tab = (root / "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py").read_text(
        encoding="utf-8"
    )
    ui = (root / "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py").read_text(
        encoding="utf-8"
    )
    broker = (root / TOUCHED[0]).read_text(encoding="utf-8")
    runtime = (root / TOUCHED[2]).read_text(encoding="utf-8")
    require(
        'QCheckBox("Inspect Project")' in ui and "setChecked(True)" in ui,
        "READ_ONLY_AGENT_UI_MODE_VISIBLE",
    )
    require(
        "Bounded read-only Project tools" in tab and "project_root=agent_root" in tab,
        "READ_ONLY_AGENT_APPROVAL_AND_WORKER_WIRING",
    )
    forbidden = ("write_text(", "write_bytes(", "subprocess", "os.system", "Popen(")
    require(
        not any(token in broker or token in runtime for token in forbidden),
        "READ_ONLY_AGENT_NO_WRITE_OR_SHELL_API",
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
    """Run all focused validators."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_protocol()
    validate_broker()
    validate_agent_loop()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
