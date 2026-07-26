# project-path: validation/test_large_file_refactor_planner_button_state_recovery_v1.py
"""Focused validation for Planner action enablement and blocked-plan recovery."""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

FEATURE_ID = "large-file-refactor-planner-button-state-recovery-v1"


def _load_enablement_module(project_root: Path) -> object:
    path = project_root / (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "planner_action_enablement.py"
    )
    spec = importlib.util.spec_from_file_location("planner_action_enablement_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _assert_enablement_contracts(project_root: Path) -> None:
    module = _load_enablement_module(project_root)
    build = module.build_planner_action_enablement

    after_analysis = build(
        has_analysis=True,
        has_plan=False,
        plan_status="",
        has_preview=False,
        validation_passed=False,
        payload_status="",
    )
    assert after_analysis.generate_split_plan is True
    assert after_analysis.generate_docstring_plan is True
    assert after_analysis.run_llm_arbitration is False
    assert after_analysis.generate_preview is False

    blocked_plan = build(
        has_analysis=True,
        has_plan=True,
        plan_status="blocked",
        has_preview=False,
        validation_passed=False,
        payload_status="",
    )
    assert blocked_plan.generate_split_plan is True
    assert blocked_plan.generate_docstring_plan is True
    assert blocked_plan.run_llm_arbitration is True
    assert blocked_plan.generate_preview is False

    ready_plan = build(
        has_analysis=True,
        has_plan=True,
        plan_status="planned",
        has_preview=False,
        validation_passed=False,
        payload_status="",
    )
    assert ready_plan.generate_split_plan is True
    assert ready_plan.generate_docstring_plan is True
    assert ready_plan.run_llm_arbitration is True
    assert ready_plan.generate_preview is True

    preview_ready = build(
        has_analysis=True,
        has_plan=True,
        plan_status="planned",
        has_preview=True,
        validation_passed=False,
        payload_status="",
    )
    assert preview_ready.validate_preview is True

    validated = build(
        has_analysis=True,
        has_plan=True,
        plan_status="planned",
        has_preview=True,
        validation_passed=True,
        payload_status="payload_ready",
    )
    assert validated.create_patch is True
    assert validated.prepare_apply_gate is True


def _assert_gui_source_contracts(project_root: Path) -> None:
    shell = project_root / (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "gui_shell.py"
    )
    helper = project_root / (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "planner_action_enablement.py"
    )
    for path in (shell, helper):
        text = path.read_text(encoding="utf-8")
        ast.parse(text, filename=str(path))
        assert len(text.splitlines()) <= 500, path

    shell_text = shell.read_text(encoding="utf-8")
    required = (
        "from .planner_action_enablement import build_planner_action_enablement",
        "actions = build_planner_action_enablement(",
        "plan_status=getattr(plan_object, \"status\", \"\")",
        "actions.generate_split_plan",
        "actions.generate_preview",
    )
    for marker in required:
        assert marker in shell_text, marker

    assert shell_text.count(
        'if getattr(plan, "status", "") == "blocked"'
    ) >= 2
    assert '"_large_file_refactor_plan_button", state in analyzed_states' not in shell_text


def validate(project_root: str) -> None:
    """Run focused source and pure-state validation."""
    root = Path(project_root).resolve()
    _assert_enablement_contracts(root)
    _assert_gui_source_contracts(root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python test_large_file_refactor_planner_button_state_recovery_v1.py <project_root>"
        )
    validate(sys.argv[1])
