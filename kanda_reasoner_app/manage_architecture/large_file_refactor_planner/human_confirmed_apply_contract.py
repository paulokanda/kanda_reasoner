# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/human_confirmed_apply_contract.py
"""Human-confirmation contract evidence for a future payload apply train."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import zipfile

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .human_confirmed_import_rewrite_contract import HumanConfirmedImportRewriteContractResult
from .models import FEATURE_ID, SCHEMA_VERSION
from .payload_apply_gate import PayloadApplyGateResult

__all__ = [
    "HUMAN_CONFIRMED_APPLY_TOKEN",
    "HumanConfirmedApplyContractResult",
    "build_human_confirmed_apply_contract",
    "write_human_confirmed_apply_contract_manifest",
]

HUMAN_CONFIRMED_APPLY_TOKEN = "CONFIRM_REVIEWED_PROJECT_PATCH_PAYLOAD"
_HUMAN_APPLY_CONTRACT_NAME = "HUMAN_CONFIRMED_APPLY_CONTRACT.json"


@dataclass(frozen=True)
class HumanConfirmedApplyContractResult:
    """Review-only human confirmation contract for a future payload apply train."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    payload_zip_path: str
    payload_manifest_path: str
    payload_apply_gate_manifest_path: str
    human_import_rewrite_contract_manifest_path: str
    human_apply_contract_manifest_path: str
    confirmation_token_required: str
    human_confirmation_present: bool
    human_confirmation_valid: bool
    human_confirmation_recorded_for_future_train_only: bool = True
    rewrite_enabled: bool = False
    apply_enabled: bool = False
    source_hash_verified: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready human apply contract dictionary."""
        return asdict(self)


def build_human_confirmed_apply_contract(
    payload_gate: PayloadApplyGateResult,
    import_contract: HumanConfirmedImportRewriteContractResult,
    *,
    active_project_root: str,
    human_confirmation: str = "",
) -> HumanConfirmedApplyContractResult:
    """Build review-only human confirmation evidence for future payload application."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(payload_gate.preview_root).resolve()
    payload_zip = Path(payload_gate.payload_zip_path).resolve()
    payload_manifest = Path(payload_gate.payload_manifest_path).resolve()
    payload_data = _read_payload_manifest(payload_manifest)
    target = Path(str(payload_data.get("target_file") or import_contract.target_file)).resolve() if payload_data else Path(import_contract.target_file).resolve()
    source_hash = str((payload_data or {}).get("source_content_hash") or import_contract.source_content_hash)
    contract_manifest = preview_root / _HUMAN_APPLY_CONTRACT_NAME
    token_valid = human_confirmation.strip() == HUMAN_CONFIRMED_APPLY_TOKEN
    blockers = _contract_blockers(
        payload_gate,
        import_contract,
        project_root,
        preview_root,
        payload_zip,
        payload_manifest,
        target,
        source_hash,
        token_valid,
        payload_data,
    )
    warnings = [
        "HUMAN_CONFIRMATION_RECORDED_FOR_FUTURE_PAYLOAD_APPLY_TRAIN_ONLY",
        "PAYLOAD_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "IMPORT_REWRITE_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "REWRITE_ENABLED_REMAINS_FALSE",
        "APPLY_ENABLED_REMAINS_FALSE",
        "SELECTED_PROJECT_SOURCE_MUST_REMAIN_UNCHANGED",
    ]
    source_hash_verified = "SELECTED_SOURCE_HASH_CHANGED" not in blockers and "TARGET_FILE_MISSING" not in blockers
    status = "human_confirmed_apply_contract_ready" if not blockers else "blocked"
    return HumanConfirmedApplyContractResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_zip_path=str(payload_zip),
        payload_manifest_path=str(payload_manifest),
        payload_apply_gate_manifest_path=payload_gate.apply_gate_manifest_path,
        human_import_rewrite_contract_manifest_path=import_contract.human_contract_manifest_path,
        human_apply_contract_manifest_path=str(contract_manifest),
        confirmation_token_required=HUMAN_CONFIRMED_APPLY_TOKEN,
        human_confirmation_present=bool(human_confirmation.strip()),
        human_confirmation_valid=token_valid,
        rewrite_enabled=False,
        apply_enabled=False,
        source_hash_verified=source_hash_verified and status.endswith("_ready"),
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_human_confirmed_apply_contract_manifest(contract: HumanConfirmedApplyContractResult) -> Path:
    """Write human apply confirmation evidence to the governed project-support Preview root."""
    manifest = Path(contract.human_apply_contract_manifest_path).resolve()
    preview_root = Path(contract.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Human apply contract manifest path is outside preview root.")
    lowered = {part.lower() for part in manifest.parts}
    forbidden = {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"}
    if lowered & forbidden:
        raise RuntimeError("Human apply contract manifest is inside a protected support root.")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(contract.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("rewrite_enabled") is not False or saved.get("apply_enabled") is not False:
        raise RuntimeError("Human apply contract must keep rewrite/apply disabled.")
    if saved.get("human_confirmation_recorded_for_future_train_only") is not True:
        raise RuntimeError("Human apply confirmation must be recorded only as future-train evidence.")
    return manifest


def _contract_blockers(
    payload_gate: PayloadApplyGateResult,
    import_contract: HumanConfirmedImportRewriteContractResult,
    project_root: Path,
    preview_root: Path,
    payload_zip: Path,
    payload_manifest: Path,
    target: Path,
    source_hash: str,
    token_valid: bool,
    payload_data: dict[str, object] | None,
) -> list[str]:
    """Return blockers that prevent human apply contract readiness."""
    blockers: list[str] = list(payload_gate.blockers) + list(import_contract.blockers)
    if payload_gate.status != "apply_gate_ready":
        blockers.append("PAYLOAD_APPLY_GATE_NOT_READY")
    if import_contract.status != "human_confirmed_import_rewrite_contract_ready":
        blockers.append("HUMAN_IMPORT_REWRITE_CONTRACT_NOT_READY")
    if token_valid is not True:
        blockers.append("HUMAN_APPLY_CONFIRMATION_TOKEN_MISSING_OR_INVALID")
    if payload_gate.apply_enabled is not False:
        blockers.append("PAYLOAD_APPLY_GATE_APPLY_ENABLED_UNEXPECTEDLY")
    if import_contract.apply_enabled is not False:
        blockers.append("IMPORT_CONTRACT_APPLY_ENABLED_UNEXPECTEDLY")
    if import_contract.rewrite_enabled is not False:
        blockers.append("IMPORT_CONTRACT_REWRITE_ENABLED_UNEXPECTEDLY")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    for path, label in (
        (payload_zip, "PAYLOAD_ZIP"),
        (payload_manifest, "PAYLOAD_MANIFEST"),
        (Path(payload_gate.apply_gate_manifest_path).resolve(), "PAYLOAD_APPLY_GATE_MANIFEST"),
        (Path(import_contract.human_contract_manifest_path).resolve(), "HUMAN_IMPORT_REWRITE_CONTRACT_MANIFEST"),
    ):
        blockers.extend(_path_blockers(project_root, preview_root, path, label))
    if not payload_zip.exists() or not payload_zip.is_file():
        blockers.append("PAYLOAD_ZIP_MISSING")
    elif not _zip_contains_manifest(payload_zip):
        blockers.append("PAYLOAD_ZIP_MANIFEST_MISSING")
    if payload_data is None:
        blockers.append("PAYLOAD_MANIFEST_UNREADABLE")
    else:
        if payload_data.get("apply_to_source") is not False:
            blockers.append("PAYLOAD_MANIFEST_APPLY_TO_SOURCE_NOT_FALSE")
        if payload_data.get("requires_human_review") is not True:
            blockers.append("PAYLOAD_MANIFEST_REQUIRES_HUMAN_REVIEW_NOT_TRUE")
        if bool(payload_data.get("import_rewrite_enabled")):
            blockers.append("IMPORT_REWRITE_ENABLED")
    if not target.exists():
        blockers.append("TARGET_FILE_MISSING")
    elif hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
        blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    return blockers


def _path_blockers(project_root: Path, preview_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for paths that must remain preview-root artifacts."""
    blockers: list[str] = []
    if not _is_relative_to(path, preview_root):
        blockers.append(label + "_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    lowered = {part.lower() for part in path.parts}
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append(label + "_INSIDE_PROTECTED_" + forbidden.upper())
    return blockers


def _checked_rules() -> list[str]:
    """Return stable rule labels checked by this contract."""
    return [
        "payload_apply_gate_ready",
        "human_import_rewrite_contract_ready",
        "human_apply_confirmation_token_exact_match",
        "human_apply_confirmation_future_train_only",
        "payload_manifest_apply_to_source_false",
        "payload_manifest_requires_human_review_true",
        "import_rewrite_enabled_false",
        "rewrite_enabled_false_in_this_train",
        "apply_enabled_false_in_this_train",
        "selected_source_hash_unchanged",
        "preview_root_inside_project_support_only",
        "manifests_outside_project_source",
        "protected_support_roots_blocked",
    ]


def _read_payload_manifest(path: Path) -> dict[str, object] | None:
    """Read a payload manifest or return None if unavailable."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _zip_contains_manifest(path: Path) -> bool:
    """Return whether the payload ZIP contains its canonical manifest."""
    try:
        with zipfile.ZipFile(path, "r") as archive:
            return "PROJECT_PATCH_PAYLOAD_MANIFEST.json" in set(archive.namelist())
    except (OSError, zipfile.BadZipFile):
        return False


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
