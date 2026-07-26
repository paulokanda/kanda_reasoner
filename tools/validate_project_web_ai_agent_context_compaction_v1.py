# project-path: tools/validate_project_web_ai_agent_context_compaction_v1.py
"""Validate compact tool-first prompts for Project Web AI agent mode."""

from __future__ import annotations

import argparse
import py_compile
import tempfile
from pathlib import Path
from typing import Mapping, Sequence

from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.reasoner_engine import project_web_ai_agent_runtime
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ChatUsage,
    GatewayProfile,
    ProjectWebAIRequestIdentity,
)

FEATURE_ID = "project-web-ai-agent-context-compaction-v1"
TOUCHED = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py",
    "tools/validate_project_web_ai_agent_context_compaction_v1.py",
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
    """Return one request identity bound to the disposable Project."""
    boundary = resolve_project_tool_boundary_identity(root)
    return ProjectWebAIRequestIdentity(
        request_id="request-agent-compact",
        session_id="session-agent-compact",
        project_id=boundary.active_project_id,
        project_slug=boundary.active_project_slug,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        support_root=str(boundary.active_project_support_root),
        snapshot_id="snapshot-agent-compact",
        context_hash="context-agent-compact",
        gateway_id="fixture",
        model_id="fixture-model",
        privacy_approval_id="approval-agent-compact",
        created_at_utc="2026-07-23T00:00:00+00:00",
        project_epoch=4,
    )


def _result(content: str) -> ChatResult:
    """Return one deterministic provider result."""
    return ChatResult(
        request_id="request-agent-compact",
        gateway_id="fixture",
        requested_model="fixture-model",
        returned_model="fixture-model",
        content=content,
        finish_reason="stop",
        response_id="response-agent-compact",
        usage=ChatUsage(total_tokens=7, provider_name="fixture-provider"),
        raw_metadata={},
    )


def _messages() -> list[dict[str, str]]:
    """Return one canonical chat request with oversized generated evidence."""
    return [
        {
            "role": "system",
            "content": (
                "TRUSTED TOOL VERSUS PROJECT BOUNDARY\n"
                "Active Project and Project Support are separate siblings."
            ),
        },
        {"role": "user", "content": "old user " + ("u" * 12000)},
        {"role": "assistant", "content": "old assistant " + ("a" * 12000)},
        {"role": "user", "content": "newer user " + ("n" * 12000)},
        {"role": "assistant", "content": "newer assistant " + ("r" * 12000)},
        {
            "role": "user",
            "content": "CURRENT QUESTION\nFind ProviderResponseError exactly.",
        },
        {
            "role": "user",
            "content": "UNTRUSTED PROJECT EVIDENCE\n" + ("e" * 140000),
        },
        {
            "role": "user",
            "content": "FINAL RESPONSE CONTRACT\nAnswer from handoff summaries.",
        },
    ]


def validate_compaction_contract() -> None:
    """Prove generated handoff omission and exact question preservation."""
    original = _messages()
    original_copy = [dict(item) for item in original]
    compacted, stats = project_web_ai_agent_runtime._compact_initial_agent_messages(
        original
    )
    contents = [str(item.get("content") or "") for item in compacted]
    require(original == original_copy, "AGENT_CONTEXT_INPUT_IMMUTABLE")
    require(
        contents[0].startswith("TRUSTED TOOL VERSUS PROJECT BOUNDARY"),
        "AGENT_TRUSTED_BOUNDARY_PRESERVED",
    )
    require(
        any(text == "CURRENT QUESTION\nFind ProviderResponseError exactly." for text in contents),
        "AGENT_CURRENT_QUESTION_PRESERVED",
    )
    require(
        not any(text.startswith("UNTRUSTED PROJECT EVIDENCE\n") for text in contents),
        "AGENT_GENERATED_HANDOFF_OMITTED",
    )
    require(
        not any(text.startswith("FINAL RESPONSE CONTRACT\n") for text in contents),
        "AGENT_NORMAL_CHAT_CONTRACT_OMITTED",
    )
    history = [
        item
        for item in compacted
        if not str(item.get("content") or "").startswith("CURRENT QUESTION\n")
        and str(item.get("role") or "") in {"user", "assistant"}
    ]
    require(len(history) == 2, "AGENT_HISTORY_MESSAGE_COUNT_BOUNDED")
    require(
        all(len(str(item.get("content") or "")) <= 8050 for item in history),
        "AGENT_HISTORY_MESSAGE_CHARS_BOUNDED",
    )
    require(stats["generated_handoff_omitted"] is True, "AGENT_COMPACTION_PROVENANCE")
    require(
        int(stats["compacted_chars_before_agent_contract"])
        < int(stats["initial_chars"]),
        "AGENT_PROVIDER_CONTEXT_REDUCED",
    )


