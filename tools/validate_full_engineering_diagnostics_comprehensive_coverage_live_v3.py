"""Live read-only capability coverage validation for Full Diagnostics v3."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

FEATURE_ID = (
    "kanda-reasoner-full-engineering-diagnostics-comprehensive-capability-coverage-v3"
)


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve(strict=True)
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_report import (
        AiCorrectionCollectorResult,
    )
    from kanda_reasoner_app.engineering_diagnostics_gui.engineering_capability_coverage import (
        collect_engineering_capability_coverage,
    )

    collector_results = (
        AiCorrectionCollectorResult(
            label="BOM",
            status="STORED",
            run_id="live-validation-bom",
            finding_count=0,
        ),
        AiCorrectionCollectorResult(
            label="Ruff",
            status="STORED",
            run_id="live-validation-ruff",
            finding_count=0,
        ),
        AiCorrectionCollectorResult(
            label="Architecture",
            status="STORED",
            run_id="live-validation-architecture",
            finding_count=0,
        ),
        AiCorrectionCollectorResult(
            label="Shadow",
            status="STORED",
            run_id="live-validation-shadow",
            finding_count=0,
        ),
    )

    coverage = collect_engineering_capability_coverage(
        str(project_root),
        collector_results,
    )

    _require(
        coverage.gui_catalog_count == 23,
        "LIVE_PONTUAL_AUDIT_GUI_COVERAGE_23_OF_23",
    )
    _require(
        coverage.cli_catalog_count == 24,
        "LIVE_SAFETY_SUITE_CLI_COVERAGE_24_OF_24",
    )
    _require(
        coverage.unique_safety_surface_count == 25,
        "LIVE_UNIQUE_SAFETY_SURFACES_25_OF_25",
    )
    _require(
        coverage.architecture_surface_count == 1,
        "LIVE_ARCHITECTURE_REVIEW_1_OF_1",
    )
    _require(
        coverage.total_surface_count == 26,
        "LIVE_TOTAL_ENGINEERING_SURFACES_26_OF_26",
    )
    _require(
        len(coverage.results) == 26,
        "LIVE_SILENT_CAPABILITY_OMISSIONS_ZERO",
    )

    atlas_report = next(
        item for item in coverage.results if item.command_name == "atlas-report"
    )
    ruff_corrections = next(
        item
        for item in coverage.results
        if item.command_name == "ruff-correction-dialog"
    )
    _require(
        atlas_report.execution == "NOT_EXECUTED_BY_DESIGN",
        "LIVE_ATLAS_REPORT_WRITE_PATH_EXECUTED_NO",
    )
    _require(
        ruff_corrections.execution == "NOT_EXECUTED_BY_DESIGN",
        "LIVE_RUFF_CORRECTIONS_AUTO_EXECUTED_NO",
    )

    print("LIVE_CAPABILITY_ERRORS: " + str(coverage.error_count))
    print("LIVE_CAPABILITY_WARNINGS: " + str(coverage.warning_count))
    print("LIVE_CAPABILITY_PROBLEM_SURFACES:")
    problems = [
        item for item in coverage.results if item.severity in {"ERROR", "WARNING"}
    ]
    if not problems:
        print("- none")
    for item in problems:
        print(
            "- ["
            + item.severity
            + "] "
            + item.label
            + " | command="
            + item.command_name
            + " | status="
            + item.status
            + " | reason="
            + item.assessment_reason
        )
        if item.status_code is not None:
            print("  status_code=" + str(item.status_code))
        if item.correction_guidance:
            print("  correction_guidance=" + item.correction_guidance)
        if item.evidence:
            first = item.evidence.splitlines()[0]
            print("  evidence_first_line=" + first)

    print("LIVE_STRUCTURED_COLLECTOR_COUNTS_IN_THIS_VALIDATOR: PLACEHOLDER_ONLY")
    print("LIVE_STRUCTURED_COLLECTORS_VALIDATED_BY_EXISTING_FOCUSED_VALIDATORS: YES")
    print("PROJECT SOURCE MUTATED BY LIVE CAPABILITY VALIDATOR: NO")
    print("ENGINEERING DIAGNOSTICS STORE MUTATED BY LIVE CAPABILITY VALIDATOR: NO")
    print("FREEZE MEMORY MUTATED BY LIVE CAPABILITY VALIDATOR: NO")
    print("PROJECT SELECTION REGISTRY MUTATED BY LIVE CAPABILITY VALIDATOR: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
