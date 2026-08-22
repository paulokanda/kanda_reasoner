# project-path: kanda_reasoner_app/error_memory/guard.py
"""Advisory Repeat Error Guard for project-specific Error Memory lessons.

This module is intentionally advisory-only.  It helps users and AI sessions
notice likely repeats before implementing or freezing a patch, but it must not
perform hard blocking, mutate lessons, or replace exact source inspection.
"""

from __future__ import annotations

import re
from pathlib import Path

from .backend import ErrorMemoryBackend, coerce_error_memory_backend
from typing import Any

from .fingerprint import build_fingerprint, extract_exception_info
from .models import compact_lesson
from .scrubber import scrub_text
from .store import bootstrap_error_memory_store, list_lessons, rebuild_index

GUARD_VERSION = "1.0"

_WORD_RE = re.compile(r"[A-Za-z0-9_]{4,}")


def _clean_text(value: Any) -> str:
    """Return a stable lower-case searchable text representation."""
    if isinstance(value, (list, tuple, set)):
        return "\n".join(_clean_text(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(_clean_text(item) for item in value.values())
    return str(value or "").strip().lower()


def _tokens(value: Any) -> set[str]:
    """Return compact searchable tokens, excluding tiny/noisy words."""
    return {match.group(0).lower() for match in _WORD_RE.finditer(str(value or ""))}


def _lesson_search_text(lesson: dict[str, Any]) -> str:
    """Return the lesson fields worth matching against current raw text."""
    fields = [
        lesson.get("symptom", ""),
        lesson.get("root_cause", ""),
        lesson.get("correct_fix", ""),
        lesson.get("do_not_repeat_rule", ""),
        lesson.get("long_term_prevention", ""),
        lesson.get("prevention_triggers", []),
        lesson.get("raw_error_snapshot_scrubbed", ""),
        lesson.get("exception", {}),
    ]
    return _clean_text(fields)


def _status_allowed(status: str, *, include_drafts: bool, include_deprecated: bool) -> bool:
    """Return whether a lesson status should participate in advisory matching."""
    normalized = str(status or "").strip().lower()
    if normalized == "active":
        return True
    if normalized == "draft":
        return include_drafts
    if normalized in {"deprecated", "superseded"}:
        return include_deprecated
    return False


def _match_label(score: int) -> str:
    """Support match label behavior.
    
    Parameters
    ----------
    score : int
        The score value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if score >= 85:
        return "exact"
    if score >= 50:
        return "partial"
    if score >= 25:
        return "weak"
    return "none"


def _score_lesson(
    incoming_exception: dict[str, Any],
    incoming_fingerprint: dict[str, Any],
    raw_text: str,
    lesson: dict[str, Any],
) -> dict[str, Any]:
    """Score a single lesson against the incoming error text."""
    raw_clean = _clean_text(raw_text)
    raw_tokens = _tokens(raw_text)
    lesson_exception = lesson.get("exception", {}) if isinstance(lesson.get("exception"), dict) else {}
    lesson_fingerprint = lesson.get("fingerprint", {}) if isinstance(lesson.get("fingerprint"), dict) else {}
    incoming_hash = str(incoming_fingerprint.get("fingerprint_hash", "") or "").strip()
    lesson_hash = str(lesson_fingerprint.get("fingerprint_hash", "") or "").strip()

    incoming_type = _clean_text(incoming_exception.get("type", ""))
    lesson_type = _clean_text(lesson_exception.get("type", ""))
    incoming_message = _clean_text(incoming_exception.get("message_normalized", ""))
    lesson_message = _clean_text(lesson_exception.get("message_normalized", ""))

    score = 0
    reasons: list[str] = []

    if incoming_hash and lesson_hash and incoming_hash == lesson_hash:
        score = max(score, 100)
        reasons.append("fingerprint hash matched exactly")

    if incoming_type and lesson_type and incoming_type == lesson_type:
        score = max(score, 35)
        reasons.append("exception type matched")
        if incoming_message and lesson_message and incoming_message == lesson_message:
            score = max(score, 90)
            reasons.append("normalized exception message matched")
        elif incoming_message and lesson_message and (incoming_message in lesson_message or lesson_message in incoming_message):
            score = max(score, 70)
            reasons.append("normalized exception message partially matched")

    if lesson_message and lesson_message in raw_clean:
        score = max(score, 65)
        reasons.append("raw error contains prior normalized message")

    trigger_hits: list[str] = []
    for trigger in lesson.get("prevention_triggers", []) or []:
        trigger_text = str(trigger or "").strip()
        if not trigger_text:
            continue
        trigger_clean = trigger_text.lower()
        if trigger_clean in raw_clean:
            trigger_hits.append(trigger_text)
    if trigger_hits:
        score = max(score, min(80, 25 + len(trigger_hits) * 15))
        reasons.append("prevention trigger matched: " + ", ".join(trigger_hits[:5]))

    lesson_text = _lesson_search_text(lesson)
    overlap = sorted(raw_tokens.intersection(_tokens(lesson_text)))
    useful_overlap = [token for token in overlap if token not in {"error", "failed", "validation", "status", "lesson"}]
    if len(useful_overlap) >= 4:
        score = max(score, min(55, 20 + len(useful_overlap) * 3))
        reasons.append("lesson vocabulary overlapped: " + ", ".join(useful_overlap[:8]))

    return {
        "lesson_id": str(lesson.get("lesson_id", "")),
        "status": str(lesson.get("status", "")),
        "match_confidence": _match_label(score),
        "score": score,
        "reasons": reasons,
        "avoidance_rule": str(lesson.get("do_not_repeat_rule", "")),
        "compact_lesson": compact_lesson(lesson),
    }


def analyze_error_against_lessons(
    selected_project_root: ErrorMemoryBackend | str | Path,
    raw_error_text: str,
    *,
    operation_phase: str = "unknown",
    include_drafts: bool = True,
    include_deprecated: bool = False,
    max_matches: int = 5,
) -> dict[str, Any]:
    """Return an advisory Repeat Error Guard report for one raw error/context.

    The result is intentionally advisory-only: callers must not treat it as a
    hard gate.  It is meant for GUI review, AI preflight, and safer planning.
    """
    backend = coerce_error_memory_backend(selected_project_root)
    root = backend.owner.source_root.expanduser().resolve(strict=False)
    bootstrap_error_memory_store(backend)
    rebuild_index(backend)

    scrubbed = scrub_text(raw_error_text or "")
    incoming_exception = extract_exception_info(
        scrubbed.text,
        selected_project_root=root,
        operation_phase=operation_phase,
    )
    incoming_fingerprint = build_fingerprint(incoming_exception)

    candidates = [
        lesson
        for lesson in list_lessons(backend, include_inactive=True)
        if _status_allowed(str(lesson.get("status", "")), include_drafts=include_drafts, include_deprecated=include_deprecated)
    ]

    scored = [
        _score_lesson(incoming_exception, incoming_fingerprint, scrubbed.text, lesson)
        for lesson in candidates
    ]
    matches = [item for item in scored if int(item.get("score", 0)) > 0]
    matches.sort(key=lambda item: int(item.get("score", 0)), reverse=True)
    matches = matches[: max(1, int(max_matches or 5))]

    top_score = int(matches[0].get("score", 0)) if matches else 0
    if top_score >= 85:
        disposition = "EXACT_REPEAT_RISK"
        recommendation = "PROCEED_WITH_CAUTION"
    elif top_score >= 50:
        disposition = "POSSIBLE_REPEAT_RISK"
        recommendation = "PROCEED_WITH_CAUTION"
    elif top_score >= 25:
        disposition = "WEAK_CONTEXT_MATCH"
        recommendation = "PROCEED_WITH_CONTEXT_CHECK"
    else:
        disposition = "NO_MATCH"
        recommendation = "PROCEED"

    return {
        "artifact_type": "error_memory_repeat_error_guard_report",
        "schema_version": "1.0",
        "guard_version": GUARD_VERSION,
        "project_root": str(root),
        "owner_scope": backend.owner.owner_scope.value,
        "owner_slug": backend.owner.owner_slug,
        "operation_phase": str(operation_phase or "unknown"),
        "hard_blocking": False,
        "disposition": disposition,
        "recommendation": recommendation,
        "full_error_memory_zip_needed": bool(top_score >= 50),
        "incoming_exception": incoming_exception,
        "incoming_fingerprint": incoming_fingerprint,
        "candidate_count": len(candidates),
        "match_count": len(matches),
        "matches": matches,
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": list(scrubbed.rules),
        },
        "notes": [
            "Advisory only; this report does not hard-block implementation or freeze.",
            "Exact source files and validation evidence must still be inspected before editing or freezing.",
        ],
    }