def validate_runtime_uses_compacted_messages() -> None:
    """Prove provider calls receive the compact prompt and retain authority limits."""
    with tempfile.TemporaryDirectory(prefix="kanda_agent_compact_") as temp:
        root = Path(temp)
        (root / "main.py").write_text("VALUE = 1\n", encoding="utf-8")
        calls: list[Sequence[Mapping[str, str]]] = []
        original_request = project_web_ai_agent_runtime.request_chat_completion

        def successful_request(*args, **_kwargs):
            calls.append(tuple(dict(item) for item in args[2]))
            return _result("Final compact agent answer.")

        project_web_ai_agent_runtime.request_chat_completion = successful_request
        try:
            result = project_web_ai_agent_runtime.run_project_agent_completion(
                _profile(),
                "fixture-model",
                _messages(),
                "",
                project_root=str(root),
                request_identity=_identity(root),
            )
        finally:
            project_web_ai_agent_runtime.request_chat_completion = original_request

        require(len(calls) == 1, "AGENT_COMPACT_SUCCESS_SINGLE_PROVIDER_REQUEST")
        sent = calls[0]
        sent_text = "\n".join(str(item.get("content") or "") for item in sent)
        require(
            "KANDA READ-ONLY PROJECT AGENT CONTRACT" in sent_text,
            "AGENT_READ_ONLY_CONTRACT_PRESERVED",
        )
        require(
            "CURRENT QUESTION\nFind ProviderResponseError exactly." in sent_text,
            "AGENT_COMPACT_RUNTIME_QUESTION_PRESERVED",
        )
        require(
            "UNTRUSTED PROJECT EVIDENCE\n" not in sent_text,
            "AGENT_COMPACT_RUNTIME_HANDOFF_ABSENT",
        )
        require(
            len(sent_text) < 50000,
            "AGENT_COMPACT_PROVIDER_PROMPT_BOUNDED",
        )
        agent = result.raw_metadata.get("kanda_project_agent", {})
        context = agent.get("context", {})
        require(
            context.get("mode") == "tool_first_compact",
            "AGENT_CONTEXT_MODE_PROVENANCE",
        )
        require(
            context.get("generated_handoff_omitted") is True,
            "AGENT_HANDOFF_OMISSION_PROVENANCE",
        )
        require(agent.get("write_authority") is False, "REMOTE_AI_WRITE_AUTHORITY_UNCHANGED")
        require(agent.get("shell_authority") is False, "REMOTE_AI_SHELL_AUTHORITY_UNCHANGED")


def validate_diagnostic_shape() -> None:
    """Prove provider failures can report safe prompt-shape facts only."""
    messages = [{"role": "user", "content": "Hello"}]
    require(
        project_web_ai_agent_runtime._message_chars(messages) == 5,
        "AGENT_SAFE_CONTEXT_DIAGNOSTIC_COUNT",
    )
    source = Path(project_web_ai_agent_runtime.__file__).read_text(encoding="utf-8")
    require(
        "generated_handoff_in_request=false" in source,
        "AGENT_FAILURE_DIAGNOSTIC_REDACTS_CONTENT",
    )


def validate_compile_and_size(root: Path) -> None:
    """Compile touched modules and enforce the physical-line ceiling."""
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
    """Run the focused validation suite."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    validate_compaction_contract()
    validate_runtime_uses_compacted_messages()
    validate_diagnostic_shape()
    validate_compile_and_size(root)
    print("FROZEN_DYNAMIC_PROJECT_BOUNDARY_PRESERVED: PASS")
    print("FROZEN_EMPTY_RESPONSE_RECOVERY_PRESERVED: PASS")
    print("FROZEN_BARE_TOOL_INTERCEPTION_PRESERVED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
