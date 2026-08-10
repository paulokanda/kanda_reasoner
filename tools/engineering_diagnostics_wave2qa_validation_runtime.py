# project-path: tools/engineering_diagnostics_wave2qa_validation_runtime.py
"""Runtime validation support for Engineering Diagnostics Wave 2Q-A."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Iterable

__all__ = [
    "run_wave2qa_command",
    "run_wave2qa_focused_tests",
    "validate_wave2qa_deterministic_read_only",
    "validate_wave2qa_manual_grouping_disposable",
]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _optional_hash(path: Path) -> str:
    return _sha256(path) if path.is_file() else "ABSENT"


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


def run_wave2qa_command(
    command: list[str],
    *,
    cwd: Path,
    markers: Iterable[str] = (),
) -> str:
    """Run one validation command with explicit Project import authority."""
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        env=dict(
            os.environ,
            PYTHONDONTWRITEBYTECODE="1",
            PYTHONPATH=str(cwd),
        ),
    )
    output = completed.stdout or ""
    print(output, end="" if output.endswith("\n") else "\n")
    _require(
        completed.returncode == 0,
        "VALIDATION_COMMAND_FAILED:" + " ".join(command),
    )
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING:" + marker)
    return output


def run_wave2qa_focused_tests(root: Path) -> None:
    """Run the frozen predecessor tests plus Wave 2Q-A tests."""
    suites = (
        ("tests.test_reasoner_symbol_atlas_active_owner_filtering_wave2n", 7),
        ("tests.test_engineering_diagnostics_wave2oa", 13),
        ("tests.test_engineering_diagnostics_wave2ob", 8),
        ("tests.test_engineering_diagnostics_wave2oc", 13),
        ("tests.test_engineering_diagnostics_wave2od", 12),
        ("tests.test_engineering_diagnostics_wave2pa", 10),
        ("tests.test_engineering_diagnostics_wave2pb", 10),
        ("tests.test_engineering_diagnostics_wave2qa", 11),
        ("tests.test_engineering_diagnostics_wave2qa_gui_scale", 7),
    )
    for module, count in suites:
        run_wave2qa_command(
            [sys.executable, "-m", "unittest", "-v", module],
            cwd=root,
            markers=("Ran " + str(count) + " tests", "OK"),
        )
    print("WAVE2N ACTIVE OWNER FILTERING TESTS: 7/7 PASS")
    print("WAVE2OA FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WAVE2OB FOCUSED PUBLIC CONTRACT TESTS: 8/8 PASS")
    print("WAVE2OC FOCUSED PUBLIC CONTRACT TESTS: 13/13 PASS")
    print("WAVE2OD FOCUSED PUBLIC CONTRACT TESTS: 12/12 PASS")
    print("WAVE2PA FOCUSED PUBLIC CONTRACT TESTS: 10/10 PASS")
    print("WAVE2PB FOCUSED PUBLIC CONTRACT TESTS: 10/10 PASS")
    print("WAVE2QA FOCUSED PUBLIC CONTRACT TESTS: 18/18 PASS")
    print("FOCUSED PUBLIC CONTRACT TESTS: 91/91 PASS")


def _state_paths(root: Path) -> tuple[Path, Path, Path]:
    from kanda_reasoner_app.engineering_diagnostics import (
        engineering_diagnostics_database_path,
    )
    from kanda_reasoner_app.project_selection_registry import (
        ProjectSelectionRegistry,
    )

    registry = ProjectSelectionRegistry(tool_source_root=root)
    boundary = registry.resolve_boundary_for_root(root)
    database = engineering_diagnostics_database_path(boundary)
    freeze_root = (
        boundary.active_project_support_root
        / "project_freeze_after_update"
        / "frozen_features_memory"
    )
    return Path(registry.registry_path), database, freeze_root


def validate_wave2qa_deterministic_read_only(root: Path) -> None:
    """Prove deterministic grouping does not mutate live Project state."""
    from kanda_reasoner_app.engineering_diagnostics import (
        RUFF_PRODUCER_ID,
        DiagnosticFindingRecord,
        DiagnosticRunRecord,
        build_deterministic_diagnostic_groups,
    )

    registry, database, freeze_root = _state_paths(root)
    before = (
        _optional_hash(registry),
        _optional_hash(database),
        _tree_hash(freeze_root),
    )
    run = DiagnosticRunRecord(
        "wave2qa-read-only",
        "attempt",
        "project",
        "a" * 64,
        RUFF_PRODUCER_ID,
        "1.0",
        "scan-identity",
        "source",
        "scope",
        "config",
        1,
        "COMPLETED",
        2,
        "digest",
        "2026-08-06T00:00:00Z",
        "2026-08-06T00:00:01Z",
        {},
    )
    finding = DiagnosticFindingRecord(
        "wave2qa-read-only",
        "issue-a",
        "evidence-a",
        "F401",
        "pkg/a.py",
        "unused import",
        "warning",
        "high",
        "F401",
        "Module.target",
        "location-a",
        "ruff",
        1,
        {},
        "Review.",
    )
    findings = (finding, replace(finding, issue_fingerprint="issue-b"))
    groups = build_deterministic_diagnostic_groups(run, findings)
    _require(groups, "WAVE2QA_DETERMINISTIC_GROUPS_MISSING")
    _require(
        all(not group.evidence.get("root_cause_claimed") for group in groups),
        "WAVE2QA_ROOT_CAUSE_CLAIMED",
    )
    after = (
        _optional_hash(registry),
        _optional_hash(database),
        _tree_hash(freeze_root),
    )
    _require(before == after, "WAVE2QA_DETERMINISTIC_GROUPING_MUTATED_STATE")
    print("WAVE2QA DETERMINISTIC GROUPING: PASS")
    print("WAVE2QA CONFIRMED ROOT CAUSE CLAIMED: NO")
    print("WAVE2QA LIVE DIAGNOSTIC DATABASE MUTATED: NO")
    print("WAVE2QA LIVE FREEZE MEMORY MUTATED: NO")


def validate_wave2qa_manual_grouping_disposable(root: Path) -> None:
    """Exercise persistent grouping only under a disposable Project fixture."""
    from kanda_reasoner_app.engineering_diagnostics import (
        DiagnosticConflictError,
        EngineeringDiagnosticsStore,
    )
    from tools.engineering_diagnostics_wave2qa_fixture_support import (
        wave2qa_boundary_fixture,
        wave2qa_persisted_run_fixture,
    )

    with tempfile.TemporaryDirectory(prefix="wave2qa_manual_grouping_") as temporary:
        project = Path(temporary) / "project"
        project.mkdir()
        boundary = wave2qa_boundary_fixture(project)
        store = EngineeringDiagnosticsStore(boundary)
        run = wave2qa_persisted_run_fixture(store, boundary)
        finding = store.list_findings(boundary, run.run_id)[0]
        state = store.create_manual_group(
            boundary,
            run.run_id,
            label="Reviewed imports",
            author="validator",
            reason="Disposable grouping contract.",
            expected_generation=0,
        )
        state = store.assign_issue_to_manual_group(
            boundary,
            run.run_id,
            finding.issue_fingerprint,
            state.groups[0].group_id,
            author="validator",
            reason="Disposable assignment.",
            expected_generation=state.generation,
        )
        state = store.mark_manual_group_reviewed(
            boundary,
            run.run_id,
            state.groups[0].group_id,
            author="validator",
            reason="Disposable review.",
            expected_generation=state.generation,
        )
        _require(state.groups[0].review_state == "REVIEWED", "GROUP_REVIEW_FAILED")
        _require(len(state.decisions) == 3, "GROUP_DECISION_HISTORY_INCOMPLETE")
        try:
            store.create_manual_group(
                boundary,
                run.run_id,
                label="Stale",
                author="validator",
                reason="Expected rejection.",
                expected_generation=0,
            )
        except DiagnosticConflictError:
            pass
        else:
            raise RuntimeError("STALE_GROUPING_GENERATION_WAS_ACCEPTED")
    print("WAVE2QA MANUAL GROUPING DISPOSABLE STATE: PASS")
    print("WAVE2QA APPEND-ONLY DECISION HISTORY: PASS")
    print("WAVE2QA STALE GENERATION REJECTION: PASS")
    print("WAVE2QA PROJECT-SPECIFIC LIVE STATE WRITTEN: NO")
