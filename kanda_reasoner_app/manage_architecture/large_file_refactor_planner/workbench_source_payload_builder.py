# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_source_payload_builder.py
"""Build source-ready payloads from validated real previews, without applying."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .cst_real_preview_writer import RealPreviewWriteResult
from .workbench_project_support_paths import preview_root_blockers
from .models import RefactorPlan, SCHEMA_VERSION
from .module_size_policy import check_resulting_module_size
from .real_preview_structural_validator import RealPreviewStructuralValidationResult
from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult

__all__ = [
    "SOURCE_PAYLOAD_READINESS_FEATURE_ID",
    "SourceApplyPayloadFile",
    "SourceApplyPayloadReadinessResult",
    "build_and_write_source_apply_payload",
]

SOURCE_PAYLOAD_READINESS_FEATURE_ID = (
    "architecture-review-large-file-refactor-source-payload-readiness-v1"
)
_PAYLOAD_MANIFEST_NAME = "SOURCE_APPLY_PAYLOAD_MANIFEST.json"
_PAYLOAD_FOLDER_NAME = "source_apply_payload"
_PREVIEW_HEADER = "# KANDA PREVIEW ARTIFACT - NOT SOURCE TRUTH"
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class SourceApplyPayloadFile:
    """One source-ready payload file staged under selected project support."""

    payload_path: str
    destination_path: str
    relative_path: str
    content_hash: str
    physical_lines: int
    compile_ok: bool
    ast_parse_ok: bool
    role: str
    symbols: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready file record."""
        return asdict(self)


@dataclass(frozen=True)
class SourceApplyPayloadReadinessResult:
    """Readiness evidence for a governed source-apply payload."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    payload_root: str
    payload_manifest_path: str
    structural_validation_status: str
    behavior_status: str
    preflight_backup_status: str
    source_hash_verified: bool
    source_mutation_enabled: bool = False
    apply_enabled: bool = False
    import_rewrite_enabled: bool = False
    files: list[SourceApplyPayloadFile] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready readiness dictionary."""
        data = asdict(self)
        data["files"] = [item.to_dict() for item in self.files]
        return data


def build_and_write_source_apply_payload(
    *,
    plan: RefactorPlan | None,
    preview_result: RealPreviewWriteResult | None,
    structural_validation: RealPreviewStructuralValidationResult | None,
    preflight_backup: WorkbenchPreflightBackupReadinessResult | None,
    active_project_root: str,
) -> SourceApplyPayloadReadinessResult:
    """Create source-ready payload files under selected project support without applying them."""
    project_root = Path(active_project_root).resolve()
    blockers = _entry_blockers(plan, preview_result, structural_validation, preflight_backup)
    if plan is None or preview_result is None:
        preview_root = Path(preview_result.preview_root).resolve() if preview_result else Path("").resolve()
        return _result(project_root, preview_root, plan, structural_validation, preflight_backup, blockers)
    target = Path(plan.target_file).resolve()
    preview_root = Path(preview_result.preview_root).resolve()
    payload_root = preview_root / _PAYLOAD_FOLDER_NAME
    blockers.extend(_root_blockers(project_root, preview_root, payload_root))
    current_hash = _sha256_file(target) if target.is_file() else ""
    if current_hash != plan.source_content_hash:
        blockers.append("STALE_SOURCE")
    if blockers:
        return _result(project_root, preview_root, plan, structural_validation, preflight_backup, blockers)
    files: list[SourceApplyPayloadFile] = []
    for item in preview_result.files:
        preview_path = (preview_root / item.relative_path).resolve()
        relative = Path(item.relative_path)
        file_blockers = _relative_path_blockers(relative)
        destination = (target.parent / relative).resolve()
        payload_path = (payload_root / relative).resolve()
        file_blockers.extend(_source_destination_blockers(project_root, target.parent, destination))
        file_blockers.extend(_payload_path_blockers(preview_root, payload_root, payload_path))
        text = ""
        if not preview_path.is_file():
            file_blockers.append("PREVIEW_FILE_MISSING")
        else:
            text = preview_path.read_text(encoding="utf-8", errors="replace")
            if _PREVIEW_HEADER not in text:
                file_blockers.append("PREVIEW_WATERMARK_MISSING")
        source_text = "" if file_blockers else _source_ready_text(text)
        file_result = _write_one_payload_file(
            payload_path=payload_path,
            destination=destination,
            relative_path=item.relative_path,
            role=item.role,
            symbols=item.symbols,
            source_text=source_text,
            blockers=file_blockers,
        )
        files.append(file_result)
    blockers.extend(item for file in files for item in file.blockers)
    status = "source_apply_payload_ready" if not blockers else "blocked"
    result = _result(project_root, preview_root, plan, structural_validation, preflight_backup, blockers, files, status)
    _write_manifest(result)
    return result


