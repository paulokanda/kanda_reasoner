"""Focused snippet selection helpers for Project Reasoner AI bridge.

This module belongs to the AI Bridge helper box. It scores source snippets
already present in the evidence prompt and builds an optional focus message for
generative answers.
"""

from __future__ import annotations

import re
from typing import Any

from .prompt_extraction import (
    extract_file_evidence_blocks,
    extract_snippet_blocks,
    extract_user_question,
)
from .prompt_modes import is_code_localized_prompt, is_generative_prompt

__all__ = [
    "score_snippet_candidate",
    "select_focus_snippets_from_prompt",
    "build_generative_focus_message",
]


def score_snippet_candidate(
    question: str,
    snippet_block: dict[str, Any],
    preferred_paths: list[str],
) -> int:
    """Return a relevance score for one snippet block."""
    q = question.strip().lower()
    path = str(snippet_block.get("path", "")).strip().lower()
    anchor = str(snippet_block.get("anchor", "")).strip().lower()
    text = str(snippet_block.get("text", "")).strip().lower()

    score = 0

    if path in preferred_paths:
        score += 180

    if anchor and anchor in q:
        score += 420

    for token in re.findall(r"[a-zA-Z0-9_.]+", q):
        if len(token) < 3:
            continue
        if token in anchor:
            score += 45
        if token in path:
            score += 20
        if token in text:
            score += 8

    if "runtime" in q and "runtime" in text:
        score += 80

    if "probe" in q and "probe" in text:
        score += 80

    if "on_apply_clicked" in q and "on_apply_clicked" in anchor:
        score += 260

    if (
        "runtime_runner_probe_apply_button" in q
        and "runtime_runner_probe_apply_button" in text
    ):
        score += 260

    if "signal" in q and (
        "connect" in text or "clicked" in text or "textchanged" in text
    ):
        score += 70

    return score


def select_focus_snippets_from_prompt(
    prompt: str,
    limit: int = 4,
) -> list[dict[str, Any]]:
    """Select the most relevant unique snippets from an evidence prompt."""
    question = extract_user_question(prompt)
    file_blocks = extract_file_evidence_blocks(prompt)
    snippet_blocks = extract_snippet_blocks(prompt)

    if not snippet_blocks:
        return []

    preferred_paths = [
        str(block.get("path", "")).strip().lower()
        for block in file_blocks[:3]
        if str(block.get("path", "")).strip()
    ]

    ranked = sorted(
        snippet_blocks,
        key=lambda block: score_snippet_candidate(question, block, preferred_paths),
        reverse=True,
    )

    out: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()

    for block in ranked:
        key = (
            str(block.get("path", "")).strip(),
            int(block.get("line", 0)),
            str(block.get("anchor", "")).strip(),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(block)
        if len(out) >= limit:
            break

    return out


def build_generative_focus_message(prompt: str) -> str:
    """Build a system focus message for generative prompts."""
    if not is_generative_prompt(prompt):
        return ""

    focus_snippets = select_focus_snippets_from_prompt(prompt, limit=4)

    if not focus_snippets:
        return ""

    lines: list[str] = []
    lines.append("GENERATION FOCUS")
    lines.append("Prioritize the snippet anchors below as primary evidence for this answer.")
    lines.append("Prefer the best matching snippets instead of summarizing all evidence equally.")

    if is_code_localized_prompt(prompt):
        lines.append(
            "For this question, answer as a code-localized walkthrough with file "
            "paths, anchors, line headers, and real snippet-backed excerpts."
        )
        lines.append("Use at least 2 of the focused snippets below when relevant.")

    lines.append("")
    lines.append("FOCUSED SNIPPETS")

    for block in focus_snippets:
        lines.append(
            "["
            + str(block.get("snippet_id", "")).strip()
            + "] "
            + str(block.get("path", "")).strip()
            + ":"
            + str(block.get("line", 0))
            + " anchor="
            + str(block.get("anchor", "")).strip()
        )

    lines.append("")
    lines.append("Answer only from the supplied evidence pack.")

    return "\n".join(lines)
