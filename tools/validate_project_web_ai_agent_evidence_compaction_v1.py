# project-path: tools/validate_project_web_ai_agent_evidence_compaction_v1.py
"""Validate bounded evidence compaction for Project Web AI agent mode."""

from __future__ import annotations

import argparse
import json
import py_compile
import tempfile
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.reasoner_engine import (
    project_web_ai_agent_evidence,
    project_web_ai_agent_runtime,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ChatUsage,
    GatewayProfile,
    ProjectWebAIRequestIdentity,
    ProviderResponseError,
)

FEATURE_ID = "project-web-ai-agent-evidence-compaction-v1"
TOUCHED = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_evidence.py",
    "tools/validate_project_web_ai_agent_evidence_compaction_v1.py",
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
        session_id="session-evidence-compaction",
        project_id=boundary.active_project_id,
        project_slug=boundary.active_project_slug,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        support_root=str(boundary.active_project_support_root),
        snapshot_id="snapshot-evidence-compaction",
        context_hash="context-evidence-compaction",
        gateway_id="fixture",
        model_id="fixture-model",
        privacy_approval_id="approval-evidence-compaction",
        created_at_utc="2026-07-23T00:00:00+00:00",
        project_epoch=9,
    )


def _result(content: str, response_id: str) -> ChatResult:
    """Return one deterministic provider result."""
    return ChatResult(
        request_id="request-evidence-compaction",
        gateway_id="fixture",
        requested_model="fixture-model",
        returned_model="fixture-model",
        content=content,
        finish_reason="stop",
        response_id=response_id,
        usage=ChatUsage(total_tokens=5, provider_name="fixture-provider"),
        raw_metadata={},
    )


def _read_request(path: str) -> str:
    """Return one canonical bare read-only file request."""
    return (
        '{"tool":"read_project_file","arguments":{"path":"'
        + path
        + '"}}'
    )


def _messages() -> list[dict[str, str]]:
    """Return one minimal Inspect Project request."""
    return [
        {"role": "system", "content": "TRUSTED TOOL VERSUS PROJECT BOUNDARY"},
        {
            "role": "user",
            "content": (
                "CURRENT QUESTION\nTrace the implementation and return exact "
                "files, functions, line ranges, and tools."
            ),
        },
    ]


