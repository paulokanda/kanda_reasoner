"""Public contract for freeze hint intake records.

Patch ZIPs produced by the AI may contain a root-level KANDA_FREEZE_HINT.json
file. This box imports that sidecar into project-local state so the Freeze
Feature After Update tab can fill the New Local Freeze Entry form with the
feature that was just implemented, instead of guessing from older local files.

This box owns code only. Project-specific intake state is stored under the
selected active project at project_freeze_after_update/freeze_hint_intake.
It does not store project-specific memory in project_freeze_ledger.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable, Mapping
import zipfile

FREEZE_HINT_FILENAME = "KANDA_FREEZE_HINT.json"
INTAKE_REL = Path("project_freeze_after_update") / "freeze_hint_intake"
HISTORY_REL = INTAKE_REL / "history"
LATEST_NAME = "latest_freeze_hint.json"
CONSUMED_NAME = "consumed_freeze_hints.json"
SCHEMA_VERSION = "1.0"

FORM_KEYS = (
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
)

LIST_TEXT_KEYS = (
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
)

MANDATORY_PROTECTED_PATHS = (
    "project_freeze_after_update/frozen_features_memory/",
)

MANDATORY_RULES = (
    "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.",
    "Do not store project-specific frozen memory inside project_freeze_ledger.",
    "Preview Freeze Entry must remain read-only and must not write files.",
    "Confirm and Write must require explicit human confirmation before writing governed freeze memory.",
    "After a local freeze write, the AI startup freeze context must be refreshed.",
    "External AI review remains advanced/fallback, not the normal local freeze path.",
)

RECOGNIZABLE_VALIDATION_HINT = (
    "Validation evidence intended for Confirm and Write must include a literal "
    "recognizable marker such as VALIDATION OK: <feature_id> or STATUS: IN_SYNC."
)

HINT_FIELD_ALIASES = {
    "primary_box": (
        "primary_box",
        "owning_box",
        "box",
    ),
    "box_type": (
        "box_type",
        "feature_type",
    ),
    "validated_files": (
        "validated_files",
        "box_paths",
        "updated_files",
        "changed_files",
        "touched_files",
    ),
    "generated_files": (
        "generated_files",
        "generated_paths",
        "created_files",
    ),
    "protected_paths": (
        "protected_paths",
        "box_paths",
    ),
    "do_not_regress_rules": (
        "do_not_regress_rules",
        "do_not_regress",
        "do_not_touch_summary",
    ),
    "known_warnings": (
        "known_warnings",
        "freeze_warning",
        "warnings",
    ),
    "planned_next_step": (
        "planned_next_step",
        "next_step",
    ),
    "notes": (
        "notes",
        "freeze_summary",
        "summary",
    ),
}

STARTER_PLACEHOLDER_PATTERNS = (
    "current validated feature - replace with exact feature title",
    "replace with the primary box for the current feature",
    "replace with the current box type",
    "starter draft only",
    "replace placeholders",
    "starter fallback",
)

STALE_LOCAL_VALIDATION_PENDING_PATTERNS = (
    "local validation pending",
    "pre-validation sidecar only",
    "pre validation sidecar only",
    "user-local validation must be run",
    "user local validation must be run",
    "user-local validation remains required",
    "user local validation remains required",
    "run the delivered validation block",
    "run the provided validation block",
    "run scripts/validate_release_guard_zip_contract_v1.py after installation",
    "before confirm and write",
    "before freeze confirmation",
    "before freezing",
)

MANDATORY_FORM_FIELDS = (
    "feature_title",
    "primary_box",
    "validated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
)


@dataclass(frozen=True)
class FreezeHintIntakePaths:
    """Resolved paths for one project's freeze hint intake box."""

    project_root: Path
    intake_root: Path
    history_root: Path
    latest_hint: Path
    consumed_hints: Path


