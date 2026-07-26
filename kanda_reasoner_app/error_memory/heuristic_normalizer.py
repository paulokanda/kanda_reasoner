# project-path: kanda_reasoner_app/error_memory/heuristic_normalizer.py
"""Deterministic Level-1 Error Memory lesson normalizer.

This module intentionally performs only mechanical cleanup for the Error Memory
GUI heuristic-correction button.  It must never invent root cause, correct fix,
prevention rules, or validation evidence.  Anything needing interpretation stays
locked in the GUI and requires AI-assisted correction.
"""

from __future__ import annotations


__all__ = ['classify_and_normalize_error_lesson_text', 'HeuristicCorrectionResult']
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import uuid
from typing import Any, Callable

from .models import active_ready_missing_reasons

ERROR_LESSON_JSON_BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
ERROR_LESSON_JSON_END = "KANDA_ERROR_LESSON_JSON_END"


def utc_now_iso() -> str:
    """Return current UTC timestamp in stable ISO format without package imports."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_lesson_id() -> str:
    """Return a stable lesson identifier without importing the full Error Memory package."""
    return "lesson-" + uuid.uuid4().hex[:12]


_SAFE_STATUSES = {"draft", "active", "deprecated", "superseded"}
_SEMANTIC_REQUIRED_TEXT_FIELDS = (
    "symptom",
    "root_cause",
    "correct_fix",
    "do_not_repeat_rule",
)
_STRUCTURAL_REQUIRED_FIELDS = (
    "exception",
    "fingerprint",
    "redaction",
)


@dataclass(frozen=True)
class HeuristicCorrectionResult:
    """Result of classifying one Error Editor payload."""

    level: int
    can_apply: bool
    label: str
    reason: str
    lesson: dict[str, Any] | None = None


def _strip_receive_ready_wrapper(text: str) -> str:
    """Return inner JSON when a receive-ready block is present."""
    stripped = str(text or "").strip()
    if ERROR_LESSON_JSON_BEGIN in stripped and ERROR_LESSON_JSON_END in stripped:
        after_begin = stripped.split(ERROR_LESSON_JSON_BEGIN, 1)[1]
        return after_begin.split(ERROR_LESSON_JSON_END, 1)[0].strip()
    return stripped


def _parse_json_object(text: str) -> dict[str, Any] | None:
    """Parse one JSON object from text or a receive-ready block."""
    candidate = _strip_receive_ready_wrapper(text)
    if not candidate:
        return None
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return dict(payload) if isinstance(payload, dict) else None


def _as_list(value: Any) -> list[str]:
    """Return a safe list of non-empty strings without semantic rewriting."""
    if value is None:
        return []
    if isinstance(value, str):
        pieces = value.replace(";", "\n").splitlines()
    elif isinstance(value, (list, tuple, set)):
        pieces = list(value)
    else:
        pieces = [value]
    return [str(item).strip() for item in pieces if str(item).strip()]


def _has_text(value: Any) -> bool:
    """Support has text behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return bool(str(value or "").strip())


def _semantic_score(payload: dict[str, Any]) -> int:
    """Count already-present semantic fields; used only to choose nested payload."""
    score = 0
    for key in _SEMANTIC_REQUIRED_TEXT_FIELDS:
        if _has_text(payload.get(key)):
            score += 1
    if _as_list(payload.get("prevention_triggers")):
        score += 1
    return score


def _best_payload_from_editor_text(text: str) -> dict[str, Any] | None:
    """Return the best deterministic JSON object from the Error Editor text.

    The old AI form sometimes left a draft wrapper whose raw_error_text field
    contained the real lesson JSON.  If that inner JSON has more meaningful
    lesson fields than the wrapper, use it.  This is a mechanical unwrap only.
    """
    outer = _parse_json_object(text)
    if outer is None:
        return None
    inner = None
    raw_error_text = outer.get("raw_error_text")
    if isinstance(raw_error_text, str) and raw_error_text.strip():
        inner = _parse_json_object(raw_error_text)
    if isinstance(inner, dict) and _semantic_score(inner) > _semantic_score(outer):
        return inner
    return outer


def _has_required_semantics(payload: dict[str, Any]) -> bool:
    """Support has required semantics behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if any(not _has_text(payload.get(key)) for key in _SEMANTIC_REQUIRED_TEXT_FIELDS):
        return False
    return bool(_as_list(payload.get("prevention_triggers")))


def _has_required_structural_fields(payload: dict[str, Any]) -> bool:
    """Support has required structural fields behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for key in _STRUCTURAL_REQUIRED_FIELDS:
        if not isinstance(payload.get(key), dict):
            return False
    redaction = payload.get("redaction")
    return bool(redaction.get("applied") and redaction.get("export_safe"))


