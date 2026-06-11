"""Prompt section helpers for Project Reasoner."""

from __future__ import annotations

from typing import Any

__all__ = [
    "append_project_summary",
    "append_memory_section",
    "append_file_evidence_section",
    "append_symbol_evidence_section",
    "append_live_source_evidence_section",
    "append_source_snippets_section",
    "is_live_source_snippet",
]


def append_project_summary(
    lines: list[str],
    project_root: str,
    summary: dict[str, Any],
) -> None:
    """Append the project summary section."""
    lines.append("")
    lines.append("PROJECT SUMMARY")
    lines.append("Project root: " + str(project_root))
    lines.append("Python files indexed: " + str(summary.get("python_file_count", "")))
    lines.append("Entry files: " + ", ".join(summary.get("entry_files", [])))
    lines.append("")


def append_memory_section(lines: list[str], memory_turns: list[Any]) -> None:
    """Append recent conversation memory."""
    if memory_turns:
        lines.append("CONVERSATION MEMORY")
        for idx, turn in enumerate(memory_turns[-3:], start=1):
            lines.append("Previous question " + str(idx) + ": " + turn.question)
            lines.append("Previous answer " + str(idx) + ": " + turn.answer[:900])
            lines.append("Model: " + turn.selected_model)
            lines.append("")
        return

    lines.append("CONVERSATION MEMORY")
    lines.append("None")
    lines.append("")


def append_file_evidence_section(lines: list[str], file_evidence: list[Any]) -> None:
    """Append file-level evidence."""
    lines.append("FILE EVIDENCE")
    for item in file_evidence:
        lines.append(f"[{item.evidence_id}] score={item.score}")
        lines.append(item.detail)
        lines.append("")


def append_symbol_evidence_section(lines: list[str], symbol_evidence: list[Any]) -> None:
    """Append symbol-level evidence."""
    lines.append("SYMBOL EVIDENCE")
    for item in symbol_evidence:
        lines.append(f"[{item.evidence_id}] score={item.score}")
        lines.append(item.detail)
        lines.append("")


def is_live_source_snippet(item: dict[str, Any]) -> bool:
    """Return True when a snippet came from live-source verification."""
    anchor = str(item.get("anchor", ""))
    return anchor.startswith("LIVE_SOURCE:")


def _append_snippet_item(lines: list[str], item: dict[str, Any]) -> None:
    """Append one snippet item."""
    lines.append(
        f"[{item['snippet_id']}] {item['path']}:{item['line']} anchor={item['anchor']}"
    )
    lines.append(str(item["text"]))
    lines.append("")


def append_live_source_evidence_section(
    lines: list[str],
    snippet_evidence: list[dict[str, Any]],
) -> None:
    """Append live-source snippets in a dedicated evidence section."""
    live_items = [item for item in snippet_evidence if is_live_source_snippet(item)]
    if not live_items:
        return

    lines.append("LIVE SOURCE EVIDENCE")
    lines.append(
        "These snippets were verified from current files under PROJECT_ROOT and may be used as code-level implementation truth."
    )
    for item in live_items:
        _append_snippet_item(lines, item)


def append_source_snippets_section(
    lines: list[str],
    snippet_evidence: list[dict[str, Any]],
) -> None:
    """Append normal JSON-derived source snippets.

    Live-source snippets are intentionally excluded here because they are shown
    in the dedicated LIVE SOURCE EVIDENCE section.
    """
    lines.append("SOURCE SNIPPETS")
    for item in snippet_evidence:
        if is_live_source_snippet(item):
            continue
        _append_snippet_item(lines, item)
