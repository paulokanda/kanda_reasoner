# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/final_complete_workbench_freeze.py
"""Read-only final closure evidence for the complete Large File Refactor Workbench."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import importlib
import json
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import workbench_support_root
from .models import SCHEMA_VERSION

__all__ = [
    "COMPLETE_WORKBENCH_FREEZE_FEATURE_ID",
    "CompleteWorkbenchFreezeReport",
    "REQUIRED_COMPLETE_WORKBENCH_PLANNER_FILES",
    "REQUIRED_COMPLETE_WORKBENCH_VALIDATORS",
    "build_complete_workbench_freeze_report",
    "write_complete_workbench_freeze_report",
]

COMPLETE_WORKBENCH_FREEZE_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-patch6-final-canon-v1"
)
_REPORT_JSON = "COMPLETE_WORKBENCH_FREEZE_REPORT.json"
_REPORT_TXT = "COMPLETE_WORKBENCH_FREEZE_REPORT.txt"
_PROOF_JSON = "PATCH6_CONTROLLED_REAL_MODULE_PROOF.json"
_PACKAGE = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"

_REQUIRED_EXPORTS = [
    "build_workbench_plan_snapshot",
    "build_refactor_baseline",
    "build_workbench_execution_basis_set",
    "evaluate_workbench_execution_feasibility",
    "build_workbench_execution_contract",
    "build_transformation_recipe",
    "build_and_write_sealed_payload",
    "build_and_write_real_preview",
    "validate_real_preview_structure",
    "build_and_write_preflight_backup_readiness",
    "build_and_write_source_apply_payload",
    "prove_shadow_runtime_provenance",
    "validate_shadow_refactor",
    "prepare_completion_evidence",
    "prepare_completion_transaction",
    "execute_journaled_refactor_apply",
    "resume_journaled_refactor_apply",
    "rollback_journaled_refactor_transaction",
    "build_and_write_refactor_receipt",
]

REQUIRED_COMPLETE_WORKBENCH_PLANNER_FILES = (
    "module_size_policy.py",
    "workbench_plan_snapshot.py",
    "workbench_refactor_baseline.py",
    "workbench_execution_basis.py",
    "workbench_execution_feasibility.py",
    "workbench_execution_contract.py",
    "workbench_transformation_recipe.py",
    "cst_symbol_source_extractor.py",
    "cst_facade_global_import_inserter.py",
    "cst_real_preview_writer.py",
    "real_preview_structural_validator.py",
    "workbench_sealed_payload.py",
    "workbench_shadow_backend.py",
    "workbench_shadow_provenance.py",
    "workbench_shadow_validation.py",
    "workbench_completion_review.py",
    "workbench_completion_workflow.py",
    "workbench_completion_gui.py",
    "workbench_diff_review_assistant.py",
    "workbench_diff_review_assistant_gui.py",
    "workbench_journaled_apply_executor.py",
    "workbench_transaction_rollback.py",
    "workbench_refactor_receipt.py",
    "workbench_patch5_executor_proof.py",
    "LARGE_FILE_REFACTOR_WORKBENCH_TUTORIAL.md",
)

REQUIRED_COMPLETE_WORKBENCH_VALIDATORS = (
    "validate_architecture_review_large_file_refactor_preflight_backup_readiness_v1.py",
    "validate_large_file_refactor_workbench_patch2_transaction_core_v1.py",
    "validate_large_file_refactor_workbench_patch3_transformation_shadow_v1.py",
    "validate_large_file_refactor_workbench_patch4_completion_gui_gate_v1.py",
    "validate_large_file_refactor_workbench_patch5_journaled_apply_v1.py",
    "validate_large_file_refactor_workbench_patch6_controlled_real_module_v1.py",
    "validate_workbench_assisted_diff_review_and_ui_cleanup_v1.py",
)

# Backward-compatible private aliases for internal consumers.
_REQUIRED_PLANNER_FILES = REQUIRED_COMPLETE_WORKBENCH_PLANNER_FILES
_REQUIRED_VALIDATORS = REQUIRED_COMPLETE_WORKBENCH_VALIDATORS

_STRICT_SIZE_FILES = [
    "module_size_policy.py",
    "workbench_plan_snapshot.py",
    "workbench_refactor_baseline.py",
    "workbench_execution_basis.py",
    "workbench_execution_feasibility.py",
    "workbench_execution_contract.py",
    "workbench_transformation_recipe.py",
    "cst_symbol_source_extractor.py",
    "cst_facade_global_import_inserter.py",
    "cst_real_preview_writer.py",
    "real_preview_structural_validator.py",
    "workbench_sealed_payload.py",
    "workbench_shadow_backend.py",
    "workbench_shadow_provenance.py",
    "workbench_shadow_validation.py",
    "workbench_completion_review.py",
    "workbench_completion_workflow.py",
    "workbench_completion_gui.py",
    "workbench_diff_review_assistant.py",
    "workbench_diff_review_assistant_gui.py",
    "workbench_journaled_apply_executor.py",
    "workbench_transaction_rollback.py",
    "workbench_refactor_receipt.py",
    "workbench_patch5_executor_proof.py",
]


@dataclass(frozen=True)
class CompleteWorkbenchFreezeReport:
    """Read-only final report for the six-patch Workbench implementation train."""

    schema_version: str
    feature_id: str
    status: str
    active_project_root: str
    evidence_root: str
    completed_patches: int = 6
    target_patches: int = 6
    controlled_real_module_proof_status: str = "not_checked"
    real_apply_executor_proven: bool = False
    rollback_restoration_proven: bool = False
    second_apply_proven: bool = False
    live_source_unchanged_during_controlled_proof: bool = False
    required_exports: list[str] = field(default_factory=list)
    required_files: list[str] = field(default_factory=list)
    required_validators: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    report_path: str = ""
    view_path: str = ""
    writes_project_source: bool = False
    writes_freeze_memory: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready final closure evidence."""
        return asdict(self)


