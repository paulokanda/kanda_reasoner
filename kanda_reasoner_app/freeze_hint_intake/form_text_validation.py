# project-path: kanda_reasoner_app/freeze_hint_intake/form_text_validation.py
"""Form text conversion and validation-marker helpers for freeze hints."""

from __future__ import annotations

import json
import re
from typing import Any, Iterable, Mapping

from .models import (
    FORM_KEYS,
    LIST_TEXT_KEYS,
    MANDATORY_PROTECTED_PATHS,
    MANDATORY_RULES,
    STALE_LOCAL_VALIDATION_PENDING_PATTERNS,
)

__all__ = []


def _hint_to_form_inputs(hint: Mapping[str, Any]) -> dict[str, str]:
    """Support hint to form inputs behavior.

    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.

    Returns
    -------
    dict[str, str]
        The mapped values.
    """

    inputs = {key: str(hint.get(key, "")).strip() for key in FORM_KEYS}
    inputs["validation_evidence_summary"] = _normalize_validation_evidence_summary(
        inputs.get("validation_evidence_summary", "")
    )
    inputs["protected_paths"] = _append_missing_lines(
        inputs.get("protected_paths", ""),
        MANDATORY_PROTECTED_PATHS,
    )
    inputs["do_not_regress_rules"] = _append_missing_lines(
        inputs.get("do_not_regress_rules", ""),
        MANDATORY_RULES,
    )
    return _clean_stale_pending_text_after_local_validation(inputs)


def _normalize_form_inputs(inputs: Mapping[str, Any]) -> dict[str, str]:
    """Support normalize form inputs behavior.

    Parameters
    ----------
    inputs : Mapping[str, Any]
        The inputs value.

    Returns
    -------
    dict[str, str]
        The mapped values.
    """

    normalized: dict[str, str] = {}
    for key in FORM_KEYS:
        normalized[key] = _field_to_text(inputs.get(key, ""), list_text=key in LIST_TEXT_KEYS)
    return normalized


def _field_to_text(value: Any, *, list_text: bool = False) -> str:
    """Support field to text behavior.

    Parameters
    ----------
    value : Any
        The input value.
    list_text : bool, optional
        The optional list text value.

    Returns
    -------
    str
        The string result.
    """

    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if list_text and isinstance(value, Iterable) and not isinstance(value, (str, bytes, Mapping)):
        return "\n".join(str(item).strip() for item in value if str(item).strip())
    if isinstance(value, Mapping):
        return json.dumps(value, ensure_ascii=True, sort_keys=True)
    return str(value).strip()


def _append_missing_lines(value: Any, required_lines: Iterable[str]) -> str:
    """Support append missing lines behavior.

    Parameters
    ----------
    value : Any
        The input value.
    required_lines : Iterable[str]
        The required lines value.

    Returns
    -------
    str
        The string result.
    """

    lines = [line.strip() for line in str(value or "").splitlines() if line.strip()]
    seen = {_normalize_line(line) for line in lines}
    for line in required_lines:
        norm = _normalize_line(line)
        if norm not in seen:
            lines.append(line)
            seen.add(norm)
    return "\n".join(lines)


def _append_text(value: Any, addition: str) -> str:
    """Support append text behavior.

    Parameters
    ----------
    value : Any
        The input value.
    addition : str
        The addition value.

    Returns
    -------
    str
        The string result.
    """

    base = str(value or "").strip()
    extra = str(addition or "").strip()
    if not extra:
        return base
    if not base:
        return extra
    if extra.lower() in base.lower():
        return base
    return base + " " + extra


def _normalize_validation_evidence_summary(value: Any) -> str:
    """Support normalize validation evidence summary behavior.

    Parameters
    ----------
    value : Any
        The input value.

    Returns
    -------
    str
        The string result.
    """

    text = _field_to_text(value)
    lines = [line.rstrip() for line in text.splitlines()]
    normalized = []
    for line in lines:
        stripped = line.strip()
        if stripped == "STARTUP PROMPT REQUEST KERNEL CHECK: STATUS IN_SYNC":
            normalized.append("STARTUP PROMPT REQUEST KERNEL CHECK")
            normalized.append("STATUS: IN_SYNC")
            continue
        if stripped == "STATUS IN_SYNC":
            normalized.append("STATUS: IN_SYNC")
            continue
        normalized.append(line)
    return "\n".join(normalized).strip()


