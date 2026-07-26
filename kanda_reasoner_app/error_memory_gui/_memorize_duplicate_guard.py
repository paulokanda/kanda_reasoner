# project-path: kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py
"""Duplicate guard and cleanup for Error Memory correction candidates.

A single saved Lesson is not a duplicate when the user is editing that saved
record directly.  A saved draft/invalid Lesson becomes cleanup-eligible when a
separate pending candidate or another saved Lesson represents the same error.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import difflib
import re
from typing import Any

from kanda_reasoner_app.error_memory.models import active_ready
from kanda_reasoner_app.error_memory.store import delete_lesson, list_lessons, rebuild_index
from kanda_reasoner_app.error_memory_gui._duplicate_match_keys import (
    component_variants,
    same_anchor_semantic_family,
    same_canonical_identifier_family,
)

DUPLICATE_CLEANUP_GUARD_VERSION = "v21_narrow_semantic_duplicate_cleanup"

__all__ = [
    "DUPLICATE_CLEANUP_GUARD_VERSION",
    "DuplicateLessonMatch",
    "find_memorize_duplicate",
    "lesson_matches_candidate_error",
    "matching_stored_lesson_ids",
    "resolve_duplicate_lesson_copies",
]


@dataclass(frozen=True)
class DuplicateLessonMatch:
    """Description of stored duplicate Lessons matching a candidate."""

    lesson_id: str
    status: str
    reason: str
    deleted_lesson_ids: tuple[str, ...] = ()
    preserved_lesson_ids: tuple[str, ...] = ()
    skipped_lesson_ids: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()


def _normalize_text(value: Any) -> str:
    """Return a stable lowercase text fingerprint input."""
    text = str(value or "").lower()
    text = text.replace("\\", "/")
    text = re.sub(r"[^a-z0-9_./:*?-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _fingerprint_hash(lesson: dict[str, Any]) -> str:
    """Return lesson fingerprint hash when present."""
    fingerprint = lesson.get("fingerprint")
    if not isinstance(fingerprint, dict):
        return ""
    return str(fingerprint.get("fingerprint_hash") or "").strip()


def _lesson_id(lesson: dict[str, Any]) -> str:
    """Return a normalized lesson id."""
    return str(lesson.get("lesson_id") or "").strip()


def _fingerprint_components(lesson: dict[str, Any]) -> set[str]:
    """Return stable non-generic fingerprint components and variants."""
    fingerprint = lesson.get("fingerprint")
    if not isinstance(fingerprint, dict):
        return set()
    components = fingerprint.get("components")
    if not isinstance(components, list):
        return set()
    result: set[str] = set()
    generic = {
        "validation",
        "error",
        "lesson",
        "draft",
        "active",
        "patch",
        "__all__",
        "public",
        "private",
        "public_api_instability",
        "duplicate_public_symbol",
        "architecture_validation",
        "architecture",
        "warning",
        "cleanup",
        "attempt",
    }
    for item in components:
        for text in component_variants(item):
            if text in generic:
                continue
            result.add(text)
    return result


def _same_fingerprint_family(candidate: dict[str, Any], stored: dict[str, Any]) -> bool:
    """Return True when fingerprint components strongly overlap."""
    left = _fingerprint_components(candidate)
    right = _fingerprint_components(stored)
    if not left or not right:
        return False
    shared = left & right
    smaller = min(len(left), len(right))
    specific_shared = {
        item for item in shared
        if ("." in item or "/" in item or item.endswith("_impl"))
    }
    if not specific_shared:
        return False
    if len(shared) >= 3 and (len(shared) / max(smaller, 1)) >= 0.45:
        return True
    return len(shared) >= 4


def _similar(left: str, right: str) -> float:
    """Return a conservative similarity score for normalized strings."""
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    return difflib.SequenceMatcher(None, left, right).ratio()


def _strong_same_error(candidate: dict[str, Any], stored: dict[str, Any]) -> str:
    """Return a reason when text fields strongly indicate the same error."""
    candidate_raw = _normalize_text(candidate.get("raw_error_text"))
    stored_raw = _normalize_text(stored.get("raw_error_text"))
    candidate_symptom = _normalize_text(candidate.get("symptom"))
    stored_symptom = _normalize_text(stored.get("symptom"))
    candidate_rule = _normalize_text(candidate.get("do_not_repeat_rule"))
    stored_rule = _normalize_text(stored.get("do_not_repeat_rule"))

    if candidate_raw and stored_raw and candidate_raw == stored_raw:
        phase_left = _normalize_text(candidate.get("operation_phase"))
        phase_right = _normalize_text(stored.get("operation_phase"))
        if not phase_left or not phase_right or phase_left == phase_right:
            return "same raw_error_text and compatible operation_phase"

    raw_score = _similar(candidate_raw, stored_raw)
    symptom_score = _similar(candidate_symptom, stored_symptom)
    rule_score = _similar(candidate_rule, stored_rule)
    if raw_score >= 0.93 and max(symptom_score, rule_score) >= 0.88:
        return "high-similarity raw error and prevention fields"
    return ""


def _stored_match_reason(candidate: dict[str, Any], stored: dict[str, Any]) -> str:
    """Return why one stored lesson matches a candidate, or an empty string."""
    candidate_id = _lesson_id(candidate)
    stored_id = _lesson_id(stored)
    if candidate_id and stored_id == candidate_id:
        return "same lesson_id target"
    if same_canonical_identifier_family(candidate, stored):
        return "same pending/final lesson identifier family"
    candidate_hash = _fingerprint_hash(candidate)
    stored_hash = _fingerprint_hash(stored)
    if candidate_hash and stored_hash and stored_hash == candidate_hash:
        return "same fingerprint.fingerprint_hash"
    if _same_fingerprint_family(candidate, stored):
        return "same fingerprint component family"
    if same_anchor_semantic_family(candidate, stored):
        return "same anchored semantic error family"
    return _strong_same_error(candidate, stored)


def _unique_matches(
    candidate: dict[str, Any],
    stored_lessons: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], str]]:
    """Return unique stored Lessons that match the same candidate error."""
    matches: list[tuple[dict[str, Any], str]] = []
    seen_ids: set[str] = set()
    for stored in stored_lessons:
        if not isinstance(stored, dict):
            continue
        reason = _stored_match_reason(candidate, stored)
        if not reason:
            continue
        stored_id = _lesson_id(stored)
        unique_key = stored_id or str(id(stored))
        if unique_key in seen_ids:
            continue
        seen_ids.add(unique_key)
        matches.append((stored, reason))
    return matches


def _has_true_duplicate_matches(
    matches: list[tuple[dict[str, Any], str]],
    *,
    candidate_has_pending_source: bool = False,
) -> bool:
    """Return True when cleanup is allowed.

    One saved match alone is the target being edited.  One saved match plus a
    separate pending candidate is a visible duplicate in the Lessons table and
    may be cleaned if the saved copy is draft or invalid.
    """
    unique_ids: set[str] = set()
    anonymous_count = 0
    for stored, _reason in matches:
        stored_id = _lesson_id(stored)
        if stored_id:
            unique_ids.add(stored_id)
        else:
            anonymous_count += 1
    stored_count = len(unique_ids) + anonymous_count
    if stored_count >= 2:
        return True
    return candidate_has_pending_source and stored_count >= 1


def _updated_key(lesson: dict[str, Any]) -> tuple[str, str]:
    """Return a deterministic sortable updated/id key."""
    timestamp = str(lesson.get("updated_at_utc") or lesson.get("created_at_utc") or "")
    return (timestamp, _lesson_id(lesson))


def _is_active_ready_lesson(lesson: dict[str, Any]) -> bool:
    """Return whether a stored lesson should be preserved by cleanup."""
    try:
        return active_ready(dict(lesson))
    except Exception:
        return False


def _can_delete_saved_duplicate(lesson: dict[str, Any]) -> bool:
    """Return whether a stored duplicate is safe to delete automatically."""
    status = str(lesson.get("status") or "").strip().lower()
    return status == "draft" or not _is_active_ready_lesson(lesson)


def _choose_preserved_match(
    matches: list[tuple[dict[str, Any], str]],
    *,
    avoid_lesson_id: str = "",
    allow_no_preserved: bool = False,
) -> tuple[dict[str, Any], str] | None:
    """Choose the one stored Lesson to keep as canonical.

    If a pending candidate duplicates only one saved draft/invalid Lesson,
    allow_no_preserved lets cleanup remove that saved draft instead of leaving
    the visible duplicate row behind.
    """
    avoid = str(avoid_lesson_id or "").strip()
    active_matches = [item for item in matches if not _can_delete_saved_duplicate(item[0])]
    if active_matches:
        explicit_active = [
            item for item in active_matches
            if str(item[0].get("status") or "").strip().lower() == "active"
        ]
        candidates = explicit_active or active_matches
        non_avoid = [item for item in candidates if _lesson_id(item[0]) != avoid]
        return sorted(non_avoid or candidates, key=lambda item: _updated_key(item[0]), reverse=True)[0]

    if allow_no_preserved and all(_can_delete_saved_duplicate(item[0]) for item in matches):
        return None

    non_avoid = [item for item in matches if _lesson_id(item[0]) != avoid]
    candidates = non_avoid or matches
    return sorted(candidates, key=lambda item: _updated_key(item[0]), reverse=True)[0]


def _preferred_duplicate_match(
    matches: list[tuple[dict[str, Any], str]],
) -> DuplicateLessonMatch:
    """Choose representative details without deleting anything."""
    preserved = _choose_preserved_match(matches)
    if preserved is None:
        return DuplicateLessonMatch(lesson_id="", status="", reason="stored matching Lessons: " + str(len(matches)))
    preserved_lesson, reason = preserved
    details = reason + "; stored matching Lessons: " + str(len(matches))
    preserved_id = _lesson_id(preserved_lesson)
    return DuplicateLessonMatch(
        lesson_id=preserved_id,
        status=str(preserved_lesson.get("status") or ""),
        reason=details,
        preserved_lesson_ids=(preserved_id,) if preserved_id else (),
    )


def _result_from_cleanup(
    matches: list[tuple[dict[str, Any], str]],
    preserved: tuple[dict[str, Any], str] | None,
    deleted_ids: list[str],
    skipped_ids: list[str],
    failures: list[str],
) -> DuplicateLessonMatch:
    """Build user-facing cleanup result details."""
    if preserved is None:
        preserved_id = ""
        preserved_status = ""
        details = "no saved draft/invalid Lesson preserved; stored matching Lessons: " + str(len(matches))
    else:
        preserved_lesson, preserved_reason = preserved
        preserved_id = _lesson_id(preserved_lesson)
        preserved_status = str(preserved_lesson.get("status") or "")
        details = preserved_reason + "; stored matching Lessons: " + str(len(matches))
    if deleted_ids:
        details += "; deleted saved duplicate Lessons: " + ", ".join(deleted_ids)
    if skipped_ids:
        details += "; preserved active-ready Lessons: " + ", ".join(skipped_ids)
    if failures:
        details += "; cleanup failures: " + ", ".join(failures)
    return DuplicateLessonMatch(
        lesson_id=preserved_id,
        status=preserved_status,
        reason=details,
        deleted_lesson_ids=tuple(sorted(deleted_ids)),
        preserved_lesson_ids=(preserved_id,) if preserved_id else (),
        skipped_lesson_ids=tuple(sorted(skipped_ids)),
        failures=tuple(failures),
    )


def lesson_matches_candidate_error(
    candidate: dict[str, Any],
    other_lesson: dict[str, Any],
) -> bool:
    """Return whether another lesson describes the same candidate error."""
    if not isinstance(candidate, dict) or not isinstance(other_lesson, dict):
        return False
    return bool(_stored_match_reason(candidate, other_lesson))


def matching_stored_lesson_ids(
    selected_project_root: str | Path,
    candidate: dict[str, Any],
) -> tuple[str, ...]:
    """Return unique stored Lesson IDs that match the candidate error."""
    if not isinstance(candidate, dict):
        return ()
    try:
        stored_lessons = list_lessons(selected_project_root, include_inactive=True)
    except Exception:
        return ()
    matches = _unique_matches(candidate, stored_lessons)
    ids: list[str] = []
    for stored, _reason in matches:
        lesson_id = _lesson_id(stored)
        if lesson_id and lesson_id not in ids:
            ids.append(lesson_id)
    return tuple(ids)


def find_memorize_duplicate(
    selected_project_root: str | Path,
    candidate: dict[str, Any],
) -> DuplicateLessonMatch | None:
    """Return a stored duplicate only when duplicate Lessons already exist."""
    if not isinstance(candidate, dict):
        return None
    try:
        stored_lessons = list_lessons(selected_project_root, include_inactive=True)
    except Exception:
        return None
    matches = _unique_matches(candidate, stored_lessons)
    if not _has_true_duplicate_matches(matches):
        return None
    return _preferred_duplicate_match(matches)


def _stored_match_count(matches: list[tuple[dict[str, Any], str]]) -> int:
    """Return unique saved Lesson count represented by matches."""
    unique_ids: set[str] = set()
    anonymous_count = 0
    for stored, _reason in matches:
        stored_id = _lesson_id(stored)
        if stored_id:
            unique_ids.add(stored_id)
        else:
            anonymous_count += 1
    return len(unique_ids) + anonymous_count


def resolve_duplicate_lesson_copies(
    selected_project_root: str | Path,
    candidate: dict[str, Any],
    *,
    candidate_has_pending_source: bool = False,
    delete_candidate_lesson_id: str = "",
) -> DuplicateLessonMatch | None:
    """Delete saved draft/invalid duplicates for the same error family.

    Hard safety rule:
    one saved match without a separate pending/correction candidate is the
    Lesson being corrected and must not be deleted. Cleanup is allowed only
    when a pending/correction candidate makes a visible duplicate pair or when
    two or more saved Lessons match the same error family.
    """
    if not isinstance(candidate, dict):
        return None
    root = Path(selected_project_root)
    try:
        stored_lessons = list_lessons(root, include_inactive=True)
    except Exception:
        return None
    matches = _unique_matches(candidate, stored_lessons)
    stored_count = _stored_match_count(matches)

    if stored_count == 0:
        return None

    # Hard no-op gate: a single saved match without a separate pending or
    # correction candidate is the row being edited, not a duplicate.  Keep this
    # immediately before any preservation/deletion choices so older cleanup
    # heuristics cannot delete the only saved draft.
    if stored_count < 2 and not candidate_has_pending_source:
        return None

    if not _has_true_duplicate_matches(
        matches,
        candidate_has_pending_source=candidate_has_pending_source,
    ):
        return None

    avoid_id = str(delete_candidate_lesson_id or "").strip()
    allow_no_preserved = bool(candidate_has_pending_source)
    preserved = _choose_preserved_match(
        matches,
        avoid_lesson_id=avoid_id,
        allow_no_preserved=allow_no_preserved,
    )
    preserved_id = _lesson_id(preserved[0]) if preserved is not None else ""
    deleted_ids: list[str] = []
    skipped_ids: list[str] = []
    failures: list[str] = []

    for stored, _reason in matches:
        stored_id = _lesson_id(stored)
        if not stored_id:
            continue
        if preserved_id and stored_id == preserved_id:
            continue
        if not _can_delete_saved_duplicate(stored):
            skipped_ids.append(stored_id)
            continue
        try:
            delete_lesson(root, stored_id)
            deleted_ids.append(stored_id)
        except Exception as exc:
            failures.append(stored_id + " -> " + str(exc))

    try:
        rebuild_index(root)
    except Exception as exc:
        failures.append("index rebuild -> " + str(exc))

    return _result_from_cleanup(matches, preserved, deleted_ids, skipped_ids, failures)