class FreezeHintIntakeError(RuntimeError):
    """Raised when freeze hint intake cannot process a sidecar safely."""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def read_freeze_hint_from_patch_zip(patch_zip: str | Path) -> dict[str, Any]:
    """Read and normalize KANDA_FREEZE_HINT.json from a patch ZIP.

    The sidecar must be at the ZIP root. The function does not write files.
    """

    zip_path = Path(patch_zip).expanduser().resolve()
    if not zip_path.is_file():
        raise FreezeHintIntakeError(f"Patch ZIP not found: {zip_path}")
    if zip_path.suffix.lower() != ".zip":
        raise FreezeHintIntakeError(f"Patch path is not a ZIP file: {zip_path}")

    try:
        with zipfile.ZipFile(zip_path) as archive:
            names = set(archive.namelist())
            if FREEZE_HINT_FILENAME not in names:
                raise FreezeHintIntakeError(f"Patch ZIP is missing {FREEZE_HINT_FILENAME}: {zip_path}")
            raw = archive.read(FREEZE_HINT_FILENAME).decode("utf-8-sig", errors="replace")
    except zipfile.BadZipFile as exc:
        raise FreezeHintIntakeError(f"Invalid patch ZIP: {zip_path}") from exc

    try:
        loaded = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FreezeHintIntakeError(f"Malformed {FREEZE_HINT_FILENAME} in {zip_path}") from exc

    if not isinstance(loaded, Mapping):
        raise FreezeHintIntakeError(f"{FREEZE_HINT_FILENAME} must contain a JSON object.")

    return _normalize_hint(dict(loaded), zip_path)