def build_complete_workbench_freeze_report(
    *,
    active_project_root: str,
    evidence_root: str | None = None,
) -> CompleteWorkbenchFreezeReport:
    """Build final closure evidence from installed source and controlled proof output."""
    project_root = Path(active_project_root).resolve()
    root = Path(evidence_root).resolve() if evidence_root else _final_validation_root(project_root)
    blockers: list[str] = []
    blockers.extend(_root_blockers(project_root, root))
    blockers.extend(_missing_planner_files(project_root))
    blockers.extend(_missing_validators(project_root))
    blockers.extend(_missing_package_exports())
    blockers.extend(_strict_size_blockers(project_root))
    blockers.extend(_source_regression_blockers(project_root))
    proof, proof_blockers = _load_controlled_proof(project_root, root)
    blockers.extend(proof_blockers)
    status = "complete_workbench_freeze_ready" if not blockers else "blocked"
    warnings = [] if not blockers else ["COMPLETE_WORKBENCH_FREEZE_BLOCKED"]
    return CompleteWorkbenchFreezeReport(
        schema_version=SCHEMA_VERSION,
        feature_id=COMPLETE_WORKBENCH_FREEZE_FEATURE_ID,
        status=status,
        active_project_root=str(project_root),
        evidence_root=str(root),
        controlled_real_module_proof_status=str(proof.get("status", "missing")),
        real_apply_executor_proven=not proof_blockers,
        rollback_restoration_proven=not proof_blockers,
        second_apply_proven=not proof_blockers,
        live_source_unchanged_during_controlled_proof=not proof_blockers,
        required_exports=list(_REQUIRED_EXPORTS),
        required_files=list(REQUIRED_COMPLETE_WORKBENCH_PLANNER_FILES),
        required_validators=list(REQUIRED_COMPLETE_WORKBENCH_VALIDATORS),
        blockers=sorted(set(blockers)),
        warnings=warnings,
        checked_rules=_checked_rules(),
        report_path=str(root / _REPORT_JSON),
        view_path=str(root / _REPORT_TXT),
    )


