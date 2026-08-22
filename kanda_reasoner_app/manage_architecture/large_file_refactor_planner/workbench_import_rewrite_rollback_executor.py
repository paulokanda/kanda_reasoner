# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_rollback_executor.py
"""Exact-token rollback for guarded import rewrite apply."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers

from .models import SCHEMA_VERSION
from .workbench_spectator_proposal_boundary import proposal_only_blocker
from .workbench_spectator_proposal_boundary import proposal_only_warning

__all__ = [
    "IMPORT_REWRITE_ROLLBACK_VISIBILITY_FEATURE_ID",
    "ImportRewriteRollbackResult",
    "execute_import_rewrite_rollback",
    "expected_import_rewrite_rollback_token",
]

IMPORT_REWRITE_ROLLBACK_VISIBILITY_FEATURE_ID = (
    "architecture-review-large-file-refactor-import-rewrite-rollback-visibility-v1"
)
_ROLLBACK_MANIFEST = "IMPORT_REWRITE_ROLLBACK_MANIFEST.json"
_ROLLBACK_EXECUTION = "IMPORT_REWRITE_ROLLBACK_EXECUTION.json"
_POST_ROLLBACK_VALIDATION = "IMPORT_REWRITE_ROLLBACK_VALIDATION.json"
_BACKUP_DIR = "import_rewrite_backups"
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_error_memory",
    "project_freeze_after_update",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class ImportRewriteRollbackResult:
    """Result evidence for exact-token import rewrite rollback."""

    schema_version: str
    feature_id: str
    status: str
    active_project_root: str
    preview_root: str
    exact_token_required: str
    exact_token_present: bool
    exact_token_valid: bool
    rollback_manifest_path: str
    rollback_execution_path: str
    post_rollback_validation_path: str
    restored_files: list[str] = field(default_factory=list)
    retained_files: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validation_status: str = "not_run"

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready result evidence."""
        return asdict(self)


def expected_import_rewrite_rollback_token(*, preview_root: str) -> str:
    """Return the exact rollback token derived from rollback manifest identity."""
    preview_path = Path(preview_root).resolve()
    manifest_path = preview_path / _ROLLBACK_MANIFEST
    if not manifest_path.exists():
        return ""
    data = _read_json(manifest_path)
    digest = _sha256_text(json.dumps(data, sort_keys=True))[:12].upper()
    return f"KANDA-IMPORT-ROLLBACK-{digest}"


def execute_import_rewrite_rollback(
    *,
    active_project_root: str,
    preview_root: str,
    exact_token: str = "",
) -> ImportRewriteRollbackResult:
    """Rollback guarded import rewrite changes after exact token and hash gates pass."""
    project_root = Path(active_project_root).resolve()
    preview_path = Path(preview_root).resolve()
    manifest_path = preview_path / _ROLLBACK_MANIFEST
    execution_path = preview_path / _ROLLBACK_EXECUTION
    validation_path = preview_path / _POST_ROLLBACK_VALIDATION
    token_required = expected_import_rewrite_rollback_token(preview_root=str(preview_path))
    token_present = bool(exact_token.strip())
    token_valid = exact_token.strip() == token_required and bool(token_required)
    blockers = _common_blockers(project_root, preview_path, manifest_path, execution_path, validation_path)
    if not token_valid:
        blockers.append("EXACT_IMPORT_REWRITE_ROLLBACK_TOKEN_REQUIRED")
    entries: list[dict[str, Any]] = []
    if not blockers:
        manifest = _read_json(manifest_path)
        entries = list(manifest.get("entries", []))
        if not entries:
            blockers.append("IMPORT_REWRITE_ROLLBACK_MANIFEST_HAS_NO_ENTRIES")
    restored: list[str] = []
    retained = sorted(
        {str(Path(str(item.get("file", ""))).resolve()) for item in entries}
    )
    if not blockers:
        blockers.append(proposal_only_blocker("import_rewrite_rollback"))
    validation_status = "not_run_proposal_only"
    status = (
        "import_rewrite_rollback_proposal_only"
        if blockers == [proposal_only_blocker("import_rewrite_rollback")]
        else "import_rewrite_rollback_blocked"
    )
    result = ImportRewriteRollbackResult(
        schema_version=SCHEMA_VERSION,
        feature_id=IMPORT_REWRITE_ROLLBACK_VISIBILITY_FEATURE_ID,
        status=status,
        active_project_root=str(project_root),
        preview_root=str(preview_path),
        exact_token_required=token_required,
        exact_token_present=token_present,
        exact_token_valid=token_valid,
        rollback_manifest_path=str(manifest_path),
        rollback_execution_path=str(execution_path),
        post_rollback_validation_path=str(validation_path),
        restored_files=restored,
        retained_files=retained,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(_warnings(retained) + [proposal_only_warning("import_rewrite_rollback")])),
        validation_status=validation_status,
    )
    _write_json(execution_path, result.to_dict())
    return result