def _entry_blockers(
    plan: RefactorPlan | None,
    preview_result: RealPreviewWriteResult | None,
    structural_validation: RealPreviewStructuralValidationResult | None,
    preflight_backup: WorkbenchPreflightBackupReadinessResult | None,
) -> list[str]:
    """Return blockers for missing or unready previous stages."""
    blockers: list[str] = []
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
    if preview_result is None or preview_result.status != "real_preview_written":
        blockers.append("REAL_PREVIEW_NOT_READY")
    if structural_validation is None or not structural_validation.status.startswith("passed"):
        blockers.append("STRUCTURAL_PREVIEW_VALIDATION_NOT_PASSED")
    if structural_validation is not None and structural_validation.behavior_status == "BEHAVIOR_VALIDATED_PASS":
        pass
    if preflight_backup is None or preflight_backup.status != "preflight_backup_ready":
        blockers.append("PREFLIGHT_BACKUP_READINESS_NOT_READY")
    if preview_result is not None and preview_result.source_mutation_enabled:
        blockers.append("PREVIEW_RESULT_ENABLED_SOURCE_MUTATION")
    return blockers


def _source_ready_text(preview_text: str) -> str:
    """Remove preview-only markers and return source-ready text."""
    cleaned: list[str] = []
    skip_prefixes = (
        "# KANDA PREVIEW ARTIFACT - NOT SOURCE TRUTH",
        "# Preview facade for ",
        "# Preview helper role:",
        "# Target source:",
        "# Source hash:",
        "# Source mutation is disabled;",
    )
    for line in preview_text.splitlines():
        if any(line.startswith(prefix) for prefix in skip_prefixes):
            continue
        cleaned.append(line)
    text = "\n".join(cleaned).lstrip("\n")
    text = text.replace("Preview facade preserving", "Refactored facade preserving")
    text = text.replace("Preview helper module", "Refactored helper module")
    if text and not text.endswith("\n"):
        text += "\n"
    return text


def _write_one_payload_file(
    *,
    payload_path: Path,
    destination: Path,
    relative_path: str,
    role: str,
    symbols: list[str],
    source_text: str,
    blockers: list[str],
) -> SourceApplyPayloadFile:
    """Write one source-ready payload file if it has no file-level blockers."""
    compile_ok = False
    ast_ok = False
    warnings: list[str] = []
    if not blockers:
        try:
            compile(source_text, str(destination), "exec")
            compile_ok = True
        except SyntaxError:
            blockers.append("SOURCE_PAYLOAD_COMPILE_FAILED")
        try:
            ast.parse(source_text)
            ast_ok = True
        except SyntaxError:
            blockers.append("SOURCE_PAYLOAD_AST_PARSE_FAILED")
        if _PREVIEW_HEADER in source_text:
            blockers.append("PREVIEW_WATERMARK_LEAKED_INTO_SOURCE_PAYLOAD")
        lines = source_text.splitlines()
        size_check = check_resulting_module_size(source_text, relative_path=relative_path)
        blockers.extend(size_check.blockers)
        if not blockers:
            payload_path.parent.mkdir(parents=True, exist_ok=True)
            payload_path.write_bytes(source_text.encode("utf-8"))
    content_hash = hashlib.sha256(source_text.encode("utf-8")).hexdigest() if source_text else ""
    return SourceApplyPayloadFile(
        payload_path=str(payload_path),
        destination_path=str(destination),
        relative_path=relative_path,
        content_hash=content_hash,
        physical_lines=len(source_text.splitlines()),
        compile_ok=compile_ok,
        ast_parse_ok=ast_ok,
        role=role,
        symbols=list(symbols),
        blockers=sorted(set(blockers)),
        warnings=warnings,
    )


def _result(
    project_root: Path,
    preview_root: Path,
    plan: RefactorPlan | None,
    structural_validation: RealPreviewStructuralValidationResult | None,
    preflight_backup: WorkbenchPreflightBackupReadinessResult | None,
    blockers: list[str],
    files: list[SourceApplyPayloadFile] | None = None,
    status: str | None = None,
) -> SourceApplyPayloadReadinessResult:
    """Build one stable readiness result."""
    target = str(plan.target_file) if plan else ""
    source_hash = str(plan.source_content_hash) if plan else ""
    payload_root = preview_root / _PAYLOAD_FOLDER_NAME
    current_hash = _sha256_file(Path(target)) if target else ""
    return SourceApplyPayloadReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id=SOURCE_PAYLOAD_READINESS_FEATURE_ID,
        status=status or "blocked",
        target_file=target,
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_root=str(payload_root),
        payload_manifest_path=str(preview_root / _PAYLOAD_MANIFEST_NAME),
        structural_validation_status=(
            structural_validation.structural_status if structural_validation else "missing"
        ),
        behavior_status=(structural_validation.behavior_status if structural_validation else "missing"),
        preflight_backup_status=(preflight_backup.status if preflight_backup else "missing"),
        source_hash_verified=bool(source_hash and current_hash == source_hash),
        source_mutation_enabled=False,
        apply_enabled=False,
        import_rewrite_enabled=False,
        files=files or [],
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
    )


