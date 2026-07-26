# project-path: tools/validate_test_protection_gap_precision_heuristic_v1.py
"""Validate the high-confidence TEST_PROTECTION_GAP precision heuristic."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import py_compile
import subprocess
import sys
import zipfile

__all__ = [
    "main",
]

FEATURE_ID = "test-protection-gap-precision-heuristic-v1"
SHARD_PREFIX = (
    "kanda_reasoner_app/manage_architecture/manage_architecture_help/"
    "manage_architecture_source_part_"
)
KNOWN_FALSE_POSITIVE_PATHS = {
    "_reasoner_tools_gui_engineering_safety_panel_catalog.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_persistence.py",
    "kanda_reasoner_app/error_memory_gui/_ai_corrector_service.py",
    "kanda_reasoner_app/error_memory_gui/_ai_evidence_recovery.py",
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_duplicate_match_keys.py",
    "kanda_reasoner_app/error_memory_gui/_duplicate_pending_cleanup.py",
    "kanda_reasoner_app/error_memory_gui/_lesson_status_summary.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_window_sync.py",
    "kanda_reasoner_app/freeze_hint_intake/form_text_validation.py",
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
    "kanda_reasoner_app/manage_architecture/ast_split_web_ai_gui.py",
}


def require(condition: bool, message: str) -> None:
    """Raise an assertion when a validation condition is not met."""
    if not condition:
        raise AssertionError(message)


def parse_args() -> argparse.Namespace:
    """Parse validator arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip")
    return parser.parse_args()


def validate_zip_contract(patch_zip: Path | None) -> None:
    """Validate the governed patch ZIP when supplied."""
    if patch_zip is None:
        print("ZIP CONTRACT: NOT_REQUESTED")
        return
    require(patch_zip.is_file(), "patch ZIP is missing")
    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = archive.namelist()
        required = {
            "INSTALL.ps1",
            "VALIDATE.ps1",
            "FREEZE.ps1",
            "PACKAGE_MANIFEST.json",
            "KANDA_FREEZE_HINT.json",
        }
        require(required.issubset(names), "patch ZIP root contract is incomplete")
        require(
            "workbench/_bundle_temp/"
            "BUNDLE_MANIFEST_test_protection_gap_precision_heuristic_v1.txt"
            in names,
            "bundle manifest is missing",
        )
        sidecar = json.loads(archive.read("KANDA_FREEZE_HINT.json"))
        require(
            sidecar.get("feature_id") == FEATURE_ID,
            "freeze hint feature_id mismatch",
        )
        for name in names:
            normalized = name.replace("\\", "/")
            parts = normalized.split("/")
            require(not normalized.startswith("/"), "absolute ZIP member")
            require(".." not in parts, "parent traversal ZIP member")
    print("ZIP CONTRACT: PASS")


