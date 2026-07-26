# project-path: validation/test_architecture_review_large_file_refactor_workbench_intake_v1.py
"""Validate Large File Refactor Workbench intake shell contracts."""
from __future__ import annotations

import py_compile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "architecture-review-large-file-refactor-workbench-intake-v1"
MODULE_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture"
PKG_ROOT = MODULE_ROOT / "large_file_refactor_planner"

REQUIRED_FILES = [
    MODULE_ROOT / "architecture_review_subtabs.py",
    PKG_ROOT / "workbench_gui.py",
    PKG_ROOT / "workbench_plan_intake.py",
    PKG_ROOT / "workbench_formatting.py",
    PKG_ROOT / "source_apply_preflight_backup_contract.py",
]


def main() -> int:
    """Run focused source checks for the Workbench intake train."""
    _require_files()
    _check_subtab_registration()
    _check_workbench_contracts()
    _check_preflight_contract()
    _check_module_sizes()
    _py_compile_required()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


def _require_files() -> None:
    for path in REQUIRED_FILES:
        if not path.is_file():
            raise AssertionError(f"Required file missing: {path}")


def _check_subtab_registration() -> None:
    text = (MODULE_ROOT / "architecture_review_subtabs.py").read_text(encoding="utf-8")
    required = [
        "build_large_file_refactor_workbench_page",
        "Large File Refactor Workbench",
        "architecture_review_large_file_refactor_workbench_subtab_ear",
        "_architecture_review_refactor_workbench_page",
        "lambda: _activate_subtab(window, 3)",
    ]
    _require_text(text, required, "architecture_review_subtabs.py")


def _check_workbench_contracts() -> None:
    gui = (PKG_ROOT / "workbench_gui.py").read_text(encoding="utf-8")
    intake = (PKG_ROOT / "workbench_plan_intake.py").read_text(encoding="utf-8")
    formatting = (PKG_ROOT / "workbench_formatting.py").read_text(encoding="utf-8")
    _require_text(
        gui,
        [
            "build_large_file_refactor_workbench_page",
            "Load Latest Planner Plan",
            "Generate Real Preview",
            "Apply Source Changes",
            "setEnabled(False)",
        ],
        "workbench_gui.py",
    )
    _require_text(
        intake,
        [
            "WORKBENCH_FEATURE_ID",
            "TARGET_NOT_IN_WARNING_MODULE_TOO_LARGE_QUEUE",
            "STALE_SOURCE",
            "TARGET_INSIDE_REFERENCE_ROOT",
            "TARGET_INSIDE_PROTECTED_OUTPUT_ROOT",
            "SHIELDING_LOGIC_BLOCKS_CROSS_MODULE_CONTAMINATION",
            "source_mutation_enabled=False",
            "real_preview_generation_enabled=False",
        ],
        "workbench_plan_intake.py",
    )
    _require_text(formatting, ["format_workbench_intake"], "workbench_formatting.py")


def _check_preflight_contract() -> None:
    text = (PKG_ROOT / "source_apply_preflight_backup_contract.py").read_text(encoding="utf-8")
    _require_text(
        text,
        [
            "SourceApplyPreflightBackupContractResult",
            "build_source_apply_preflight_backup_contract",
            "write_source_apply_preflight_backup_contract_manifest",
            "apply_enabled=False",
            "source_mutation_enabled=False",
            "SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN_MISSING_OR_INVALID",
        ],
        "source_apply_preflight_backup_contract.py",
    )


def _check_module_sizes() -> None:
    for path in REQUIRED_FILES:
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count > 500:
            raise AssertionError(f"Module exceeds 500 physical lines: {path}={count}")


def _py_compile_required() -> None:
    for path in REQUIRED_FILES:
        py_compile.compile(str(path), doraise=True)


def _require_text(text: str, needles: list[str], label: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise AssertionError(f"Missing text in {label}: {missing}")


if __name__ == "__main__":
    raise SystemExit(main())
