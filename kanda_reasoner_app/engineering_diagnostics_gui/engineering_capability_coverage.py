# project-path: kanda_reasoner_app/engineering_diagnostics_gui/engineering_capability_coverage.py
"""Comprehensive Engineering Safety capability coverage for Full Diagnostics."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from io import StringIO
from threading import Event
import time
from typing import TYPE_CHECKING

from kanda_reasoner_app.engineering_safety.capability_bridge import (
    get_engineering_safety_capability_views,
    run_engineering_safety_capability,
)

from ._engineering_capability_assessment import (
    bounded_evidence,
    classify_output,
    correction_guidance,
)
from ._engineering_capability_models import (
    EngineeringCapabilityCoverage,
    EngineeringCapabilityResult,
)
from .models import EngineeringDiagnosticsGuiCancelled

if TYPE_CHECKING:
    from .ai_correction_report import AiCorrectionCollectorResult

__all__ = [
    "collect_engineering_capability_coverage",
]

_STRUCTURED_GUI_COMMANDS = {
    "bom-scan": "BOM",
    "ruff-quality": "Ruff",
    "shadow-audit": "Shadow",
}
_MANUAL_COMMANDS = {"ruff-correction-dialog"}
_WRITE_PATH_COMMANDS = {"atlas-report"}
_PROJECT_READ_ONLY_COMMANDS = {
    "shadow-plan",
    "facade-fix-plan",
    "evidence-freshness",
    "stack-brief",
    "list-tools",
}
_CLI_ONLY_COMMANDS = ("logic-placement", "symbol-atlas")


def _collector_map(
    collector_results: tuple[AiCorrectionCollectorResult, ...],
) -> dict[str, AiCorrectionCollectorResult]:
    return {item.label: item for item in collector_results}


def _structured_result(
    command_name: str,
    section: str,
    label: str,
    collector: AiCorrectionCollectorResult | None,
) -> EngineeringCapabilityResult:
    if collector is None:
        return EngineeringCapabilityResult(
            surface="PONTUAL_GUI",
            section=section,
            label=label,
            command_name=command_name,
            scope_mode="STRUCTURED_PROJECT_WIDE",
            status="NOT_RUN",
            severity="WARNING",
            assessment_reason=(
                "The canonical structured Diagnostics collector was not present "
                "in this Full Engineering Diagnostics run."
            ),
            execution="COVERED_BY_STRUCTURED_DIAGNOSTIC",
            correction_guidance=(
                "Run the canonical structured collector before proposing fixes."
            ),
        )
    if collector.status != "STORED":
        return EngineeringCapabilityResult(
            surface="PONTUAL_GUI",
            section=section,
            label=label,
            command_name=command_name,
            scope_mode="STRUCTURED_PROJECT_WIDE",
            status="FAILED",
            severity="ERROR",
            assessment_reason=(
                "The canonical structured Diagnostics collector did not store "
                "a valid completed run."
            ),
            execution="COVERED_BY_STRUCTURED_DIAGNOSTIC",
            finding_count=collector.finding_count,
            evidence=bounded_evidence(collector.error_text),
            correction_guidance=(
                "Inspect the collector failure and exact current source before "
                "changing the collector or its canonical owner."
            ),
        )
    findings = int(collector.finding_count)
    return EngineeringCapabilityResult(
        surface="PONTUAL_GUI",
        section=section,
        label=label,
        command_name=command_name,
        scope_mode="STRUCTURED_PROJECT_WIDE",
        status="FINDINGS" if findings else "CLEAN",
        severity="WARNING" if findings else "INFO",
        assessment_reason=(
            "Canonical structured Diagnostics run completed with "
            + str(findings)
            + " findings."
        ),
        execution="COVERED_BY_STRUCTURED_DIAGNOSTIC",
        finding_count=findings,
        evidence=(
            "Run ID: "
            + (collector.run_id or "(none)")
            + "\nFinding count: "
            + str(findings)
        ),
        correction_guidance=(
            "Use grouped correction dossiers for exact owners, affected paths, "
            "remediation guidance, tests, and rollback expectations."
        ),
    )


def _manual_result(
    section: str,
    label: str,
    command_name: str,
) -> EngineeringCapabilityResult:
    return EngineeringCapabilityResult(
        surface="PONTUAL_GUI",
        section=section,
        label=label,
        command_name=command_name,
        scope_mode="MANUAL_GOVERNED",
        status="MANUAL_REVIEW_REQUIRED",
        severity="INFO",
        assessment_reason=(
            "Interactive correction is intentionally not auto-executed by "
            "Full Engineering Diagnostics."
        ),
        execution="NOT_EXECUTED_BY_DESIGN",
        correction_guidance=(
            "Open the governed Ruff correction workflow only after reviewing "
            "structured Ruff findings and exact source."
        ),
    )


def _write_path_result(
    section: str,
    label: str,
    command_name: str,
) -> EngineeringCapabilityResult:
    return EngineeringCapabilityResult(
        surface="PONTUAL_GUI",
        section=section,
        label=label,
        command_name=command_name,
        scope_mode="WRITE_PATH_GOVERNED",
        status="COVERED_BY_READ_ONLY_ATLAS",
        severity="INFO",
        assessment_reason=(
            "Diagnostics remains read-only, so the Atlas Report write path is "
            "not executed. Read-only Symbol Atlas and targeted Atlas health "
            "surfaces are evaluated instead."
        ),
        execution="NOT_EXECUTED_BY_DESIGN",
        correction_guidance=(
            "Treat failures from read-only Atlas surfaces as Atlas health defects. "
            "Do not enable a report write path merely to test Diagnostics."
        ),
    )


def _panel_result(
    section: str,
    label: str,
    command_name: str,
    project_root: str,
) -> EngineeringCapabilityResult:
    scope_mode = (
        "PROJECT_WIDE_READ_ONLY"
        if command_name in _PROJECT_READ_ONLY_COMMANDS
        else "TARGETED_SMOKE"
    )
    started = time.perf_counter()
    try:
        result = run_engineering_safety_capability(command_name, project_root)
    except Exception as exc:  # noqa: BLE001 - capability isolation boundary.
        elapsed = time.perf_counter() - started
        return EngineeringCapabilityResult(
            surface="PONTUAL_GUI",
            section=section,
            label=label,
            command_name=command_name,
            scope_mode=scope_mode,
            status="FAILED",
            severity="ERROR",
            assessment_reason="Public capability runner raised an exception.",
            execution="EXECUTED_PUBLIC_CONTRACT",
            status_code=1,
            elapsed_seconds=elapsed,
            evidence=bounded_evidence(type(exc).__name__ + ": " + str(exc)),
            correction_guidance=correction_guidance(
                command_name,
                "FAILED",
                type(exc).__name__ + ": " + str(exc),
            ),
        )
    elapsed = time.perf_counter() - started
    status_code = int(getattr(result, "status_code", getattr(result, "status", 0)))
    stdout = str(getattr(result, "stdout", "") or "")
    stderr = str(getattr(result, "stderr", "") or "")
    status, severity, reason, findings = classify_output(
        command_name,
        status_code,
        stdout,
        stderr,
        scope_mode,
    )
    evidence = "\n".join(
        part for part in (stdout.strip(), stderr.strip()) if part
    )
    return EngineeringCapabilityResult(
        surface="PONTUAL_GUI",
        section=section,
        label=label,
        command_name=command_name,
        scope_mode=scope_mode,
        status=status,
        severity=severity,
        assessment_reason=reason,
        execution="EXECUTED_PUBLIC_CONTRACT",
        status_code=status_code,
        elapsed_seconds=elapsed,
        finding_count=findings,
        evidence=bounded_evidence(evidence),
        correction_guidance=correction_guidance(command_name, status, stderr),
    )


def _run_cli_direct(args: list[str]) -> tuple[int, str, str]:
    from kanda_reasoner_app.safety_suite_cli import commands

    stdout = StringIO()
    stderr = StringIO()
    status_code = 0
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            value = commands.main(args)
            if isinstance(value, int):
                status_code = value
        except SystemExit as exc:
            status_code = int(exc.code or 0) if isinstance(exc.code, int) else 1
        except Exception as exc:  # noqa: BLE001
            stderr.write(type(exc).__name__ + ": " + str(exc))
            status_code = 1
    return status_code, stdout.getvalue(), stderr.getvalue()


def _cli_only_result(
    command_name: str,
    project_root: str,
) -> EngineeringCapabilityResult:
    if command_name == "symbol-atlas":
        args = ["symbol-atlas", "--root", project_root]
        scope_mode = "PROJECT_WIDE_READ_ONLY"
        label = "Symbol Atlas Read-Only"
    else:
        args = [
            "logic-placement",
            "--root",
            project_root,
            "--target",
            "reasoner_tools_gui_engineering_safety_panel.py",
            "--task",
            "Validate logic-placement capability health for Engineering Safety.",
        ]
        scope_mode = "TARGETED_SMOKE"
        label = "Logic Placement"
    started = time.perf_counter()
    code, stdout, stderr = _run_cli_direct(args)
    elapsed = time.perf_counter() - started
    status, severity, reason, findings = classify_output(
        command_name,
        code,
        stdout,
        stderr,
        scope_mode,
    )
    evidence = "\n".join(
        part for part in (stdout.strip(), stderr.strip()) if part
    )
    return EngineeringCapabilityResult(
        surface="SAFETY_CLI_ONLY",
        section="Project Symbol Atlas",
        label=label,
        command_name=command_name,
        scope_mode=scope_mode,
        status=status,
        severity=severity,
        assessment_reason=reason,
        execution="EXECUTED_PUBLIC_CLI",
        status_code=code,
        elapsed_seconds=elapsed,
        finding_count=findings,
        evidence=bounded_evidence(evidence),
        correction_guidance=correction_guidance(command_name, status, stderr),
    )


def _architecture_result(
    collector_results: tuple[AiCorrectionCollectorResult, ...],
) -> EngineeringCapabilityResult:
    collector = _collector_map(collector_results).get("Architecture")
    if collector is None:
        return EngineeringCapabilityResult(
            surface="ARCHITECTURE_REVIEW",
            section="Architecture",
            label="Architecture Review",
            command_name="architecture-review",
            scope_mode="STRUCTURED_PROJECT_WIDE",
            status="NOT_RUN",
            severity="WARNING",
            assessment_reason="Architecture structured collector was not present.",
            execution="COVERED_BY_STRUCTURED_DIAGNOSTIC",
            correction_guidance="Run Architecture structured diagnostics.",
        )
    if collector.status != "STORED":
        return EngineeringCapabilityResult(
            surface="ARCHITECTURE_REVIEW",
            section="Architecture",
            label="Architecture Review",
            command_name="architecture-review",
            scope_mode="STRUCTURED_PROJECT_WIDE",
            status="FAILED",
            severity="ERROR",
            assessment_reason="Architecture structured collector failed.",
            execution="COVERED_BY_STRUCTURED_DIAGNOSTIC",
            evidence=bounded_evidence(collector.error_text),
            correction_guidance=(
                "Inspect Architecture Review public evidence and exact source."
            ),
        )
    findings = int(collector.finding_count)
    return EngineeringCapabilityResult(
        surface="ARCHITECTURE_REVIEW",
        section="Architecture",
        label="Architecture Review",
        command_name="architecture-review",
        scope_mode="STRUCTURED_PROJECT_WIDE",
        status="FINDINGS" if findings else "CLEAN",
        severity="WARNING" if findings else "INFO",
        assessment_reason=(
            "Architecture structured diagnostics completed with "
            + str(findings)
            + " findings."
        ),
        execution="COVERED_BY_STRUCTURED_DIAGNOSTIC",
        finding_count=findings,
        evidence="Run ID: " + (collector.run_id or "(none)"),
        correction_guidance=(
            "Use Architecture correction groups and exact owner boundaries."
        ),
    )


def collect_engineering_capability_coverage(
    project_root: str,
    collector_results: tuple[AiCorrectionCollectorResult, ...],
    cancellation: Event | None = None,
) -> EngineeringCapabilityCoverage:
    """Account for every GUI/CLI Engineering Safety surface explicitly."""
    from kanda_reasoner_app.safety_suite_cli import commands

    catalog = tuple(get_engineering_safety_capability_views())
    cli_names = tuple(commands.available_cli_commands())
    collector_by_label = _collector_map(collector_results)
    results: list[EngineeringCapabilityResult] = []

    for tool in catalog:
        if cancellation is not None and cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled(
                "engineering capability coverage cancelled"
            )
        section = str(tool.section)
        label = str(tool.label)
        command_name = str(tool.command_name)

        if command_name in _STRUCTURED_GUI_COMMANDS:
            results.append(
                _structured_result(
                    command_name,
                    section,
                    label,
                    collector_by_label.get(_STRUCTURED_GUI_COMMANDS[command_name]),
                )
            )
            continue
        if command_name in _MANUAL_COMMANDS:
            results.append(_manual_result(section, label, command_name))
            continue
        if command_name in _WRITE_PATH_COMMANDS:
            results.append(_write_path_result(section, label, command_name))
            continue

        results.append(_panel_result(section, label, command_name, project_root))

    gui_names = tuple(str(tool.command_name) for tool in catalog)
    gui_set = set(gui_names)
    cli_set = set(cli_names)

    for command_name in _CLI_ONLY_COMMANDS:
        if cancellation is not None and cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled(
                "engineering capability coverage cancelled"
            )
        if command_name not in cli_set:
            results.append(
                EngineeringCapabilityResult(
                    surface="SAFETY_CLI_ONLY",
                    section="Project Symbol Atlas",
                    label=command_name,
                    command_name=command_name,
                    scope_mode="CAPABILITY_INVENTORY",
                    status="MISSING_CAPABILITY",
                    severity="ERROR",
                    assessment_reason="Expected CLI capability is absent from inventory.",
                    execution="NOT_AVAILABLE",
                    correction_guidance=(
                        "Reconcile the public Safety Suite CLI catalog before "
                        "adding duplicate code."
                    ),
                )
            )
            continue
        results.append(_cli_only_result(command_name, project_root))

    atlas_failures = tuple(
        item.command_name
        for item in results
        if item.section == "Project Symbol Atlas"
        and item.severity == "ERROR"
    )
    if atlas_failures:
        for index, item in enumerate(results):
            if item.command_name != "atlas-report":
                continue
            results[index] = replace(
                item,
                status="DEGRADED_DEPENDENCY",
                severity="WARNING",
                assessment_reason=(
                    "Atlas Report write path was not executed, but read-only "
                    "Symbol Atlas dependencies failed: "
                    + ", ".join(atlas_failures)
                    + "."
                ),
                correction_guidance=(
                    "Repair the failing read-only Symbol Atlas dependency first. "
                    "Do not enable the Atlas Report write path in Diagnostics."
                ),
            )
            break

    results.append(_architecture_result(collector_results))

    return EngineeringCapabilityCoverage(
        results=tuple(results),
        gui_catalog_count=len(gui_names),
        cli_catalog_count=len(cli_names),
        unique_safety_surface_count=len(gui_set | cli_set),
        architecture_surface_count=1,
    )
