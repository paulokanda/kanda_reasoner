"""Project Analysis Evidence migration helpers.

This module belongs to the reasoner_symbol_atlas box. It only moves generated
analysis evidence from the legacy reference folder into the canonical active
project evidence folder when explicitly requested by the caller.

The helper is intentionally project-root dynamic and does not hardcode any
single project path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any, Iterable, Sequence

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_paths import (
    resolve_project_analysis_evidence_paths,
)


_JSON_GLOB = "*.json"
_BACKUP_TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"


@dataclass(frozen=True)
class ProjectAnalysisEvidenceMigrationFile:
    """One planned or executed evidence-file migration action."""

    relative_path: str
    source_path: str
    target_path: str
    action: str
    copied: bool = False
    backup_path: str = ""
    source_sha256: str = ""
    target_sha256_before: str = ""
    note: str = ""

    def to_json_data(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "relative_path": self.relative_path,
            "source_path": self.source_path,
            "target_path": self.target_path,
            "action": self.action,
            "copied": self.copied,
            "backup_path": self.backup_path,
            "source_sha256": self.source_sha256,
            "target_sha256_before": self.target_sha256_before,
            "note": self.note,
        }


@dataclass(frozen=True)
class ProjectAnalysisEvidenceMigrationReport:
    """Migration report for Project Analysis Evidence files."""

    project_root: str
    legacy_evidence_root: str
    canonical_evidence_root: str
    dry_run: bool
    status: str
    files: list[ProjectAnalysisEvidenceMigrationFile] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def copied_count(self) -> int:
        """Return the number of files copied by this operation."""
        return sum(1 for item in self.files if item.copied)

    @property
    def planned_copy_count(self) -> int:
        """Return the number of files that would be copied or updated."""
        return sum(
            1
            for item in self.files
            if item.action in {"copy", "backup_and_copy"}
        )

    def to_json_data(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "project_root": self.project_root,
            "legacy_evidence_root": self.legacy_evidence_root,
            "canonical_evidence_root": self.canonical_evidence_root,
            "dry_run": self.dry_run,
            "status": self.status,
            "copied_count": self.copied_count,
            "planned_copy_count": self.planned_copy_count,
            "files": [item.to_json_data() for item in self.files],
            "notes": list(self.notes),
        }


def plan_project_analysis_evidence_migration(
    project_root: str | Path,
    *,
    include_patterns: Sequence[str] | None = None,
) -> ProjectAnalysisEvidenceMigrationReport:
    """Return a dry-run plan for migrating legacy evidence JSON files."""
    return _build_migration_report(
        project_root,
        include_patterns=include_patterns,
        apply_changes=False,
        backup_existing=True,
    )


def migrate_project_analysis_evidence(
    project_root: str | Path,
    *,
    include_patterns: Sequence[str] | None = None,
    apply_changes: bool = False,
    backup_existing: bool = True,
) -> ProjectAnalysisEvidenceMigrationReport:
    """Migrate legacy evidence JSON files into the canonical folder.

    By default this function is a dry run. Set apply_changes=True to copy files.
    Existing target files are never deleted. If an existing target differs from
    the source, it is backed up before copying unless backup_existing is False.
    """
    return _build_migration_report(
        project_root,
        include_patterns=include_patterns,
        apply_changes=apply_changes,
        backup_existing=backup_existing,
    )


def write_project_analysis_evidence_migration_report(
    report: ProjectAnalysisEvidenceMigrationReport,
    output_path: str | Path,
) -> Path:
    """Write a migration report as UTF-8 JSON and return the output path."""
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(report.to_json_data(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return target


def _build_migration_report(
    project_root: str | Path,
    *,
    include_patterns: Sequence[str] | None,
    apply_changes: bool,
    backup_existing: bool,
) -> ProjectAnalysisEvidenceMigrationReport:
    paths = resolve_project_analysis_evidence_paths(project_root)
    legacy_root = Path(paths.legacy_evidence_dir)
    canonical_root = Path(paths.canonical_evidence_dir)
    root = Path(paths.project_root)

    notes: list[str] = []
    if not legacy_root.exists():
        return ProjectAnalysisEvidenceMigrationReport(
            project_root=str(root),
            legacy_evidence_root=str(legacy_root),
            canonical_evidence_root=str(canonical_root),
            dry_run=not apply_changes,
            status="missing_legacy_evidence",
            files=[],
            notes=["Legacy evidence folder does not exist."],
        )

    patterns = tuple(include_patterns or (_JSON_GLOB,))
    source_files = list(_iter_evidence_files(legacy_root, patterns))
    if not source_files:
        return ProjectAnalysisEvidenceMigrationReport(
            project_root=str(root),
            legacy_evidence_root=str(legacy_root),
            canonical_evidence_root=str(canonical_root),
            dry_run=not apply_changes,
            status="no_files",
            files=[],
            notes=["Legacy evidence folder exists but no matching files were found."],
        )

    results: list[ProjectAnalysisEvidenceMigrationFile] = []
    error_seen = False
    for source_file in source_files:
        try:
            results.append(
                _plan_or_apply_file(
                    source_file=source_file,
                    legacy_root=legacy_root,
                    canonical_root=canonical_root,
                    apply_changes=apply_changes,
                    backup_existing=backup_existing,
                )
            )
        except OSError as exc:
            error_seen = True
            relative_path = _safe_relative_path(source_file, legacy_root)
            results.append(
                ProjectAnalysisEvidenceMigrationFile(
                    relative_path=relative_path,
                    source_path=str(source_file),
                    target_path=str(canonical_root / relative_path),
                    action="error",
                    copied=False,
                    note=str(exc),
                )
            )

    if error_seen:
        status = "error"
    elif any(item.action in {"copy", "backup_and_copy"} for item in results):
        status = "migrated" if apply_changes else "migration_available"
    else:
        status = "already_current"

    if apply_changes:
        notes.append("Migration was applied. Legacy evidence was not deleted.")
    else:
        notes.append("Dry run only. No files were copied.")

    return ProjectAnalysisEvidenceMigrationReport(
        project_root=str(root),
        legacy_evidence_root=str(legacy_root),
        canonical_evidence_root=str(canonical_root),
        dry_run=not apply_changes,
        status=status,
        files=results,
        notes=notes,
    )


def _plan_or_apply_file(
    *,
    source_file: Path,
    legacy_root: Path,
    canonical_root: Path,
    apply_changes: bool,
    backup_existing: bool,
) -> ProjectAnalysisEvidenceMigrationFile:
    relative_path = _safe_relative_path(source_file, legacy_root)
    target_file = canonical_root / relative_path
    source_hash = _sha256_file(source_file)

    if target_file.exists():
        target_hash = _sha256_file(target_file)
        if source_hash == target_hash:
            return ProjectAnalysisEvidenceMigrationFile(
                relative_path=relative_path,
                source_path=str(source_file),
                target_path=str(target_file),
                action="skip_same",
                copied=False,
                source_sha256=source_hash,
                target_sha256_before=target_hash,
                note="Canonical evidence already matches legacy evidence.",
            )
        if not backup_existing:
            return ProjectAnalysisEvidenceMigrationFile(
                relative_path=relative_path,
                source_path=str(source_file),
                target_path=str(target_file),
                action="skip_changed_target",
                copied=False,
                source_sha256=source_hash,
                target_sha256_before=target_hash,
                note="Target differs and backup_existing is False.",
            )
        action = "backup_and_copy"
    else:
        target_hash = ""
        action = "copy"

    if not apply_changes:
        return ProjectAnalysisEvidenceMigrationFile(
            relative_path=relative_path,
            source_path=str(source_file),
            target_path=str(target_file),
            action=action,
            copied=False,
            source_sha256=source_hash,
            target_sha256_before=target_hash,
            note="Planned only. No file was copied.",
        )

    backup_path = ""
    target_file.parent.mkdir(parents=True, exist_ok=True)
    if target_file.exists() and action == "backup_and_copy":
        backup = _build_backup_path(target_file)
        shutil.copy2(target_file, backup)
        backup_path = str(backup)
    shutil.copy2(source_file, target_file)

    return ProjectAnalysisEvidenceMigrationFile(
        relative_path=relative_path,
        source_path=str(source_file),
        target_path=str(target_file),
        action=action,
        copied=True,
        backup_path=backup_path,
        source_sha256=source_hash,
        target_sha256_before=target_hash,
        note="Copied legacy evidence into canonical evidence folder.",
    )


def _iter_evidence_files(root: Path, patterns: Sequence[str]) -> Iterable[Path]:
    seen: set[Path] = set()
    for pattern in patterns:
        for item in root.rglob(pattern):
            if item.is_file() and item not in seen:
                seen.add(item)
                yield item


def _safe_relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return path.name


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _build_backup_path(target_file: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime(_BACKUP_TIMESTAMP_FORMAT)
    candidate = target_file.with_name(f"{target_file.name}.bak_{timestamp}")
    suffix = 1
    while candidate.exists():
        candidate = target_file.with_name(f"{target_file.name}.bak_{timestamp}_{suffix}")
        suffix += 1
    return candidate
