# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_agent_runtime.py
"""Iterative read-only Project agent runtime for Project Web AI.

The remote model may request bounded local reads through KANDA. This runtime
never writes source, runs commands, or grants direct filesystem authority.
"""

from __future__ import annotations

from threading import Event
from typing import Mapping, Sequence

from kanda_reasoner_app.reasoner_engine.project_web_ai_boundary_context import (
    ProjectAgentBoundaryContext,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_agent_protocol import (
    ProjectAgentProtocolError,
    inject_agent_contract,
    parse_agent_tool_request,
    render_agent_tool_result,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_read_tools import (
    ProjectReadToolBroker,
    ProjectReadToolError,
)
from kanda_reasoner_app.reasoner_engine import (
    project_web_ai_agent_evidence,
    project_web_ai_agent_terminal,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ChatUsage,
    GatewayProfile,
    ProviderCancelledError,
    ProviderError,
    ProviderResponseError,
    ProjectWebAIRequestIdentity,
)
from kanda_reasoner_app.web_ai_provider_runtime import (
    request_chat_completion,
    stream_chat_completion,
)

__all__ = ["run_project_agent_completion"]

MAX_AGENT_ROUNDS = 6
MAX_AGENT_MESSAGE_CHARS = 180_000
MAX_AGENT_HISTORY_MESSAGES = 2
MAX_AGENT_HISTORY_CHARS = 8_000
_CURRENT_QUESTION_PREFIX = "CURRENT QUESTION\n"
_PROJECT_EVIDENCE_PREFIX = "UNTRUSTED PROJECT EVIDENCE\n"
_NORMAL_FINAL_CONTRACT_PREFIX = "FINAL RESPONSE CONTRACT\n"


def _compact_initial_agent_messages(
    messages: Sequence[Mapping[str, str]],
) -> tuple[list[dict[str, str]], dict[str, object]]:
    """Return a compact tool-first agent prompt without generated handoff text."""
    copied = [dict(item) for item in messages]
    original_chars = _message_chars(copied)
    system: list[dict[str, str]] = []
    body = copied
    if copied and str(copied[0].get("role") or "") == "system":
        system = [copied[0]]
        body = copied[1:]

    evidence_omitted = 0
    final_contract_omitted = 0
    filtered: list[dict[str, str]] = []
    for item in body:
        content = str(item.get("content") or "")
        if content.startswith(_PROJECT_EVIDENCE_PREFIX):
            evidence_omitted += 1
            continue
        if content.startswith(_NORMAL_FINAL_CONTRACT_PREFIX):
            final_contract_omitted += 1
            continue
        filtered.append(item)

    question_index = -1
    for index, item in enumerate(filtered):
        if str(item.get("content") or "").startswith(_CURRENT_QUESTION_PREFIX):
            question_index = index

    retained_history: list[dict[str, str]] = []
    current_and_tail: list[dict[str, str]] = []
    if question_index >= 0:
        history = [
            item
            for item in filtered[:question_index]
            if str(item.get("role") or "") in {"user", "assistant"}
        ]
        retained_history = [
            _bounded_history_message(item)
            for item in history[-MAX_AGENT_HISTORY_MESSAGES:]
        ]
        current_and_tail = filtered[question_index:]
    else:
        retained_history = [
            _bounded_history_message(item)
            for item in filtered[-MAX_AGENT_HISTORY_MESSAGES:]
        ]

    compacted = system + retained_history + current_and_tail
    stats: dict[str, object] = {
        "mode": "tool_first_compact",
        "generated_handoff_omitted": evidence_omitted > 0,
        "normal_final_contract_omitted": final_contract_omitted > 0,
        "initial_message_count": len(copied),
        "compacted_message_count": len(compacted),
        "initial_chars": original_chars,
        "compacted_chars_before_agent_contract": _message_chars(compacted),
        "history_messages_retained": len(retained_history),
    }
    return compacted, stats


def _bounded_history_message(item: Mapping[str, str]) -> dict[str, str]:
    """Return one bounded history item without changing its role."""
    role = str(item.get("role") or "")
    content = str(item.get("content") or "")
    if len(content) > MAX_AGENT_HISTORY_CHARS:
        content = content[:MAX_AGENT_HISTORY_CHARS] + "\n[history truncated by KANDA]"
    return {"role": role, "content": content}


def _message_chars(messages: Sequence[Mapping[str, str]]) -> int:
    """Return the total provider-visible message character count."""
    return sum(len(str(item.get("content") or "")) for item in messages)


def run_project_agent_completion(
    profile: GatewayProfile,
    model_id: str,
    messages: Sequence[Mapping[str, str]],
    api_key: str,
    *,
    project_root: str,
    request_identity: ProjectWebAIRequestIdentity,
    cancel_event: Event | None = None,
) -> ChatResult:
    """Run a bounded read-only tool loop and return the final model answer."""
    boundary = ProjectAgentBoundaryContext.from_request(
        project_root, request_identity
    )
    broker = ProjectReadToolBroker(
        project_root, boundary=boundary, cancel_event=cancel_event
    )
    compact_messages, context_stats = _compact_initial_agent_messages(messages)
    conversation = inject_agent_contract(compact_messages, boundary)
    context_stats["provider_message_count"] = len(conversation)
    context_stats["provider_chars"] = _message_chars(conversation)
    tool_trace: list[dict[str, object]] = []
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    total_cost = 0.0
    cost_known = False
    provider_name = ""
    last_result: ChatResult | None = None
    transport_modes: list[str] = []
    seen_requests: set[str] = set()
    duplicate_requests = 0
    terminal_reason = "maximum_tool_rounds"
    tool_results: list[str] = []

    for round_number in range(1, MAX_AGENT_ROUNDS + 1):
        _raise_if_cancelled(cancel_event)
        _enforce_message_budget(conversation)
        result = _request_agent_turn(
            profile,
            model_id,
            conversation,
            api_key,
            request_id=request_identity.request_id,
            cancel_event=cancel_event,
        )
        last_result = result
        transport_modes.append(_result_transport_mode(result))
        prompt_tokens += result.usage.prompt_tokens
        completion_tokens += result.usage.completion_tokens
        total_tokens += result.usage.total_tokens
        provider_name = result.usage.provider_name or provider_name
        if result.usage.cost_usd is not None:
            total_cost += result.usage.cost_usd
            cost_known = True

        try:
            request = parse_agent_tool_request(result.content)
        except ProjectAgentProtocolError as exc:
            conversation.append({"role": "assistant", "content": result.content})
            conversation.append(
                {
                    "role": "user",
                    "content": (
                        "KANDA PROJECT TOOL REQUEST REJECTED\n"
                        + str(exc)
                        + "\nReturn one corrected marker block or answer normally."
                    ),
                }
            )
            tool_trace.append(
                {
                    "round": round_number,
                    "tool": "protocol_rejection",
                    "ok": False,
                }
            )
            continue

        if request is None:
            return _final_agent_result(
                result,
                tool_trace=tool_trace,
                usage=ChatUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    cost_usd=total_cost if cost_known else None,
                    provider_name=provider_name,
                ),
                transport_modes=transport_modes,
                context_stats=context_stats,
            )

        conversation.append({"role": "assistant", "content": result.content})
        if project_web_ai_agent_terminal.register_tool_request(
            seen_requests, request.tool, request.arguments
        ):
            duplicate_requests += 1
            tool_trace.append(
                {
                    "round": round_number,
                    "tool": request.tool,
                    "ok": False,
                    "duplicate": True,
                }
            )
            conversation.append(
                {
                    "role": "user",
                    "content": (
                        "KANDA DUPLICATE PROJECT TOOL REQUEST REJECTED\n"
                        "The exact request already ran and would add no evidence. "
                        "Use existing results, request a different read-only tool, "
                        "or answer now."
                    ),
                }
            )
            if (
                duplicate_requests
                >= project_web_ai_agent_terminal.MAX_DUPLICATE_TOOL_REQUESTS
            ):
                terminal_reason = "duplicate_tool_loop"
                break
            continue
        try:
            tool_result = broker.execute(request.tool, request.arguments)
        except ProjectReadToolError as exc:
            result_text = render_agent_tool_result(
                request,
                ok=False,
                error=str(exc),
                round_number=round_number,
            )
            tool_trace.append(
                {
                    "round": round_number,
                    "tool": request.tool,
                    "ok": False,
                    "error": str(exc)[:240],
                }
            )
        else:
            result_text = render_agent_tool_result(
                request,
                ok=True,
                payload=tool_result.payload,
                round_number=round_number,
            )
            tool_trace.append(
                {
                    "round": round_number,
                    "tool": request.tool,
                    "ok": True,
                    "summary": project_web_ai_agent_evidence.tool_summary(
                        tool_result.payload
                    ),
                }
            )
        tool_results.append(result_text)
        project_web_ai_agent_terminal.append_grounded_tool_result(
            conversation,
            project_web_ai_agent_evidence.compact_tool_result_text(result_text),
        )

    if last_result is None:
        raise ProviderResponseError("Project agent did not start a model request.")
    terminal_messages, terminal_stats = (
        project_web_ai_agent_evidence.build_terminal_synthesis_messages(
            conversation, tool_results
        )
    )
    context_stats.update(terminal_stats)
    project_web_ai_agent_terminal.append_terminal_synthesis_prompt(
        terminal_messages
    )
    context_stats["terminal_provider_message_count"] = len(terminal_messages)
    context_stats["terminal_provider_chars"] = _message_chars(terminal_messages)
    _raise_if_cancelled(cancel_event)
    _enforce_message_budget(terminal_messages)
    terminal = _request_agent_turn(
        profile,
        model_id,
        terminal_messages,
        api_key,
        request_id=request_identity.request_id,
        cancel_event=cancel_event,
        max_tokens=project_web_ai_agent_evidence.TERMINAL_SYNTHESIS_MAX_TOKENS,
    )
    transport_modes.append(_result_transport_mode(terminal))
    prompt_tokens += terminal.usage.prompt_tokens
    completion_tokens += terminal.usage.completion_tokens
    total_tokens += terminal.usage.total_tokens
    provider_name = terminal.usage.provider_name or provider_name
    if terminal.usage.cost_usd is not None:
        total_cost += terminal.usage.cost_usd
        cost_known = True
    try:
        terminal_request = parse_agent_tool_request(terminal.content)
    except ProjectAgentProtocolError as exc:
        raise ProviderResponseError(
            "Project agent terminal synthesis returned an invalid tool request."
        ) from exc
    if terminal_request is not None:
        raise ProviderResponseError(
            "Project agent terminal synthesis requested another tool instead of "
            "answering from collected evidence."
        )
    context_stats["terminal_synthesis_used"] = True
    context_stats["terminal_reason"] = terminal_reason
    context_stats["duplicate_tool_requests"] = duplicate_requests
    return _final_agent_result(
        terminal,
        tool_trace=tool_trace,
        usage=ChatUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=total_cost if cost_known else None,
            provider_name=provider_name,
        ),
        transport_modes=transport_modes,
        context_stats=context_stats,
    )