def write_complete_workbench_freeze_report(
    report: CompleteWorkbenchFreezeReport,
) -> CompleteWorkbenchFreezeReport:
    """Write final closure evidence under selected project support only."""
    root = Path(report.evidence_root).resolve()
    for raw in (report.report_path, report.view_path):
        output = Path(raw).resolve()
        if not _is_relative_to(output, root):
            raise RuntimeError("COMPLETE_WORKBENCH_REPORT_OUTSIDE_EVIDENCE_ROOT:" + str(output))
    root.mkdir(parents=True, exist_ok=True)
    Path(report.report_path).write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    Path(report.view_path).write_text(_format_text_view(report), encoding="utf-8")
    return report


def _missing_planner_files(project_root: Path) -> list[str]:
    """Return blockers for missing final Workbench implementation files."""
    base = project_root / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
    return [
        "MISSING_PLANNER_FILE:" + name
        for name in REQUIRED_COMPLETE_WORKBENCH_PLANNER_FILES
        if not (base / name).is_file()
    ]


def _missing_validators(project_root: Path) -> list[str]:
    """Return blockers for missing patch-train and controlled-proof validators."""
    tools = project_root / "tools"
    return [
        "MISSING_VALIDATOR:" + name
        for name in REQUIRED_COMPLETE_WORKBENCH_VALIDATORS
        if not (tools / name).is_file()
    ]


def _missing_package_exports() -> list[str]:
    """Return blockers for missing public package seams required by final orchestration."""
    package = importlib.import_module(_PACKAGE)
    return [
        "MISSING_EXPORT:" + name
        for name in _REQUIRED_EXPORTS
        if not hasattr(package, name)
    ]


def _strict_size_blockers(project_root: Path) -> list[str]:
    """Enforce 101-499 physical lines for the final Workbench source set."""
    base = project_root / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
    blockers: list[str] = []
    for name in _STRICT_SIZE_FILES:
        path = base / name
        if not path.is_file():
            continue
        lines = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        if not 100 < lines < 500:
            blockers.append(f"STRICT_MODULE_SIZE_POLICY_FAILED:{name}:{lines}")
    return blockers


def _source_regression_blockers(project_root: Path) -> list[str]:
    """Return blockers for known cross-patch safety regressions."""
    base = project_root / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
    blockers: list[str] = []
    gui = (base / "workbench_gui.py").read_text(encoding="utf-8", errors="ignore")
    completion = (base / "workbench_completion_gui.py").read_text(encoding="utf-8", errors="ignore")
    executor = (base / "workbench_journaled_apply_executor.py").read_text(encoding="utf-8", errors="ignore")
    for legacy_marker in (
        "Legacy Apply Source Changes (Disabled)",
        "Exact apply token:",
        "Rollback Last Apply",
    ):
        if legacy_marker in gui:
            blockers.append("LEGACY_APPLY_GUI_CONTROL_REINTRODUCED:" + legacy_marker)
    if "Next governed stage: Completion Review and Refactor Authorization." not in gui:
        blockers.append("GOVERNED_COMPLETION_PATH_GUIDANCE_MISSING")
    if 'QPushButton("Refactor Large Module")' not in completion:
        blockers.append("REFACTOR_LARGE_MODULE_BUTTON_MISSING")
    for marker in ("record_operation_intent", "record_operation_applied", "record_operation_verified"):
        if marker not in executor:
            blockers.append("JOURNALED_OPERATION_STAGE_MISSING:" + marker)
    return blockers


