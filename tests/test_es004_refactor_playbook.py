"""Focused tests for ES004 Refactor Playbook."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.engineering_safety import (  # noqa: E402
    RefactorPlaybookInput,
    build_refactor_playbook_report,
    build_refactor_playbook_steps,
)
from kanda_reasoner_app.engineering_safety.refactor_playbook import (  # noqa: E402
    ENGINEERING_SAFETY_REFACTOR_PLAYBOOK_PHASES,
    infer_refactor_playbook_risk_level,
)


def test_refactor_playbook_builds_safe_steps() -> None:
    input_data = RefactorPlaybookInput(
        project_root="E:\\developer_tools",
        target_file='ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py',
        refactor_goal="Extract scoring helpers without changing public behavior.",
        public_symbols=["build_risk_change_radar_report"],
        existing_tests=["python tests\\test_es002_risk_change_radar.py"],
        box_boundary_constraints=["stay inside engineering_safety"],
        do_not_touch=["reasoner_tools_gui"],
    )
    steps = build_refactor_playbook_steps(input_data)
    assert steps
    assert any("Do not touch" in step for step in steps)
    assert any("engineering_safety" in step for step in steps)


def test_refactor_playbook_report_is_structured() -> None:
    input_data = RefactorPlaybookInput(
        project_root="E:\\developer_tools",
        target_file='ask_' 'ai_project_reasoner' '/engineering_safety/crash_triage.py',
        architecture_warnings=["MODULE_TOO_LARGE warning would increase risk."],
        dependencies=['ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py'],
        existing_tests=["python tests\\test_es003_crash_triage.py"],
    )
    report = build_refactor_playbook_report(input_data)
    data = report.to_dict()
    assert data["report_type"] == "refactor_playbook"
    assert data["risk_level"] in {"medium", "high"}
    assert data["affected_files"] == [
        'ask_' 'ai_project_reasoner' '/engineering_safety/crash_triage.py'
    ]
    assert "python tests\\test_es003_crash_triage.py" in data["tests_to_run"]
    assert "validate" in "\n".join(data["tests_to_run"])


def test_refactor_playbook_risk_increases_for_governance() -> None:
    input_data = RefactorPlaybookInput(
        project_root="E:\\developer_tools",
        target_file="_project_reference/ACTIVE_PROJECT_ GOVERNANCE/REASONER_PROJECT_CANON.json",
    )
    assert infer_refactor_playbook_risk_level(input_data) == "critical"


def test_refactor_playbook_public_contract() -> None:
    assert "inspect" in ENGINEERING_SAFETY_REFACTOR_PLAYBOOK_PHASES
    assert callable(build_refactor_playbook_report)


if __name__ == "__main__":
    test_refactor_playbook_builds_safe_steps()
    test_refactor_playbook_report_is_structured()
    test_refactor_playbook_risk_increases_for_governance()
    test_refactor_playbook_public_contract()
    print("ES004 Refactor Playbook tests passed.")
