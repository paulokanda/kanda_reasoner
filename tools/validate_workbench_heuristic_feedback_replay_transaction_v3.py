"""Focused validation for feedback-aware transactional Heuristic stage replay v3."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "architecture-review-workbench-heuristic-feedback-replay-transaction-v3"
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def _text(name: str) -> str:
    return (PKG / name).read_text(encoding="utf-8")


def _static_checks() -> None:
    split = _text("split_planner.py")
    search = _text("workbench_heuristic_feedback_search.py")
    service = _text("workbench_stage_correction_service.py")
    controller = _text("workbench_heuristic_correction_qt_controller.py")

    assert 'preferred_strategy: str = ""' in split
    assert "_prefer_candidate_strategy" in split
    print("FEEDBACK_AWARE_ALTERNATE_STRATEGY_SUPPORT: PASS")

    assert "context.blockers" in search
    assert "REPLAY_TARGET_STAGE" in search
    assert "if replay.passed" in search
    assert "current blocked Workbench snapshot was preserved" in search
    print("BLOCKER_CONTEXT_DRIVES_BOUNDED_SEARCH: PASS")

    assert "build_workbench_dependency_readiness" in search
    assert "build_and_write_real_preview" in search
    assert "validate_real_preview_structure" in search
    assert "build_and_write_preflight_backup_readiness" in search
    assert "build_and_write_source_apply_payload" in search
    print("SEQUENTIAL_TARGET_STAGE_REPLAY_CHAIN: PASS")

    assert "or not candidate.replay.passed" in service
    assert "_apply_replay_state" in service
    assert "TARGET STAGE PASS" in service
    print("COMMIT_ONLY_AFTER_TARGET_STAGE_PASS: PASS")

    gui = _text("workbench_stage_correction_gui.py")
    gui_tree = ast.parse(gui)
    gui_functions = {
        node.name for node in gui_tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "render_replay" in controller
    assert "result.replay is not None" in controller
    assert "_render_replay_evidence" in gui_functions
    assert "render_replay=_render_replay_evidence" in gui
    assert "format_real_preview_result(preview)" in gui
    assert "preview_validation_guidance(preview)" in gui
    print("REPLAY_RENDERER_SYMBOL_DEFINED_AND_BOUND: PASS")
    print("GUI_RENDERS_ACCEPTED_REPLAY_EVIDENCE: PASS")

    combined = search + service + controller
    forbidden = ("setEnabled(True)", "status = 'passed'", 'status = "passed"')
    assert not any(item in combined for item in forbidden)
    print("NO_FORCE_ENABLE_OR_SYNTHETIC_PASS: PASS")


def _dynamic_search_checks() -> None:
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
        workbench_heuristic_feedback_search as module,
    )

    original = {
        name: getattr(module, name)
        for name in (
            "analyze_python_file",
            "_settings_from_plan",
            "_settings_variants",
            "_strategy_order",
            "build_split_plan",
            "build_docstring_proposals",
            "attach_docstring_proposals_to_plan",
            "_replay_candidate",
        )
    }
    try:
        module.analyze_python_file = lambda _path: SimpleNamespace(name="report")
        module._settings_from_plan = lambda _plan: SimpleNamespace()
        module._settings_variants = lambda _base, _context: [("original_settings", SimpleNamespace())]
        module._strategy_order = lambda _plan, _context: ("responsibility_dominant", "dependency_dominant")

        def build_plan(_report, _settings, source_path=None, preferred_strategy=""):
            return _Plan(preferred_strategy)

        module.build_split_plan = build_plan
        module.build_docstring_proposals = lambda _report, _plan: []
        module.attach_docstring_proposals_to_plan = lambda plan, _props: plan

        replay_calls: list[str] = []

        def replay(**kwargs):
            strategy = kwargs["strategy"]
            replay_calls.append(strategy)
            return module.WorkbenchCorrectionReplayEvidence(
                target_stage="REAL_PREVIEW",
                passed=strategy == "dependency_dominant",
                reached_stage="REAL_PREVIEW",
                strategy=strategy,
                settings_label=kwargs["settings_label"],
                blockers=() if strategy == "dependency_dominant" else ("PREVIEW_BLOCKER",),
            )

        module._replay_candidate = replay
        context = SimpleNamespace(
            target_file="target.py",
            stage="REAL_PREVIEW",
            blockers=("PREVIEW_BLOCKER",),
            active_project_root="project",
        )
        result = module.search_feedback_aware_heuristic_correction(
            plan=_Plan("current"),
            context=context,
        )
        assert result.ok
        assert result.strategy == "dependency_dominant"
        assert replay_calls[-1] == "dependency_dominant"
        print("FAILED_VARIANT_SKIPPED_PASSING_VARIANT_SELECTED: PASS")

        module._replay_candidate = lambda **kwargs: module.WorkbenchCorrectionReplayEvidence(
            target_stage="REAL_PREVIEW",
            passed=False,
            reached_stage="REAL_PREVIEW",
            strategy=kwargs["strategy"],
            settings_label=kwargs["settings_label"],
            blockers=("STILL_BLOCKED",),
        )
        failed = module.search_feedback_aware_heuristic_correction(
            plan=_Plan("current"),
            context=context,
        )
        assert not failed.ok
        assert failed.corrected_plan is None
        assert "snapshot was preserved" in failed.message
        print("NO_PASSING_CANDIDATE_PRESERVES_CURRENT_SNAPSHOT: PASS")
    finally:
        for name, value in original.items():
            setattr(module, name, value)


def _line_count_checks() -> None:
    touched = (
        "split_planner.py",
        "workbench_heuristic_feedback_search.py",
        "workbench_stage_correction_service.py",
        "workbench_stage_correction_gui.py",
        "workbench_heuristic_correction_qt_controller.py",
        "workbench_heuristic_correction_qt_worker.py",
    )
    for name in touched:
        count = len(_text(name).splitlines())
        assert count <= 500, f"{name} has {count} lines"
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


class _Plan:
    def __init__(self, strategy: str):
        self.strategy = strategy
        self.docstring_proposals = []
        self.import_migration = {
            "heuristic_candidate_selection": {"selected_strategy": strategy}
        }

    def to_dict(self):
        return {"strategy": self.strategy}


def main() -> None:
    _static_checks()
    _dynamic_search_checks()
    _line_count_checks()
    print("WORKBENCH_HEURISTIC_FEEDBACK_REPLAY_TRANSACTION: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
