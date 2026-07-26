# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_agent_terminal.py
"""Terminal-synthesis safeguards for the read-only Project Web AI agent."""

from __future__ import annotations

import json
from typing import Mapping

__all__ = [
    "MAX_DUPLICATE_TOOL_REQUESTS",
    "append_grounded_tool_result",
    "append_terminal_synthesis_prompt",
    "register_tool_request",
]

MAX_DUPLICATE_TOOL_REQUESTS = 2
_GROUNDING_REMINDER = (
    "\nFINAL ANSWER GROUNDING: Name only files, symbols, tools, and line ranges "
    "explicitly supported by KANDA tool results. State unresolved details "
    "instead of inventing them."
)
_TERMINAL_SYNTHESIS_PROMPT = (
    "KANDA TERMINAL SYNTHESIS\nThe read-only tool phase is closed. Do not "
    "request another tool. Answer the current question now using only exact "
    "KANDA tool results already present. Do not invent files, functions, "
    "classes, tools, or line ranges; mark unsupported details unresolved."
)


def register_tool_request(
    seen: set[str], tool: str, arguments: Mapping[str, object]
) -> bool:
    """Return true for a duplicate; otherwise register the request identity."""
    fingerprint = json.dumps(
        {"tool": str(tool), "arguments": dict(arguments)},
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    if fingerprint in seen:
        return True
    seen.add(fingerprint)
    return False


def append_grounded_tool_result(
    conversation: list[dict[str, str]], result_text: str
) -> None:
    """Append one tool result plus a strict evidence-grounding reminder."""
    conversation.append(
        {"role": "user", "content": str(result_text) + _GROUNDING_REMINDER}
    )


def append_terminal_synthesis_prompt(
    conversation: list[dict[str, str]],
) -> None:
    """Close the tool phase and require a final evidence-only answer."""
    conversation.append({"role": "user", "content": _TERMINAL_SYNTHESIS_PROMPT})