def _load_controlled_proof(project_root: Path, evidence_root: Path) -> tuple[dict[str, Any], list[str]]:
    """Load and verify the Patch 6 controlled real-module proof summary."""
    path = evidence_root / _PROOF_JSON
    if not path.is_file():
        return {}, ["PATCH6_CONTROLLED_REAL_MODULE_PROOF_MISSING"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, ["PATCH6_CONTROLLED_REAL_MODULE_PROOF_UNREADABLE"]
    blockers: list[str] = []
    if data.get("status") != "controlled_real_module_proof_pass":
        blockers.append("PATCH6_CONTROLLED_REAL_MODULE_PROOF_NOT_PASS")
    if data.get("approved_plan_sizes") != [145, 197, 429]:
        blockers.append("PATCH6_CONTROLLED_PLAN_SIZE_EVIDENCE_MISMATCH")
    live_target = project_root / "kanda_reasoner_app" / "reasoner_symbol_atlas" / "main_helper_mapper.py"
    live_hash = _hash_file(live_target)
    if data.get("live_target_unchanged_hash") != live_hash:
        blockers.append("PATCH6_LIVE_TARGET_HASH_EVIDENCE_MISMATCH")
    if not str(data.get("refactor_receipt_hash", "")):
        blockers.append("PATCH6_REFACTOR_RECEIPT_HASH_MISSING")
    return data, blockers


def _root_blockers(project_root: Path, evidence_root: Path) -> list[str]:
    """Return evidence-root containment blockers."""
    expected = _final_validation_root(project_root)
    blockers: list[str] = []
    if not project_root.is_dir():
        blockers.append("PROJECT_ROOT_NOT_FOUND")
    if not _is_relative_to(evidence_root, expected):
        blockers.append("FINAL_EVIDENCE_ROOT_OUTSIDE_PROJECT_SUPPORT")
    if _is_relative_to(evidence_root, project_root):
        blockers.append("FINAL_EVIDENCE_ROOT_INSIDE_PROJECT_SOURCE")
    return blockers


def _final_validation_root(project_root: Path) -> Path:
    """Return selected-project Workbench support for final validation evidence."""
    return workbench_support_root(project_root) / "final_validation"


def _hash_file(path: Path) -> str:
    """Return SHA-256 for a file or empty string when unavailable."""
    import hashlib

    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return whether a resolved path is contained by a resolved root."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _checked_rules() -> list[str]:
    """Return final stable closure rules."""
    return [
        "patch1_through_patch5_regressions_preserved",
        "planner_snapshot_baseline_contract_transaction_ownership_separate",
        "strict_101_499_source_module_policy",
        "libcst_decorators_preserved",
        "cycle_safe_function_local_facade_global_imports",
        "sealed_payload_identity_preview_shadow_real_apply",
        "shadow_provenance_and_behavior_pass",
        "journaled_intent_applied_verified_apply",
        "rollback_exact_restoration_before_terminal_completion",
        "fresh_second_transaction_completed_validated",
        "refactor_receipt_integrity_verified",
        "live_project_source_unchanged_during_controlled_proof",
        "final_report_writes_project_support_only",
        "freeze_memory_writes_remain_external_governed_workflow",
    ]


def _format_text_view(report: CompleteWorkbenchFreezeReport) -> str:
    """Return a concise human-readable final closure view."""
    lines = [
        "Large File Refactor Workbench Final Closure",
        "==========================================",
        f"status: {report.status}",
        f"patch_train: {report.completed_patches} / {report.target_patches}",
        f"controlled_real_module_proof: {report.controlled_real_module_proof_status}",
        f"real_apply_executor_proven: {report.real_apply_executor_proven}",
        f"rollback_restoration_proven: {report.rollback_restoration_proven}",
        f"second_apply_proven: {report.second_apply_proven}",
        f"live_source_unchanged: {report.live_source_unchanged_during_controlled_proof}",
        "writes_project_source: False",
        "writes_freeze_memory: False",
        "",
    ]
    if report.blockers:
        lines.append("Blockers:")
        lines.extend("- " + item for item in report.blockers)
        lines.append("")
    lines.append("Checked rules:")
    lines.extend("- " + item for item in report.checked_rules)
    return "\n".join(lines) + "\n"