def _has_recognizable_validation_marker(value: Any) -> bool:
    """Support has recognizable validation marker behavior.

    Parameters
    ----------
    value : Any
        The input value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    folded = str(value or "").casefold()
    markers = (
        "validation ok",
        "install ok",
        "py_compile passed",
        "validator passed",
        "status: in_sync",
        "installed / validated / closed",
        "installed/validated/closed",
        "validation confirmed",
    )
    if any(marker in folded for marker in markers):
        return True
    return "installed" in folded and "validated" in folded and "closed" in folded


def _has_stale_local_validation_pending_text(value: Any) -> bool:
    """Support has stale local validation pending text behavior.

    Parameters
    ----------
    value : Any
        The input value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    folded = str(value or "").casefold()
    return any(pattern in folded for pattern in STALE_LOCAL_VALIDATION_PENDING_PATTERNS)


def _has_local_validation_completion_marker(value: Any) -> bool:
    """Support has local validation completion marker behavior.

    Parameters
    ----------
    value : Any
        The input value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    for raw_line in str(value or "").splitlines():
        line = raw_line.strip()
        folded = line.casefold()
        if not line:
            continue
        if folded.startswith("sandbox validation ok"):
            continue
        if folded.startswith("validation ok:"):
            return True
        if folded.startswith("local validation passed"):
            return True
        if folded.startswith("freeze hint merge ok"):
            return True
    return False


def _has_safe_validation_evidence_marker(value: Any) -> bool:
    """Support has safe validation evidence marker behavior.

    Parameters
    ----------
    value : Any
        The input value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    text = str(value or "")
    if _has_stale_local_validation_pending_text(text) and not _has_local_validation_completion_marker(text):
        return False
    return _has_recognizable_validation_marker(text)


def _clean_stale_pending_text_after_local_validation(inputs: Mapping[str, Any]) -> dict[str, str]:
    """Support clean stale pending text after local validation behavior.

    Parameters
    ----------
    inputs : Mapping[str, Any]
        The inputs value.

    Returns
    -------
    dict[str, str]
        The mapped values.
    """

    cleaned = _normalize_form_inputs(dict(inputs))
    evidence = cleaned.get("validation_evidence_summary", "")
    if not _has_local_validation_completion_marker(evidence):
        return cleaned
    for key in ("validation_evidence_summary", "known_warnings", "planned_next_step", "notes"):
        cleaned[key] = _strip_stale_pending_validation_text(cleaned.get(key, ""))
    return cleaned


def _strip_stale_pending_validation_text(value: Any) -> str:
    """Support strip stale pending validation text behavior.

    Parameters
    ----------
    value : Any
        The input value.

    Returns
    -------
    str
        The string result.
    """

    text = str(value or "")
    if not text.strip():
        return ""
    kept_lines: list[str] = []
    for raw_line in text.splitlines():
        cleaned_line = _strip_stale_pending_validation_sentences(raw_line)
        if cleaned_line.strip():
            kept_lines.append(cleaned_line.strip())
    return "\n".join(kept_lines).strip()


def _strip_stale_pending_validation_sentences(line: str) -> str:
    """Support strip stale pending validation sentences behavior.

    Parameters
    ----------
    line : str
        The line value.

    Returns
    -------
    str
        The string result.
    """

    text = str(line or "").strip()
    if not text:
        return ""
    if not _has_stale_local_validation_pending_text(text):
        return text
    parts = re.split(r"(?<=[.!?])\s+", text)
    kept = [
        part.strip()
        for part in parts
        if part.strip() and not _has_stale_local_validation_pending_text(part)
    ]
    return " ".join(kept).strip()


def _normalize_line(value: str) -> str:
    """Support normalize line behavior.

    Parameters
    ----------
    value : str
        The input value.

    Returns
    -------
    str
        The string result.
    """

    return " ".join(str(value or "").lower().split())
