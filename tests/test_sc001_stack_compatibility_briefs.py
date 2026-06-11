from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.stack_compatibility.stack_briefs as stack_briefs
from kanda_reasoner_app.stack_compatibility import (
    STACK_COMPATIBILITY_RISK_LEVELS,
    StackCompatibilityFinding,
    StackCompatibilityReport,
    build_stack_compatibility_brief,
    default_stack_compatibility_output_dir,
    render_stack_compatibility_markdown,
)


def test_sc001_stack_compatibility_public_contract() -> None:
    assert "medium" in STACK_COMPATIBILITY_RISK_LEVELS
    assert "build_stack_compatibility_brief" in stack_briefs.__all__
    assert "StackCompatibilityReport" in stack_briefs.__all__


def test_sc001_builds_dependency_risk_report() -> None:
    report = build_stack_compatibility_brief(
        [
            "PySide6==6.6.0",
            "requests",
            "pandas>=2.0",
            "# ignored",
        ],
        python_version="3.11.0",
    )
    assert isinstance(report, StackCompatibilityReport)
    assert report.report_type == "stack_compatibility_brief"
    assert report.risk_level == "medium"
    codes = {finding.code for finding in report.findings}
    assert "HIGH_RISK_STACK_PACKAGE" in codes
    assert "UNPINNED_REQUIREMENT" in codes
    assert "VERSION_RANGE_REQUIREMENT" in codes
    assert "PYTHON_VERSION_CHECK_REQUIRED" in codes
    assert isinstance(report.findings[0], StackCompatibilityFinding)


def test_sc001_markdown_and_output_dir() -> None:
    report = build_stack_compatibility_brief(["requests==2.31.0"])
    markdown = render_stack_compatibility_markdown(report)
    assert "# Stack Compatibility Brief" in markdown
    assert "Risk level:" in markdown
    assert default_stack_compatibility_output_dir("E:/developer_tools").as_posix().endswith(
        "workbench/stack_compatibility_reports"
    )


if __name__ == "__main__":
    test_sc001_stack_compatibility_public_contract()
    test_sc001_builds_dependency_risk_report()
    test_sc001_markdown_and_output_dir()
    print("SC001 Stack Compatibility Briefs tests passed.")
