"""Validate architecture warning classifier precision for governed KANDA code."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

__all__ = ["main"]

FEATURE_ID = "architecture-warning-classifier-precision-v1"
TARGET_WARNING_CODES = {
    "IMPORT_HEAVINESS_STARTUP",
    "MIXED_RESPONSIBILITY_FILE",
    "STALE_VARIANT_SOURCE_OF_TRUTH",
}


def require(condition: bool, message: str) -> None:
    """Raise when a focused validation requirement is not satisfied."""
    if not condition:
        raise AssertionError(message)


def load_architecture(root: Path):
    """Import the current architecture facade from the selected Tool root."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.manage_architecture import manage_architecture

    return manage_architecture


def module_fixture(architecture, path: str):
    """Return a minimal ModuleInfo fixture for classifier tests."""
    normalized = path.replace("\\", "/")
    module_id = normalized[:-3].replace("/", ".")
    filename = Path(normalized).name
    return architecture.ModuleInfo(
        module_id=module_id,
        package=module_id.rpartition(".")[0],
        path=normalized,
        filename=filename,
        is_init=False,
        is_helper=False,
        helper_group=None,
        line_count=20,
        docstring="",
        doc_meta={},
    )


def validate_governed_validator_classification(architecture) -> None:
    """Prove governed validator CLIs are not treated as public API owners."""
    tool_validator = module_fixture(
        architecture,
        "tools/validate_example_feature_v1.py",
    )
    script_repair = module_fixture(
        architecture,
        "scripts/repair_example_feature_v1.py",
    )
    normal_module = module_fixture(
        architecture,
        "package/validate_domain_value.py",
    )
    require(
        architecture.is_validator_script(tool_validator),
        "TOOLS_VALIDATOR_NOT_CLASSIFIED",
    )
    require(
        architecture.is_validator_script(script_repair),
        "SCRIPTS_REPAIR_NOT_CLASSIFIED",
    )
    require(
        not architecture.is_validator_script(normal_module),
        "NORMAL_MODULE_FALSE_VALIDATOR_CLASSIFICATION",
    )
    print("GOVERNED_VALIDATOR_CLASSIFICATION: PASS")


def validate_stale_variant_precision(architecture) -> None:
    """Preserve real stale detection while accepting active backup services."""
    require(
        not architecture._filename_has_stale_marker(
            "show_project_backup_service.py"
        ),
        "ACTIVE_BACKUP_SERVICE_FALSE_POSITIVE",
    )
    require(
        architecture._filename_has_stale_marker("old_backup_service.py"),
        "REAL_STALE_BACKUP_SIGNAL_LOST",
    )
    print("ACTIVE_BACKUP_SERVICE_CLASSIFICATION: PASS")
    print("REAL_STALE_VARIANT_SIGNAL_RETAINED: PASS")


def validate_mixed_responsibility_precision(architecture) -> None:
    """Accept declared adapters without suppressing unrelated mixed modules."""
    local_ai = module_fixture(
        architecture,
        "kanda_reasoner_app/local_ai_configuration.py",
    )
    workflow_adapter = module_fixture(
        architecture,
        "kanda_reasoner_app/manage_workflows/ai_review/adapter.py",
    )
    unrelated = module_fixture(architecture, "package/unrelated_service.py")
    local_domains = {"gui_ui": ["pyside6"], "ai_bridge": ["local_ai"]}
    workflow_domains = {
        "ai_bridge": ["local_ai"],
        "workflow_governance": ["manage_workflows"],
    }
    require(
        architecture._is_documented_mixed_responsibility_boundary(
            local_ai,
            local_domains,
        ),
        "LOCAL_AI_ADAPTER_BOUNDARY_NOT_RECOGNIZED",
    )
    require(
        architecture._is_documented_mixed_responsibility_boundary(
            workflow_adapter,
            workflow_domains,
        ),
        "WORKFLOW_AI_ADAPTER_BOUNDARY_NOT_RECOGNIZED",
    )
    require(
        not architecture._is_documented_mixed_responsibility_boundary(
            unrelated,
            local_domains,
        ),
        "UNRELATED_MIXED_MODULE_FALSE_EXEMPTION",
    )
    print("DOCUMENTED_MIXED_RESPONSIBILITY_BOUNDARIES: PASS")
    print("UNRELATED_MIXED_RESPONSIBILITY_NEGATIVE_FIXTURE: PASS")