def _make_large_project(root: Path) -> list[str]:
    """Create six large deterministic Python files."""
    paths: list[str] = []
    for file_number in range(1, 7):
        name = "large_module_" + str(file_number) + ".py"
        paths.append(name)
        lines = [
            (
                "VALUE_"
                + str(file_number)
                + "_"
                + str(line_number)
                + " = '"
                + ("x" * 96)
                + "'"
            )
            for line_number in range(1, 501)
        ]
        (root / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return paths


def _message_chars(messages: list[dict[str, str]]) -> int:
    return sum(len(str(item.get("content") or "")) for item in messages)


def _ledger_from_messages(messages: list[dict[str, str]]) -> dict[str, object]:
    for item in messages:
        content = str(item.get("content") or "")
        prefix = "KANDA COMPACT PROJECT EVIDENCE LEDGER\n"
        if not content.startswith(prefix):
            continue
        payload = content[len(prefix):].split("\nThis ledger is derived", 1)[0]
        parsed = json.loads(payload)
        if isinstance(parsed, dict):
            return parsed
    raise AssertionError("terminal evidence ledger missing")


def validate_large_evidence_is_bounded() -> None:
    """Prove six large reads are compacted before every provider turn."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_evidence_") as temp:
        root = Path(temp)
        paths = _make_large_project(root)
        responses = [
            _result(_read_request(path), "tool-" + str(index))
            for index, path in enumerate(paths, start=1)
        ]
        responses.append(_result("Grounded compact answer.", "terminal-answer"))
        calls: list[tuple[list[dict[str, str]], dict[str, object]]] = []
        original_request = project_web_ai_agent_runtime.request_chat_completion

        def provider(*args, **kwargs):
            calls.append(([dict(item) for item in args[2]], dict(kwargs)))
            return responses[len(calls) - 1]

        project_web_ai_agent_runtime.request_chat_completion = provider
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                _messages(),
                "",
                project_root=str(root),
                request_identity=_identity(root, "request-large-evidence"),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request

        require(len(calls) == 7, "EVIDENCE_COMPACTION_SIX_READS_PLUS_TERMINAL")
        iterative_chars = [_message_chars(messages) for messages, _ in calls[:-1]]
        require(
            max(iterative_chars) < 60_000,
            "ITERATIVE_PROVIDER_CONTEXT_BOUNDED_BELOW_60000_CHARS",
        )
        terminal_messages, terminal_kwargs = calls[-1]
        terminal_chars = _message_chars(terminal_messages)
        require(
            terminal_chars < 40_000,
            "TERMINAL_PROVIDER_CONTEXT_BOUNDED_BELOW_40000_CHARS",
        )
        require(
            terminal_kwargs.get("max_tokens")
            == project_web_ai_agent_evidence.TERMINAL_SYNTHESIS_MAX_TOKENS,
            "TERMINAL_COMPLETION_BUDGET_RESERVED",
        )
        ledger = _ledger_from_messages(terminal_messages)
        items = ledger.get("items", [])
        require(ledger.get("item_count") == 6, "TERMINAL_LEDGER_RETAINS_SIX_RESULTS")
        require(isinstance(items, list) and len(items) == 6, "TERMINAL_LEDGER_ITEM_COUNT")
        require(
            all(isinstance(item, dict) and item.get("tool") == "read_project_file"
                for item in items),
            "TERMINAL_LEDGER_TOOL_PROVENANCE",
        )
        serialized = json.dumps(ledger, ensure_ascii=True)
        require(
            all(path in serialized for path in paths),
            "TERMINAL_LEDGER_EXACT_PATHS_RETAINED",
        )
        require(
            "truncated_by_kanda" in serialized,
            "TERMINAL_LEDGER_TRUNCATION_EXPLICIT",
        )
        require(
            "VALUE_1_500" not in serialized,
            "TERMINAL_LEDGER_RAW_TAIL_OMITTED",
        )
        require(
            result.content == "Grounded compact answer.",
            "EVIDENCE_COMPACTION_FINAL_ANSWER",
        )
        context = result.raw_metadata["kanda_project_agent"]["context"]
        require(
            context.get("terminal_evidence_mode") == "bounded_ledger",
            "TERMINAL_EVIDENCE_MODE_PROVENANCE",
        )
        require(
            int(context.get("pre_terminal_compaction_chars", 0)) > terminal_chars,
            "PRE_TERMINAL_COMPACTION_REDUCTION_PROVEN",
        )
        require(
            context.get("terminal_provider_chars") == terminal_chars,
            "TERMINAL_PROVIDER_CHAR_PROVENANCE",
        )
        require(
            context.get("terminal_max_tokens")
            == project_web_ai_agent_evidence.TERMINAL_SYNTHESIS_MAX_TOKENS,
            "TERMINAL_TOKEN_BUDGET_PROVENANCE",
        )


def validate_iterative_result_shape() -> None:
    """Prove provider-visible reads retain exact metadata and line numbering."""
    raw = (
        "KANDA_PROJECT_TOOL_RESULT_BEGIN\n"
        + json.dumps(
            {
                "tool": "read_project_file_range",
                "round": 2,
                "ok": True,
                "result": {
                    "path": "package/module.py",
                    "start_line": 40,
                    "end_line": 42,
                    "line_count_returned": 3,
                    "truncated": False,
                    "content": "alpha\nbeta\ngamma",
                },
                "error": "",
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        + "\nKANDA_PROJECT_TOOL_RESULT_END"
    )
    compacted = project_web_ai_agent_evidence.compact_tool_result_text(raw)
    require("package/module.py" in compacted, "COMPACT_RESULT_EXACT_PATH_RETAINED")
    require("40: alpha" in compacted, "COMPACT_RESULT_START_LINE_NUMBERED")
    require("42: gamma" in compacted, "COMPACT_RESULT_END_LINE_NUMBERED")
    require(
        len(compacted) <= project_web_ai_agent_evidence.MAX_PROVIDER_TOOL_RESULT_CHARS + 800,
        "COMPACT_RESULT_PROVIDER_BOUND_ENFORCED",
    )


def validate_terminal_stream_recovery_uses_reserved_budget() -> None:
    """Prove empty terminal non-stream recovery preserves the token override."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_stream_budget_") as temp:
        root = Path(temp)
        paths = _make_large_project(root)
        non_stream_calls: list[dict[str, object]] = []
        stream_calls: list[dict[str, object]] = []
        original_request = project_web_ai_agent_runtime.request_chat_completion
        original_stream = project_web_ai_agent_runtime.stream_chat_completion

        def provider(*args, **kwargs):
            non_stream_calls.append(dict(kwargs))
            if len(non_stream_calls) <= 6:
                return _result(
                    _read_request(paths[len(non_stream_calls) - 1]),
                    "tool-" + str(len(non_stream_calls)),
                )
            raise ProviderResponseError("Gateway returned an empty response.")

        def stream_provider(*_args, **kwargs):
            stream_calls.append(dict(kwargs))
            return _result("Recovered compact answer.", "stream-terminal")

        project_web_ai_agent_runtime.request_chat_completion = provider
        project_web_ai_agent_runtime.stream_chat_completion = stream_provider
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                _messages(),
                "",
                project_root=str(root),
                request_identity=_identity(root, "request-stream-budget"),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request
            project_web_ai_agent_runtime.stream_chat_completion = original_stream

        require(len(stream_calls) == 1, "TERMINAL_STREAM_RECOVERY_SINGLE_ATTEMPT")
        require(
            stream_calls[0].get("max_tokens")
            == project_web_ai_agent_evidence.TERMINAL_SYNTHESIS_MAX_TOKENS,
            "TERMINAL_STREAM_RECOVERY_BUDGET_PRESERVED",
        )
        require(
            stream_calls[0].get("allow_non_stream_fallback") is False,
            "TERMINAL_STREAM_NON_STREAM_FALLBACK_DISABLED",
        )
        require(
            result.content == "Recovered compact answer.",
            "TERMINAL_STREAM_RECOVERY_FINAL_ANSWER",
        )


