# project-path: tools/engineering_diagnostics_wave2qb_validation_runtime.py
"""Runtime validation support for Engineering Diagnostics Wave 2Q-B."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys

from tools.engineering_diagnostics_wave2qa_validation_runtime import (
    run_wave2qa_command,
    run_wave2qa_focused_tests,
)

__all__ = [
    "run_wave2qb_focused_tests",
    "validate_wave2qb_shadow_read_only",
]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    if not path.is_file():
        return "ABSENT"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_hash(path: Path) -> str:
    if not path.exists():
        return "ABSENT"
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(_sha256(item).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def run_wave2qb_focused_tests(root: Path) -> None:
    """Run all frozen predecessors and the complete Wave 2Q-B suite."""
    run_wave2qa_focused_tests(root)
    run_wave2qa_command(
        [sys.executable, "-m", "unittest", "-v", "tests.test_engineering_diagnostics_wave2qb"],
        cwd=root,
        markers=("Ran 11 tests", "OK"),
    )
    run_wave2qa_command(
        [sys.executable, "-m", "unittest", "-v", "tests.test_engineering_diagnostics_wave2qb_gui_scale"],
        cwd=root,
        markers=("Ran 6 tests", "OK"),
    )
    print("WAVE2QB FOCUSED PUBLIC CONTRACT TESTS: 17/17 PASS")
    print("FOCUSED PUBLIC CONTRACT TESTS: 108/108 PASS")


def validate_wave2qb_shadow_read_only(root: Path) -> int:
    """Run the real public Shadow audit and prove no live state mutation."""
    from kanda_reasoner_app.engineering_diagnostics import (
        build_shadow_diagnostic_run,
        collect_shadow_findings,
        engineering_diagnostics_database_path,
    )
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    registry = Path(ProjectSelectionRegistry(tool_source_root=root).registry_path)
    database = engineering_diagnostics_database_path(boundary)
    freeze_root = (
        boundary.active_project_support_root
        / "project_freeze_after_update"
        / "frozen_features_memory"
    )
    before = (_sha256(registry), _sha256(database), _tree_hash(freeze_root))
    collection = collect_shadow_findings(root)
    run = build_shadow_diagnostic_run(
        collection,
        boundary=boundary,
        attempt_id="wave2qb-live-read-only",
        source_fingerprint="validation-source-fingerprint",
        operation_generation=1,
    )
    _require(run.findings == tuple(run.findings), "WAVE2QB_RUN_IMMUTABILITY_FAILURE")
    after = (_sha256(registry), _sha256(database), _tree_hash(freeze_root))
    _require(before == after, "WAVE2QB_SHADOW_COLLECTION_MUTATED_LIVE_STATE")
    print("WAVE2QB LIVE SHADOW PUBLIC AUDIT: PASS")
    print("WAVE2QB LIVE SHADOW FINDING COUNT: " + str(len(run.findings)))
    print("WAVE2QB SHADOW COLLECTION SOURCE MUTATED: NO")
    print("WAVE2QB LIVE DIAGNOSTIC DATABASE MUTATED: NO")
    print("WAVE2QB LIVE FREEZE MEMORY MUTATED: NO")
    return len(run.findings)
