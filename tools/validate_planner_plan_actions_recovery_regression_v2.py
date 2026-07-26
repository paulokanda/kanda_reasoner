"""Validate planner action recovery behavior after blocked states."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "planner-plan-actions-recovery-regression-v2"
REL = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "planner_action_enablement.py"
)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("planner_action_enablement_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load planner_action_enablement module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build(module, **overrides):
    kwargs = {
        "has_analysis": True,
        "has_plan": True,
        "plan_status": "planned",
        "has_preview": False,
        "validation_passed": False,
        "payload_status": "",
        "ai_review_running": False,
        "has_docstring_plan": False,
        "ai_correctable_plan": False,
    }
    kwargs.update(overrides)
    return module.build_planner_action_enablement(**kwargs)


def validate(project_root: Path) -> None:
    module = load_module(project_root / REL)

    planned = build(module)
    assert planned.generate_docstring_plan is True
    assert planned.run_llm_arbitration is True
    print("PLANNED_PLAN_RECOVERY_ACTIONS_ENABLED: PASS")

    blocked = build(module, plan_status="blocked", ai_correctable_plan=False)
    assert blocked.generate_split_plan is True
    assert blocked.generate_docstring_plan is True
    assert blocked.run_llm_arbitration is True
    assert blocked.generate_preview is False
    print("BLOCKED_PLAN_RECOVERY_ACTIONS_ENABLED: PASS")
    print("BLOCKED_PLAN_PREVIEW_STAYS_DISABLED: PASS")

    blocked_ai = build(module, plan_status="blocked", ai_correctable_plan=True)
    assert blocked_ai.generate_docstring_plan is True
    assert blocked_ai.run_llm_arbitration is True
    assert blocked_ai.generate_preview is False
    print("AI_CORRECTABLE_CLASSIFICATION_NO_LONGER_GATES_RECOVERY_ACTIONS: PASS")

    no_docs = build(module, has_docstring_plan=False)
    assert no_docs.run_llm_arbitration is True
    print("EMPTY_DOCSTRING_PROPOSAL_LIST_DOES_NOT_DISABLE_LOCAL_AI_REVIEW: PASS")

    no_plan = build(module, has_plan=False, plan_status="")
    assert no_plan.generate_docstring_plan is False
    assert no_plan.run_llm_arbitration is False
    assert no_plan.generate_preview is False
    print("NO_PLAN_ACTIONS_STAY_DISABLED: PASS")

    running = build(module, ai_review_running=True)
    assert running.generate_split_plan is False
    assert running.generate_docstring_plan is False
    assert running.run_llm_arbitration is False
    assert running.generate_preview is False
    print("CONCURRENT_ACTIONS_STAY_DISABLED_WHILE_WORK_RUNNING: PASS")

    print("VALIDATION OK: " + FEATURE_ID)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    validate(Path(args.project_root).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
