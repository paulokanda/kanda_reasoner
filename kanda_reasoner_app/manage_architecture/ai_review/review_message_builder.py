# project-path: kanda_reasoner_app/manage_architecture/ai_review/review_message_builder.py
"""Build bounded prompts for Tab 1 advisory AI review."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import ADVISORY_BANNER, DEFAULT_MAX_AUDIT_CHARS, Tab1AIReviewRequest

__all__ = [
    "build_tab1_ai_review_messages",
    "limit_audit_text",
    "mark_project_root",
]

TRUNCATION_NOTE = "[... truncated for model context ...]"


def _path_variants(path_text: str) -> tuple[str, ...]:
    """Return path text variants that should be replaced by a root marker."""
    if not path_text:
        return ()

    variants = {path_text}
    variants.add(path_text.replace("\\", "/"))
    variants.add(path_text.replace("/", "\\"))
    try:
        resolved = str(Path(path_text).expanduser().resolve())
        variants.add(resolved)
        variants.add(resolved.replace("\\", "/"))
        variants.add(resolved.replace("/", "\\"))
    except Exception:
        pass

    return tuple(sorted(variants, key=len, reverse=True))


def mark_project_root(text: str, project_root: str) -> str:
    """Replace the absolute project root in audit text with <PROJECT_ROOT>."""
    marked = str(text)
    for variant in _path_variants(str(project_root).strip()):
        if variant and variant not in (".", "./", ".\\"):
            marked = marked.replace(variant, "<PROJECT_ROOT>")
    return marked


def limit_audit_text(
    audit_text: str,
    max_chars: int = DEFAULT_MAX_AUDIT_CHARS,
) -> tuple[str, bool]:
    """Return bounded audit text and whether truncation was required."""
    text = str(audit_text)
    if max_chars <= 0:
        return "", bool(text)
    if len(text) <= max_chars:
        return text, False

    note = "\n\n" + TRUNCATION_NOTE + "\n\n"
    if max_chars <= len(note) + 20:
        return text[:max_chars], True

    remaining = max_chars - len(note)
    head_len = remaining // 2
    tail_len = remaining - head_len
    return text[:head_len] + note + text[-tail_len:], True


def _count_issue_lines(audit_text: str) -> int:
    """Count likely deterministic finding lines in the audit output."""
    prefixes = ("ERROR ", "WARNING ", "FAIL ", "PASS ", "SKIP ")
    count = 0
    for line in audit_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefixes):
            count += 1
    return count


def build_tab1_ai_review_messages(
    request: Tab1AIReviewRequest,
) -> list[dict[str, Any]]:
    """Build local-model chat messages for an advisory Tab 1 audit review."""
    marked = mark_project_root(request.audit_text, request.project_root)
    bounded, truncated = limit_audit_text(marked, request.max_audit_chars)
    issue_count = _count_issue_lines(bounded)

    system_text = (
        "You are a read-only software architecture review assistant for Kanda "
        "Reasoner Tab 1. Your job is to interpret deterministic audit output. "
        "You are advisory only. You must not claim to replace deterministic "
        "validation. You must not write code, apply patches, or mark anything "
        "frozen. Prefer precise risk ranking and safe next inspection steps. "
        "Use only the supplied audit output. If evidence is insufficient, say so."
    )

    user_text = (
        ADVISORY_BANNER
        + "\n\n"
        + "Review source: "
        + request.source_label
        + "\n"
        + "Project root marker: <PROJECT_ROOT>\n"
        + "Likely finding lines in supplied text: "
        + str(issue_count)
        + "\n"
        + "Audit text was truncated: "
        + str(truncated)
        + "\n\n"
        + "Return exactly these sections in plain text:\n"
        + "1. Advisory summary\n"
        + "2. Highest risks first\n"
        + "3. Suggested next inspection files\n"
        + "4. Safest next actions\n"
        + "5. What deterministic validation still decides\n\n"
        + "Audit output:\n"
        + "```text\n"
        + bounded
        + "\n```"
    )

    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": user_text},
    ]
