# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_final_integration_hardening.py
"""Final integration hardening checks for the Large File Refactor Workbench.

This module is read-only.  It validates that the Workbench import chain,
compatibility aliases, size gates, GUI layout guards, and script-path safety
remain intact before later advanced trains expand behavior.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import importlib
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION

__all__ = [
    "FINAL_INTEGRATION_HARDENING_FEATURE_ID",
    "FinalIntegrationHardeningReport",
    "build_final_integration_hardening_report",
    "write_final_integration_hardening_report",
]

FINAL_INTEGRATION_HARDENING_FEATURE_ID = (
    "architecture-review-large-file-refactor-final-integration-hardening-v1"
)
_REPORT_NAME = "LARGE_FILE_REFACTOR_FINAL_INTEGRATION_HARDENING.json"
_PACKAGE = "kanda_reasoner_app.manage_architecture.large_file_refactor_planner"
_REQUIRED_FILES = [
    "workbench_plan_intake.py",
    "workbench_execution_basis.py",
    "workbench_execution_feasibility.py",
    "workbench_dependency_readiness.py",
    "cst_real_preview_writer.py",
    "real_preview_structural_validator.py",
    "workbench_preflight_backup_readiness.py",
    "workbench_source_payload_builder.py",
    "workbench_guarded_source_apply.py",
    "workbench_post_apply_validator.py",
    "workbench_rollback_executor.py",
    "workbench_behavior_validation.py",
    "import_migration_preview.py",
    "workbench_import_rewrite_apply_readiness.py",
    "workbench_import_rewrite_apply_executor.py",
    "workbench_import_rewrite_rollback_executor.py",
    "dependency_clusterer.py",
    "helper_import_synthesizer.py",
    "cst_docstring_inserter.py",
    "workbench_gui.py",
    "workbench_gui_layout.py",
    "workbench_dynamic_python_risks.py",
    "workbench_transformation_recipe.py",
    "workbench_sealed_payload.py",
    "workbench_shadow_backend.py",
    "workbench_shadow_provenance.py",
    "workbench_shadow_validation.py",
    "workbench_source_mutation_primitives.py",
    "workbench_journaled_apply_models.py",
    "workbench_journaled_apply_support.py",
    "workbench_journaled_apply_executor.py",
    "workbench_transaction_rollback.py",
    "workbench_refactor_receipt.py",
    "workbench_patch5_executor_proof.py",
    "workbench_completion_apply_bridge.py",
]

_STRICT_SIZE_FILES = {
    "workbench_dynamic_python_risks.py",
    "workbench_transformation_recipe.py",
    "workbench_sealed_payload.py",
    "workbench_shadow_backend.py",
    "workbench_shadow_provenance.py",
    "workbench_shadow_validation.py",
    "workbench_source_mutation_primitives.py",
    "workbench_journaled_apply_models.py",
    "workbench_journaled_apply_support.py",
    "workbench_journaled_apply_executor.py",
    "workbench_transaction_rollback.py",
    "workbench_refactor_receipt.py",
    "workbench_patch5_executor_proof.py",
    "workbench_completion_apply_bridge.py",
}

_REQUIRED_EXPORTS: dict[str, tuple[str, ...]] = {
    "workbench_execution_basis": (
        "build_workbench_execution_basis_set",
        "execution_basis_is_fresh",
    ),
    "workbench_execution_feasibility": (
        "evaluate_workbench_execution_feasibility",
    ),
    "workbench_post_apply_validator": (
        "PostApplyValidationResult",
        "WorkbenchPostApplyValidationResult",
        "validate_and_write_post_apply",
    ),
    "workbench_guarded_apply_formatting": ("format_post_apply_validation",),
    "workbench_import_rewrite_apply_readiness": (
        "build_and_write_import_rewrite_apply_readiness",
        "expected_import_rewrite_apply_token",
    ),
    "workbench_import_rewrite_apply_executor": (
        "execute_guarded_import_rewrite_apply",
        "expected_guarded_import_rewrite_apply_token",
    ),
    "workbench_import_rewrite_rollback_executor": (
        "execute_import_rewrite_rollback",
        "expected_import_rewrite_rollback_token",
    ),
    "workbench_behavior_validation": ("run_workbench_behavior_validation",),
    "cst_real_preview_writer": ("build_and_write_real_preview",),
    "workbench_dynamic_python_risks": ("analyze_dynamic_python_risks",),
    "workbench_transformation_recipe": ("build_transformation_recipe",),
    "workbench_sealed_payload": ("build_and_write_sealed_payload", "verify_sealed_payload"),
    "workbench_shadow_backend": ("choose_shadow_backend",),
    "workbench_shadow_provenance": ("prove_shadow_runtime_provenance",),
    "workbench_shadow_validation": ("validate_shadow_refactor",),
    "workbench_journaled_apply_executor": (
        "execute_journaled_refactor_apply",
        "resume_journaled_refactor_apply",
        "finalize_journaled_refactor_transaction",
    ),
    "workbench_transaction_rollback": ("rollback_journaled_refactor_transaction",),
    "workbench_refactor_receipt": ("build_and_write_refactor_receipt",),
    "workbench_patch5_executor_proof": ("find_patch5_executor_proof",),
    "helper_import_synthesizer": ("synthesize_helper_imports",),
    "dependency_clusterer": ("build_dependency_clusters",),
}
_PROHIBITED_GUI_SNIPPETS = ("content.parentWidget()",)
_PROHIBITED_SCRIPT_CHARS = ("\x0b", "\x0c", "\x00")


@dataclass(frozen=True)
class FinalIntegrationHardeningReport:
    """Read-only report for final Workbench integration hardening."""

    schema_version: str
    feature_id: str
    status: str
    project_root: str
    checked_files: list[str] = field(default_factory=list)
    checked_modules: list[str] = field(default_factory=list)
    line_counts: dict[str, int] = field(default_factory=dict)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready report dictionary."""
        return asdict(self)