def _request_agent_turn(
    profile: GatewayProfile,
    model_id: str,
    messages: Sequence[Mapping[str, str]],
    api_key: str,
    *,
    request_id: str,
    cancel_event: Event | None,
    max_tokens: int | None = None,
) -> ChatResult:
    """Run one agent turn with one bounded alternate-transport recovery."""
    request_options = {} if max_tokens is None else {"max_tokens": max_tokens}
    try:
        result = request_chat_completion(
            profile, model_id, messages, api_key, request_id=request_id,
            **request_options
        )
    except ProviderResponseError as exc:
        if not _is_empty_response_error(exc):
            raise
        _raise_if_cancelled(cancel_event)
        try:
            result = stream_chat_completion(
                profile, model_id, messages, api_key, request_id=request_id,
                cancel_event=cancel_event, allow_non_stream_fallback=False,
                **request_options
            )
        except ProviderCancelledError:
            raise
        except ProviderError as recovery_exc:
            shape = (
                "agent_messages=" + str(len(messages))
                + "; agent_chars=" + str(_message_chars(messages))
                + "; generated_handoff_in_request=false"
                + "; agent_max_tokens="
                + (str(max_tokens) if max_tokens is not None else "default")
            )
            raise recovery_exc.__class__(
                "Project agent stream recovery failed after an empty "
                "non-streaming response. " + str(recovery_exc) + " " + shape
            ) from recovery_exc
        return _with_transport_mode(
            result,
            "stream_recovery_after_empty_non_stream",
        )
    return _with_transport_mode(result, "non_stream")


