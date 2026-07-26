# project-path: kanda_reasoner_app/freeze_after_update/migration.py
"""Safe migration for Freeze Feature After Update external state storage."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    PROJECT_FREEZE_AFTER_UPDATE_DIR,
    analysis_project_freeze_after_update_dir,
    ensure_show_project_lifecycle_manifest,
    legacy_project_freeze_after_update_dir,
    project_analysis_evidence_root,
)


@dataclass(frozen=True)
class FreezeStateMigrationResult:
    """Result of one safe freeze-state migration attempt."""

    ok: bool
    project_root: str
    show_project_root: str
    legacy_root: str
    canonical_root: str
    backup_root: str
    migrated_to_canonical: bool
    legacy_backup_created: bool
    legacy_removed: bool
    conflict_detected: bool
    warnings: list[str]
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable result dictionary."""
        return asdict(self)


def _utc_stamp() -> str:
    """Return a filesystem-safe UTC timestamp."""
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _atomic_write_text(path: Path, text: str) -> None:
    """Write a UTF-8 text file atomically in the target directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
        dir=str(path.parent),
        prefix="." + path.name + ".",
        suffix=".tmp",
    )
    tmp_name = handle.name
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        tmp_path = Path(tmp_name)
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def _dir_has_content(path: Path) -> bool:
    """Return True when a directory exists and has at least one child."""
    if not path.exists() or not path.is_dir():
        return False
    try:
        return any(path.iterdir())
    except OSError:
        return False


def _validate_freeze_root(path: Path) -> list[str]:
    """Return validation errors for a migrated freeze root."""
    errors: list[str] = []
    if not path.exists() or not path.is_dir():
        return ["canonical freeze root does not exist: " + str(path)]
    memory_root = path / "frozen_features_memory"
    if not memory_root.exists():
        return errors
    index_path = memory_root / "freeze_index.json"
    if index_path.is_file():
        try:
            data = json.loads(index_path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            errors.append("freeze_index.json is malformed: " + str(exc))
        else:
            if not isinstance(data, dict):
                errors.append("freeze_index.json must contain a JSON object")
            elif "freezes" in data and not isinstance(data.get("freezes"), list):
                errors.append("freeze_index.json freezes field must be a list")
    entries_root = memory_root / "entries"
    if entries_root.exists() and not entries_root.is_dir():
        errors.append("entries path exists but is not a directory: " + str(entries_root))
    return errors


def _copy_tree_strict(source: Path, destination: Path) -> None:
    """Copy a tree only when the destination does not exist."""
    if destination.exists():
        raise FileExistsError("Destination already exists: " + str(destination))
    shutil.copytree(source, destination, dirs_exist_ok=False)


def migrate_freeze_after_update_state(
    project_root: str | Path,
    *,
    clean_legacy: bool = False,
) -> FreezeStateMigrationResult:
    """Migrate freeze state to the external project-support root safely.

    The migration copies legacy data to the canonical external root, validates
    the copied state, creates an external backup of the legacy folder, and only
    removes the legacy in-source folder when clean_legacy is True and the backup
    is available. Existing canonical state is never overwritten or merged.
    """
    root = Path(project_root).expanduser().resolve(strict=False)
    show_root = project_analysis_evidence_root(root)
    legacy_root = legacy_project_freeze_after_update_dir(root)
    canonical_root = analysis_project_freeze_after_update_dir(root)
    backup_parent = show_root / "migration_backups"
    backup_root = backup_parent / (PROJECT_FREEZE_AFTER_UPDATE_DIR + "_legacy_backup_" + _utc_stamp())

    warnings: list[str] = []
    errors: list[str] = []
    migrated_to_canonical = False
    legacy_backup_created = False
    legacy_removed = False
    conflict_detected = False

    try:
        show_root.mkdir(parents=True, exist_ok=True)
        ensure_show_project_lifecycle_manifest(root)
    except OSError as exc:
        errors.append("Could not prepare show-project lifecycle manifest: " + str(exc))

    if errors:
        return FreezeStateMigrationResult(
            ok=False,
            project_root=str(root),
            show_project_root=str(show_root),
            legacy_root=str(legacy_root),
            canonical_root=str(canonical_root),
            backup_root=str(backup_root),
            migrated_to_canonical=False,
            legacy_backup_created=False,
            legacy_removed=False,
            conflict_detected=False,
            warnings=warnings,
            errors=errors,
        )

    legacy_exists = legacy_root.exists() and legacy_root.is_dir()
    canonical_exists = canonical_root.exists() and canonical_root.is_dir()

    if canonical_exists and legacy_exists:
        conflict_detected = True
        warnings.append("Both legacy and canonical freeze roots exist. Canonical is source of truth; legacy will not be merged.")
    elif legacy_exists and not canonical_exists:
        tmp_root = show_root / (PROJECT_FREEZE_AFTER_UPDATE_DIR + ".__migration_tmp__" + _utc_stamp())
        try:
            _copy_tree_strict(legacy_root, tmp_root)
            validation_errors = _validate_freeze_root(tmp_root)
            if validation_errors:
                errors.extend(validation_errors)
                shutil.rmtree(tmp_root, ignore_errors=True)
            else:
                os.replace(str(tmp_root), str(canonical_root))
                migrated_to_canonical = True
                canonical_exists = True
        except Exception as exc:
            errors.append("Could not migrate legacy freeze root to canonical root: " + str(exc))
            if tmp_root.exists():
                shutil.rmtree(tmp_root, ignore_errors=True)

    if canonical_exists or migrated_to_canonical:
        validation_errors = _validate_freeze_root(canonical_root)
        errors.extend(validation_errors)
    elif not legacy_exists:
        canonical_root.mkdir(parents=True, exist_ok=True)
        migrated_to_canonical = True

    if legacy_exists and not errors:
        try:
            backup_parent.mkdir(parents=True, exist_ok=True)
            _copy_tree_strict(legacy_root, backup_root)
            backup_errors = _validate_freeze_root(backup_root)
            if backup_errors:
                errors.extend("legacy backup validation failed: " + item for item in backup_errors)
            else:
                legacy_backup_created = True
        except Exception as exc:
            errors.append("Could not create legacy backup: " + str(exc))

    if clean_legacy and legacy_exists and legacy_backup_created and not errors:
        try:
            shutil.rmtree(legacy_root)
            legacy_removed = True
        except OSError as exc:
            errors.append("Could not remove legacy freeze root after backup: " + str(exc))

    if not clean_legacy and legacy_exists and not legacy_removed:
        warnings.append("Legacy freeze root was preserved because clean_legacy is False.")

    report = FreezeStateMigrationResult(
        ok=not errors,
        project_root=str(root),
        show_project_root=str(show_root),
        legacy_root=str(legacy_root),
        canonical_root=str(canonical_root),
        backup_root=str(backup_root) if legacy_backup_created else "",
        migrated_to_canonical=migrated_to_canonical,
        legacy_backup_created=legacy_backup_created,
        legacy_removed=legacy_removed,
        conflict_detected=conflict_detected,
        warnings=warnings,
        errors=errors,
    )

    if report.ok:
        _atomic_write_text(
            canonical_root / "migration_report.json",
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        )

    return report