def _restore_entries(
    entries: list[dict[str, Any]],
    project_root: Path,
    preview_root: Path,
) -> tuple[list[str], list[str], list[str]]:
    """Compatibility helper: identify recovery targets without writing source."""
    _ = project_root
    _ = preview_root
    retained = sorted(
        {str(Path(str(item.get("file", ""))).resolve()) for item in entries}
    )
    return [], retained, [proposal_only_blocker("import_rewrite_rollback")]

def _entry_blockers(
    target: Path,
    backup: Path,
    project_root: Path,
    preview_root: Path,
    before_hash: str,
) -> list[str]:
    """Return per-entry rollback blockers."""
    blockers: list[str] = []
    if not before_hash:
        blockers.append("IMPORT_REWRITE_BACKUP_HASH_MISSING")
    if not _is_relative_to(target, project_root):
        blockers.append(f"IMPORT_REWRITE_ROLLBACK_TARGET_OUTSIDE_PROJECT:{target}")
    if not target.exists():
        blockers.append(f"IMPORT_REWRITE_ROLLBACK_TARGET_MISSING:{target}")
    if not backup.exists():
        blockers.append(f"IMPORT_REWRITE_ROLLBACK_BACKUP_MISSING:{backup}")
    backup_root = (preview_root / _BACKUP_DIR).resolve()
    if not _is_relative_to(backup, backup_root):
        blockers.append(f"IMPORT_REWRITE_BACKUP_OUTSIDE_BACKUP_ROOT:{backup}")
    for path, label in ((target, "TARGET"), (backup, "BACKUP")):
        lowered = {part.lower() for part in path.parts}
        for forbidden in _PROTECTED_PARTS:
            if forbidden.lower() in lowered:
                blockers.append(f"IMPORT_REWRITE_ROLLBACK_{label}_INSIDE_PROTECTED_{forbidden.upper()}")
    return blockers


def _write_post_rollback_validation(restored_files: list[str], validation_path: Path) -> dict[str, Any]:
    """Write structural validation evidence after import rewrite rollback."""
    blockers: list[str] = []
    checked: list[str] = []
    for filename in restored_files:
        path = Path(filename).resolve()
        try:
            text = path.read_text(encoding="utf-8")
            compile(text, str(path), "exec")
            checked.append(str(path))
        except Exception as exc:  # pragma: no cover - parser exception varies by Python version.
            blockers.append(f"IMPORT_REWRITE_ROLLBACK_PARSE_FAILED:{path}:{exc}")
    report = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": IMPORT_REWRITE_ROLLBACK_VISIBILITY_FEATURE_ID,
        "status": "IMPORT_REWRITE_ROLLBACK_STRUCTURAL_PASS" if not blockers else "IMPORT_REWRITE_ROLLBACK_STRUCTURAL_FAIL",
        "checked_files": checked,
        "behavior_equivalence_claimed": False,
        "blockers": blockers,
        "warnings": ["IMPORT_REWRITE_ROLLBACK_BEHAVIOR_NOT_CLAIMED"],
    }
    _write_json(validation_path, report)
    return report


def _common_blockers(
    project_root: Path,
    preview_root: Path,
    manifest_path: Path,
    execution_path: Path,
    validation_path: Path,
) -> list[str]:
    """Return common no-leak and readiness blockers."""
    blockers: list[str] = []
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    if not manifest_path.exists():
        blockers.append("IMPORT_REWRITE_ROLLBACK_MANIFEST_MISSING")
    for path, label in ((manifest_path, "MANIFEST"), (execution_path, "EXECUTION"), (validation_path, "VALIDATION")):
        if not _is_relative_to(path, preview_root):
            blockers.append(f"IMPORT_REWRITE_ROLLBACK_{label}_OUTSIDE_PREVIEW_ROOT")
        lowered = {part.lower() for part in path.parts}
        for forbidden in _PROTECTED_PARTS:
            if forbidden.lower() in lowered:
                blockers.append(f"IMPORT_REWRITE_ROLLBACK_{label}_INSIDE_PROTECTED_{forbidden.upper()}")
    return blockers


def _allowed_preview_roots_for(project_root: Path) -> list[Path]:
    """Return the selected project's persistent Workbench Preview support root."""
    return [preview_runs_root(project_root)]


def _warnings(retained_files: list[str]) -> list[str]:
    """Return rollback warnings."""
    warnings = [
        "IMPORT_REWRITE_ROLLBACK_EXACT_TOKEN_GATED",
        "IMPORT_REWRITE_ROLLBACK_BEHAVIOR_NOT_CLAIMED",
    ]
    if retained_files:
        warnings.append("IMPORT_REWRITE_ROLLBACK_RETAINED_CHANGED_FILES_FOR_MANUAL_REVIEW")
    return sorted(set(warnings))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    """Write JSON evidence with UTF-8 encoding."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from path."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def _sha256_text(text: str) -> str:
    """Hash text using UTF-8 bytes."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