def validate_normal_answer_unchanged() -> None:
    """Prove an immediate final answer keeps the normal provider budget path."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_normal_answer_") as temp:
        root = Path(temp)
        observed: list[dict[str, object]] = []
        original_request = project_web_ai_agent_runtime.request_chat_completion

        def provider(*_args, **kwargs):
            observed.append(dict(kwargs))
            return _result("Immediate answer.", "normal-answer")

        project_web_ai_agent_runtime.request_chat_completion = provider
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                _messages(),
                "",
                project_root=str(root),
                request_identity=_identity(root, "request-normal-answer"),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request

        require(result.content == "Immediate answer.", "NORMAL_AGENT_ANSWER_UNCHANGED")
        require(len(observed) == 1, "NORMAL_AGENT_SINGLE_PROVIDER_TURN")
        require("max_tokens" not in observed[0], "NORMAL_AGENT_DEFAULT_BUDGET_UNCHANGED")


def validate_source_contract(root: Path) -> None:
    """Compile touched modules and enforce frozen authority boundaries."""
    for relative in TOUCHED:
        path = root / relative
        py_compile.compile(str(path), doraise=True)
        require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "TOUCHED_SOURCE_MODULES_MAX_500_LINES " + relative,
        )
        path.read_bytes().decode("ascii")
    runtime = (root / TOUCHED[0]).read_text(encoding="utf-8")
    evidence = (root / TOUCHED[1]).read_text(encoding="utf-8")
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
    require(
        "MAX_AGENT_ROUNDS = 6" in runtime,
        "FROZEN_SIX_READ_CEILING_PRESERVED",
    )
    require(
        "build_terminal_synthesis_messages" in runtime
        and "bounded_ledger" in evidence,
        "EVIDENCE_COMPACTION_WIRING_PRESENT",
    )
    combined = runtime + evidence
    forbidden = (
        "subprocess",
        "os.system",
        "Popen(",
        "write_project_file",
        "write_text(",
        "write_bytes(",
    )
    require(
        not any(token in combined for token in forbidden),
        "EVIDENCE_COMPACTION_ADDS_NO_WRITE_OR_SHELL_AUTHORITY",
    )
    print("ASCII_ONLY_TOUCHED_SOURCE: PASS")
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run the focused evidence-compaction validation suite."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_source_contract(root)
    validate_iterative_result_shape()
    validate_large_evidence_is_bounded()
    validate_terminal_stream_recovery_uses_reserved_budget()
    validate_normal_answer_unchanged()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
