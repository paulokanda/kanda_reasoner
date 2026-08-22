# project-path: kanda_reasoner_app/source_hygiene/bom_fixer.py
"""Safe UTF-8 BOM removal with backup, validation, and rollback."""

from __future__ import annotations

import hashlib
import json
import py_compile
from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.project_source_proposal_boundary import (
    PROJECT_REPAIR_PROPOSAL_ONLY_MARKER,
)

from .bom_scanner import UTF8_BOM_BYTES, iter_bom_scan_files, scan_file_for_bom
from .schemas import SourceHygieneFinding, SourceHygieneReport, utc_timestamp

PYTHON_SUFFIXES = frozenset({".py", ".pyi", ".pyw"})
JSON_SUFFIXES = frozenset({".json"})
JSONL_SUFFIXES = frozenset({".jsonl"})

__all__ = [
    "BomFixResult",
    "JSON_SUFFIXES",
    "JSONL_SUFFIXES",
    "PYTHON_SUFFIXES",
    "fix_project_utf8_bom",
    "remove_utf8_bom_from_file",
    "validate_text_file_after_bom_fix",
]


@dataclass(frozen=True)
class BomFixResult:
    """Result of one UTF-8 BOM fix attempt."""

    path: str
    changed: bool
    success: bool
    backup_path: str = ""
    message: str = ""
    proposal_only: bool = False
    proposed_sha256: str = ""

    def to_finding(self) -> SourceHygieneFinding:
        """Convert the fix result into a source hygiene finding."""
        if self.proposal_only and self.success:
            code = "UTF8_BOM_PROPOSAL_ONLY"
            severity = "info"
            action = "Review the proposed BOM-free payload outside Project source."
        elif self.changed and self.success:
            code = "UTF8_BOM_REMOVED"
            severity = "info"
            action = "No further action required."
        elif not self.changed and self.success:
            code = "UTF8_BOM_NOT_PRESENT"
            severity = "info"
            action = "No file change was needed."
        else:
            code = "UTF8_BOM_FIX_FAILED"
            severity = "error"
            action = "Inspect the file and backup before retrying."
        return SourceHygieneFinding(
            code=code,
            path=self.path,
            message=self.message,
            severity=severity,
            confidence="high",
            evidence={
                "backup_path": self.backup_path,
                "changed": self.changed,
                "proposal_only": self.proposal_only,
                "proposed_sha256": self.proposed_sha256,
            },
            suggested_action=action,
        )


def remove_utf8_bom_from_file(
    path: str | Path,
    project_root: str | Path | None = None,
    backup_root: str | Path | None = None,
    validate: bool = True,
) -> BomFixResult:
    """Return a BOM-removal proposal without mutating Project source."""
    del backup_root
    file_path = Path(path).resolve()
    root = (
        Path(project_root).resolve()
        if project_root is not None
        else file_path.parent
    )
    display_path = _display_path(file_path, root)
    try:
        payload = file_path.read_bytes()
    except OSError as exc:
        return BomFixResult(
            path=display_path,
            changed=False,
            success=False,
            message="Could not read file before BOM proposal: " + str(exc),
        )
    if not payload.startswith(UTF8_BOM_BYTES):
        return BomFixResult(
            path=display_path,
            changed=False,
            success=True,
            message="File does not start with a UTF-8 BOM.",
        )
    proposed = payload[len(UTF8_BOM_BYTES) :]
    if validate:
        _validate_proposed_text_after_bom_fix(file_path, proposed)
    return BomFixResult(
        path=display_path,
        changed=False,
        success=True,
        message=PROJECT_REPAIR_PROPOSAL_ONLY_MARKER + ":UTF8_BOM",
        proposal_only=True,
        proposed_sha256=hashlib.sha256(proposed).hexdigest(),
    )


def _validate_proposed_text_after_bom_fix(
    file_path: Path,
    proposed: bytes,
) -> None:
    """Validate proposed BOM-free bytes without writing them to source."""
    text = proposed.decode("utf-8")
    suffix = file_path.suffix.lower()
    if suffix in PYTHON_SUFFIXES:
        compile(text, str(file_path), "exec")
    elif suffix in JSON_SUFFIXES:
        json.loads(text)
    elif suffix in JSONL_SUFFIXES:
        for line in text.splitlines():
            if line.strip():
                json.loads(line)


def fix_project_utf8_bom(
    project_root: str | Path,
    paths: list[str | Path] | tuple[str | Path, ...] | None = None,
    backup_root: str | Path | None = None,
    validate: bool = True,
) -> SourceHygieneReport:
    """Remove UTF-8 BOM from selected files and return a structured report."""
    root = Path(project_root).resolve()
    if paths is None:
        candidate_files = iter_bom_scan_files(root)
    else:
        candidate_files = [Path(path) for path in paths]

    results: list[BomFixResult] = []
    for file_path in candidate_files:
        findings = scan_file_for_bom(file_path, project_root=root, check_utf8=True)
        if not any(finding.code == "UTF8_BOM_DETECTED" for finding in findings):
            continue
        results.append(
            remove_utf8_bom_from_file(
                file_path,
                project_root=root,
                backup_root=backup_root,
                validate=validate,
            )
        )

    changed_count = sum(1 for result in results if result.changed and result.success)
    proposal_count = sum(1 for result in results if result.proposal_only)
    failed_count = sum(1 for result in results if not result.success)
    summary = (
        "BOM proposal scan completed. "
        + "files_with_bom="
        + str(len(results))
        + "; changed="
        + str(changed_count)
        + "; proposal_only="
        + str(proposal_count)
        + "; failed="
        + str(failed_count)
        + "."
    )
    return SourceHygieneReport(
        project_root=str(root),
        report_type="bom_fix",
        summary=summary,
        findings=tuple(result.to_finding() for result in results),
        input_sources=("project_root",),
    )


def validate_text_file_after_bom_fix(path: str | Path) -> None:
    """Validate a text file after BOM removal."""
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    suffix = file_path.suffix.lower()
    if suffix in PYTHON_SUFFIXES:
        py_compile.compile(str(file_path), doraise=True)
    elif suffix in JSON_SUFFIXES:
        json.loads(text)
    elif suffix in JSONL_SUFFIXES:
        for line in text.splitlines():
            if line.strip():
                json.loads(line)


def _make_backup_path(
    file_path: Path,
    project_root: Path,
    backup_root: str | Path | None,
) -> Path:
    """Support make backup path behavior.
    
    Parameters
    ----------
    file_path : Path
        The file path.
    project_root : Path
        The project root path.
    backup_root : str | Path | None
        The backup root value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    if backup_root is None:
        stamp = utc_timestamp().replace(":", "").replace("-", "")
        backup_base = project_root / "workbench" / "source_hygiene_backups" / stamp
    else:
        backup_base = Path(backup_root).resolve()
    try:
        relative = file_path.relative_to(project_root)
    except ValueError:
        relative = Path(file_path.name)
    return backup_base / relative.with_name(relative.name + ".bak")


def _display_path(path: Path, root: Path | None) -> str:
    """Support display path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path | None
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    if root is None:
        return str(path)
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)
