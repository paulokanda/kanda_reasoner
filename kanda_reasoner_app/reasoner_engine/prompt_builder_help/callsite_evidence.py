"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from typing import Any

from .prompt_classification import is_which_method_calls_question, norm_text, tokenize_query

__all__ = [
    "extract_exact_call_targets",
    "prioritize_callsite_snippets",
    "append_callsite_evidence_section",
]


def extract_exact_call_targets(question: str) -> list[str]:
    q = norm_text(question)
    if not is_which_method_calls_question(q):
        return []

    out: list[str] = []
    for token in tokenize_query(q):
        if ("_" in token or "." in token) and len(token) >= 6:
            out.append(token)
    return out


def prioritize_callsite_snippets(
    question: str,
    snippet_evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    exact_call_targets = extract_exact_call_targets(question)
    if not exact_call_targets:
        return []

    prioritized: list[dict[str, Any]] = []

    for snippet in list(snippet_evidence):
        text = str(snippet.get("text", "") or "")
        text_norm = text.lower()
        anchor = str(snippet.get("anchor", "") or "").strip().lower()

        matched = False
        for target in exact_call_targets:
            target_tail = target.split(".")[-1].lower()

            has_direct_call = (
                f"{target_tail}(" in text_norm and f"def {target_tail}(" not in text_norm
            )
            import_only = f"import {target_tail}" in text_norm and not has_direct_call
            is_callee_definition = anchor == target_tail or anchor.endswith("." + target_tail)

            if has_direct_call and not import_only and not is_callee_definition:
                matched = True
                break

        if matched:
            prioritized.append(snippet)

    def _callsite_rank(snippet: dict[str, Any]) -> tuple[int, int, int, int]:
        text = str(snippet.get("text", "") or "").lower()
        anchor = str(snippet.get("anchor", "") or "").strip().lower()
        line = int(snippet.get("line", 10**9) or 10**9)

        call_positions: list[int] = []
        import_positions: list[int] = []

        for target in exact_call_targets:
            target_tail = target.split(".")[-1].lower()

            call_pos = text.find(f"{target_tail}(")
            if call_pos != -1:
                call_positions.append(call_pos)

            import_pos = text.find(f"import {target_tail}")
            if import_pos != -1:
                import_positions.append(import_pos)

        first_call_pos = min(call_positions) if call_positions else 10**9
        first_import_pos = min(import_positions) if import_positions else 10**9

        has_import_before_call = first_import_pos < first_call_pos
        is_method_like_anchor = "." in anchor
        is_class_like_anchor = not is_method_like_anchor

        return (
            1 if has_import_before_call else 0,
            1 if is_class_like_anchor else 0,
            first_call_pos,
            line,
        )

    prioritized.sort(key=_callsite_rank)
    return prioritized


def append_callsite_evidence_section(
    lines: list[str],
    prioritized_callsite_snippets: list[dict[str, Any]],
) -> None:
    if not prioritized_callsite_snippets:
        return

    lines.append("")
    lines.append("CALL-SITE EVIDENCE")
    lines.append(
        "For caller questions, prefer these snippets first. "
        "A valid caller snippet must show the actual invocation of the asked callee, "
        "not merely the callee definition or an import."
    )
    for i, snippet in enumerate(prioritized_callsite_snippets[:5], start=1):
        lines.append(
            f"[CS{i:02d}] path={snippet.get('path')} line={snippet.get('line')} anchor={snippet.get('anchor')}"
        )
        lines.append(str(snippet.get("text", "")).rstrip())
        lines.append("")