def _is_empty_response_error(exc: ProviderResponseError) -> bool:
    """Return whether the provider failure is eligible for transport recovery."""
    message = str(exc).lower()
    return (
        "empty response" in message
        or "did not contain a usable choice" in message
    )


def _with_transport_mode(result: ChatResult, mode: str) -> ChatResult:
    """Return one result with safe per-turn transport provenance."""
    metadata = dict(result.raw_metadata)
    transport = metadata.get("kanda_transport")
    details = dict(transport) if isinstance(transport, Mapping) else {}
    details["mode"] = str(mode)
    metadata["kanda_transport"] = details
    return ChatResult(
        request_id=result.request_id,
        gateway_id=result.gateway_id,
        requested_model=result.requested_model,
        returned_model=result.returned_model,
        content=result.content,
        finish_reason=result.finish_reason,
        response_id=result.response_id,
        usage=result.usage,
        raw_metadata=metadata,
    )


def _result_transport_mode(result: ChatResult) -> str:
    """Return the safe per-turn transport mode for aggregate provenance."""
    transport = result.raw_metadata.get("kanda_transport", {})
    if not isinstance(transport, Mapping):
        return "unknown"
    return str(transport.get("mode") or "unknown")


def _final_agent_result(
    result: ChatResult,
    *,
    tool_trace: list[dict[str, object]],
    usage: ChatUsage,
    transport_modes: Sequence[str],
    context_stats: Mapping[str, object],
) -> ChatResult:
    """Return the final answer with bounded agent provenance."""
    metadata = dict(result.raw_metadata)
    agent_mode = (
        "project_agent_stream_recovery"
        if "stream_recovery_after_empty_non_stream" in transport_modes
        else "project_agent_non_stream"
    )
    metadata["kanda_transport"] = {
        "mode": agent_mode,
        "tool_rounds": len(tool_trace),
        "turn_modes": list(transport_modes),
    }
    metadata["kanda_project_agent"] = {
        "read_only": True,
        "tool_rounds": len(tool_trace),
        "tools": tool_trace,
        "write_authority": False,
        "shell_authority": False,
        "boundary_identity_bound": True,
        "context": dict(context_stats),
    }
    return ChatResult(
        request_id=result.request_id,
        gateway_id=result.gateway_id,
        requested_model=result.requested_model,
        returned_model=result.returned_model,
        content=result.content,
        finish_reason=result.finish_reason,
        response_id=result.response_id,
        usage=usage,
        raw_metadata=metadata,
    )


def _raise_if_cancelled(cancel_event: Event | None) -> None:
    """Raise the canonical cancellation error before each provider or tool step."""
    if cancel_event is not None and cancel_event.is_set():
        raise ProviderCancelledError("Request cancelled by user.")


def _enforce_message_budget(messages: Sequence[Mapping[str, str]]) -> None:
    """Fail closed when iterative tool evidence exceeds the bounded prompt size."""
    total = sum(len(str(item.get("content") or "")) for item in messages)
    if total > MAX_AGENT_MESSAGE_CHARS:
        raise ProviderResponseError(
            "Project agent context exceeded the bounded message budget."
        )
