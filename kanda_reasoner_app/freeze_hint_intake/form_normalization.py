# project-path: kanda_reasoner_app/freeze_hint_intake/form_normalization.py
"""Freeze hint normalization, form text, validation marker, and stale-text helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

from .form_text_validation import (
    _append_missing_lines,
    _append_text,
    _clean_stale_pending_text_after_local_validation,
    _field_to_text,
    _has_local_validation_completion_marker,
    _has_recognizable_validation_marker,
    _has_safe_validation_evidence_marker,
    _has_stale_local_validation_pending_text,
    _hint_to_form_inputs,
    _normalize_form_inputs,
    _normalize_line,
    _normalize_validation_evidence_summary,
    _strip_stale_pending_validation_sentences,
    _strip_stale_pending_validation_text,
)
from .models import (
    FORM_KEYS,
    HINT_FIELD_ALIASES,
    LIST_TEXT_KEYS,
    MANDATORY_FORM_FIELDS,
    SCHEMA_VERSION,
    STARTER_PLACEHOLDER_PATTERNS,
    FreezeHintIntakeError,
)
from .paths_io import _coerce_mapping, _safe_slug, _source_signature

def _normalize_hint(raw_hint: Mapping[str, Any], source: Any) -> dict[str, Any]:
    """Support normalize hint behavior.
    
    Parameters
    ----------
    raw_hint : Mapping[str, Any]
        The raw hint value.
    source : Any
        The source value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    hint = dict(raw_hint)
    if hint.get("kind") and str(hint.get("kind")) != "kanda_freeze_hint":
        raise FreezeHintIntakeError("KANDA_FREEZE_HINT.json kind must be kanda_freeze_hint.")

    hint.setdefault("schema_version", SCHEMA_VERSION)
    hint.setdefault("kind", "kanda_freeze_hint")
    _apply_hint_metadata_aliases(hint)

    for key in FORM_KEYS:
        hint[key] = _field_to_text(hint.get(key, ""), list_text=key in LIST_TEXT_KEYS)

    if not str(hint.get("feature_title", "")).strip():
        raise FreezeHintIntakeError("KANDA_FREEZE_HINT.json missing feature_title.")
    if not str(hint.get("validation_evidence_summary", "")).strip():
        raise FreezeHintIntakeError("KANDA_FREEZE_HINT.json missing validation_evidence_summary.")

    hint["feature_id"] = _safe_slug(str(hint.get("feature_id") or hint.get("feature_title") or "freeze-hint"))
    if isinstance(source, Mapping):
        hint["source"] = _coerce_mapping(source)
    elif source is not None:
        source_path = Path(source)
        if source_path.exists():
            hint["source"] = _source_signature(source_path)
        else:
            hint["source"] = {"source_path": str(source_path)}
    else:
        hint["source"] = _coerce_mapping(hint.get("source"))

    return hint

def _patch_boundary_allowed_paths(hint: Mapping[str, Any]) -> list[str]:
    """Support patch boundary allowed paths behavior.
    
    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    boundary = hint.get("patch_boundary")
    if not isinstance(boundary, Mapping):
        return []
    for key in ("allowed_paths", "validated_files", "updated_files", "changed_files", "touched_files"):
        value = boundary.get(key)
        paths = _coerce_path_text_list(value)
        if paths:
            return paths
    return []

def _patch_boundary_generated_paths(hint: Mapping[str, Any]) -> list[str]:
    """Support patch boundary generated paths behavior.
    
    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    boundary = hint.get("patch_boundary")
    if not isinstance(boundary, Mapping):
        return []
    for key in ("generated_files", "generated_paths", "created_files"):
        paths = _coerce_path_text_list(boundary.get(key))
        if paths:
            return paths
    return []

