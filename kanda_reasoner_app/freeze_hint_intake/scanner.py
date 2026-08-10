"""Patch ZIP scanning and KANDA_FREEZE_HINT.json import for freeze hint intake."""

from __future__ import annotations

from .form_text_validation import (
    _has_safe_validation_evidence_marker,
    _hint_to_form_inputs,
)

__all__: list[str] = []


import json
from pathlib import Path
from typing import Any, Mapping
import zipfile

from .models import FREEZE_HINT_FILENAME, FreezeHintIntakeError
from .paths_io import _default_staging_dir, _resolve_project_root, _safe_mtime_ns, _source_signature, build_freeze_hint_intake_paths
from .form_normalization import _normalize_hint
from .frozen_matching import _find_matching_frozen_feature
from .records import (
    _existing_validated_latest_source_mtime_ns,
    _preserve_existing_validated_record_if_same_hint,
    save_freeze_hint_record,
)
from .consumed_hints import _is_consumed, _load_consumed, _remember_consumed_hint

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
    project's external project_freeze_after_update/freeze_hint_intake box and returned.
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
        if _is_consumed(consumed, signature, hint, project_root=root):
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