def _write_manifest(result: SourceApplyPayloadReadinessResult) -> None:
    """Write the payload manifest under preview root only."""
    path = Path(result.payload_manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    if not _is_relative_to(path, preview_root):
        raise RuntimeError("Source payload manifest path is outside preview root.")
    if _protected_parts(path):
        raise RuntimeError("Source payload manifest path is inside a protected root.")
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(path.read_text(encoding="utf-8"))
    if saved.get("source_mutation_enabled") is not False:
        raise RuntimeError("Source payload readiness must not enable source mutation.")
    if saved.get("apply_enabled") is not False:
        raise RuntimeError("Source payload readiness must not enable apply.")


def _root_blockers(project_root: Path, preview_root: Path, payload_root: Path) -> list[str]:
    """Return root-level containment blockers."""
    blockers: list[str] = []
    blockers.extend(preview_root_blockers(project_root, preview_root))
    if not _is_relative_to(payload_root, preview_root):
        blockers.append("PAYLOAD_ROOT_OUTSIDE_PREVIEW_ROOT")
    if _protected_parts(payload_root):
        blockers.append("PAYLOAD_ROOT_INSIDE_PROTECTED_ROOT")
    return blockers


def _relative_path_blockers(relative: Path) -> list[str]:
    """Reject absolute, traversal, or nested payload paths for v1."""
    parts = relative.parts
    blockers: list[str] = []
    if relative.is_absolute() or ".." in parts:
        blockers.append("UNSAFE_RELATIVE_PATH")
    if len(parts) != 1:
        blockers.append("NESTED_SOURCE_PAYLOAD_PATH_NOT_SUPPORTED_IN_V1")
    if relative.suffix != ".py":
        blockers.append("SOURCE_PAYLOAD_FILE_NOT_PYTHON")
    return blockers


def _source_destination_blockers(project_root: Path, target_dir: Path, destination: Path) -> list[str]:
    """Validate future source destination without writing it."""
    blockers: list[str] = []
    if not _is_relative_to(destination, project_root):
        blockers.append("DESTINATION_OUTSIDE_PROJECT_ROOT")
    if destination.parent.resolve() != target_dir.resolve():
        blockers.append("DESTINATION_NOT_IN_TARGET_MODULE_DIRECTORY")
    if _protected_parts(destination):
        blockers.append("DESTINATION_INSIDE_PROTECTED_ROOT")
    return blockers


def _payload_path_blockers(preview_root: Path, payload_root: Path, path: Path) -> list[str]:
    """Validate project-support source payload path."""
    blockers: list[str] = []
    if not _is_relative_to(path, payload_root):
        blockers.append("PAYLOAD_FILE_OUTSIDE_PAYLOAD_ROOT")
    if not _is_relative_to(path, preview_root):
        blockers.append("PAYLOAD_FILE_OUTSIDE_PREVIEW_ROOT")
    if _protected_parts(path):
        blockers.append("PAYLOAD_FILE_INSIDE_PROTECTED_ROOT")
    return blockers


def _checked_rules() -> list[str]:
    """Return stable checked rule labels."""
    return [
        "planner_plan_required",
        "real_preview_required",
        "structural_validation_required",
        "preflight_backup_readiness_required",
        "source_hash_fresh",
        "preview_watermark_required_on_input_preview",
        "preview_watermark_removed_from_source_payload",
        "payload_staged_under_daily_work_preview_root",
        "source_destination_same_directory_as_target",
        "source_mutation_remains_disabled",
        "apply_remains_disabled",
        "import_rewrite_remains_disabled",
    ]


def _warnings() -> list[str]:
    """Return stable warning labels for this train."""
    return [
        "SOURCE_PAYLOAD_READY_DOES_NOT_APPLY_SOURCE",
        "SOURCE_PAYLOAD_IS_DERIVED_FROM_VALIDATED_PREVIEW_NOT_LOOSE_ARTIFACT",
        "EXACT_TOKEN_GUARDED_APPLY_NOT_ENABLED_IN_THIS_TRAIN",
        "IMPORT_REWRITE_APPLICATION_NOT_ENABLED",
        "BEHAVIOR_EQUIVALENCE_NOT_CLAIMED",
    ]


def _sha256_file(path: Path) -> str:
    """Return sha256 hash for an existing file or empty string."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return True when path is inside root after resolution."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _protected_parts(path: Path) -> list[str]:
    """Return protected path parts present in path."""
    return [part for part in path.resolve().parts if part in _PROTECTED_PARTS]
