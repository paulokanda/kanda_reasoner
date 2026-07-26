# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/human_confirmed_import_rewrite_contract.py
"""Human-confirmation contract evidence for future import rewrite application."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .import_rewrite_application_gate import (
    IMPORT_REWRITE_CONFIRMATION_TOKEN,
    ImportRewriteApplicationGateResult,
)
from .models import FEATURE_ID, SCHEMA_VERSION

__all__ = [
    "HumanConfirmedImportRewriteContractResult",
    "build_human_confirmed_import_rewrite_contract",
    "write_human_confirmed_import_rewrite_contract_manifest",
]

_HUMAN_IMPORT_REWRITE_CONTRACT_NAME = "HUMAN_CONFIRMED_IMPORT_REWRITE_CONTRACT.json"


@dataclass(frozen=True)
class HumanConfirmedImportRewriteContractResult:
    """Review-only human confirmation contract for a future import rewrite train."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    import_rewrite_gate_manifest_path: str
    human_contract_manifest_path: str
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
        """Return a JSON-ready human confirmation contract dictionary."""
        return asdict(self)


def build_human_confirmed_import_rewrite_contract(
    import_gate: ImportRewriteApplicationGateResult,
    *,
    active_project_root: str,
    human_confirmation: str = "",
) -> HumanConfirmedImportRewriteContractResult:
    """Build review-only human confirmation evidence for future import rewriting."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(import_gate.preview_root).resolve()
    target = Path(import_gate.target_file).resolve()
    contract_manifest = preview_root / _HUMAN_IMPORT_REWRITE_CONTRACT_NAME
    token_valid = human_confirmation.strip() == IMPORT_REWRITE_CONFIRMATION_TOKEN
    blockers = _contract_blockers(import_gate, project_root, preview_root, target, token_valid)
    warnings = [
        "HUMAN_CONFIRMATION_RECORDED_FOR_FUTURE_IMPORT_REWRITE_TRAIN_ONLY",
        "IMPORT_REWRITE_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "REWRITE_ENABLED_REMAINS_FALSE",
        "APPLY_ENABLED_REMAINS_FALSE",
        "SELECTED_PROJECT_SOURCE_MUST_REMAIN_UNCHANGED",
    ]
    source_hash_verified = "SELECTED_SOURCE_HASH_CHANGED" not in blockers and "TARGET_FILE_MISSING" not in blockers
    status = "human_confirmed_import_rewrite_contract_ready" if not blockers else "blocked"
    return HumanConfirmedImportRewriteContractResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=import_gate.source_content_hash,
        preview_root=str(preview_root),
        import_rewrite_gate_manifest_path=import_gate.import_rewrite_gate_manifest_path,
        human_contract_manifest_path=str(contract_manifest),
        confirmation_token_required=IMPORT_REWRITE_CONFIRMATION_TOKEN,
        human_confirmation_present=bool(human_confirmation.strip()),
        human_confirmation_valid=token_valid,
        rewrite_enabled=False,
        apply_enabled=False,
        source_hash_verified=source_hash_verified and status.endswith("_ready"),
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_human_confirmed_import_rewrite_contract_manifest(
    contract: HumanConfirmedImportRewriteContractResult,
) -> Path:
    """Write human-confirmation evidence to the governed project-support Preview root."""
    manifest = Path(contract.human_contract_manifest_path).resolve()
    preview_root = Path(contract.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Human import rewrite contract manifest path is outside preview root.")
    lowered = {part.lower() for part in manifest.parts}
    forbidden = {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"}
    if lowered & forbidden:
        raise RuntimeError("Human import rewrite contract manifest is inside a protected support root.")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(contract.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("rewrite_enabled") is not False or saved.get("apply_enabled") is not False:
        raise RuntimeError("Human import rewrite contract must keep rewrite/apply disabled.")
    if saved.get("human_confirmation_recorded_for_future_train_only") is not True:
        raise RuntimeError("Human confirmation must be recorded only as future-train evidence.")
    return manifest


def _contract_blockers(
    import_gate: ImportRewriteApplicationGateResult,
    project_root: Path,
    preview_root: Path,
    target: Path,
    token_valid: bool,
) -> list[str]:
    """Return blockers that prevent human import rewrite contract readiness."""
    blockers: list[str] = list(import_gate.blockers)
    if import_gate.status != "import_rewrite_gate_ready":
        blockers.append("IMPORT_REWRITE_APPLICATION_GATE_NOT_READY")
    if token_valid is not True:
        blockers.append("HUMAN_CONFIRMATION_TOKEN_MISSING_OR_INVALID")
    if import_gate.rewrite_enabled is not False:
        blockers.append("IMPORT_REWRITE_GATE_REWRITE_ENABLED_UNEXPECTEDLY")
    if import_gate.apply_enabled is not False:
        blockers.append("IMPORT_REWRITE_GATE_APPLY_ENABLED_UNEXPECTEDLY")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    gate_manifest = Path(import_gate.import_rewrite_gate_manifest_path).resolve()
    if not _is_relative_to(gate_manifest, preview_root):
        blockers.append("IMPORT_REWRITE_GATE_MANIFEST_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(gate_manifest, project_root):
        blockers.append("IMPORT_REWRITE_GATE_MANIFEST_INSIDE_PROJECT_SOURCE")
    lowered = {part.lower() for part in preview_root.parts} | {part.lower() for part in gate_manifest.parts}
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append("IMPORT_REWRITE_CONTRACT_INSIDE_PROTECTED_" + forbidden.upper())
    if not target.exists():
        blockers.append("TARGET_FILE_MISSING")
    else:
        current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if current_hash != import_gate.source_content_hash:
            blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    return blockers


def _checked_rules() -> list[str]:
    """Return stable rule labels checked by this contract."""
    return [
        "import_rewrite_application_gate_ready",
        "human_confirmation_token_exact_match",
        "human_confirmation_future_train_only",
        "rewrite_enabled_false_in_this_train",
        "apply_enabled_false_in_this_train",
        "selected_source_hash_unchanged",
        "preview_root_inside_project_support_only",
        "manifest_outside_project_source",
        "protected_support_roots_blocked",
    ]


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
