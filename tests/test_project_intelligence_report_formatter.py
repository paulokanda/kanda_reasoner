"""Validation for Project Intelligence Report Formatter v1."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_intelligence.models import (  # noqa: E402
    ADVISORY_SOURCE_TRUTH_WARNING,
    EngineFinding,
    EngineReport,
)
from kanda_reasoner_app.project_intelligence.report_formatter import (  # noqa: E402
    EngineReportFormatter,
    STANDARD_SECTION_TITLES,
    format_engine_report,
)


def _snapshot(root: Path) -> set[str]:
    return {item.relative_to(root).as_posix() for item in root.rglob("*")}


def _build_report(finding_count: int = 2) -> EngineReport:
    findings = []
    for index in range(finding_count):
        findings.append(
            EngineFinding(
                finding_id="finding-" + str(index),
                severity="warning" if index == 0 else "info",
                category="validation",
                title="Validation finding " + str(index),
                message="Finding message " + str(index),
                file_path="module_" + str(index) + ".py",
                line_number=index + 1,
                evidence="evidence=" + str(index),
                recommendation="Inspect file " + str(index),
            )
        )
    return EngineReport(
        engine_id="project-intelligence-test-engine-v1",
        engine_version="1.0.0",
        status="completed_with_findings",
        generated_at="2026-06-28T00:00:00+00:00",
        project_root_label="fixture_project",
        summary="Formatter fixture summary.",
        findings=findings,
        warnings=["Warning A"],
        errors=["Error A"],
        next_steps=["Inspect source A", "Run validation A"],
        ai_must_not_assume=["Do not assume validation passed."],
        metadata={"sample": "value"},
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_report_formatter_") as temp_dir:
        fixture_root = Path(temp_dir)
        (fixture_root / "input.py").write_text("def sample():\n    return 1\n", encoding="utf-8")
        before = _snapshot(fixture_root)

        report = _build_report(finding_count=4)
        text = format_engine_report(
            report,
            title="Project Intelligence Test Report",
            suggested_validation=["python tests/test_project_intelligence_report_formatter.py"],
            max_findings=2,
        )
        after = _snapshot(fixture_root)

        if before != after:
            raise AssertionError("Report formatter wrote files into the target project root.")

        for section in STANDARD_SECTION_TITLES:
            heading = "## " + section
            if heading not in text:
                raise AssertionError("Missing report section: " + heading)

        required_text = [
            "Project Intelligence Test Report",
            "Formatter fixture summary.",
            ADVISORY_SOURCE_TRUTH_WARNING,
            "Do not assume validation passed.",
            "Validation finding 0",
            "Evidence: evidence=0",
            "Recommendation: Inspect file 0",
            "Truncated 2 additional findings.",
            "Warning A",
            "Error A",
            "python tests/test_project_intelligence_report_formatter.py",
        ]
        for item in required_text:
            if item not in text:
                raise AssertionError("Formatted report missing text: " + item)

        default_text = EngineReportFormatter().format_report(_build_report(finding_count=0))
        if "No advisory findings were produced." not in default_text:
            raise AssertionError("Expected empty finding message in default report.")
        if "Run the patch-specific validation command before freezing or editing." not in default_text:
            raise AssertionError("Expected default validation note.")

        json.dumps(report.to_dict(), ensure_ascii=True, sort_keys=True)

    print("VALIDATION OK: project-intelligence-report-formatter-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
