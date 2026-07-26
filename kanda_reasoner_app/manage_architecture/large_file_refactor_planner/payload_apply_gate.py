# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/payload_apply_gate.py
"""Human-confirmation gate for governed project patch payloads."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import zipfile

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import FEATURE_ID, SCHEMA_VERSION, ProjectPatchPayloadResult

__all__ = [
    "PayloadApplyGateResult",
    "build_payload_apply_gate",
    "write_payload_apply_gate_manifest",
]

_APPLY_GATE_MANIFEST_NAME = "PAYLOAD_APPLY_GATE.json"
_CONFIRMATION_TOKEN = "CONFIRM_REVIEWED_PROJECT_PATCH_PAYLOAD"


@dataclass(frozen=True)
class PayloadApplyGateResult:
    """Review-only gate evidence for future payload apply operations."""

    schema_version: str
    feature_id: str
    status: str
    payload_zip_path: str
    payload_manifest_path: str
    preview_root: str
    apply_gate_manifest_path: str
    confirmation_token_required: str
    human_confirmation_present: bool
    human_confirmation_required: bool = True
    apply_enabled: bool = False
    source_hash_verified: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready apply gate dictionary."""
        return asdict(self)


def build_payload_apply_gate(
    payload: ProjectPatchPayloadResult,
    *,
    active_project_root: str,
    human_confirmation: str = "",
) -> PayloadApplyGateResult:
    """Build review-only apply gate evidence without applying any payload."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(payload.preview_root).resolve()
    payload_zip = Path(payload.payload_zip_path).resolve()
    payload_manifest = Path(payload.payload_manifest_path).resolve()
    apply_manifest = preview_root / _APPLY_GATE_MANIFEST_NAME
    checked = _checked_rules()
    blockers = _payload_apply_blockers(payload, project_root, preview_root, payload_zip, payload_manifest)
    confirmation_present = human_confirmation.strip() == _CONFIRMATION_TOKEN
    warnings = [
        "PAYLOAD_APPLY_IS_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "SELECTED_PROJECT_SOURCE_MUST_REMAIN_UNCHANGED",
    ]
    if confirmation_present:
        warnings.append("HUMAN_CONFIRMATION_RECORDED_FOR_FUTURE_APPLY_TRAIN_ONLY")
    status = "apply_gate_ready" if not blockers else "blocked"
    source_hash_verified = "SELECTED_SOURCE_HASH_CHANGED" not in blockers and "PAYLOAD_MANIFEST_UNREADABLE" not in blockers
    return PayloadApplyGateResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        payload_zip_path=str(payload_zip),
        payload_manifest_path=str(payload_manifest),
        preview_root=str(preview_root),
        apply_gate_manifest_path=str(apply_manifest),
        confirmation_token_required=_CONFIRMATION_TOKEN,
        human_confirmation_present=confirmation_present,
        apply_enabled=False,
        source_hash_verified=source_hash_verified and status == "apply_gate_ready",
        checked_rules=checked,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_payload_apply_gate_manifest(gate: PayloadApplyGateResult) -> Path:
    """Write apply gate evidence to the project-support Preview root only."""
    manifest = Path(gate.apply_gate_manifest_path).resolve()
    preview_root = Path(gate.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Apply gate manifest path is outside preview root.")
    lowered = {part.lower() for part in manifest.parts}
    forbidden = {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"}
    if lowered & forbidden:
        raise RuntimeError("Apply gate manifest path is inside a protected support root.")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(gate.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("apply_enabled") is not False:
        raise RuntimeError("Apply gate manifest must keep apply_enabled false.")
    return manifest


def _payload_apply_blockers(
    payload: ProjectPatchPayloadResult,
    project_root: Path,
    preview_root: Path,
    payload_zip: Path,
    payload_manifest: Path,
) -> list[str]:
    """Return blockers for unsafe or premature payload apply gating."""
    blockers = list(payload.blockers)
    if payload.status != "payload_ready" or not payload.patch_payload_created:
        blockers.append("PAYLOAD_NOT_READY")
    blockers.extend(_preview_root_blockers(project_root, preview_root))
    blockers.extend(_path_blockers(project_root, payload_zip, "PAYLOAD_ZIP"))
    blockers.extend(_path_blockers(project_root, payload_manifest, "PAYLOAD_MANIFEST"))
    if not payload_zip.exists() or not payload_zip.is_file():
        blockers.append("PAYLOAD_ZIP_MISSING")
    elif not _zip_contains_manifest(payload_zip):
        blockers.append("PAYLOAD_ZIP_MANIFEST_MISSING")
    data = _read_payload_manifest(payload_manifest)
    if data is None:
        blockers.append("PAYLOAD_MANIFEST_UNREADABLE")
    else:
        if data.get("apply_to_source") is not False:
            blockers.append("PAYLOAD_MANIFEST_APPLY_TO_SOURCE_NOT_FALSE")
        if data.get("requires_human_review") is not True:
            blockers.append("PAYLOAD_MANIFEST_REQUIRES_HUMAN_REVIEW_NOT_TRUE")
        if bool(data.get("import_rewrite_enabled")):
            blockers.append("IMPORT_REWRITE_ENABLED")
        target_text = str(data.get("target_file") or "")
        source_hash = str(data.get("source_content_hash") or "")
        if target_text and source_hash:
            target = Path(target_text).resolve()
            if not target.exists():
                blockers.append("TARGET_FILE_MISSING")
            elif hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
                blockers.append("SELECTED_SOURCE_HASH_CHANGED")
        else:
            blockers.append("PAYLOAD_MANIFEST_SOURCE_HASH_MISSING")
    return blockers


def _checked_rules() -> list[str]:
    """Return stable checked-rule labels."""
    return [
        "payload_status_payload_ready",
        "payload_zip_inside_daily_work_preview_root",
        "payload_manifest_inside_daily_work_preview_root",
        "payload_zip_contains_project_patch_payload_manifest",
        "payload_manifest_apply_to_source_false",
        "payload_manifest_requires_human_review_true",
        "import_rewrite_enabled_false",
        "selected_source_hash_unchanged",
        "apply_enabled_false_in_this_train",
    ]


def _read_payload_manifest(path: Path) -> dict[str, object] | None:
    """Read a payload manifest or return None if unavailable."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _zip_contains_manifest(path: Path) -> bool:
    """Return whether the project patch payload ZIP contains its manifest."""
    try:
        with zipfile.ZipFile(path, "r") as archive:
            return "PROJECT_PATCH_PAYLOAD_MANIFEST.json" in set(archive.namelist())
    except (OSError, zipfile.BadZipFile):
        return False


def _preview_root_blockers(project_root: Path, preview_root: Path) -> list[str]:
    """Return blockers for Preview roots outside selected project support."""
    return project_preview_root_blockers(project_root, preview_root)


def _path_blockers(project_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for paths that must remain project-support artifacts."""
    blockers: list[str] = []
    support_preview_root = preview_runs_root(project_root)
    if _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    if not _is_relative_to(path, support_preview_root):
        blockers.append(label + "_OUTSIDE_PROJECT_SUPPORT_PREVIEW_ROOT")
    lowered = {part.lower() for part in path.parts}
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append(label + "_INSIDE_PROTECTED_" + forbidden.upper())
    return blockers


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
