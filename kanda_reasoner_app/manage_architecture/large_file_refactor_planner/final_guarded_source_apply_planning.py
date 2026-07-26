# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/final_guarded_source_apply_planning.py
"""Final guarded source-apply planning evidence without source mutation."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .human_confirmed_apply_contract import HumanConfirmedApplyContractResult
from .models import FEATURE_ID, SCHEMA_VERSION

__all__ = [
    "FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN",
    "FinalGuardedSourceApplyPlanResult",
    "build_final_guarded_source_apply_plan",
    "write_final_guarded_source_apply_plan_manifest",
]

FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN = "CONFIRM_PLAN_FINAL_GUARDED_SOURCE_APPLY"
_FINAL_PLAN_NAME = "FINAL_GUARDED_SOURCE_APPLY_PLAN.json"


@dataclass(frozen=True)
class FinalGuardedSourceApplyPlanResult:
    """Planning-only readiness record for a future guarded source-apply train."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    payload_zip_path: str
    human_apply_contract_manifest_path: str
    final_plan_manifest_path: str
    confirmation_token_required: str
    planning_confirmation_present: bool
    planning_confirmation_valid: bool
    planning_recorded_for_future_train_only: bool = True
    rewrite_enabled: bool = False
    apply_enabled: bool = False
    source_mutation_enabled: bool = False
    source_hash_verified: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready guarded source-apply planning dictionary."""
        return asdict(self)


def build_final_guarded_source_apply_plan(
    human_apply_contract: HumanConfirmedApplyContractResult,
    *,
    active_project_root: str,
    planning_confirmation: str = "",
) -> FinalGuardedSourceApplyPlanResult:
    """Build planning-only evidence for a future guarded source-apply implementation."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(human_apply_contract.preview_root).resolve()
    target = Path(human_apply_contract.target_file).resolve()
    source_hash = human_apply_contract.source_content_hash
    payload_zip = Path(human_apply_contract.payload_zip_path).resolve()
    contract_manifest = Path(human_apply_contract.human_apply_contract_manifest_path).resolve()
    final_manifest = preview_root / _FINAL_PLAN_NAME
    token_valid = planning_confirmation.strip() == FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN
    blockers = _plan_blockers(
        human_apply_contract,
        project_root,
        preview_root,
        target,
        source_hash,
        payload_zip,
        contract_manifest,
        token_valid,
    )
    warnings = [
        "FINAL_SOURCE_APPLY_RECORDED_FOR_FUTURE_TRAIN_ONLY",
        "SOURCE_MUTATION_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "IMPORT_REWRITE_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "REWRITE_ENABLED_REMAINS_FALSE",
        "APPLY_ENABLED_REMAINS_FALSE",
        "SOURCE_MUTATION_ENABLED_REMAINS_FALSE",
    ]
    status = "final_guarded_source_apply_plan_ready" if not blockers else "blocked"
    source_hash_verified = "SELECTED_SOURCE_HASH_CHANGED" not in blockers and "TARGET_FILE_MISSING" not in blockers
    return FinalGuardedSourceApplyPlanResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_zip_path=str(payload_zip),
        human_apply_contract_manifest_path=str(contract_manifest),
        final_plan_manifest_path=str(final_manifest),
        confirmation_token_required=FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
        planning_confirmation_present=bool(planning_confirmation.strip()),
        planning_confirmation_valid=token_valid,
        planning_recorded_for_future_train_only=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_mutation_enabled=False,
        source_hash_verified=source_hash_verified and status.endswith("_ready"),
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_final_guarded_source_apply_plan_manifest(plan: FinalGuardedSourceApplyPlanResult) -> Path:
    """Write final source-apply planning evidence to the governed project-support Preview root."""
    manifest = Path(plan.final_plan_manifest_path).resolve()
    preview_root = Path(plan.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Final source-apply plan manifest path is outside preview root.")
    lowered = {part.lower() for part in manifest.parts}
    forbidden = {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"}
    if lowered & forbidden:
        raise RuntimeError("Final source-apply plan manifest is inside a protected support root.")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("rewrite_enabled") is not False or saved.get("apply_enabled") is not False:
        raise RuntimeError("Final source-apply plan must keep rewrite/apply disabled.")
    if saved.get("source_mutation_enabled") is not False:
        raise RuntimeError("Final source-apply plan must keep source mutation disabled.")
    if saved.get("planning_recorded_for_future_train_only") is not True:
        raise RuntimeError("Final source-apply planning must be future-train evidence only.")
    return manifest


def _plan_blockers(
    human_apply_contract: HumanConfirmedApplyContractResult,
    project_root: Path,
    preview_root: Path,
    target: Path,
    source_hash: str,
    payload_zip: Path,
    contract_manifest: Path,
    token_valid: bool,
) -> list[str]:
    """Return blockers that prevent final source-apply plan readiness."""
    blockers: list[str] = list(human_apply_contract.blockers)
    if human_apply_contract.status != "human_confirmed_apply_contract_ready":
        blockers.append("HUMAN_APPLY_CONTRACT_NOT_READY")
    if token_valid is not True:
        blockers.append("FINAL_SOURCE_APPLY_PLANNING_TOKEN_MISSING_OR_INVALID")
    if human_apply_contract.apply_enabled is not False:
        blockers.append("HUMAN_APPLY_CONTRACT_APPLY_ENABLED_UNEXPECTEDLY")
    if human_apply_contract.rewrite_enabled is not False:
        blockers.append("HUMAN_APPLY_CONTRACT_REWRITE_ENABLED_UNEXPECTEDLY")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    blockers.extend(_path_blockers(project_root, preview_root, payload_zip, "PAYLOAD_ZIP"))
    blockers.extend(_path_blockers(project_root, preview_root, contract_manifest, "HUMAN_APPLY_CONTRACT_MANIFEST"))
    if not payload_zip.exists() or not payload_zip.is_file():
        blockers.append("PAYLOAD_ZIP_MISSING")
    if not contract_manifest.exists() or not contract_manifest.is_file():
        blockers.append("HUMAN_APPLY_CONTRACT_MANIFEST_MISSING")
    if not target.exists():
        blockers.append("TARGET_FILE_MISSING")
    elif hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
        blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    return blockers


def _path_blockers(project_root: Path, preview_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for paths that must stay in the governed preview root."""
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
    """Return stable rule labels checked by this planning contract."""
    return [
        "human_apply_contract_ready",
        "final_source_apply_planning_token_exact_match",
        "future_train_evidence_only",
        "rewrite_enabled_false_in_this_train",
        "apply_enabled_false_in_this_train",
        "source_mutation_enabled_false_in_this_train",
        "selected_source_hash_unchanged",
        "preview_root_inside_project_support_only",
        "artifacts_outside_project_source",
        "protected_support_roots_blocked",
    ]


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