def _coerce_path_text_list(value: Any) -> list[str]:
    """Support coerce path text list behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if value is None:
        return []
    if isinstance(value, str):
        raw_items = value.replace(";", "\n").splitlines()
    elif isinstance(value, Iterable) and not isinstance(value, (str, bytes, Mapping)):
        raw_items = list(value)
    else:
        raw_items = [value]
    result: list[str] = []
    for raw in raw_items:
        text = str(raw).strip().strip('"').strip("'").replace("\\", "/")
        if text and text not in result:
            result.append(text)
    return result

def _do_not_regress_from_architecture_characteristics(hint: Mapping[str, Any]) -> list[str]:
    """Support do not regress from architecture characteristics behavior.
    
    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    value = hint.get("protected_architecture_characteristics")
    items: list[str] = []
    for item in _coerce_path_text_list(value):
        readable = item.replace("_", " ").strip()
        if readable:
            items.append("Preserve " + readable + ".")
    return items

def _is_starter_placeholder(value: Any) -> bool:
    """Support is starter placeholder behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    text = str(value or "").strip().lower()
    if not text:
        return False
    return any(pattern in text for pattern in STARTER_PLACEHOLDER_PATTERNS)

def _value_or_empty_if_placeholder(value: Any) -> str:
    """Support value or empty if placeholder behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = str(value or "").strip()
    return "" if _is_starter_placeholder(text) else text

def _field_value_or_empty_if_placeholder(field_name: str, value: Any) -> str:
    """Support field value or empty if placeholder behavior.
    
    Parameters
    ----------
    field_name : str
        The field name value.
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = str(value or "").strip()
    if field_name == "validation_evidence_summary":
        return text
    return "" if _is_starter_placeholder(text) else text

def _merge_lines(existing: Any, additions: Iterable[str]) -> str:
    """Support merge lines behavior.
    
    Parameters
    ----------
    existing : Any
        The existing value.
    additions : Iterable[str]
        The additions value.
    
    Returns
    -------
    str
        The string result.
    """
    
    lines = _coerce_path_text_list(existing)
    for item in additions:
        text = str(item).strip()
        if text and text not in lines:
            lines.append(text)
    return "\n".join(lines)

def _repair_hint_form_inputs_from_raw_hint(record: Mapping[str, Any]) -> dict[str, str]:
    """Support repair hint form inputs from raw hint behavior.
    
    Parameters
    ----------
    record : Mapping[str, Any]
        The record value.
    
    Returns
    -------
    dict[str, str]
        The mapped values.
    """
    
    hint = record.get("hint")
    if not isinstance(hint, Mapping):
        return {}
    try:
        normalized_hint = _normalize_hint(dict(hint), record.get("source"))
        return _hint_to_form_inputs(normalized_hint)
    except Exception:
        return {}

def _form_has_mandatory_freeze_fields(form_inputs: Mapping[str, Any]) -> bool:
    """Support form has mandatory freeze fields behavior.
    
    Parameters
    ----------
    form_inputs : Mapping[str, Any]
        The form inputs value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for key in MANDATORY_FORM_FIELDS:
        value = str(form_inputs.get(key) or "").strip()
        if not value:
            return False
        if key != "validation_evidence_summary" and _is_starter_placeholder(value):
            return False
    return True

