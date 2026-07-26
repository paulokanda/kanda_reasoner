# project-path: kanda_reasoner_app/error_memory_gui/_lesson_payloads.py
"""Pure lesson payload helpers for the Error Memory GUI tab."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.intake import build_lesson_from_ai_form, parse_error_lesson_ai_response
from kanda_reasoner_app.error_memory.intake_normalization import (
    _normalize_regression_check_for_error_memory_json,
)
from kanda_reasoner_app.error_memory.models import active_ready, utc_now_iso
from kanda_reasoner_app.error_memory_gui._text_payloads import json_payload_from_text, text_has_formatted_lesson_payload

__all__ = [
    "canonical_draft_lesson_from_partial",
    "lesson_from_formatted_text",
    "text_is_formatted_error_lesson_payload",
]


def lesson_from_formatted_text(text: str, *, selected_project_root: Path) -> dict[str, Any]:
    """Build a lesson from either canonical lesson JSON or AI formulary JSON."""
    payload = json_payload_from_text(text)
    if isinstance(payload, dict) and str(payload.get("lesson_id", "")).strip():
        lesson = dict(payload)
        normalized_regression = _normalize_regression_check_for_error_memory_json(
            lesson.get("regression_check")
        )
        if normalized_regression is not None:
            lesson["regression_check"] = normalized_regression
        return lesson
    form = parse_error_lesson_ai_response(text)
    return build_lesson_from_ai_form(
        selected_project_root=Path(selected_project_root),
        form_inputs=form,
        fallback_raw_error_text="",
        fallback_operation_phase="unknown",
    )


def _list_from_semicolon_or_lines(value: Any) -> list[str]:
    """Return stripped list values from a loose string/list input."""
    if isinstance(value, str):
        return [item.strip() for item in value.replace(";", "\n").splitlines() if item.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def canonical_draft_lesson_from_partial(
    lesson: dict[str, Any],
    *,
    project_slug: str,
    source_text: str = "",
) -> dict[str, Any]:
    """Return a schema-saveable draft lesson without inventing semantics.

    Older AI/draft blocks may contain useful lesson fields but miss store-required
    draft keys such as raw_error_text. Mark Draft must preserve the draft as a
    durable draft, not fail with a missing key. This helper only fills structural
    defaults and copies existing user-provided text such as raw_error_snapshot_scrubbed
    into raw_error_text when needed. It must not promote the lesson to active or
    invent root cause, fixes, validation evidence, or prevention rules.
    """
    payload = dict(lesson or {})
    now = utc_now_iso()
    payload["schema_version"] = str(payload.get("schema_version") or "1.0")
    payload["lesson_id"] = str(payload.get("lesson_id") or "lesson-draft-missing-id").strip()
    payload["status"] = "draft"
    payload["project_slug"] = str(payload.get("project_slug") or project_slug).strip()
    payload["operation_phase"] = str(payload.get("operation_phase") or "unknown").strip()
    payload["created_at_utc"] = str(payload.get("created_at_utc") or now).strip()
    payload["updated_at_utc"] = now

    raw_text = str(payload.get("raw_error_text") or "").strip()
    snapshot_text = str(payload.get("raw_error_snapshot_scrubbed") or "").strip()
    source_snapshot = str(source_text or "").strip()
    if not raw_text:
        raw_text = (
            snapshot_text
            or source_snapshot
            or str(payload.get("symptom") or "").strip()
            or "Draft Error Memory lesson preserved from incomplete editor JSON."
        )
    if not snapshot_text:
        snapshot_text = raw_text
    payload["raw_error_text"] = raw_text
    payload["raw_error_snapshot_scrubbed"] = snapshot_text

    for key in (
        "symptom",
        "root_cause",
        "wrong_assumption",
        "correct_fix",
        "long_term_prevention",
        "do_not_repeat_rule",
    ):
        payload[key] = str(payload.get(key) or "").strip()

    if not isinstance(payload.get("prevention_triggers"), list):
        payload["prevention_triggers"] = _list_from_semicolon_or_lines(payload.get("prevention_triggers"))
    if not isinstance(payload.get("validation_evidence"), list):
        payload["validation_evidence"] = _list_from_semicolon_or_lines(payload.get("validation_evidence"))
    if not isinstance(payload.get("exception"), dict):
        payload["exception"] = {}
    if not isinstance(payload.get("fingerprint"), dict):
        payload["fingerprint"] = {}
    if not isinstance(payload.get("regression_check"), dict):
        payload["regression_check"] = {
            "type": "not_available",
            "command": "",
            "expected_marker": "",
            "required_before_freeze": False,
        }

    redaction = payload.get("redaction") if isinstance(payload.get("redaction"), dict) else {}
    redaction["applied"] = bool(redaction.get("applied", True))
    redaction["export_safe"] = bool(redaction.get("export_safe", True))
    rules = _list_from_semicolon_or_lines(redaction.get("rules"))
    if not rules:
        rules = ["Draft preserved from incomplete Error Memory editor JSON; review redaction before active promotion."]
    redaction["rules"] = rules
    payload["redaction"] = redaction

    if active_ready(dict(payload)):
        payload["promotion_status"] = "active_ready"
    elif not str(payload.get("promotion_status") or "").strip():
        payload["promotion_status"] = "needs_ai_review"
    return payload


def text_is_formatted_error_lesson_payload(text: str, *, selected_project_root: Path) -> bool:
    """Return whether text is a formatted Error Memory lesson, not just any JSON."""
    if not text_has_formatted_lesson_payload(text):
        return False
    try:
        lesson = lesson_from_formatted_text(text, selected_project_root=selected_project_root)
    except Exception:
        return False
    return bool(
        str(lesson.get("symptom", "")).strip()
        and str(lesson.get("do_not_repeat_rule", "")).strip()
    )
