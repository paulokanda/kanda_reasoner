"""Validate ownership of blocked-plan correction in the refactor workbench."""

from __future__ import annotations

import hashlib
import tempfile
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import sys
from types import ModuleType

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATHS = {
    "kanda_reasoner_app": PROJECT_ROOT / "kanda_reasoner_app",
    "kanda_reasoner_app.manage_architecture": PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture",
    "kanda_reasoner_app.manage_architecture.large_file_refactor_planner": PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner",
}
for package_name, package_path in PACKAGE_PATHS.items():
    package = ModuleType(package_name)
    package.__path__ = [str(package_path)]
    package.__package__ = package_name
    sys.modules.setdefault(package_name, package)

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_action_enablement import (
    build_planner_action_enablement,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (
    export_latest_planner_workbench_handoff,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_gui_progression import (
    build_workbench_gui_progression,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (
    build_workbench_plan_snapshot,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_snapshot_bridge import (
    load_latest_snapshot_into_workbench,
    materialize_workbench_owned_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_context import (
    stage_correction_needed,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _analysis(target: Path, source_hash: str) -> ModuleAnalysisReport:
    return ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        line_count_physical=620,
        module_docstring_present=True,
        module_docstring_preview="fixture",
        all_names=[],
        public_api_symbols=[],
        imports=[],
        symbols=[],
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
        risk_flags=[],
        analysis_errors=[],
    )


def _plan(target: Path, source_hash: str, *, status: str) -> RefactorPlan:
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        settings={
            "ideal_physical_lines": 400,
            "maximum_physical_lines": 499,
            "minimum_helper_physical_lines": 101,
        },
        public_api_before=[],
        public_api_after_expected=[],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[
            ProposedModule(
                schema_version=SCHEMA_VERSION,
                filename="fixture.py",
                role="public_facade",
                symbols=[],
                estimated_lines=180,
                status="planned",
            )
        ],
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=(
            ["FIXTURE_PLAN_BLOCKER"] if status == "blocked" else []
        ),
        status=status,
    )


def _snapshot(
    root: Path,
    *,
    status: str,
    candidate_path: str | None = None,
):
    target = root / "pkg" / "fixture.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("def fixture():\n    return 1\n", encoding="utf-8")
    source_hash = _sha256(target)
    window = SimpleNamespace(
        _large_file_refactor_last_plan=_plan(target, source_hash, status=status),
        _large_file_refactor_last_analysis=_analysis(target, source_hash),
        _large_file_refactor_planner_candidates=[
            SimpleNamespace(path=candidate_path or str(target))
        ],
    )
    return target, window, build_workbench_plan_snapshot(
        export_latest_planner_workbench_handoff(window)
    )


def _check_plan_actions() -> None:
    planned = build_planner_action_enablement(
        has_analysis=True,
        has_plan=True,
        plan_status="planned",
        has_preview=False,
        validation_passed=False,
        payload_status="",
        has_docstring_plan=False,
    )
    blocked = build_planner_action_enablement(
        has_analysis=True,
        has_plan=True,
        plan_status="blocked",
        has_preview=False,
        validation_passed=False,
        payload_status="",
        has_docstring_plan=False,
    )
    for state in (planned, blocked):
        assert state.generate_split_plan
        assert state.generate_docstring_plan
        assert state.run_llm_arbitration
    assert not blocked.generate_preview
    print("PLAN_ACTIONS_RECOVERY_BUTTONS_ENABLED_FOR_BLOCKED_PLAN: PASS")
    print("PLAN_ACTIONS_EMPTY_DOCSTRING_STATE_DOES_NOT_DISABLE_LOCAL_AI_ACTION: PASS")
    print("BLOCKED_PLAN_PREVIEW_REMAINS_DISABLED_IN_PLANNER: PASS")




def _check_plan_action_click_paths() -> None:
    planner_root = (
        PROJECT_ROOT
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
    )
    gui = (planner_root / "gui_shell.py").read_text(encoding="utf-8")
    projection = (planner_root / "planner_status_projection.py").read_text(
        encoding="utf-8"
    )
    assert "if report is None or plan is None or not proposals:" not in gui
    web_start = projection.index("web_ready = bool(")
    web_end = projection.index("    )", web_start)
    web_block = projection[web_start:web_end]
    assert "exchange_base.docstring_proposals" not in web_block
    print("PLAN_ACTIONS_LOCAL_AI_EMPTY_DOCSTRING_CLICK_PATH: PASS")
    print("PLAN_ACTIONS_WEB_AI_COPY_EMPTY_DOCSTRING_PATH: PASS")


def _check_correction_only_ownership() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        _target, window, snapshot = _snapshot(root, status="blocked")
        intake = build_workbench_plan_intake(
            snapshot=snapshot,
            active_project_root=str(root),
        )
        assert intake.status == "plan_intake_correction_ready"
        assert intake.workbench_snapshot_owned
        assert not intake.ready_for_real_preview
        assert not intake.source_mutation_enabled
        assert not intake.real_preview_generation_enabled
        assert intake.blockers == ["PLANNER_PLAN_BLOCKED"]
        assert "PLANNER_PLAN_OWNED_FOR_CORRECTION_ONLY" in intake.warnings
        print("BLOCKED_PLAN_CORRECTION_ONLY_OWNERSHIP: PASS")

        progression = build_workbench_gui_progression(intake=intake)
        assert not progression.dependency_analysis_enabled
        assert not progression.real_preview_enabled
        assert not progression.preflight_enabled
        print("CORRECTION_ONLY_OWNERSHIP_KEEPS_EXECUTION_STAGES_CLOSED: PASS")

        bridge_window = window
        result, message = load_latest_snapshot_into_workbench(
            bridge_window,
            str(root),
        )
        assert result is not None
        assert result.status == "plan_intake_correction_ready"
        assert message == ""
        owned = materialize_workbench_owned_plan(bridge_window)
        assert owned is not None and owned.status == "blocked"
        bridge_window._large_file_refactor_workbench_intake = result
        assert stage_correction_needed(
            bridge_window,
            "PLAN_INTAKE",
            str(root),
        )
        print("PLANNER_HANDOFF_BLOCKED_PLAN_ACCEPTED_FOR_CORRECTION_LANE: PASS")
        print("PLAN_INTAKE_CORRECTION_ROUTES_BECOME_ELIGIBLE: PASS")


def _check_shields() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        target, _window, snapshot = _snapshot(root, status="blocked")

        target.write_text("def fixture():\n    return 2\n", encoding="utf-8")
        stale = build_workbench_plan_intake(
            snapshot=snapshot,
            active_project_root=str(root),
        )
        assert stale.status == "blocked"
        assert not stale.workbench_snapshot_owned
        assert "STALE_SOURCE" in stale.blockers
        print("STALE_SOURCE_STILL_REJECTED_BEFORE_WORKBENCH_OWNERSHIP: PASS")

    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
        root = Path(tmp).resolve()
        _target, _window, snapshot = _snapshot(root, status="blocked")
        wrong_root = build_workbench_plan_intake(
            snapshot=snapshot,
            active_project_root=str(Path(other).resolve()),
        )
        assert wrong_root.status == "blocked"
        assert not wrong_root.workbench_snapshot_owned
        assert "TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT" in wrong_root.blockers
        print("BOX_ROOT_SHIELD_STILL_REJECTS_CROSS_PROJECT_TARGET: PASS")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        target, _window, snapshot = _snapshot(
            root,
            status="blocked",
            candidate_path=str(root / "pkg" / "different.py"),
        )
        queue_mismatch = build_workbench_plan_intake(
            snapshot=snapshot,
            active_project_root=str(root),
        )
        assert target.is_file()
        assert queue_mismatch.status == "blocked"
        assert not queue_mismatch.workbench_snapshot_owned
        assert "TARGET_NOT_IN_WARNING_MODULE_TOO_LARGE_QUEUE" in queue_mismatch.blockers
        print("WARNING_QUEUE_SHIELD_STILL_REJECTS_CROSS_MODULE_CONTAMINATION: PASS")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        _target, _window, snapshot = _snapshot(root, status="blocked")
        tampered = replace(snapshot, snapshot_hash="0" * 64)
        mismatch = build_workbench_plan_intake(
            snapshot=tampered,
            active_project_root=str(root),
        )
        assert mismatch.status == "blocked"
        assert not mismatch.workbench_snapshot_owned
        assert "WORKBENCH_SNAPSHOT_HASH_MISMATCH" in mismatch.blockers
        print("SNAPSHOT_INTEGRITY_SHIELD_STILL_FAILS_CLOSED: PASS")


def _check_planned_handoff_unchanged() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        _target, window, _snapshot_value = _snapshot(root, status="planned")
        intake, message = load_latest_snapshot_into_workbench(window, str(root))
        assert intake is not None
        assert intake.status == "plan_intake_ready"
        assert intake.workbench_snapshot_owned
        assert intake.ready_for_real_preview
        assert message == ""
        print("PLANNED_PLAN_NORMAL_WORKBENCH_HANDOFF_PRESERVED: PASS")


def main() -> int:
    _check_plan_actions()
    _check_plan_action_click_paths()
    _check_correction_only_ownership()
    _check_shields()
    _check_planned_handoff_unchanged()
    print("BOX_SHIELD_NO_LEAK_BOUNDARY_PRESERVED: PASS")
    print("VALIDATION OK: planner-workbench-blocked-plan-correction-ownership-v3")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
