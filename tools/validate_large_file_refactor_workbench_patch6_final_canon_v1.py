# project-path: tools/validate_large_file_refactor_workbench_patch6_final_canon_v1.py
"""Validate Patch 6 tutorial, protocol canon, and final closure report."""
from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.final_complete_workbench_freeze import (  # noqa: E402
    build_complete_workbench_freeze_report,
    write_complete_workbench_freeze_report,
)

FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-"
    "patch6-final-canon-closure-v1"
)
MAIN_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-"
    "patch6-controlled-real-module-final-canon-v1"
)

_TUTORIAL = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
    / "LARGE_FILE_REFACTOR_WORKBENCH_TUTORIAL.md"
)
_PROTOCOL = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_library"
    / "ACTIVE_PROMPTS"
    / "06_refactor_and_architecture_hardening"
    / "large_module_refactor_protocol.md"
)
_METADATA = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_library"
    / "METADATA"
    / "large_module_refactor_protocol.meta.json"
)

_PATCH6_SOURCE_FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_symbol_source_extractor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_facade_global_import_inserter.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_real_preview_writer.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/real_preview_structural_validator.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/final_complete_workbench_freeze.py",
    "tools/patch6_controlled_real_module_support.py",
    "tools/validate_large_file_refactor_workbench_patch6_controlled_real_module_v1.py",
    "tools/validate_large_file_refactor_workbench_patch6_final_canon_v1.py",
]


def run_validation() -> None:
    """Validate final documentation, strict source sizing, and closure evidence."""
    _validate_tutorial()
    print("FINAL_TUTORIAL: PASS")
    _validate_protocol_canon()
    print("FINAL_CANON_PROTOCOL_V7_4: PASS")
    _validate_routing_sync()
    print("FINAL_CANON_ROUTING_SYNC_V7_4: PASS")
    _validate_patch6_source_sizes()
    print("PATCH6_SOURCE_SIZE_POLICY_101_499: PASS")
    report = build_complete_workbench_freeze_report(
        active_project_root=str(PROJECT_ROOT),
    )
    if report.status != "complete_workbench_freeze_ready" or report.blockers:
        raise AssertionError(
            "FINAL_CLOSURE_REPORT_BLOCKED:" + "|".join(report.blockers)
        )
    if not (
        report.real_apply_executor_proven
        and report.rollback_restoration_proven
        and report.second_apply_proven
        and report.live_source_unchanged_during_controlled_proof
    ):
        raise AssertionError("FINAL_CLOSURE_PROOF_FLAGS_NOT_COMPLETE")
    write_complete_workbench_freeze_report(report)
    print("FINAL_CLOSURE_REPORT: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"VALIDATION OK: {MAIN_FEATURE_ID}")


def _validate_tutorial() -> None:
    """Require final tutorial ownership, safety, and completion contracts."""
    if not _TUTORIAL.is_file():
        raise AssertionError("FINAL_WORKBENCH_TUTORIAL_MISSING")
    text = _TUTORIAL.read_text(encoding="utf-8")
    required = [
        "100 < physical_lines < 500",
        "Refactor Large Module",
        "Semantic Diff",
        "Shadow provenance proof",
        "INTENT_RECORDED",
        "ROLLBACK_CONFLICT",
        "COMPLETED_VALIDATED",
        "6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55",
        "197",
        "145",
        "429",
    ]
    missing = [marker for marker in required if marker not in text]
    if missing:
        raise AssertionError("FINAL_TUTORIAL_MARKERS_MISSING:" + "|".join(missing))


def _validate_protocol_canon() -> None:
    """Require final protocol precedence and v7.4 metadata identity."""
    text = _PROTOCOL.read_text(encoding="utf-8")
    required = [
        "Final Large File Refactor Planner -> Workbench execution canon (v7.4)",
        "100 < physical_lines < 500",
        "There are no facade, package-marker, constants, adapter, generated-validator, or structural-role exceptions",
        "Refactor Large Module",
        "Journaled serial-lane exact-byte apply",
        "Rollback verifies current hashes",
        "controlled proof target",
    ]
    missing = [marker for marker in required if marker not in text]
    if missing:
        raise AssertionError("FINAL_PROTOCOL_MARKERS_MISSING:" + "|".join(missing))
    metadata = json.loads(_METADATA.read_text(encoding="utf-8"))
    if metadata.get("version") != "7.4":
        raise AssertionError("FINAL_PROTOCOL_METADATA_VERSION_NOT_7_4")
    if metadata.get("updated_for") != "large-file-refactor-workbench-final-canon-v7-4":
        raise AssertionError("FINAL_PROTOCOL_METADATA_UPDATED_FOR_MISMATCH")



def _validate_routing_sync() -> None:
    """Require active routing surfaces to reference the final v7.4 protocol."""
    root = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library"
    files = [
        root / "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
        root / "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md",
        root / "ROUTING/PROMPT_NAVIGATION_INDEX.md",
    ]
    for path in files:
        text = path.read_text(encoding="utf-8")
        if "v7.4" not in text:
            raise AssertionError("FINAL_ROUTING_V7_4_MARKER_MISSING:" + str(path))
    routing = json.loads((root / "ROUTING/prompt_navigation_index.json").read_text(encoding="utf-8"))
    match = next(
        (item for item in routing.get("entries", []) if item.get("prompt_id") == "large_module_refactor_protocol"),
        None,
    )
    if match is None or "v7.4" not in str(match.get("display_name", "")):
        raise AssertionError("FINAL_ROUTING_JSON_PROTOCOL_VERSION_NOT_V7_4")
    template_meta = json.loads(
        (root / "METADATA/large_module_refactor_template.meta.json").read_text(encoding="utf-8")
    )
    if template_meta.get("aligned_with") != "large_module_refactor_protocol_v7.4":
        raise AssertionError("FINAL_TEMPLATE_NOT_ALIGNED_WITH_PROTOCOL_V7_4")

def _validate_patch6_source_sizes() -> None:
    """Enforce strict physical-line policy for every Patch 6 Python source file."""
    for relative in _PATCH6_SOURCE_FILES:
        path = PROJECT_ROOT / relative
        if not path.is_file():
            raise AssertionError("PATCH6_SOURCE_FILE_MISSING:" + relative)
        lines = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        if not 100 < lines < 500:
            raise AssertionError(f"PATCH6_SOURCE_SIZE_POLICY_FAILED:{relative}:{lines}")


if __name__ == "__main__":
    run_validation()