def scan_and_save_latest_freeze_hint(
    project_root: str | Path,
    *,
    staging_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Scan the project staging folder for the newest unused freeze hint.

    If a valid unconsumed hint is found, it is saved under the selected
    project's project_freeze_after_update/freeze_hint_intake box and returned.
    If none is found, the function returns ok=False and does not change files.
    Consumed or already-frozen sidecars are skipped, not terminal blockers, so
    a newer frozen patch ZIP cannot hide the next current unconsumed patch ZIP.
    Older stale sidecars remain blocked by the validated-latest timestamp guard.
    """

    root = _resolve_project_root(project_root)
    paths = build_freeze_hint_intake_paths(root)
    scan_root = Path(staging_dir).expanduser().resolve() if staging_dir else _default_staging_dir(root)

    if not scan_root.exists() or not scan_root.is_dir():
        return {
            "ok": False,
            "operation": "scan_and_save_latest_freeze_hint",
            "project_root": str(root),
            "staging_dir": str(scan_root),
            "errors": [],
            "warnings": ["Freeze hint staging folder was not found."],
        }

    consumed = _load_consumed(paths.consumed_hints)
    candidates = sorted(scan_root.glob("*.zip"), key=lambda item: _safe_mtime_ns(item), reverse=True)
    skipped: list[str] = []
    stale_skipped: list[str] = []
    errors: list[str] = []
    newest_consumed_blocked = False
    existing_validated_source_mtime = _existing_validated_latest_source_mtime_ns(paths)

    for candidate in candidates:
        try:
            hint = read_freeze_hint_from_patch_zip(candidate)
        except FreezeHintIntakeError as exc:
            errors.append(str(exc))
            continue

        signature = _source_signature(candidate)
        if _is_consumed(consumed, signature, hint):
            skipped.append(candidate.name)
            newest_consumed_blocked = True
            continue

        frozen_match = _find_matching_frozen_feature(
            root,
            {"hint": hint, "form_inputs": _hint_to_form_inputs(hint)},
        )
        if frozen_match is not None:
            _remember_consumed_hint(
                paths,
                source_signature=signature,
                hint=hint,
                used_freeze_id=str(frozen_match.get("freeze_id") or ""),
            )
            skipped.append(candidate.name)
            newest_consumed_blocked = True
            continue

        if (
            existing_validated_source_mtime is not None
            and _safe_mtime_ns(candidate) < existing_validated_source_mtime
        ):
            stale_skipped.append(candidate.name)
            continue

        if newest_consumed_blocked and not _has_safe_validation_evidence_marker(
            str(hint.get("validation_evidence_summary") or "")
        ):
            stale_skipped.append(candidate.name)
            continue

        preserved = _preserve_existing_validated_record_if_same_hint(paths, hint, signature)
        if preserved is not None:
            return {
                "ok": True,
                "operation": "scan_and_save_latest_freeze_hint",
                "project_root": str(root),
                "staging_dir": str(scan_root),
                "record": preserved,
                "source_patch_zip": str(candidate),
                "skipped_consumed": skipped,
                "skipped_stale_older_than_validated_latest": stale_skipped,
                "errors": [],
                "warnings": [
                    "Existing freeze hint intake record was preserved because it already contains recognizer-friendly local validation evidence."
                ],
            }

        record = save_freeze_hint_record(root, hint, source_signature=signature)
        return {
            "ok": True,
            "operation": "scan_and_save_latest_freeze_hint",
            "project_root": str(root),
            "staging_dir": str(scan_root),
            "record": record,
            "source_patch_zip": str(candidate),
            "skipped_consumed": skipped,
            "skipped_stale_older_than_validated_latest": stale_skipped,
            "errors": [],
            "warnings": [],
        }

    warnings = ["No unused KANDA_FREEZE_HINT.json sidecar was found in staged patch ZIPs."]
    if skipped:
        warnings.append("Newest matching freeze hint sidecars were already consumed: " + ", ".join(skipped[:5]))
    if newest_consumed_blocked:
        warnings.append("Stopped at the newest consumed or already-frozen freeze hint sidecar instead of falling through to older stale sidecars.")
    if stale_skipped:
        warnings.append("Older staged sidecars were ignored because a newer validated latest hint exists: " + ", ".join(stale_skipped[:5]))
    return {
        "ok": False,
        "operation": "scan_and_save_latest_freeze_hint",
        "project_root": str(root),
        "staging_dir": str(scan_root),
        "skipped_consumed": skipped,
        "skipped_stale_older_than_validated_latest": stale_skipped,
        "errors": errors,
        "warnings": warnings,
    }


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
        "Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: "
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
    hint = _clean_stale_pending_text_after_local_validation(hint)
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

def build_freeze_hint_intake_paths(project_root: str | Path) -> FreezeHintIntakePaths:
    """Build project-local paths for the freeze hint intake box."""

    root = _resolve_project_root(project_root)
    intake_root = root / INTAKE_REL
    return FreezeHintIntakePaths(
        project_root=root,
        intake_root=intake_root,
        history_root=root / HISTORY_REL,
        latest_hint=intake_root / LATEST_NAME,
        consumed_hints=intake_root / CONSUMED_NAME,
    )


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------



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



def _same_feature_id_alias(left: Any, right: Any) -> bool:
    """Return True for equivalent feature IDs across underscore/hyphen slug styles.

    KANDA_FREEZE_HINT.json sidecars are normalized to safe slugs when saved
    (for example, freeze_tab_restore_v1 becomes freeze-tab-restore-v1), while
    validation markers and validation scripts often keep the original underscore
    feature_id. These are the same feature identity and must not block merging
    post-validation evidence into the project-local freeze hint intake record.
    """

    left_text = str(left or "").strip()
    right_text = str(right or "").strip()
    if not left_text or not right_text:
        return False
    if left_text == right_text:
        return True
    return _safe_slug(left_text) == _safe_slug(right_text)

def _same_feature_identity(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Return True when two freeze hints describe the same feature/patch."""

    left_id = str(left.get("feature_id") or "").strip()
    right_id = str(right.get("feature_id") or "").strip()
    left_patch = str(left.get("patch_name") or "").strip()
    right_patch = str(right.get("patch_name") or "").strip()
    if left_id and right_id and _same_feature_id_alias(left_id, right_id):
        if left_patch and right_patch:
            return left_patch == right_patch
        return True
    left_title = str(left.get("feature_title") or "").strip()
    right_title = str(right.get("feature_title") or "").strip()
    return bool(left_title and right_title and left_title == right_title and (not left_patch or not right_patch or left_patch == right_patch))


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


def _find_matching_frozen_feature(project_root: Path, record: Mapping[str, Any]) -> dict[str, Any] | None:
    """Return a frozen feature match for the latest hint, if any.

    The local freeze writer should mark a hint used after Confirm and Write, but
    this function protects the workflow when project state is imperfect:
    - freeze_index.json may be missing the newest entry;
    - the entry file may exist even when the index is stale;
    - the saved hint may use underscores while the freeze ID uses hyphens.

    Detection therefore checks both freeze_index.json and entry/*.md files.
    """

    if not isinstance(record, Mapping):
        return None

    candidate_slugs = _candidate_feature_slugs_from_record(record)
    if not candidate_slugs:
        return None

    index_match = _find_matching_frozen_feature_in_index(project_root, candidate_slugs)
    if index_match is not None:
        return index_match

    return _find_matching_frozen_feature_in_entry_files(project_root, candidate_slugs)


def _candidate_feature_slugs_from_record(record: Mapping[str, Any]) -> set[str]:
    hint = record.get("hint") if isinstance(record.get("hint"), Mapping) else {}
    form_inputs = record.get("form_inputs") if isinstance(record.get("form_inputs"), Mapping) else {}
    candidates = {
        _safe_slug(str(hint.get("feature_id") or "")),
        _safe_slug(str(hint.get("feature_title") or "")),
        _safe_slug(str(form_inputs.get("feature_title") or "")),
    }
    cleaned = {slug for slug in candidates if slug and slug != "freeze-hint"}
    return cleaned


def _find_matching_frozen_feature_in_index(project_root: Path, candidate_slugs: set[str]) -> dict[str, Any] | None:
    index_path = project_root / "project_freeze_after_update" / "frozen_features_memory" / "freeze_index.json"
    if not index_path.exists():
        return None

    try:
        index_data = json.loads(index_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return None

    freezes = index_data.get("freezes") if isinstance(index_data, Mapping) else None
    if not isinstance(freezes, list):
        return None

    for item in freezes:
        if not isinstance(item, Mapping):
            continue
        if not _freeze_index_item_can_consume_hint(item):
            continue
        item_slugs = _freeze_index_item_slugs(item)
        if candidate_slugs.intersection(item_slugs):
            return dict(item)
    return None


def _freeze_index_item_can_consume_hint(item: Mapping[str, Any]) -> bool:
    status = str(item.get("status") or "").strip().casefold()
    if status and status not in {"frozen", "active", "validated"}:
        return False
    superseded_by = str(item.get("superseded_by") or "").strip()
    return not superseded_by


def _freeze_index_item_slugs(item: Mapping[str, Any]) -> set[str]:
    freeze_id = str(item.get("freeze_id") or "").strip()
    feature_title = str(item.get("feature_title") or item.get("title") or "").strip()
    entry_path = str(item.get("entry") or "").strip()
    slugs = {_safe_slug(freeze_id), _safe_slug(feature_title)}
    tail = _freeze_feature_tail_slug(freeze_id)
    if tail:
        slugs.add(tail)
    if entry_path:
        entry_stem = Path(entry_path).stem
        slugs.add(_safe_slug(entry_stem))
        entry_tail = _freeze_feature_tail_slug(entry_stem)
        if entry_tail:
            slugs.add(entry_tail)
    slugs.discard("freeze-hint")
    slugs.discard("")
    return slugs


def _find_matching_frozen_feature_in_entry_files(project_root: Path, candidate_slugs: set[str]) -> dict[str, Any] | None:
    entries_root = project_root / "project_freeze_after_update" / "frozen_features_memory" / "entries"
    if not entries_root.exists() or not entries_root.is_dir():
        return None

    for entry_file in sorted(entries_root.glob("freeze-*.md"), key=lambda item: item.name.lower()):
        if not entry_file.is_file():
            continue
        match = _entry_file_frozen_match(entry_file, candidate_slugs, project_root)
        if match is not None:
            return match
    return None


def _entry_file_frozen_match(entry_file: Path, candidate_slugs: set[str], project_root: Path) -> dict[str, Any] | None:
    try:
        text = entry_file.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return None

    head = text[:12000]
    slugs = {_safe_slug(entry_file.stem)}
    tail = _freeze_feature_tail_slug(entry_file.stem)
    if tail:
        slugs.add(tail)

    for pattern in (
        r"freeze_id:\s*[\"\']?([^\"\'\n]+)",
        r"feature_title:\s*[\"\']?([^\"\'\n]+)",
        r"title:\s*[\"\']?([^\"\'\n]+)",
        r'^#\s+(.+)$',
    ):
        for match in re.finditer(pattern, head, flags=re.MULTILINE):
            captured = match.group(1).strip().strip('"\'')
            if captured:
                slugs.add(_safe_slug(captured))
                tail = _freeze_feature_tail_slug(captured)
                if tail:
                    slugs.add(tail)

    # Do not infer frozen status from arbitrary body prose or validation
    # evidence. A freeze entry for one feature may mention another feature in
    # validation notes, protected-path summaries, or next-step text. Only the
    # entry filename, freeze_id, feature_title, title, or H1 heading may identify
    # the feature that the entry itself freezes. This prevents related frozen
    # repair entries from hiding the next current unconsumed patch ZIP.

    slugs.discard("freeze-hint")
    slugs.discard("")
    if not candidate_slugs.intersection(slugs):
        return None

    freeze_id = entry_file.stem
    freeze_id_match = re.search(r"freeze_id:\s*[\"\']?([^\"\'\n]+)", head)
    if freeze_id_match:
        freeze_id = freeze_id_match.group(1).strip().strip('"\'') or freeze_id

    rel_entry = entry_file
    try:
        rel_entry = entry_file.relative_to(project_root)
    except ValueError:
        pass

    return {
        "freeze_id": freeze_id,
        "status": "frozen",
        "entry": str(rel_entry).replace("\\", "/"),
        "source": "entry_file_scan",
    }

def _freeze_feature_tail_slug(freeze_id: str) -> str:
    """Return feature portion from freeze-YYYYMMDD-feature-id freeze IDs."""

    slug = _safe_slug(freeze_id)
    match = re.match(r"^freeze-[0-9]{8}-(.+)$", slug)
    if match:
        return match.group(1)
    return slug


def _normalize_hint(raw_hint: Mapping[str, Any], source: Any) -> dict[str, Any]:
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
    boundary = hint.get("patch_boundary")
    if not isinstance(boundary, Mapping):
        return []
    for key in ("generated_files", "generated_paths", "created_files"):
        paths = _coerce_path_text_list(boundary.get(key))
        if paths:
            return paths
    return []


def _coerce_path_text_list(value: Any) -> list[str]:
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
    value = hint.get("protected_architecture_characteristics")
    items: list[str] = []
    for item in _coerce_path_text_list(value):
        readable = item.replace("_", " ").strip()
        if readable:
            items.append("Preserve " + readable + ".")
    return items


def _is_starter_placeholder(value: Any) -> bool:
    text = str(value or "").strip().lower()
    if not text:
        return False
    return any(pattern in text for pattern in STARTER_PLACEHOLDER_PATTERNS)


def _value_or_empty_if_placeholder(value: Any) -> str:
    text = str(value or "").strip()
    return "" if _is_starter_placeholder(text) else text


def _field_value_or_empty_if_placeholder(field_name: str, value: Any) -> str:
    text = str(value or "").strip()
    if field_name == "validation_evidence_summary":
        return text
    return "" if _is_starter_placeholder(text) else text


def _merge_lines(existing: Any, additions: Iterable[str]) -> str:
    lines = _coerce_path_text_list(existing)
    for item in additions:
        text = str(item).strip()
        if text and text not in lines:
            lines.append(text)
    return "\n".join(lines)


def _repair_hint_form_inputs_from_raw_hint(record: Mapping[str, Any]) -> dict[str, str]:
    hint = record.get("hint")
    if not isinstance(hint, Mapping):
        return {}
    try:
        normalized_hint = _normalize_hint(dict(hint), record.get("source"))
        return _hint_to_form_inputs(normalized_hint)
    except Exception:
        return {}


def _form_has_mandatory_freeze_fields(form_inputs: Mapping[str, Any]) -> bool:
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
    paths = _hint_path_list(hint)
    if not paths:
        return ""
    normalized = [item.replace("\\", "/").strip("/") for item in paths]
    if normalized and all(item.startswith("tests/") for item in normalized):
        return "tests-only validation shielding"
    if any(item.startswith("tests/") for item in normalized):
        return "source and tests update"
    return "project source update"


def _hint_to_form_inputs(hint: Mapping[str, Any]) -> dict[str, str]:
    inputs = {key: str(hint.get(key, "")).strip() for key in FORM_KEYS}
    inputs["validation_evidence_summary"] = _normalize_validation_evidence_summary(
        inputs.get("validation_evidence_summary", "")
    )
    inputs["protected_paths"] = _append_missing_lines(inputs.get("protected_paths", ""), MANDATORY_PROTECTED_PATHS)
    inputs["do_not_regress_rules"] = _append_missing_lines(inputs.get("do_not_regress_rules", ""), MANDATORY_RULES)
    return _clean_stale_pending_text_after_local_validation(inputs)


def _normalize_form_inputs(inputs: Mapping[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key in FORM_KEYS:
        normalized[key] = _field_to_text(inputs.get(key, ""), list_text=key in LIST_TEXT_KEYS)
    return normalized


def _field_to_text(value: Any, *, list_text: bool = False) -> str:
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
    lines = [line.strip() for line in str(value or "").splitlines() if line.strip()]
    seen = {_normalize_line(line) for line in lines}
    for line in required_lines:
        norm = _normalize_line(line)
        if norm not in seen:
            lines.append(line)
            seen.add(norm)
    return "\n".join(lines)


def _append_text(value: Any, addition: str) -> str:
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
    folded = str(value or "").casefold()
    return any(pattern in folded for pattern in STALE_LOCAL_VALIDATION_PENDING_PATTERNS)


def _has_local_validation_completion_marker(value: Any) -> bool:
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
    text = str(value or "")
    if _has_stale_local_validation_pending_text(text) and not _has_local_validation_completion_marker(text):
        return False
    return _has_recognizable_validation_marker(text)


def _clean_stale_pending_text_after_local_validation(inputs: Mapping[str, Any]) -> dict[str, str]:
    cleaned = _normalize_form_inputs(dict(inputs))
    evidence = cleaned.get("validation_evidence_summary", "")
    if not _has_local_validation_completion_marker(evidence):
        return cleaned
    for key in ("validation_evidence_summary", "known_warnings", "planned_next_step", "notes"):
        cleaned[key] = _strip_stale_pending_validation_text(cleaned.get(key, ""))
    return cleaned


def _strip_stale_pending_validation_text(value: Any) -> str:
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
    text = str(line or "").strip()
    if not text:
        return ""
    if not _has_stale_local_validation_pending_text(text):
        return text
    parts = re.split(r"(?<=[.!?])\s+", text)
    kept = [part.strip() for part in parts if part.strip() and not _has_stale_local_validation_pending_text(part)]
    return " ".join(kept).strip()


def _normalize_line(value: str) -> str:
    return " ".join(str(value or "").lower().split())


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------


def _resolve_project_root(project_root: str | Path) -> Path:
    root = Path(project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise FreezeHintIntakeError(f"Project root is not a directory: {root}")
    if root.name == "project_freeze_ledger":
        raise FreezeHintIntakeError("Refusing project_freeze_ledger as active project root.")
    return root


def _default_staging_dir(project_root: Path) -> Path:
    anchor = project_root.anchor
    if anchor:
        return Path(anchor) / (project_root.name + "_delete_after_daily_work")
    return project_root.parent / (project_root.name + "_delete_after_daily_work")


def _source_signature(path: Path) -> dict[str, Any]:
    resolved = Path(path).expanduser().resolve()
    stat = resolved.stat()
    return {
        "source_path": str(resolved),
        "source_name": resolved.name,
        "source_mtime_ns": int(stat.st_mtime_ns),
        "source_size_bytes": int(stat.st_size),
    }


def _safe_mtime_ns(path: Path) -> int:
    try:
        return int(path.stat().st_mtime_ns)
    except OSError:
        return 0


def _load_consumed(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "kind": "kanda_consumed_freeze_hints", "items": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {"schema_version": SCHEMA_VERSION, "kind": "kanda_consumed_freeze_hints", "items": []}
    if not isinstance(data, dict):
        return {"schema_version": SCHEMA_VERSION, "kind": "kanda_consumed_freeze_hints", "items": []}
    if not isinstance(data.get("items"), list):
        data["items"] = []
    return data


def _remember_consumed_hint(
    paths: FreezeHintIntakePaths,
    *,
    source_signature: Mapping[str, Any],
    hint: Mapping[str, Any],
    used_freeze_id: str,
) -> None:
    """Record an already-frozen staged hint as consumed.

    This prevents New Local Freeze Entry from repeatedly re-importing a staged
    patch ZIP for a feature that already exists in frozen_features_memory.
    """

    consumed = _load_consumed(paths.consumed_hints)
    used_at = _utc_now()
    consumed_item = {
        "consumed_at_utc": used_at,
        "used_freeze_id": str(used_freeze_id or "").strip(),
        "source": _coerce_mapping(source_signature),
        "feature_id": str(hint.get("feature_id") or "").strip(),
        "feature_title": str(hint.get("feature_title") or "").strip(),
    }
    consumed.setdefault("items", [])
    if not any(_same_consumed_source(item, consumed_item) for item in consumed["items"] if isinstance(item, Mapping)):
        consumed["items"].append(consumed_item)
    consumed["updated_at_utc"] = used_at
    _atomic_write_json(paths.consumed_hints, consumed)


def _is_consumed(consumed: Mapping[str, Any], signature: Mapping[str, Any], hint: Mapping[str, Any]) -> bool:
    """Return True only for consumed records that really belong to this feature.

    A prior false already-frozen match can leave a consumed_freeze_hints.json
    item for the current patch but with an unrelated used_freeze_id. That stale
    false-consumed item must not hide the current valid unconsumed patch forever.
    The consumed item is authoritative only when its source/feature matches and
    its used_freeze_id is absent/legacy or names the same feature identity.
    """

    probe = {
        "source": dict(signature),
        "feature_id": str(hint.get("feature_id") or ""),
        "feature_title": str(hint.get("feature_title") or ""),
    }
    for item in consumed.get("items", []):
        if not isinstance(item, Mapping):
            continue
        if not _same_consumed_source(item, probe):
            continue
        if _consumed_freeze_id_confirms_hint(item, hint):
            return True
    return False


def _consumed_freeze_id_confirms_hint(item: Mapping[str, Any], hint: Mapping[str, Any]) -> bool:
    """Reject false-consumed records whose used_freeze_id names another feature.

    Do not infer consumed status from arbitrary old consumed records when the
    recorded used_freeze_id belongs to a different repair. This lets runtime-lite
    remain selectable after an earlier false-positive consumed it.
    """

    used_freeze_id = str(item.get("used_freeze_id") or "").strip()
    if not used_freeze_id:
        return True
    if not used_freeze_id.startswith("freeze-"):
        return True

    hint_slugs = {
        _safe_slug(str(hint.get("feature_id") or "")),
        _safe_slug(str(hint.get("feature_title") or "")),
    }
    hint_slugs.discard("")
    hint_slugs.discard("freeze-hint")
    if not hint_slugs:
        return True

    freeze_slugs = {_safe_slug(used_freeze_id)}
    freeze_tail = _freeze_feature_tail_slug(used_freeze_id)
    if freeze_tail:
        freeze_slugs.add(freeze_tail)
    freeze_slugs.discard("")
    freeze_slugs.discard("freeze-hint")

    return bool(hint_slugs.intersection(freeze_slugs))


def _same_consumed_source(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    left_source = _coerce_mapping(left.get("source"))
    right_source = _coerce_mapping(right.get("source"))
    keys = ("source_path", "source_mtime_ns", "source_size_bytes")
    if all(str(left_source.get(key, "")) and str(left_source.get(key, "")) == str(right_source.get(key, "")) for key in keys):
        return True

    # Older intake records may not have a complete source signature. Fall back
    # to feature identity so an already-frozen hint is not re-imported forever.
    left_id = str(left.get("feature_id") or "")
    right_id = str(right.get("feature_id") or "")
    if left_id and right_id and _same_feature_id_alias(left_id, right_id):
        return True
    left_title = str(left.get("feature_title") or "").strip()
    right_title = str(right.get("feature_title") or "").strip()
    return bool(left_title and right_title and left_title == right_title)


def _history_filename(saved_at_utc: str, hint: Mapping[str, Any]) -> str:
    stamp = re.sub(r"[^0-9A-Za-z]+", "", saved_at_utc)[:15]
    feature = _safe_slug(str(hint.get("feature_id") or hint.get("feature_title") or "freeze-hint"))
    return stamp + "_" + feature + ".json"


def _safe_slug(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "freeze-hint"



def _coerce_mapping(value: Any) -> dict[str, Any]:
    """Return a dictionary for mapping-like values and tolerate legacy scalars.

    Earlier formulary-data records may contain fields such as
    ``"source": "formulary_data_zip"``.  Those records are valid historical
    intake state, but ``dict("formulary_data_zip")`` raises ValueError.  The
    intake contract must treat non-mapping source values as absent metadata, not
    crash the Freeze tab formulary.
    """

    if isinstance(value, Mapping):
        return dict(value)
    return {}

def _source_name(record: Mapping[str, Any]) -> str:
    source = _coerce_mapping(record.get("source"))
    name = str(source.get("source_name") or record.get("source_zip") or "").strip()
    if name:
        return name
    path_text = str(source.get("source_path") or "").strip()
    return Path(path_text).name if path_text else "unknown"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _atomic_write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
