# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/import_rewrite_application_gate.py
"""Gate-only evidence for future import rewrite application."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import FEATURE_ID, SCHEMA_VERSION, ImportMigrationPreview
from .payload_apply_gate import PayloadApplyGateResult

__all__ = [
    "IMPORT_REWRITE_CONFIRMATION_TOKEN",
    "ImportRewriteApplicationGateResult",
    "build_import_rewrite_application_gate",
    "write_import_rewrite_application_gate_manifest",
]

IMPORT_REWRITE_CONFIRMATION_TOKEN = "CONFIRM_REVIEWED_IMPORT_REWRITE_PREVIEW"
_IMPORT_REWRITE_GATE_MANIFEST_NAME = "IMPORT_REWRITE_APPLICATION_GATE.json"


@dataclass(frozen=True)
class ImportRewriteApplicationGateResult:
    """Review-only gate evidence for a future import rewrite train."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    apply_gate_manifest_path: str
    import_rewrite_gate_manifest_path: str
    importer_count: int
    confirmation_token_required: str
    human_confirmation_present: bool
    human_confirmation_required: bool = True
    rewrite_enabled: bool = False
    apply_enabled: bool = False
    source_hash_verified: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready import rewrite gate dictionary."""
        return asdict(self)


def build_import_rewrite_application_gate(
    import_preview: ImportMigrationPreview,
    apply_gate: PayloadApplyGateResult,
    *,
    active_project_root: str,
    human_confirmation: str = "",
) -> ImportRewriteApplicationGateResult:
    """Build review-only evidence for future import rewrite application."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(apply_gate.preview_root).resolve()
    target = Path(import_preview.target_file).resolve()
    gate_manifest = preview_root / _IMPORT_REWRITE_GATE_MANIFEST_NAME
    confirmation_present = human_confirmation.strip() == IMPORT_REWRITE_CONFIRMATION_TOKEN
    blockers = _gate_blockers(import_preview, apply_gate, project_root, preview_root, target)
    warnings = [
        "IMPORT_REWRITE_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "IMPORT_REWRITE_REMAINS_REVIEW_ONLY",
        "SELECTED_PROJECT_SOURCE_MUST_REMAIN_UNCHANGED",
    ]
    if confirmation_present:
        warnings.append("HUMAN_CONFIRMATION_RECORDED_FOR_FUTURE_IMPORT_REWRITE_TRAIN_ONLY")
    source_hash_verified = "SELECTED_SOURCE_HASH_CHANGED" not in blockers and "TARGET_FILE_MISSING" not in blockers
    status = "import_rewrite_gate_ready" if not blockers else "blocked"
    return ImportRewriteApplicationGateResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=import_preview.source_content_hash,
        preview_root=str(preview_root),
        apply_gate_manifest_path=apply_gate.apply_gate_manifest_path,
        import_rewrite_gate_manifest_path=str(gate_manifest),
        importer_count=len(import_preview.records),
        confirmation_token_required=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        human_confirmation_present=confirmation_present,
        rewrite_enabled=False,
        apply_enabled=False,
        source_hash_verified=source_hash_verified and status == "import_rewrite_gate_ready",
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_import_rewrite_application_gate_manifest(gate: ImportRewriteApplicationGateResult) -> Path:
    """Write import rewrite gate evidence to the governed project-support Preview root."""
    manifest = Path(gate.import_rewrite_gate_manifest_path).resolve()
    preview_root = Path(gate.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Import rewrite gate manifest path is outside preview root.")
    lowered = {part.lower() for part in manifest.parts}
    forbidden = {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"}
    if lowered & forbidden:
        raise RuntimeError("Import rewrite gate manifest path is inside a protected support root.")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(gate.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("rewrite_enabled") is not False or saved.get("apply_enabled") is not False:
        raise RuntimeError("Import rewrite gate manifest must keep rewrite/apply disabled.")
    return manifest


def _gate_blockers(
    import_preview: ImportMigrationPreview,
    apply_gate: PayloadApplyGateResult,
    project_root: Path,
    preview_root: Path,
    target: Path,
) -> list[str]:
    """Return blockers that prevent future import rewrite readiness."""
    blockers: list[str] = list(import_preview.blockers) + list(apply_gate.blockers)
    if apply_gate.status != "apply_gate_ready":
        blockers.append("PAYLOAD_APPLY_GATE_NOT_READY")
    if apply_gate.apply_enabled is not False:
        blockers.append("PAYLOAD_APPLY_GATE_ENABLED_UNEXPECTEDLY")
    if import_preview.status not in {"preview_only", "ready"}:
        blockers.append("IMPORT_MIGRATION_PREVIEW_NOT_READY")
    if import_preview.rewrite_enabled is not False:
        blockers.append("IMPORT_REWRITE_ALREADY_ENABLED")
    blockers.extend(_preview_root_blockers(project_root, preview_root))
    blockers.extend(_apply_gate_manifest_blockers(project_root, preview_root, Path(apply_gate.apply_gate_manifest_path)))
    if not target.exists():
        blockers.append("TARGET_FILE_MISSING")
    else:
        current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if current_hash != import_preview.source_content_hash:
            blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    for record in import_preview.records:
        if record.status != "preview_only":
            blockers.append("IMPORT_RECORD_NOT_PREVIEW_ONLY")
        if record.action != "review_only_no_rewrite":
            blockers.append("IMPORT_RECORD_ACTION_NOT_REVIEW_ONLY")
        if record.blockers:
            blockers.append("IMPORT_RECORD_HAS_BLOCKERS")
    return blockers


def _checked_rules() -> list[str]:
    """Return stable rule labels checked by this gate."""
    return [
        "payload_apply_gate_ready",
        "payload_apply_gate_apply_enabled_false",
        "import_migration_preview_status_preview_only",
        "import_migration_rewrite_enabled_false",
        "import_records_review_only",
        "selected_source_hash_unchanged",
        "preview_root_inside_project_support_only",
        "manifest_outside_project_source",
        "rewrite_enabled_false_in_this_train",
        "apply_enabled_false_in_this_train",
    ]


def _apply_gate_manifest_blockers(project_root: Path, preview_root: Path, path: Path) -> list[str]:
    """Return blockers for an unsafe apply gate manifest path."""
    blockers: list[str] = []
    resolved = path.resolve()
    if _is_relative_to(resolved, project_root):
        blockers.append("APPLY_GATE_MANIFEST_INSIDE_PROJECT_SOURCE")
    if not _is_relative_to(resolved, preview_root):
        blockers.append("APPLY_GATE_MANIFEST_OUTSIDE_PREVIEW_ROOT")
    if not resolved.exists():
        blockers.append("APPLY_GATE_MANIFEST_MISSING")
    lowered = {part.lower() for part in resolved.parts}
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append("APPLY_GATE_MANIFEST_INSIDE_PROTECTED_" + forbidden.upper())
    return blockers


def _preview_root_blockers(project_root: Path, preview_root: Path) -> list[str]:
    """Return blockers for Preview roots outside selected project support."""
    return project_preview_root_blockers(project_root, preview_root)


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
