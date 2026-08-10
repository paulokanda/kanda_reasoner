"""Saved freeze hint records, validation-evidence merge, and latest-hint preservation."""

from __future__ import annotations

from .form_text_validation import (
    _clean_stale_pending_text_after_local_validation,
    _has_safe_validation_evidence_marker,
    _hint_to_form_inputs,
    _normalize_validation_evidence_summary,
)

__all__: list[str] = []


import json
from pathlib import Path
from typing import Any, Mapping

from .models import RECOGNIZABLE_VALIDATION_HINT, SCHEMA_VERSION, FreezeHintIntakePaths
from .paths_io import (
    _atomic_write_json,
    _coerce_mapping,
    _history_filename,
    _resolve_project_root,
    _utc_now,
    build_freeze_hint_intake_paths,
)
from .form_normalization import _normalize_hint
from .frozen_matching import (
    _find_matching_frozen_feature,
    _same_feature_id_alias,
    _same_feature_identity,
)
from .consumed_hints import _load_consumed, _same_consumed_source

def save_freeze_hint_record(
    project_root: str | Path,
    hint: Mapping[str, Any],
    *,
    source_signature: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Save a normalized freeze hint record under the selected project."""

    root = _resolve_project_root(project_root)
    paths = build_freeze_hint_intake_paths(root)
    normalized_hint = _normalize_hint(dict(hint), source_signature)
    form_inputs = _hint_to_form_inputs(normalized_hint)
    saved_at = _utc_now()
    record = {
        "schema_version": SCHEMA_VERSION,
        "kind": "kanda_saved_freeze_hint",
        "saved_at_utc": saved_at,
        "used_at_utc": None,
        "project_root": str(root),
        "source": _coerce_mapping(normalized_hint.get("source")),
        "hint": normalized_hint,
        "form_inputs": form_inputs,
    }

    paths.intake_root.mkdir(parents=True, exist_ok=True)
    paths.history_root.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(paths.latest_hint, record)

    history_name = _history_filename(saved_at, normalized_hint)
    _atomic_write_json(paths.history_root / history_name, record)
    return record

def load_latest_freeze_hint_record(project_root: str | Path, *, include_used: bool = False) -> dict[str, Any]:
    """Load the latest saved freeze hint record for the active project."""

    root = _resolve_project_root(project_root)
    paths = build_freeze_hint_intake_paths(root)
    if not paths.latest_hint.exists():
        return {
            "ok": False,
            "operation": "load_latest_freeze_hint_record",
            "project_root": str(root),
            "errors": [],
            "warnings": ["No saved freeze hint record exists yet."],
        }

    try:
        record = json.loads(paths.latest_hint.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "operation": "load_latest_freeze_hint_record",
            "project_root": str(root),
            "errors": ["Saved freeze hint record is malformed: " + str(exc)],
            "warnings": [],
        }

    if not isinstance(record, Mapping):
        return {
            "ok": False,
            "operation": "load_latest_freeze_hint_record",
            "project_root": str(root),
            "errors": ["Saved freeze hint record is not a JSON object."],
            "warnings": [],
        }

    if record.get("used_at_utc") and not include_used:
        return {
            "ok": False,
            "operation": "load_latest_freeze_hint_record",
            "project_root": str(root),
            "errors": [],
            "warnings": ["Latest saved freeze hint record has already been used."],
        }

    return {
        "ok": True,
        "operation": "load_latest_freeze_hint_record",
        "project_root": str(root),
        "record": dict(record),
        "errors": [],
        "warnings": [],
    }

def merge_validation_evidence_into_latest_hint(
    project_root: str | Path,
    validation_evidence_summary: str,
    *,
    feature_id: str = "",
    feature_title: str = "",
) -> dict[str, Any]:
    """Merge post-validation evidence into the latest saved freeze hint.

    Patch ZIP sidecars are created before the user's local validation block runs.
    Therefore a sidecar may contain sandbox evidence or a pending validation
    note, but the Confirm and Write gate needs recognizer-friendly local
    evidence after validation passes. Validation blocks should call this
    function after successful validation so New Local Freeze Entry receives the
    current feature data plus the exact validation output.
    """

    root = _resolve_project_root(project_root)
    paths = build_freeze_hint_intake_paths(root)
    loaded = load_latest_freeze_hint_record(root)
    if not loaded.get("ok"):
        return loaded

    evidence = _normalize_validation_evidence_summary(validation_evidence_summary)
    if not evidence.strip():
        return {
            "ok": False,
            "operation": "merge_validation_evidence_into_latest_hint",
            "project_root": str(root),
            "errors": ["validation_evidence_summary is empty."],
            "warnings": [],
        }

    warnings = []
    if not _has_safe_validation_evidence_marker(evidence):
        warnings.append(RECOGNIZABLE_VALIDATION_HINT)

    record = dict(loaded.get("record") or {})
    hint = dict(record.get("hint") or {})
    form_inputs = dict(record.get("form_inputs") or {})

    requested_feature_id = str(feature_id or "").strip()
    requested_feature_title = str(feature_title or "").strip()
    current_feature_id = str(hint.get("feature_id") or "").strip()
    current_feature_title = str(hint.get("feature_title") or form_inputs.get("feature_title") or "").strip()

    if requested_feature_id and current_feature_id and not _same_feature_id_alias(requested_feature_id, current_feature_id):
        return {
            "ok": False,
            "operation": "merge_validation_evidence_into_latest_hint",
            "project_root": str(root),
            "errors": [
                "feature_id mismatch: latest freeze hint is "
                + current_feature_id
                + "; validation evidence is for "
                + requested_feature_id
                + "."
            ],
            "warnings": warnings,
        }

    if requested_feature_title and current_feature_title and requested_feature_title != current_feature_title:
        warnings.append(
            "feature_title differs from latest freeze hint: "
            + current_feature_title
            + " versus "
            + requested_feature_title
            + ". Keeping latest freeze hint identity."
        )

    hint["validation_evidence_summary"] = evidence
    form_inputs["validation_evidence_summary"] = evidence
    cleaned_hint = dict(hint)
    cleaned_hint.update(_clean_stale_pending_text_after_local_validation(hint))
    hint = cleaned_hint
    form_inputs = _clean_stale_pending_text_after_local_validation(form_inputs)
    record["hint"] = hint
    record["form_inputs"] = form_inputs
    record["validation_evidence_merged_at_utc"] = _utc_now()

    _atomic_write_json(paths.latest_hint, record)
    history_name = _history_filename(record["validation_evidence_merged_at_utc"], hint)
    _atomic_write_json(paths.history_root / history_name, record)

    return {
        "ok": True,
        "operation": "merge_validation_evidence_into_latest_hint",
        "project_root": str(root),
        "feature_id": current_feature_id,
        "feature_title": current_feature_title,
        "errors": [],
        "warnings": warnings,
    }

def mark_latest_freeze_hint_used(project_root: str | Path, *, freeze_id: str = "") -> dict[str, Any]:
    """Mark the latest saved freeze hint as used after a confirmed freeze write."""

    root = _resolve_project_root(project_root)
    paths = build_freeze_hint_intake_paths(root)
    loaded = load_latest_freeze_hint_record(root, include_used=True)
    if not loaded.get("ok"):
        return loaded

    record = dict(loaded.get("record") or {})
    used_at = _utc_now()
    record["used_at_utc"] = used_at
    record["used_freeze_id"] = str(freeze_id or "").strip()
    _atomic_write_json(paths.latest_hint, record)

    consumed = _load_consumed(paths.consumed_hints)
    source = _coerce_mapping(record.get("source"))
    hint = dict(record.get("hint") or {})
    consumed_item = {
        "consumed_at_utc": used_at,
        "used_freeze_id": str(freeze_id or "").strip(),
        "source": source,
        "feature_id": str(hint.get("feature_id") or "").strip(),
        "feature_title": str(hint.get("feature_title") or record.get("form_inputs", {}).get("feature_title") or "").strip(),
    }
    consumed.setdefault("items", [])
    if not any(_same_consumed_source(item, consumed_item) for item in consumed["items"] if isinstance(item, Mapping)):
        consumed["items"].append(consumed_item)
    consumed["updated_at_utc"] = used_at
    _atomic_write_json(paths.consumed_hints, consumed)

    return {
        "ok": True,
        "operation": "mark_latest_freeze_hint_used",
        "project_root": str(root),
        "used_freeze_id": str(freeze_id or "").strip(),
        "errors": [],
        "warnings": [],
    }

def _consume_latest_hint_if_already_frozen(project_root: Path) -> bool:
    """Mark the saved latest hint used when it already has frozen memory.

    The latest intake record is a draft source, not a permanent queue item.
    If that feature is already in frozen_features_memory, it must not keep
    refilling New Local Freeze Entry. This helper is intentionally called before
    and after scanning staged ZIPs so both stale latest records and newly scanned
    already-frozen sidecars are consumed.
    """

    loaded = load_latest_freeze_hint_record(project_root)
    if not loaded.get("ok"):
        return False
    latest_record = dict(loaded.get("record") or {})
    frozen_match = _find_matching_frozen_feature(project_root, latest_record)
    if frozen_match is None:
        return False
    mark_latest_freeze_hint_used(project_root, freeze_id=str(frozen_match.get("freeze_id") or ""))
    return True

def _existing_validated_latest_source_mtime_ns(paths: FreezeHintIntakePaths) -> int | None:
    """Return source mtime for an unconsumed latest hint with validation evidence.

    New Local Freeze Entry should represent the current validated feature. If a
    current latest record already has recognizer-friendly validation evidence,
    older unrelated staged ZIPs must not overwrite it merely because the newest
    current patch was consumed or already frozen. Returning the latest source
    timestamp lets the scanner ignore older stale sidecars while still allowing
    a genuinely newer patch to replace the saved latest hint.
    """

    if not paths.latest_hint.exists():
        return None

    try:
        existing = json.loads(paths.latest_hint.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return None

    if not isinstance(existing, Mapping):
        return None
    if existing.get("used_at_utc"):
        return None
    if not _record_has_recognizable_validation_evidence(existing):
        return None

    source = _coerce_mapping(existing.get("source"))
    try:
        mtime = int(source.get("source_mtime_ns") or 0)
    except (TypeError, ValueError):
        return None
    return mtime if mtime > 0 else None

def _preserve_existing_validated_record_if_same_hint(
    paths: FreezeHintIntakePaths,
    incoming_hint: Mapping[str, Any],
    incoming_signature: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Preserve an already validated same-feature intake record during rescans.

    New Local Freeze Entry scans staged ZIPs before loading the saved hint.
    A staged ZIP sidecar is created before local validation, while the saved
    latest_freeze_hint.json may already have been upgraded by
    merge_validation_evidence_into_latest_hint after validation passed. If the
    same staged ZIP is scanned again, do not downgrade recognizer-friendly local
    validation evidence back to the pre-validation sidecar placeholder.
    """

    if not paths.latest_hint.exists():
        return None

    try:
        existing = json.loads(paths.latest_hint.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return None

    if not isinstance(existing, Mapping):
        return None
    if existing.get("used_at_utc"):
        return None

    existing_hint = dict(existing.get("hint") or {})
    existing_form = dict(existing.get("form_inputs") or {})
    existing_source = _coerce_mapping(existing.get("source") or existing_hint.get("source"))

    same_source = _same_source_identity(existing_source, incoming_signature)
    same_feature = _same_feature_identity(existing_hint, incoming_hint)
    if not same_source and not same_feature:
        return None

    existing_evidence = str(
        existing_form.get("validation_evidence_summary")
        or existing_hint.get("validation_evidence_summary")
        or ""
    )
    incoming_evidence = str(incoming_hint.get("validation_evidence_summary") or "")

    if _has_safe_validation_evidence_marker(existing_evidence) and not _has_safe_validation_evidence_marker(incoming_evidence):
        return dict(existing)

    return None

def _same_source_identity(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Return True when two source signatures identify the same staged ZIP."""

    if not left or not right:
        return False
    strong_keys = ("source_path", "source_mtime_ns", "source_size_bytes")
    if all(str(left.get(key, "")) and str(left.get(key, "")) == str(right.get(key, "")) for key in strong_keys):
        return True
    fallback_keys = ("source_name", "source_size_bytes")
    return all(str(left.get(key, "")) and str(left.get(key, "")) == str(right.get(key, "")) for key in fallback_keys)

def _record_has_recognizable_validation_evidence(record: Mapping[str, Any]) -> bool:
    hint = record.get("hint") if isinstance(record, Mapping) else {}
    form_inputs = record.get("form_inputs") if isinstance(record, Mapping) else {}
    evidence_parts = []
    if isinstance(hint, Mapping):
        evidence_parts.append(str(hint.get("validation_evidence_summary") or ""))
    if isinstance(form_inputs, Mapping):
        evidence_parts.append(str(form_inputs.get("validation_evidence_summary") or ""))
    evidence = "\n".join(part for part in evidence_parts if part.strip())
    return _has_safe_validation_evidence_marker(evidence)
