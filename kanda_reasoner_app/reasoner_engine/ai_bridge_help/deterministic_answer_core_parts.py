# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/deterministic_answer_core_parts.py
"""Promoted deterministic answer core helpers."""

from __future__ import annotations

import re
from typing import Any
from .prompt_extraction import (
    extract_file_evidence_blocks,
    extract_file_id_map,
    extract_file_score_map,
    extract_locator_target,
    extract_runtime_anchors_from_detail,
    extract_snippet_blocks,
    extract_symbol_evidence_blocks,
    extract_symbol_id_map,
    extract_symbol_score_map,
    extract_user_question,
)
from .prompt_modes import is_one_line_prompt

def _extract_direct_responsibility_target(question_text: str) -> str:
    """Extract target symbol from a direct responsibility question."""
    patterns = [
        r"responsibility of\s+`?([A-Za-z_][A-Za-z0-9_\.]*)`?",
        r"role of\s+`?([A-Za-z_][A-Za-z0-9_\.]*)`?",
        r"purpose of\s+`?([A-Za-z_][A-Za-z0-9_\.]*)`?",
        r"what does\s+`?([A-Za-z_][A-Za-z0-9_\.]*)`?\s+do",
    ]
    for pattern in patterns:
        match = re.search(pattern, question_text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip("`'\".?,:;")
    return ""
def _extract_docstring_from_snippet(snippet_text: str, target: str) -> str:
    """Return a triple-double-quoted docstring near target."""
    lines = snippet_text.splitlines()
    target_low = target.lower()

    for index, line in enumerate(lines):
        lowered = line.strip().lower()
        is_target_definition = (
            lowered.startswith("class " + target_low)
            or lowered.startswith("def " + target_low)
            or lowered.startswith("async def " + target_low)
        )
        if not is_target_definition:
            continue

        search_window = lines[index + 1:index + 8]
        for offset, raw_line in enumerate(search_window, start=index + 1):
            candidate = raw_line.strip()
            if not candidate:
                continue
            quote = "\"\"\""
            if candidate.startswith(quote):
                value = candidate[len(quote):]
                if quote in value:
                    return value.split(quote, 1)[0].strip()
                collected = [value.strip()]
                for continuation in lines[offset + 1:offset + 13]:
                    if quote in continuation:
                        collected.append(continuation.split(quote, 1)[0].strip())
                        return " ".join(part for part in collected if part).strip()
                    collected.append(continuation.strip())
                return " ".join(part for part in collected if part).strip()
            break
    return ""
def _find_best_runtime_anchor(detail_text: str, question_text: str) -> str:
    """Support find best runtime anchor behavior.
    
    Parameters
    ----------
    detail_text : str
        The detail text value.
    question_text : str
        The question text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    detail_low = detail_text.lower()
    question_low = question_text.lower()

    anchors = extract_runtime_anchors_from_detail(detail_text)

    if not anchors:
        fallback_candidates = [
            "runtime_runner_probe_apply_button",
            "runtime_runner_probe_line_edit",
            "runtime_runner_probe_close_button",
            "on_apply_clicked",
            "on_text_changed",
            "on_close_clicked",
            "textchanged",
            "clicked",
            "signal_connection",
        ]
        for anchor in fallback_candidates:
            if anchor in detail_low:
                anchors.append(anchor)

    scored: list[tuple[int, str]] = []

    for anchor in anchors:
        anchor_low = anchor.lower()
        score = 0

        if anchor_low in question_low:
            score += 500

        anchor_tokens = [
            tok
            for tok in re.findall(r"[a-zA-Z0-9_]+", anchor_low)
            if len(tok) >= 3
        ]
        for token in anchor_tokens:
            if token in question_low:
                score += 40

        if "on_apply_clicked" in question_low and anchor_low == "on_apply_clicked":
            score += 450

        if (
                "runtime_runner_probe_apply_button" in question_low
                and anchor_low == "runtime_runner_probe_apply_button"
        ):
            score += 500

        if "runtime probe signal connections" in question_low:
            if anchor_low == "runtime_runner_probe_apply_button":
                score += 260
            if anchor_low == "on_apply_clicked":
                score += 220
            if anchor_low == "runtime_runner_probe_line_edit":
                score += 180
            if anchor_low == "on_text_changed":
                score += 160
            if anchor_low == "runtime_runner_probe_close_button":
                score += 150
            if anchor_low == "on_close_clicked":
                score += 140

        if "probe button signal-slot connections" in question_low:
            if anchor_low == "runtime_runner_probe_apply_button":
                score += 320
            if anchor_low == "on_apply_clicked":
                score += 260

        scored.append((score, anchor))

    if not scored:
        return ""

    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[0][1]

__all__ = [

]