def _apply_hint_metadata_aliases(hint: dict[str, Any]) -> None:
    """Promote sidecar metadata into freeze-form fields.

    Older sidecars used flat fields such as box_paths or validation_tests.
    Newer governed patch sidecars may use structured delivery metadata such as
    patch_boundary.allowed_paths, owning_box, feature_type, summary, and
    protected_architecture_characteristics. The freeze form must understand both
    shapes so users do not have to repair mandatory fields manually.
    """

    allowed_paths = _patch_boundary_allowed_paths(hint)
    generated_paths = _patch_boundary_generated_paths(hint)

    if allowed_paths and not _has_non_empty_value(hint.get("validated_files")):
        hint["validated_files"] = allowed_paths
    if allowed_paths and not _has_non_empty_value(hint.get("protected_paths")):
        hint["protected_paths"] = allowed_paths
    if generated_paths and not _has_non_empty_value(hint.get("generated_files")):
        hint["generated_files"] = generated_paths

    architecture_rules = _do_not_regress_from_architecture_characteristics(hint)
    if architecture_rules:
        hint["do_not_regress_rules"] = _merge_lines(
            hint.get("do_not_regress_rules") or hint.get("do_not_regress") or "",
            architecture_rules,
        )

    for target_key, aliases in HINT_FIELD_ALIASES.items():
        if _has_non_empty_value(hint.get(target_key)):
            continue
        for alias in aliases:
            if alias == target_key:
                continue
            value = hint.get(alias)
            if _has_non_empty_value(value):
                hint[target_key] = value
                break

    if not _has_non_empty_value(hint.get("validated_files")):
        validation_tests = hint.get("validation_tests")
        if _has_non_empty_value(validation_tests):
            hint["validated_files"] = validation_tests

    if not _has_non_empty_value(hint.get("primary_box")):
        inferred_box = _infer_primary_box_from_hint_paths(hint)
        if inferred_box:
            hint["primary_box"] = inferred_box

    if not _has_non_empty_value(hint.get("box_type")):
        inferred_type = _infer_box_type_from_hint_paths(hint)
        if inferred_type:
            hint["box_type"] = inferred_type

    box_type = str(hint.get("box_type") or "").strip()
    if box_type and "_" in box_type and box_type == str(hint.get("feature_type") or "").strip():
        hint["box_type"] = box_type.replace("_", " ")

    if not _has_non_empty_value(hint.get("planned_next_step")):
        expected_title = str(hint.get("expected_freeze_title") or hint.get("feature_title") or "").strip()
        if expected_title:
            hint["planned_next_step"] = "Preview Freeze Entry, then Confirm and Write after human review for " + expected_title + "."

def _has_non_empty_value(value: Any) -> bool:
    """Support has non empty value behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping):
        return bool(value)
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return any(str(item).strip() for item in value)
    return bool(str(value).strip())

def _hint_path_list(hint: Mapping[str, Any]) -> list[str]:
    """Support hint path list behavior.
    
    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    paths: list[str] = []
    paths.extend(_patch_boundary_allowed_paths(hint))
    paths.extend(_patch_boundary_generated_paths(hint))
    for key in ("box_paths", "validated_files", "validation_tests", "protected_paths"):
        value = hint.get(key)
        if isinstance(value, str):
            paths.extend(line.strip() for line in value.splitlines() if line.strip())
        elif isinstance(value, Iterable) and not isinstance(value, (str, bytes, Mapping)):
            paths.extend(str(item).strip() for item in value if str(item).strip())
    result: list[str] = []
    for path in paths:
        normalized = str(path).replace("\\", "/").strip()
        if normalized and normalized not in result:
            result.append(normalized)
    return result

def _infer_primary_box_from_hint_paths(hint: Mapping[str, Any]) -> str:
    """Support infer primary box from hint paths behavior.
    
    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.
    
    Returns
    -------
    str
        The string result.
    """
    
    boxes: list[str] = []
    for path_text in _hint_path_list(hint):
        normalized = path_text.replace("\\", "/").strip("/")
        parts = [part for part in normalized.split("/") if part]
        if not parts:
            continue
        if parts[0] == "tests":
            box = "tests"
        elif len(parts) >= 2 and parts[0] == "kanda_reasoner_app":
            box = "/".join(parts[:2])
        elif len(parts) >= 2 and parts[0] == "kanda_prompt_workspace":
            box = "/".join(parts[:2])
        else:
            box = parts[0]
        if box not in boxes:
            boxes.append(box)
    return " + ".join(boxes)

def _infer_box_type_from_hint_paths(hint: Mapping[str, Any]) -> str:
    """Support infer box type from hint paths behavior.
    
    Parameters
    ----------
    hint : Mapping[str, Any]
        The hint value.
    
    Returns
    -------
    str
        The string result.
    """
    
    paths = _hint_path_list(hint)
    if not paths:
        return ""
    normalized = [item.replace("\\", "/").strip("/") for item in paths]
    if normalized and all(item.startswith("tests/") for item in normalized):
        return "tests-only validation shielding"
    if any(item.startswith("tests/") for item in normalized):
        return "source and tests update"
    return "project source update"