def _normalize_safe_structure(
    payload: dict[str, Any],
    *,
    project_slug: str,
    now_factory: Callable[[], str] = utc_now_iso,
    id_factory: Callable[[], str] = new_lesson_id,
) -> dict[str, Any]:
    """Apply Level-1 structural normalization only."""
    lesson = dict(payload)
    now = now_factory()
    if str(lesson.get("schema_version") or "").strip() != "1.0":
        lesson["schema_version"] = "1.0"
    if not str(lesson.get("project_slug") or "").strip():
        lesson["project_slug"] = str(project_slug or "").strip() or "unknown_project"
    if not str(lesson.get("lesson_id") or "").strip():
        lesson["lesson_id"] = id_factory()
    status = str(lesson.get("status") or "").strip().lower()
    if status not in _SAFE_STATUSES:
        lesson["status"] = "draft"
    else:
        lesson["status"] = status
    if not str(lesson.get("created_at_utc") or "").strip():
        lesson["created_at_utc"] = now
    lesson["updated_at_utc"] = now
    lesson["prevention_triggers"] = _as_list(lesson.get("prevention_triggers"))
    if "validation_evidence" in lesson:
        lesson["validation_evidence"] = _as_list(lesson.get("validation_evidence"))
    else:
        lesson["validation_evidence"] = []
    if not isinstance(lesson.get("regression_check"), dict):
        lesson["regression_check"] = {
            "type": "not_available",
            "command": "",
            "expected_marker": "",
            "required_before_freeze": False,
        }
    raw_text = str(lesson.get("raw_error_text") or "").strip()
    snapshot_text = str(lesson.get("raw_error_snapshot_scrubbed") or "").strip()
    if not raw_text and snapshot_text:
        lesson["raw_error_text"] = snapshot_text
    if not snapshot_text and raw_text:
        lesson["raw_error_snapshot_scrubbed"] = raw_text
    redaction = lesson.get("redaction") if isinstance(lesson.get("redaction"), dict) else {}
    rules = redaction.get("rules")
    if isinstance(rules, str):
        rules = [item.strip() for item in rules.replace(";", "\n").splitlines() if item.strip()]
    elif isinstance(rules, (list, tuple, set)):
        rules = [str(item).strip() for item in rules if str(item).strip()]
    else:
        rules = []
    if not rules and redaction.get("applied") and redaction.get("export_safe"):
        rules = ["Draft preserved from incomplete Error Memory editor JSON; review redaction before active promotion."]
    if rules:
        redaction["rules"] = rules
        lesson["redaction"] = redaction
    return lesson


def classify_and_normalize_error_lesson_text(
    text: str,
    *,
    project_slug: str,
    now_factory: Callable[[], str] = utc_now_iso,
    id_factory: Callable[[], str] = new_lesson_id,
) -> HeuristicCorrectionResult:
    """Classify one Error Editor payload and return a Level-1 normalization.

    Level 1: parseable lesson with complete semantics and required structural
    objects; only safe metadata/wrapper/list normalization is applied.
    Level 2: parseable lesson, but structural requirements need review.
    Level 3: invalid or semantically incomplete; AI/user reasoning is needed.
    """
    payload = _best_payload_from_editor_text(text)
    if payload is None:
        return HeuristicCorrectionResult(
            level=3,
            can_apply=False,
            label="Need AI to Correct",
            reason="Error Editor text is not one parseable lesson JSON object or receive-ready block.",
        )
    if not _has_required_semantics(payload):
        return HeuristicCorrectionResult(
            level=3,
            can_apply=False,
            label="Need AI to Correct",
            reason="The lesson is missing symptom, root cause, correction, do-not-repeat rule, or prevention triggers.",
            lesson=dict(payload),
        )
    normalized = _normalize_safe_structure(
        payload,
        project_slug=project_slug,
        now_factory=now_factory,
        id_factory=id_factory,
    )
    if not _has_required_structural_fields(normalized):
        normalized["promotion_status"] = "needs_ai_review"
        return HeuristicCorrectionResult(
            level=2,
            can_apply=False,
            label="Need AI to Correct",
            reason="The lesson is parseable, but required structural fields such as exception, fingerprint, or redaction are missing or unsafe.",
            lesson=normalized,
        )
    active_missing = active_ready_missing_reasons(dict(normalized))
    if active_missing:
        normalized["promotion_status"] = "needs_ai_review"
        shown = active_missing[:20]
        missing_text = "\n- ".join(shown)
        if len(active_missing) > 20:
            missing_text += "\n- ... " + str(len(active_missing) - 20) + " more item(s)"
        return HeuristicCorrectionResult(
            level=2,
            can_apply=False,
            label="Need AI to Correct",
            reason=(
                "Deterministic normalization would only produce a draft. "
                "Heuristic Correction is restricted to active-ready results and cannot invent validation evidence.\n\n"
                "Missing active-ready items:\n- " + missing_text
            ),
            lesson=normalized,
        )
    normalized["promotion_status"] = "active_ready"
    normalized["status"] = "active"
    return HeuristicCorrectionResult(
        level=1,
        can_apply=True,
        label="Heuristic Correction",
        reason="Level 1 only: safe wrapper/schema/project/timestamp/list normalization produced an active-ready lesson. No root cause, fix, rule, or evidence is invented.",
        lesson=normalized,
    )
