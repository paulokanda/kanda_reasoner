# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/post_apply_validation.py
"""Post-apply validation and hash evidence checks for guarded source apply."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import zipfile

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import FEATURE_ID, SCHEMA_VERSION
from .module_size_policy import check_resulting_module_size

__all__ = [
    "POST_APPLY_VALIDATION_TOKEN",
    "PostApplyValidationResult",
    "build_post_apply_validation",
    "write_post_apply_validation_manifest",
]

POST_APPLY_VALIDATION_TOKEN = "CONFIRM_VALIDATE_POST_APPLY_STATE"
_POST_APPLY_MANIFEST_NAME = "POST_APPLY_VALIDATION_HASH_EVIDENCE.json"
_EXECUTION_MANIFEST_NAME = "GUARDED_SOURCE_APPLY_EXECUTION.json"
_PAYLOAD_MANIFEST_NAME = "PROJECT_PATCH_PAYLOAD_MANIFEST.json"


@dataclass(frozen=True)
class PostApplyValidationResult:
    """Validation result for the state produced by guarded source apply."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    preview_root: str
    execution_manifest_path: str
    post_apply_manifest_path: str
    payload_zip_path: str
    backup_snapshot_path: str
    source_content_hash_before: str
    source_content_hash_after_expected: str
    source_content_hash_after_actual: str
    confirmation_token_required: str
    validation_confirmation_present: bool
    validation_confirmation_valid: bool
    backup_snapshot_verified_unchanged: bool = False
    source_hash_transition_verified: bool = False
    written_files_verified: bool = False
    payload_zip_verified: bool = False
    loose_preview_artifacts_used_as_source_of_truth: bool = False
    import_rewrite_applied: bool = False
    protected_roots_touched: bool = False
    project_reference_touched: bool = False
    module_size_gate_passed: bool = False
    syntax_gate_passed: bool = False
    checked_files: list[str] = field(default_factory=list)
    written_files: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready post-apply validation dictionary."""
        return asdict(self)


def build_post_apply_validation(
    execution_manifest_path: str,
    *,
    active_project_root: str,
    validation_confirmation: str = "",
) -> PostApplyValidationResult:
    """Validate post-apply state without writing selected project source."""
    project_root = Path(active_project_root).resolve()
    execution_manifest = Path(execution_manifest_path).resolve()
    execution = _read_json_file(execution_manifest)
    preview_root = Path(str(execution.get("preview_root", execution_manifest.parent))).resolve()
    target = Path(str(execution.get("target_file", ""))).resolve()
    payload_zip = Path(str(execution.get("payload_zip_path", ""))).resolve()
    backup = Path(str(execution.get("backup_snapshot_path", ""))).resolve()
    written = [str(item) for item in execution.get("written_files", []) if str(item)]
    expected_after = str(execution.get("source_content_hash_after", ""))
    before_hash = str(execution.get("source_content_hash_before", ""))
    actual_after = _sha256_file(target) if target.is_file() else ""
    token_valid = validation_confirmation.strip() == POST_APPLY_VALIDATION_TOKEN
    blockers = _validation_blockers(
        project_root,
        preview_root,
        execution_manifest,
        execution,
        target,
        payload_zip,
        backup,
        written,
        before_hash,
        expected_after,
        actual_after,
        token_valid,
    )
    checked_files = _existing_python_files([target, *[Path(item) for item in written]])
    status = "post_apply_validation_passed" if not blockers else "blocked"
    return PostApplyValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        preview_root=str(preview_root),
        execution_manifest_path=str(execution_manifest),
        post_apply_manifest_path=str(preview_root / _POST_APPLY_MANIFEST_NAME),
        payload_zip_path=str(payload_zip),
        backup_snapshot_path=str(backup),
        source_content_hash_before=before_hash,
        source_content_hash_after_expected=expected_after,
        source_content_hash_after_actual=actual_after,
        confirmation_token_required=POST_APPLY_VALIDATION_TOKEN,
        validation_confirmation_present=bool(validation_confirmation.strip()),
        validation_confirmation_valid=token_valid,
        backup_snapshot_verified_unchanged="BACKUP_SNAPSHOT_HASH_CHANGED" not in blockers and "BACKUP_SNAPSHOT_MISSING" not in blockers,
        source_hash_transition_verified="SOURCE_HASH_TRANSITION_INVALID" not in blockers and "TARGET_AFTER_HASH_MISMATCH" not in blockers,
        written_files_verified="WRITTEN_FILE_LIST_INVALID" not in blockers and "WRITTEN_FILE_MISSING" not in blockers,
        payload_zip_verified="PAYLOAD_ZIP_MISSING" not in blockers and "PAYLOAD_MANIFEST_INVALID" not in blockers,
        loose_preview_artifacts_used_as_source_of_truth=False,
        import_rewrite_applied=bool(execution.get("rewrite_enabled")),
        protected_roots_touched=any("PROTECTED" in item for item in blockers),
        project_reference_touched=any("PROJECT_REFERENCE" in item for item in blockers),
        module_size_gate_passed="MODULE_SIZE_GATE_FAILED" not in blockers,
        syntax_gate_passed="PYTHON_SYNTAX_INVALID" not in blockers,
        checked_files=[str(path) for path in checked_files],
        written_files=sorted(written),
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
    )


def write_post_apply_validation_manifest(result: PostApplyValidationResult) -> Path:
    """Write post-apply validation evidence under the governed preview root."""
    manifest = Path(result.post_apply_manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Post-apply validation manifest path is outside preview root.")
    _raise_if_protected(manifest, "post-apply validation manifest")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("loose_preview_artifacts_used_as_source_of_truth") is not False:
        raise RuntimeError("Post-apply validation must not use loose preview artifacts as source of truth.")
    if saved.get("status") == "post_apply_validation_passed" and saved.get("blockers"):
        raise RuntimeError("Passed post-apply validation cannot include blockers.")
    return manifest


def _validation_blockers(
    project_root: Path,
    preview_root: Path,
    execution_manifest: Path,
    execution: dict[str, object],
    target: Path,
    payload_zip: Path,
    backup: Path,
    written: list[str],
    before_hash: str,
    expected_after: str,
    actual_after: str,
    token_valid: bool,
) -> list[str]:
    """Return blockers for post-apply validation."""
    blockers: list[str] = []
    if not token_valid:
        blockers.append("POST_APPLY_VALIDATION_TOKEN_MISSING_OR_INVALID")
    if execution.get("status") != "guarded_source_apply_ready":
        blockers.append("GUARDED_EXECUTION_NOT_READY")
    if execution.get("apply_enabled") is not True or execution.get("source_mutation_enabled") is not True:
        blockers.append("GUARDED_EXECUTION_DID_NOT_ENABLE_SOURCE_MUTATION")
    if execution.get("rewrite_enabled") is not False:
        blockers.append("IMPORT_REWRITE_APPLIED_OR_ENABLED")
    blockers.extend(_artifact_path_blockers(project_root, preview_root, execution_manifest, "EXECUTION_MANIFEST"))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, payload_zip, "PAYLOAD_ZIP"))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, backup, "BACKUP_SNAPSHOT"))
    blockers.extend(_target_path_blockers(project_root, target, "TARGET"))
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    if not execution_manifest.is_file():
        blockers.append("EXECUTION_MANIFEST_MISSING")
    if not payload_zip.is_file():
        blockers.append("PAYLOAD_ZIP_MISSING")
    if not backup.is_file():
        blockers.append("BACKUP_SNAPSHOT_MISSING")
    elif before_hash and _sha256_file(backup) != before_hash:
        blockers.append("BACKUP_SNAPSHOT_HASH_CHANGED")
    if not target.is_file():
        blockers.append("TARGET_FILE_MISSING")
    if not before_hash or not expected_after or before_hash == expected_after:
        blockers.append("SOURCE_HASH_TRANSITION_INVALID")
    if expected_after and actual_after != expected_after:
        blockers.append("TARGET_AFTER_HASH_MISMATCH")
    blockers.extend(_payload_blockers(payload_zip, before_hash))
    blockers.extend(_written_file_blockers(project_root, preview_root, payload_zip, target.parent, written))
    blockers.extend(_python_integrity_blockers([target, *[Path(item) for item in written]]))
    return blockers


def _payload_blockers(payload_zip: Path, before_hash: str) -> list[str]:
    """Return blockers for the governed payload ZIP used by the executor."""
    payload = _read_payload_manifest(payload_zip)
    if payload is None:
        return ["PAYLOAD_MANIFEST_INVALID"]
    blockers: list[str] = []
    if payload.get("requires_human_review") is not True:
        blockers.append("PAYLOAD_MANIFEST_REQUIRES_HUMAN_REVIEW_NOT_TRUE")
    if payload.get("apply_to_source") is not False:
        blockers.append("PAYLOAD_MANIFEST_APPLY_TO_SOURCE_NOT_FALSE")
    if bool(payload.get("import_rewrite_enabled")):
        blockers.append("PAYLOAD_MANIFEST_IMPORT_REWRITE_ENABLED")
    if payload.get("source_content_hash") != before_hash:
        blockers.append("PAYLOAD_MANIFEST_SOURCE_HASH_MISMATCH")
    return blockers


def _written_file_blockers(project_root: Path, preview_root: Path, payload_zip: Path, target_root: Path, written: list[str]) -> list[str]:
    """Return blockers for written file evidence and payload byte matching."""
    blockers: list[str] = []
    if not written:
        return ["WRITTEN_FILE_LIST_INVALID"]
    try:
        with zipfile.ZipFile(payload_zip, "r") as archive:
            names = set(archive.namelist())
            for item in written:
                path = Path(item).resolve()
                blockers.extend(_target_path_blockers(project_root, path, "WRITTEN_FILE"))
                if _is_relative_to(path, preview_root):
                    blockers.append("WRITTEN_FILE_INSIDE_PREVIEW_ROOT")
                if not path.is_file():
                    blockers.append("WRITTEN_FILE_MISSING")
                    continue
                relative = path.relative_to(target_root.resolve()).as_posix()
                if relative not in names:
                    blockers.append("WRITTEN_FILE_NOT_FOUND_IN_PAYLOAD_ZIP")
                    continue
                if path.read_bytes() != archive.read(relative):
                    blockers.append("WRITTEN_FILE_CONTENT_MISMATCH_WITH_PAYLOAD_ZIP")
    except (OSError, ValueError, zipfile.BadZipFile, KeyError):
        blockers.append("WRITTEN_FILE_PAYLOAD_COMPARISON_FAILED")
    return blockers


def _python_integrity_blockers(paths: list[Path]) -> list[str]:
    """Return syntax and module-size blockers for written Python files."""
    blockers: list[str] = []
    seen: set[Path] = set()
    for path in paths:
        candidate = path.resolve()
        if candidate in seen or candidate.suffix != ".py" or not candidate.is_file():
            continue
        seen.add(candidate)
        text = candidate.read_text(encoding="utf-8")
        if check_resulting_module_size(text, relative_path=candidate.name).blockers:
            blockers.append("MODULE_SIZE_GATE_FAILED")
        try:
            ast.parse(text, filename=str(candidate))
        except SyntaxError:
            blockers.append("PYTHON_SYNTAX_INVALID")
    return blockers


def _artifact_path_blockers(project_root: Path, preview_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for support artifacts that must stay under preview root."""
    blockers: list[str] = []
    if not _is_relative_to(path, preview_root):
        blockers.append(label + "_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    blockers.extend(_protected_root_blockers(path, label))
    return blockers


def _target_path_blockers(project_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for selected project source paths."""
    blockers: list[str] = []
    if not _is_relative_to(path, project_root):
        blockers.append(label + "_OUTSIDE_PROJECT_SOURCE")
    blockers.extend(_protected_root_blockers(path, label))
    return blockers


def _protected_root_blockers(path: Path, label: str) -> list[str]:
    """Return blockers for protected support and reference roots."""
    lowered = {part.lower() for part in path.parts}
    blockers: list[str] = []
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append(label + "_INSIDE_PROTECTED_" + forbidden.upper())
    if ".project_reference" in lowered or "_project_reference" in lowered:
        blockers.append(label + "_INSIDE_PROJECT_REFERENCE")
    return blockers


def _read_payload_manifest(payload_zip: Path) -> dict[str, object] | None:
    """Read the payload manifest from the governed project patch payload ZIP."""
    try:
        with zipfile.ZipFile(payload_zip, "r") as archive:
            raw = archive.read(_PAYLOAD_MANIFEST_NAME).decode("utf-8")
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def _read_json_file(path: Path) -> dict[str, object]:
    """Return a JSON object from path, or an empty mapping when invalid."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for a file, or an empty string when missing."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""


def _existing_python_files(paths: list[Path]) -> list[Path]:
    """Return unique existing Python files from paths."""
    result: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        candidate = path.resolve()
        if candidate.suffix == ".py" and candidate.is_file() and candidate not in seen:
            result.append(candidate)
            seen.add(candidate)
    return result


def _raise_if_protected(path: Path, label: str) -> None:
    """Raise if a support artifact path reaches protected support or reference roots."""
    blockers = _protected_root_blockers(path, label)
    if blockers:
        raise RuntimeError(label + " path is inside a protected or reference root.")


def _checked_rules() -> list[str]:
    """Return stable rule labels checked by this validator."""
    return [
        "post_apply_validation_token_exact_match",
        "guarded_execution_manifest_ready",
        "source_hash_transition_before_to_after_verified",
        "backup_snapshot_unchanged_after_apply",
        "payload_zip_used_as_source_of_written_bytes",
        "loose_preview_artifacts_not_used_as_source_of_truth",
        "written_files_inside_selected_project_source_only",
        "project_reference_roots_excluded",
        "protected_support_roots_not_touched",
        "module_size_gate_max_500_lines",
        "python_syntax_gate_for_written_files",
        "import_rewrite_not_applied_in_this_train",
    ]


def _warnings() -> list[str]:
    """Return stable warning labels for operator review."""
    return [
        "POST_APPLY_VALIDATION_DOES_NOT_MUTATE_SOURCE",
        "ROLLBACK_RECOVERY_IS_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "IMPORT_REWRITE_APPLICATION_REMAINS_DISABLED",
    ]


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
