"""Freeze form autofill arbitration for the latest freeze hint intake state."""

from __future__ import annotations

from .form_text_validation import (
    _append_missing_lines,
    _append_text,
    _clean_stale_pending_text_after_local_validation,
    _has_safe_validation_evidence_marker,
    _normalize_form_inputs,
)

__all__: list[str] = []


from pathlib import Path
from typing import Any, Iterable, Mapping

from .models import FORM_KEYS, MANDATORY_PROTECTED_PATHS, MANDATORY_RULES
from .paths_io import _resolve_project_root, _source_name
from .form_normalization import (
    _field_value_or_empty_if_placeholder,
    _form_has_mandatory_freeze_fields,
    _is_starter_placeholder,
    _repair_hint_form_inputs_from_raw_hint,
)
from .records import _consume_latest_hint_if_already_frozen, load_latest_freeze_hint_record
from .scanner import scan_and_save_latest_freeze_hint

def resolve_freeze_hint_autofill_state(
    project_root: str | Path,
    fallback_inputs: Mapping[str, Any],
    *,
    staging_dir: str | Path | None = None,
    manual_form_inputs: Mapping[str, Any] | None = None,
    preview_form_inputs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve the single authoritative autofill state for the freeze form.

    This function is the contract-level arbitration point for New Local Freeze
    Entry autofill. It makes the truth-source priority executable instead of
    letting separate read paths compete:

    0. current preview-session form data, when valid;
    1. manual AI review form data, only when coherent with the current feature;
    2. latest project-local freeze hint with validation evidence;
    3. newest valid unconsumed staged sidecar;
    4. existing latest hint when scan finds no usable newer sidecar;
    5. safe starter fallback only when no valid current feature evidence exists.

    The GUI should render the returned form inputs and use
    confirm_write_enabled as the contract-level writeability signal.
    """

    root = _resolve_project_root(project_root)
    fallback = _normalize_form_inputs(dict(fallback_inputs))

    preview = _select_preview_snapshot(preview_form_inputs, fallback)
    if preview is not None:
        return preview

    manual = _select_manual_review_form(root, manual_form_inputs, fallback)
    if manual is not None:
        return manual

    _consume_latest_hint_if_already_frozen(root)

    scan_result = scan_and_save_latest_freeze_hint(root, staging_dir=staging_dir)
    _consume_latest_hint_if_already_frozen(root)

    load_result = load_latest_freeze_hint_record(root)

    if not load_result.get("ok"):
        result = dict(fallback)
        warnings = list(scan_result.get("warnings") or []) + list(load_result.get("warnings") or [])
        if warnings:
            result["known_warnings"] = _append_text(result.get("known_warnings", ""), " ".join(warnings))
        return _autofill_state_result(
            root,
            source_kind="starter_fallback",
            form_inputs=result,
            record=None,
            scan_result=scan_result,
            warnings=warnings,
        )

    record = dict(load_result.get("record") or {})
    merged = _merge_record_form_inputs_with_fallback(record, fallback)
    source_kind = "latest_freeze_hint"
    if scan_result.get("ok") and scan_result.get("record"):
        source_kind = "staged_sidecar_or_preserved_latest"

    return _autofill_state_result(
        root,
        source_kind=source_kind,
        form_inputs=merged,
        record=record,
        scan_result=scan_result,
        warnings=list(scan_result.get("warnings") or []),
    )

def build_freeze_form_inputs_from_latest_hint(
    project_root: str | Path,
    fallback_inputs: Mapping[str, Any],
) -> dict[str, Any]:
    """Return form inputs using the contract-level autofill state machine."""

    state = resolve_freeze_hint_autofill_state(project_root, fallback_inputs)
    return dict(state.get("form_inputs") or {})

def _select_preview_snapshot(
    preview_form_inputs: Mapping[str, Any] | None,
    fallback: Mapping[str, str],
) -> dict[str, Any] | None:
    """Return tier-0 in-memory preview data when it is writeable."""

    if not preview_form_inputs:
        return None
    form = _merge_form_inputs_with_fallback(preview_form_inputs, fallback)
    if not _form_has_recognizable_validation_marker(form):
        return None
    if not str(form.get("feature_title") or "").strip():
        return None
    return _autofill_state_result(
        None,
        source_kind="preview_session_snapshot",
        form_inputs=form,
        record=None,
        scan_result={"warnings": []},
        warnings=[],
    )

def _select_manual_review_form(
    project_root: Path,
    manual_form_inputs: Mapping[str, Any] | None,
    fallback: Mapping[str, str],
) -> dict[str, Any] | None:
    """Return tier-1 manual review data only when it matches current context."""

    if not manual_form_inputs:
        return None
    manual_form = _merge_form_inputs_with_fallback(manual_form_inputs, fallback)
    if not _form_has_recognizable_validation_marker(manual_form):
        return None
    manual_title = str(manual_form.get("feature_title") or "").strip()
    if not manual_title:
        return None

    latest = load_latest_freeze_hint_record(project_root)
    if latest.get("ok"):
        record = dict(latest.get("record") or {})
        latest_title = _record_feature_title(record)
        if latest_title and latest_title != manual_title:
            return None
        return _autofill_state_result(
            project_root,
            source_kind="manual_ai_review_json",
            form_inputs=manual_form,
            record=record,
            scan_result={"warnings": []},
            warnings=[],
        )

    # If no latest context exists, a manual review with recognizer-friendly
    # validation evidence is still allowed as an explicit human-directed input.
    return _autofill_state_result(
        project_root,
        source_kind="manual_ai_review_json_without_latest_context",
        form_inputs=manual_form,
        record=None,
        scan_result={"warnings": []},
        warnings=["Manual AI review data was accepted because no latest freeze hint context exists."],
    )

def _merge_record_form_inputs_with_fallback(
    record: Mapping[str, Any],
    fallback: Mapping[str, str],
) -> dict[str, str]:
    """Merge saved form inputs over the starter fallback.

    Saved records created by older intake logic may have a valid raw hint but
    stale/blank form_inputs. Re-derive form inputs from the raw hint and use
    that repaired current-feature evidence whenever saved form fields are empty
    or still contain starter placeholders. This fixes the form generator rather
    than asking the user to manually overwrite placeholders.
    """

    form_inputs = _normalize_form_inputs(dict(record.get("form_inputs") or {}))
    repaired_inputs = _repair_hint_form_inputs_from_raw_hint(record)

    merged = dict(fallback)
    for key in FORM_KEYS:
        value = _field_value_or_empty_if_placeholder(key, form_inputs.get(key, ""))
        if not value:
            value = _field_value_or_empty_if_placeholder(key, repaired_inputs.get(key, ""))
        if value:
            merged[key] = value

    # Once current freeze-hint evidence exists, starter-only warning/next-step
    # text must not leak into the preview as if the form were still generic.
    for key in ("known_warnings", "planned_next_step", "notes"):
        if _is_starter_placeholder(merged.get(key, "")):
            merged[key] = ""
        repaired_value = _field_value_or_empty_if_placeholder(key, repaired_inputs.get(key, ""))
        if repaired_value:
            merged[key] = repaired_value

    merged["protected_paths"] = _append_missing_lines(
        merged.get("protected_paths", ""),
        MANDATORY_PROTECTED_PATHS,
    )
    merged["do_not_regress_rules"] = _append_missing_lines(
        merged.get("do_not_regress_rules", ""),
        MANDATORY_RULES,
    )

    hint_title = str(merged.get("feature_title", "")).strip() or "the current feature"
    source_name = _source_name(record)
    merged["known_warnings"] = _append_text(
        merged.get("known_warnings", ""),
        "Auto-filled from saved KANDA_FREEZE_HINT.json intake data for "
        + hint_title
        + ". Human review is still required before Confirm and Write.",
    )
    merged["notes"] = _append_text(
        merged.get("notes", ""),
        "Freeze-intake data was loaded from <project>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake. Source patch ZIP: "
        + source_name
        + ".",
    )
    return _clean_stale_pending_text_after_local_validation(merged)

def _merge_form_inputs_with_fallback(
    inputs: Mapping[str, Any],
    fallback: Mapping[str, str],
) -> dict[str, str]:
    """Merge an arbitrary form-input mapping over the starter fallback."""

    normalized = _normalize_form_inputs(dict(inputs or {}))
    merged = dict(fallback)
    for key in FORM_KEYS:
        value = str(normalized.get(key, "")).strip()
        if value:
            merged[key] = value
    merged["protected_paths"] = _append_missing_lines(
        merged.get("protected_paths", ""),
        MANDATORY_PROTECTED_PATHS,
    )
    merged["do_not_regress_rules"] = _append_missing_lines(
        merged.get("do_not_regress_rules", ""),
        MANDATORY_RULES,
    )
    return _clean_stale_pending_text_after_local_validation(merged)

def _autofill_state_result(
    project_root: Path | None,
    *,
    source_kind: str,
    form_inputs: Mapping[str, Any],
    record: Mapping[str, Any] | None,
    scan_result: Mapping[str, Any],
    warnings: Iterable[str],
) -> dict[str, Any]:
    """Build a stable state result for the freeze form arbitration function."""

    normalized = _normalize_form_inputs(dict(form_inputs))
    normalized = _clean_stale_pending_text_after_local_validation(normalized)
    has_validation = _form_has_recognizable_validation_marker(normalized)
    has_mandatory = _form_has_mandatory_freeze_fields(normalized)
    is_starter = source_kind == "starter_fallback"
    return {
        "ok": True,
        "operation": "resolve_freeze_hint_autofill_state",
        "project_root": str(project_root) if project_root is not None else "",
        "source_kind": source_kind,
        "form_inputs": normalized,
        "record": dict(record or {}),
        "scan_result": dict(scan_result or {}),
        "preview_read_only": True,
        "confirm_write_enabled": bool(has_validation and has_mandatory and not is_starter),
        "mandatory_fields_status": "complete" if has_mandatory else "missing_or_placeholder",
        "validation_evidence_status": "recognized" if has_validation else "missing_or_unrecognized",
        "warnings": list(warnings or []),
        "errors": [],
    }

def _form_has_recognizable_validation_marker(form_inputs: Mapping[str, Any]) -> bool:
    """Return True when form inputs contain safe validation evidence."""

    return _has_safe_validation_evidence_marker(
        str(form_inputs.get("validation_evidence_summary") or "")
    )

def _record_feature_title(record: Mapping[str, Any]) -> str:
    """Return the feature title encoded in a saved record."""

    form = record.get("form_inputs") if isinstance(record.get("form_inputs"), Mapping) else {}
    hint = record.get("hint") if isinstance(record.get("hint"), Mapping) else {}
    return str(
        (form or {}).get("feature_title")
        or (hint or {}).get("feature_title")
        or ""
    ).strip()
