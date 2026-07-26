# project-path: kanda_reasoner_app/error_memory_gui/_duplicate_match_keys.py
"""Conservative duplicate-family matching helpers for Error Memory."""
from __future__ import annotations

import re
from typing import Any

__all__ = [
    "component_variants",
    "same_anchor_semantic_family",
    "same_canonical_identifier_family",
]

_COMMON_ANCHOR_TAILS = {
    "kanda_freeze_hint.json",
    "validate_patch_zip.py",
    "manage_architecture.py",
    "validate_ai_response_patch_delivery.py",
    "pre_output_contract_gates.md",
    "tell_ai_read_before_all.md",
}

_COMMON_ANCHOR_WORDS = {
    "error", "memory", "lesson", "draft", "active", "validation",
    "validator", "validate", "patch", "freeze", "public", "private",
    "helper", "helpers", "module", "modules", "python", "script",
    "scripts", "tools", "status", "success", "failed", "failure",
    "kanda_reasoner", "kanda_reasoner_app", "delete_after_daily_work",
    "project_error_memory", "pending_ai_assisted_error_lesson_intake",
    "duplicate_public_symbol", "public_api_instability",
}


def _normalize_text(value: Any) -> str:
    text = str(value or "").lower().replace("\\", "/")
    text = re.sub(r"[^a-z0-9_./:*?-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _flatten(value: Any) -> list[Any]:
    if isinstance(value, dict):
        result: list[Any] = []
        for item in value.values():
            result.extend(_flatten(item))
        return result
    if isinstance(value, (list, tuple, set)):
        result: list[Any] = []
        for item in value:
            result.extend(_flatten(item))
        return result
    return [value]


def component_variants(value: Any) -> set[str]:
    """Return comparable component variants from strings or dict payloads."""
    variants: set[str] = set()
    for item in _flatten(value):
        text = _normalize_text(item)
        if not text:
            continue
        variants.add(text)
        tail = text.rsplit("/", 1)[-1]
        if tail:
            variants.add(tail)
    expanded = set(variants)
    for item in variants:
        if item.endswith(".py"):
            expanded.add(item[:-3])
        if item.endswith(".json"):
            expanded.add(item[:-5])
        if item.endswith(".md"):
            expanded.add(item[:-3])
        if "*" in item:
            expanded.add(item.replace("*", ""))
    return {item for item in expanded if len(item) >= 8}


def _lesson_id(lesson: dict[str, Any]) -> str:
    return str(lesson.get("lesson_id") or "").strip()


def _fingerprint_hash(lesson: dict[str, Any]) -> str:
    fingerprint = lesson.get("fingerprint")
    if not isinstance(fingerprint, dict):
        return ""
    return str(fingerprint.get("fingerprint_hash") or "").strip()


def _canonical_slug(value: Any) -> str:
    text = _normalize_text(value).rsplit("/", 1)[-1]
    if not text or re.fullmatch(r"[0-9a-f]{24,}", text):
        return ""
    for suffix in (".json", ".py", ".md"):
        if text.endswith(suffix):
            text = text[: -len(suffix)]
    for prefix in ("lesson-", "kanda_error_lesson_json_", "kanda-error-lesson-json-"):
        if text.startswith(prefix):
            text = text[len(prefix):]
    if text.startswith("pending-"):
        text = text[len("pending-"):]
    return text.strip("-_ ")


def _identifier_slugs(lesson: dict[str, Any]) -> set[str]:
    return {
        slug for slug in (
            _canonical_slug(_lesson_id(lesson)),
            _canonical_slug(_fingerprint_hash(lesson)),
        ) if len(slug) >= 12
    }


def same_canonical_identifier_family(
    candidate: dict[str, Any],
    stored: dict[str, Any],
) -> bool:
    """Return True for pending/final lesson ids of the same error."""
    left = _identifier_slugs(candidate)
    right = _identifier_slugs(stored)
    return bool(left and right and (left & right))


def _text_tokens(value: Any) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9_./:-]{4,}", _normalize_text(value)))
    generic = {
        "validation", "error", "failed", "failure", "because",
        "lesson", "draft", "status", "correct", "correction", "memory",
    }
    return {item for item in tokens if item not in generic}


def _semantic_tokens(lesson: dict[str, Any]) -> set[str]:
    keys = (
        "raw_error_text", "raw_error_snapshot_scrubbed", "symptom",
        "root_cause", "correct_fix", "do_not_repeat_rule",
        "validation_command_summary",
    )
    result: set[str] = set()
    for key in keys:
        result.update(_text_tokens(lesson.get(key)))
    exception = lesson.get("exception")
    if isinstance(exception, dict):
        for key in ("relative_file_path", "function_or_test_name", "message_normalized"):
            result.update(_text_tokens(exception.get(key)))
    return result


def _clean_anchor_tail(value: str) -> str:
    tail = value.rsplit("/", 1)[-1].strip("-_:*? ")
    if tail.endswith(('.py', '.json', '.md', '.txt')):
        tail = tail.rsplit('.', 1)[0]
    return tail


def _is_specific_anchor(value: str) -> bool:
    text = _normalize_text(value)
    if not text:
        return False
    tail = text.rsplit("/", 1)[-1]
    if tail in _COMMON_ANCHOR_TAILS:
        return False
    cleaned_tail = _clean_anchor_tail(text)
    if not cleaned_tail or cleaned_tail in _COMMON_ANCHOR_WORDS:
        return False
    if len(cleaned_tail) < 10:
        return False
    if "." not in text and "/" not in text:
        return False
    if re.fullmatch(r"v\d+", cleaned_tail):
        return False
    return True


def _specific_anchors(tokens: set[str]) -> set[str]:
    anchors: set[str] = set()
    for token in tokens:
        if not _is_specific_anchor(token):
            continue
        anchors.add(token)
        tail = token.rsplit("/", 1)[-1]
        if tail and tail not in _COMMON_ANCHOR_TAILS:
            anchors.add(tail)
        if tail.endswith(('.py', '.json', '.md', '.txt')):
            anchors.add(tail.rsplit('.', 1)[0])
    return {item for item in anchors if _is_specific_anchor(item)}


def same_anchor_semantic_family(
    candidate: dict[str, Any],
    stored: dict[str, Any],
) -> bool:
    """Return True only for rare exact anchor overlap plus strong text overlap.

    This is intentionally a fallback.  It must not group broad public-surface,
    validation, or architecture lessons just because they share generic words or
    common project paths.  Exact ids, fingerprint hashes, and exact raw text are
    handled elsewhere before this helper is used.
    """
    left = _semantic_tokens(candidate)
    right = _semantic_tokens(stored)
    if not left or not right:
        return False
    anchors = _specific_anchors(left) & _specific_anchors(right)
    if not anchors:
        return False
    shared = left & right
    smaller = min(len(left), len(right))
    if len(shared) < 7:
        return False
    return (len(shared) / max(smaller, 1)) >= 0.45
