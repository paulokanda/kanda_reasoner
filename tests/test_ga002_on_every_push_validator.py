"""Focused tests for the GA002 On Every Push validator."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.governance_automation import on_every_push_validator
from kanda_reasoner_app.governance_automation.on_every_push_validator import (
    GA_PUSH_STATUS_FAIL,
    GA_PUSH_STATUS_PASS,
    OnEveryPushCheckResult,
    build_check_result_from_output,
    build_default_push_commands,
    build_on_every_push_report,
    classify_validation_text,
    default_on_every_push_report_dir,
    render_on_every_push_markdown,
)


def test_on_every_push_classifies_validation_outputs() -> None:
    assert classify_validation_text("No validation issues.") == GA_PUSH_STATUS_PASS
    assert classify_validation_text("Summary: pass=8 fail=0 warn=0 skip=3") == GA_PUSH_STATUS_PASS
    assert classify_validation_text("ERROR   CROSS_BOX_PUBLIC_SYMBOL_COLLISION") == GA_PUSH_STATUS_FAIL
    assert classify_validation_text("Traceback (most recent call last):") == GA_PUSH_STATUS_FAIL


def test_on_every_push_report_uses_explicit_evidence() -> None:
    arch = build_check_result_from_output(
        "architecture_validation",
        'python ask_' 'ai_project_reasoner' '\\manage_architecture\\manage_architecture.py --validate',
        "No validation issues.",
    )
    workflow = build_check_result_from_output(
        "workflow_validation",
        'python ask_' 'ai_project_reasoner' '\\manage_workflows\\manage_workflows.py --validate',
        "Summary: pass=8 fail=0 warn=0 skip=3",
    )
    report = build_on_every_push_report("<PROJECT_ROOT>", [arch, workflow], ["Local gate."])
    data = report.to_dict()

    assert data["overall_status"] == GA_PUSH_STATUS_PASS
    assert len(data["commands"]) == 3
    assert data["check_results"][0]["name"] == "architecture_validation"
    markdown = render_on_every_push_markdown(report)
    assert "# On Every Push Validation Report" in markdown
    assert "Overall status: pass" in markdown
    assert "Local gate." in markdown


def test_on_every_push_public_contract_is_directly_imported() -> None:
    assert hasattr(on_every_push_validator, "__all__")
    exported = set(on_every_push_validator.__all__)
    assert "build_on_every_push_report" in exported
    assert "render_on_every_push_markdown" in exported
    commands = build_default_push_commands("<PROJECT_ROOT>")
    assert any("manage_architecture" in command for command in commands)
    output_dir = default_on_every_push_report_dir("<PROJECT_ROOT>")
    assert output_dir.as_posix().endswith("workbench/on_every_push_reports")
    result = OnEveryPushCheckResult(name="x", status="bad")
    assert result.normalized_status() == "unknown"


if __name__ == "__main__":
    test_on_every_push_classifies_validation_outputs()
    test_on_every_push_report_uses_explicit_evidence()
    test_on_every_push_public_contract_is_directly_imported()
    print("GA002 On Every Push Validator tests passed.")