def build_final_integration_hardening_report(
    *,
    project_root: str | Path,
    patch_extract_root: str | Path | None = None,
) -> FinalIntegrationHardeningReport:
    """Build a read-only integration report for Workbench hardening gates."""
    root = Path(project_root).resolve()
    lfrp_root = root / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
    blockers: list[str] = []
    warnings: list[str] = []
    checked_files: list[str] = []
    line_counts: dict[str, int] = {}
    _check_required_files(lfrp_root, checked_files, line_counts, blockers)
    _check_gui_layout_safety(lfrp_root, blockers)
    checked_modules = _check_required_exports(blockers, warnings)
    if patch_extract_root is not None:
        _check_patch_script_text(Path(patch_extract_root).resolve(), blockers)
    status = "integration_hardening_pass" if not blockers else "integration_hardening_blocked"
    return FinalIntegrationHardeningReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FINAL_INTEGRATION_HARDENING_FEATURE_ID,
        status=status,
        project_root=str(root),
        checked_files=checked_files,
        checked_modules=checked_modules,
        line_counts=line_counts,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_final_integration_hardening_report(
    *,
    project_root: str | Path,
    output_dir: str | Path,
    patch_extract_root: str | Path | None = None,
) -> FinalIntegrationHardeningReport:
    """Write final integration hardening report under a caller-provided evidence root."""
    report = build_final_integration_hardening_report(
        project_root=project_root,
        patch_extract_root=patch_extract_root,
    )
    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / _REPORT_NAME).write_text(
        _json_dumps(report.to_dict()),
        encoding="utf-8",
    )
    return report


def _check_required_files(
    lfrp_root: Path,
    checked_files: list[str],
    line_counts: dict[str, int],
    blockers: list[str],
) -> None:
    """Check expected Workbench files and physical line-count hard limit."""
    if not lfrp_root.exists():
        blockers.append(f"LFRP_ROOT_MISSING:{lfrp_root}")
        return
    for filename in _REQUIRED_FILES:
        path = lfrp_root / filename
        if not path.exists():
            blockers.append(f"REQUIRED_FILE_MISSING:{filename}")
            continue
        text = path.read_text(encoding="utf-8")
        count = len(text.splitlines())
        checked_files.append(str(path))
        line_counts[filename] = count
        if count > 500:
            blockers.append(f"MODULE_TOO_LARGE:{filename}:{count}")
        if filename in _STRICT_SIZE_FILES and not 100 < count < 500:
            blockers.append(f"PATCH3_MODULE_SIZE_POLICY_VIOLATION:{filename}:{count}")


def _check_gui_layout_safety(lfrp_root: Path, blockers: list[str]) -> None:
    """Check GUI source for known PySide ownership regression patterns."""
    gui_path = lfrp_root / "workbench_gui.py"
    if not gui_path.exists():
        return
    text = gui_path.read_text(encoding="utf-8")
    for snippet in _PROHIBITED_GUI_SNIPPETS:
        if snippet in text:
            blockers.append(f"PROHIBITED_GUI_LAYOUT_SNIPPET:{snippet}")
    layout_path = lfrp_root / "workbench_gui_layout.py"
    if layout_path.exists():
        layout_text = layout_path.read_text(encoding="utf-8")
        if "QScrollArea" not in layout_text:
            blockers.append("WORKBENCH_SCROLL_AREA_HELPER_MISSING_QSCROLLAREA")


def _check_required_exports(blockers: list[str], warnings: list[str]) -> list[str]:
    """Import required non-GUI modules and verify compatibility exports."""
    checked: list[str] = []
    try:
        importlib.import_module(_PACKAGE)
        checked.append(_PACKAGE)
    except Exception as exc:  # pragma: no cover - failure details are evidence.
        blockers.append(f"PACKAGE_IMPORT_FAILED:{exc}")
    for module_name, names in _REQUIRED_EXPORTS.items():
        fqmn = f"{_PACKAGE}.{module_name}"
        try:
            module = importlib.import_module(fqmn)
            checked.append(fqmn)
        except Exception as exc:  # pragma: no cover - failure details are evidence.
            blockers.append(f"MODULE_IMPORT_FAILED:{module_name}:{exc}")
            continue
        for name in names:
            if not hasattr(module, name):
                blockers.append(f"REQUIRED_EXPORT_MISSING:{module_name}.{name}")
    if not _pyside_available():
        warnings.append("PYSIDE6_NOT_AVAILABLE_GUI_WIDGET_INSTANTIATION_SKIPPED")
    return checked


def _check_patch_script_text(patch_root: Path, blockers: list[str]) -> None:
    """Check patch scripts for control-character path regressions."""
    for script_name in ("INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"):
        path = patch_root / script_name
        if not path.exists():
            blockers.append(f"PATCH_SCRIPT_MISSING:{script_name}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for char in _PROHIBITED_SCRIPT_CHARS:
            if char.encode("utf-8").decode("unicode_escape") in text:
                blockers.append(f"PATCH_SCRIPT_CONTROL_CHARACTER:{script_name}:{char}")
        if "tools\validate" in text:
            blockers.append(f"PATCH_SCRIPT_ESCAPE_PRONE_TOOLS_PATH:{script_name}")


def _pyside_available() -> bool:
    """Return whether PySide6 can be imported in this environment."""
    try:
        importlib.import_module("PySide6")
        return True
    except Exception:
        return False


def _json_dumps(data: dict[str, Any]) -> str:
    """Return deterministic JSON text."""
    import json

    return json.dumps(data, indent=2, sort_keys=True) + "\n"