def load_architecture_module(project_root: Path):
    """Import the architecture module from the selected project root."""
    root_text = str(project_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.manage_architecture import manage_architecture

    return manage_architecture


def make_module(module_type, **overrides):
    """Build a synthetic ModuleInfo with deterministic defaults."""
    values = {
        "module_id": "sample_pkg.owner",
        "package": "sample_pkg",
        "path": "sample_pkg/owner.py",
        "filename": "owner.py",
        "is_init": False,
        "is_helper": False,
        "helper_group": None,
        "line_count": 240,
        "docstring": "",
        "doc_meta": {},
        "imports": [],
        "public_symbols": ["Owner", "apply_change", "save_change"],
        "has_explicit_all": True,
        "all_symbols": ["Owner", "apply_change", "save_change"],
        "top_level_imported_symbols": [],
        "direct_internal_imports": [],
        "used_by": ["sample_pkg.a", "sample_pkg.b", "sample_pkg.c"],
    }
    values.update(overrides)
    return module_type(**values)


def validate_synthetic_precision(module) -> None:
    """Prove broad filename and __all__ signals no longer trigger alone."""
    module_type = module.ModuleInfo
    rejected = {
        "filename_marker_only": make_module(
            module_type,
            path="sample_pkg/engine_catalog.py",
            filename="engine_catalog.py",
            public_symbols=[],
            has_explicit_all=False,
            all_symbols=[],
        ),
        "explicit_all_builder_only": make_module(
            module_type,
            path="sample_pkg/payload_builder.py",
            filename="payload_builder.py",
            public_symbols=["Payload", "build_payload"],
            all_symbols=["Payload", "build_payload"],
        ),
        "private_module": make_module(
            module_type,
            path="sample_pkg/_mutation_service.py",
            filename="_mutation_service.py",
        ),
        "root_module": make_module(
            module_type,
            module_id="root_engine",
            package="",
            path="root_engine.py",
            filename="root_engine.py",
        ),
        "tool_module": make_module(
            module_type,
            module_id="tools.apply_tool",
            package="tools",
            path="tools/apply_tool.py",
            filename="apply_tool.py",
        ),
        "small_mutation_owner": make_module(
            module_type,
            path="sample_pkg/project_mutation_lane.py",
            filename="project_mutation_lane.py",
            line_count=90,
        ),
        "single_consumer": make_module(
            module_type,
            path="sample_pkg/project_mutation_lane.py",
            filename="project_mutation_lane.py",
            used_by=["sample_pkg.a"],
        ),
        "model_module": make_module(
            module_type,
            path="sample_pkg/mutation_models.py",
            filename="mutation_models.py",
            public_symbols=["MutationRecord", "MutationState"],
            all_symbols=["MutationRecord", "MutationState"],
        ),
    }
    for name, candidate in rejected.items():
        require(
            not module._looks_like_important_owner_module(candidate),
            "false positive heuristic case: " + name,
        )

    accepted = {
        "strong_mutation_owner": make_module(
            module_type,
            path="sample_pkg/project_mutation_lane.py",
            filename="project_mutation_lane.py",
            public_symbols=[
                "MutationPort",
                "MutationRequest",
                "ProjectMutationLaneStore",
            ],
            all_symbols=[
                "MutationPort",
                "MutationRequest",
                "ProjectMutationLaneStore",
            ],
        ),
        "destructive_store": make_module(
            module_type,
            path="sample_pkg/store.py",
            filename="store.py",
            line_count=170,
            public_symbols=["Store", "delete_item", "save_item"],
            all_symbols=["Store", "delete_item", "save_item"],
        ),
        "rollback_bridge": make_module(
            module_type,
            path="sample_pkg/completion_apply_bridge.py",
            filename="completion_apply_bridge.py",
            line_count=170,
            public_symbols=[
                "CompletionResult",
                "execute_completion_transaction",
                "rollback_completion_transaction",
            ],
            all_symbols=[
                "CompletionResult",
                "execute_completion_transaction",
                "rollback_completion_transaction",
            ],
        ),
    }
    for name, candidate in accepted.items():
        require(
            module._looks_like_important_owner_module(candidate),
            "real high-risk case was missed: " + name,
        )
        evidence = module._test_protection_candidate_evidence(candidate)
        require(evidence, "accepted case has no evidence: " + name)
    print("PRECISION_HEURISTIC_SYNTHETIC_CASES: PASS")


def validate_source_shards(project_root: Path) -> None:
    """Compile and enforce line and ASCII limits for source shards."""
    for index in range(1, 22):
        relative = Path(SHARD_PREFIX + str(index) + "_private_impl.py")
        path = project_root / relative
        require(path.is_file(), "missing source shard: " + str(relative))
        text = path.read_text(encoding="utf-8")
        require(text.isascii(), "non-ASCII source shard: " + str(relative))
        require(
            len(text.splitlines()) <= 500,
            "source shard exceeds 500 lines: " + str(relative),
        )
        py_compile.compile(str(path), doraise=True)
    validator = project_root / "tools/validate_test_protection_gap_precision_heuristic_v1.py"
    py_compile.compile(str(validator), doraise=True)
    require(
        len(validator.read_text(encoding="utf-8").splitlines()) <= 500,
        "focused validator exceeds 500 lines",
    )
    print("SOURCE_SHARDS_COMPILE_AND_SIZE: PASS")


def validate_real_project_scan(project_root: Path) -> None:
    """Run the complete audit and verify only high-confidence gaps remain."""
    validator = (
        project_root
        / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    )
    result = subprocess.run(
        [
            sys.executable,
            str(validator),
            "--root",
            str(project_root),
            "--validate",
        ],
        cwd=str(project_root),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require("Errors: 0" in output, "architecture validation reported errors")
    warning_lines = [
        line
        for line in output.splitlines()
        if line.startswith("WARNING TEST_PROTECTION_GAP")
    ]
    require(warning_lines, "no real high-confidence gap remained")
    require(len(warning_lines) <= 25, "precision warning count exceeds 25")
    require(
        not any("suppressed after" in line for line in warning_lines),
        "test-protection suppression marker remains",
    )
    require(
        all("High-confidence mutation or persistence owner" in line for line in warning_lines),
        "legacy broad warning wording remains",
    )
    for false_path in KNOWN_FALSE_POSITIVE_PATHS:
        require(
            not any(false_path in line for line in warning_lines),
            "known false positive remains: " + false_path,
        )
    require(
        any(
            "kanda_reasoner_app/engineering_safety/project_mutation_lane.py"
            in line
            for line in warning_lines
        ),
        "known real mutation owner was not retained",
    )
    print("TEST_PROTECTION_GAP_WARNING_COUNT: " + str(len(warning_lines)))
    print("KNOWN_FALSE_POSITIVES_REMOVED: PASS")
    print("REAL_MUTATION_OWNER_RETAINED: PASS")
    print("ARCHITECTURE_ERROR_COUNT: 0")


def main() -> int:
    """Run the complete focused validation."""
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    patch_zip = Path(args.patch_zip).expanduser().resolve() if args.patch_zip else None
    validate_zip_contract(patch_zip)
    validate_source_shards(project_root)
    module = load_architecture_module(project_root)
    validate_synthetic_precision(module)
    validate_real_project_scan(project_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
