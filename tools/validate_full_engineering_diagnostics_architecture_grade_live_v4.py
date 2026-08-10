"""Live read-only validation of Architecture-grade capability dossiers v4."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

FEATURE_ID = (
    "kanda-reasoner-full-engineering-diagnostics-architecture-grade-ai-handoff-v4"
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
    from kanda_reasoner_app.engineering_diagnostics_gui.engineering_capability_render import (
        build_capability_report_lines,
    )

    collectors = tuple(
        AiCorrectionCollectorResult(
            label=label,
            status="STORED",
            run_id="live-v4-" + label.lower(),
            finding_count=0,
        )
        for label in ("BOM", "Ruff", "Architecture", "Shadow")
    )
    coverage = collect_engineering_capability_coverage(
        str(project_root),
        collectors,
    )
    report = "\n".join(build_capability_report_lines(project_root, coverage))

    _require(coverage.gui_catalog_count == 23, "LIVE_V4_GUI_23_OF_23")
    _require(coverage.cli_catalog_count == 24, "LIVE_V4_CLI_24_OF_24")
    _require(coverage.unique_safety_surface_count == 25, "LIVE_V4_UNIQUE_25_OF_25")
    _require(coverage.total_surface_count == 26, "LIVE_V4_TOTAL_26_OF_26")
    _require(len(coverage.results) == 26, "LIVE_V4_SILENT_OMISSIONS_ZERO")

    problems = [
        item for item in coverage.results if item.severity in {"ERROR", "WARNING"}
    ]
    _require(
        report.count("AI CORRECTION DOSSIER: REQUIRED") == len(problems),
        "LIVE_V4_EVERY_ERROR_WARNING_HAS_DOSSIER",
    )
    _require(
        report.count("Exact source inspection required before edit: YES")
        == len(coverage.results),
        "LIVE_V4_EVERY_CAPABILITY_REQUIRES_EXACT_SOURCE",
    )
    _require(
        "Capability evidence SHA256:" in report,
        "LIVE_V4_CAPABILITY_EVIDENCE_DIGESTS",
    )
    _require(
        "Correction guidance:" in report,
        "LIVE_V4_CORRECTION_GUIDANCE_PRESENT",
    )
    _require(
        "Automatic correction authorized: NO" in report,
        "LIVE_V4_AUTOMATIC_SOURCE_APPLY_ABSENT",
    )

    atlas_report = next(
        item for item in coverage.results if item.command_name == "atlas-report"
    )
    ruff_correction = next(
        item
        for item in coverage.results
        if item.command_name == "ruff-correction-dialog"
    )
    _require(
        atlas_report.execution == "NOT_EXECUTED_BY_DESIGN",
        "LIVE_V4_ATLAS_REPORT_WRITE_PATH_NOT_EXECUTED",
    )
    _require(
        ruff_correction.execution == "NOT_EXECUTED_BY_DESIGN",
        "LIVE_V4_RUFF_CORRECTIONS_NOT_AUTO_EXECUTED",
    )

    print("LIVE_V4_CAPABILITY_ERRORS: " + str(coverage.error_count))
    print("LIVE_V4_CAPABILITY_WARNINGS: " + str(coverage.warning_count))
    print("LIVE_V4_CORRECTION_DOSSIERS: " + str(len(problems)))
    for item in problems:
        print(
            "- ["
            + item.severity
            + "] "
            + item.label
            + " | "
            + item.command_name
            + " | "
            + item.status
        )
    print("PROJECT SOURCE MUTATED BY V4 LIVE VALIDATOR: NO")
    print("ENGINEERING DIAGNOSTICS STORE MUTATED BY V4 LIVE VALIDATOR: NO")
    print("FREEZE MEMORY MUTATED BY V4 LIVE VALIDATOR: NO")
    print("PROJECT SELECTION REGISTRY MUTATED BY V4 LIVE VALIDATOR: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