def validate_gui_import_precision(architecture) -> None:
    """Accept known GUI owners while preserving a non-GUI negative fixture."""
    gui_module = module_fixture(
        architecture,
        "kanda_reasoner_app/project_structure_visualizer/web_runtime.py",
    )
    non_gui_module = module_fixture(
        architecture,
        "package/domain_service.py",
    )
    require(
        architecture._is_intentional_gui_import_surface(gui_module),
        "KNOWN_GUI_OWNER_NOT_RECOGNIZED",
    )
    require(
        not architecture._is_intentional_gui_import_surface(non_gui_module),
        "NON_GUI_MODULE_FALSE_GUI_EXEMPTION",
    )
    print("INTENTIONAL_GUI_IMPORT_OWNER_CLASSIFICATION: PASS")
    print("NON_GUI_IMPORT_NEGATIVE_FIXTURE: PASS")


def validate_full_architecture_scan(root: Path) -> None:
    """Run the current full scan and reject corrected warning families."""
    scanner = (
        root
        / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    )
    result = subprocess.run(
        [sys.executable, str(scanner), "--root", str(root), "--validate"],
        cwd=str(root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    output = result.stdout or ""
    require(result.returncode == 0, "FULL_ARCHITECTURE_SCAN_FAILED")
    for code in TARGET_WARNING_CODES:
        require(code not in output, code + "_REMAINS")
    for prefix in ("tools/validate_", "scripts/validate_"):
        fragment = "MISSING_PUBLIC_SURFACE_CONTROL " + prefix
        require(fragment not in output, fragment + " remains")
    print("IMPORT_HEAVINESS_STARTUP_FALSE_POSITIVES: 0")
    print("MIXED_RESPONSIBILITY_FALSE_POSITIVES: 0")
    print("STALE_BACKUP_SERVICE_FALSE_POSITIVES: 0")
    print("GOVERNED_VALIDATOR_PUBLIC_SURFACE_FALSE_POSITIVES: 0")



def validate_validator_hash_chain(root: Path) -> None:
    """Prove predecessor validator hashes follow the current warning owner."""
    split_path = (
        root
        / "tools/validate_manage_architecture_warning_policy_brick_wall_split_v1.py"
    )
    closure_path = (
        root
        / "tools/validate_architecture_public_surface_manifest_validator_all_closure_v1r2.py"
    )
    split_source = split_path.read_text(encoding="utf-8")
    closure_source = closure_path.read_text(encoding="utf-8")
    require(
        "06f5ff41d867a15bc7f56942bfc72b055729f3255d5cccdf135ec00458a48349"
        in split_source,
        "SPLIT_VALIDATOR_HELPER_HASH_NOT_RENEWED",
    )
    require(
        "b7f905d345979cb8c36edeb75ec41c07052834925a0a4d3d5112505ce07ce139"
        in split_source,
        "SPLIT_VALIDATOR_RECONSTRUCTED_HASH_NOT_RENEWED",
    )
    require(
        "_apply_governed_validator_classification_policy" in split_source,
        "SPLIT_VALIDATOR_POLICY_ORDER_NOT_RENEWED",
    )
    require(
        "58d51b4deb2804e7b2fba635f10728e45fb8f7231f274b4ad1347e148c259178"
        in closure_source,
        "CLOSURE_VALIDATOR_SPLIT_HASH_NOT_RENEWED",
    )
    require(
        "09d9be5b1079dd818b0a3a3afe8a120238746d5dbeb2afd8304db0145e8fe809"
        in closure_source,
        "CLOSURE_VALIDATOR_NON_ALL_HASH_NOT_RENEWED",
    )
    print("WARNING_POLICY_VALIDATOR_HASH_CHAIN: PASS")


def validate_module_sizes(root: Path) -> None:
    """Keep every touched Python module within the governed hard limit."""
    touched = (
        root
        / "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
        "source_loader_warning_policy_extended_private_impl.py",
        root
        / "tools/validate_manage_architecture_warning_policy_brick_wall_split_v1.py",
        root
        / "tools/validate_architecture_public_surface_manifest_validator_all_closure_v1r2.py",
        root / "tools/validate_architecture_warning_classifier_precision_v1.py",
    )
    for path in touched:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(line_count <= 500, "MODULE_TOO_LARGE: " + str(path))
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run focused warning-classifier precision validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", "--root", dest="root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        architecture = load_architecture(root)
        validate_governed_validator_classification(architecture)
        validate_stale_variant_precision(architecture)
        validate_mixed_responsibility_precision(architecture)
        validate_gui_import_precision(architecture)
        validate_full_architecture_scan(root)
        validate_validator_hash_chain(root)
        validate_module_sizes(root)
        print("VALIDATION OK: " + FEATURE_ID)
        print("STATUS: IN_SYNC")
        return 0
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
