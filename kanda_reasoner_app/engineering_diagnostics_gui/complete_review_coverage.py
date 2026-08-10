"""Adapt Complete Engineering Review results into Diagnostics coverage."""

from __future__ import annotations

from dataclasses import replace
from threading import Event

from kanda_reasoner_app.engineering_safety.capability_bridge import (
    get_engineering_safety_capability_views,
)

from kanda_reasoner_app.engineering_safety.complete_review_contract import (
    CompleteEngineeringReviewItem,
    CompleteEngineeringReviewResult,
)

from ._engineering_capability_assessment import (
    bounded_evidence,
    correction_guidance,
    finding_count,
)
from ._engineering_capability_models import (
    EngineeringCapabilityCoverage,
    EngineeringCapabilityResult,
)
from .ai_correction_report import AiCorrectionCollectorResult
from .engineering_capability_coverage import (
    _architecture_result,
    _cli_only_result,
    _structured_result,
)
from .models import EngineeringDiagnosticsGuiCancelled

__all__ = ["coverage_from_complete_engineering_review"]

_STRUCTURED_GUI_COMMANDS = {
    "bom-scan": "BOM",
    "ruff-quality": "Ruff",
    "shadow-audit": "Shadow",
}
_PROJECT_WIDE_READ_ONLY = {
    "bom-scan",
    "ruff-quality",
    "shadow-audit",
    "shadow-plan",
    "facade-fix-plan",
    "evidence-freshness",
    "stack-brief",
    "list-tools",
}
_MANUAL = {"ruff-correction-dialog"}
_DRAFT = {"release-notes", "api-contract", "property-test"}
_PLANNING = {"push-plan", "risk-radar", "crash-triage", "refactor-playbook"}
_CLI_ONLY_COMMANDS = ("logic-placement", "symbol-atlas")


_ASSESSMENT_STATUS = {
    "CLEAN": ("CLEAN", "INFO"),
    "PASS_WITH_FINDINGS": ("FINDINGS", "WARNING"),
    "DEGRADED": ("DEGRADED", "WARNING"),
    "INVALID_COVERAGE": ("INVALID_COVERAGE", "WARNING"),
    "MISSING_EVIDENCE": ("MISSING_EVIDENCE", "WARNING"),
    "DRAFT": ("DRAFT", "INFO"),
    "NOT_RUN": ("NOT_RUN", "INFO"),
    "MANUAL_REVIEW_REQUIRED": ("MANUAL_REVIEW_REQUIRED", "INFO"),
    "FAILED": ("FAILED", "ERROR"),
}


def _scope_mode(command_name: str) -> str:
    if command_name in _MANUAL:
        return "MANUAL_GOVERNED"
    if command_name == "atlas-report":
        return "FULL_AUDIT_GOVERNED_EVIDENCE_WRITE"
    if command_name in _DRAFT:
        return "GOVERNED_DRAFT"
    if command_name in _PLANNING:
        return "TARGETED_OR_PLANNING"
    if command_name in _PROJECT_WIDE_READ_ONLY:
        return "PROJECT_WIDE_READ_ONLY"
    return "TARGETED_SMOKE"


def _review_item_result(
    item: CompleteEngineeringReviewItem,
) -> EngineeringCapabilityResult:
    status, severity = _ASSESSMENT_STATUS.get(
        item.assessment,
        ("DEGRADED", "WARNING"),
    )
    evidence_text = "\n".join(
        part for part in (item.stdout.strip(), item.stderr.strip()) if part
    )
    count = finding_count(evidence_text)
    return EngineeringCapabilityResult(
        surface="PONTUAL_GUI",
        section=item.section,
        label=item.label,
        command_name=item.command_name,
        scope_mode=_scope_mode(item.command_name),
        status=status,
        severity=severity,
        assessment_reason=item.assessment_reason,
        execution="CONSUMED_COMPLETE_ENGINEERING_REVIEW_RESULT",
        status_code=item.status_code,
        finding_count=count,
        evidence=bounded_evidence(evidence_text),
        correction_guidance=correction_guidance(
            item.command_name,
            status,
            item.stderr,
        ),
    )


def _missing_review_result(
    section: str,
    label: str,
    command_name: str,
) -> EngineeringCapabilityResult:
    return EngineeringCapabilityResult(
        surface="PONTUAL_GUI",
        section=section,
        label=label,
        command_name=command_name,
        scope_mode="CAPABILITY_INVENTORY",
        status="MISSING_CAPABILITY_RESULT",
        severity="ERROR",
        assessment_reason=(
            "Complete Engineering Review did not return this canonical catalog item."
        ),
        execution="MISSING_FROM_COMPLETE_REVIEW_RESULT",
        correction_guidance=(
            "Reconcile the Full Audit public result contract before changing "
            "Diagnostics or adding duplicate execution."
        ),
    )


def coverage_from_complete_engineering_review(
    review: CompleteEngineeringReviewResult,
    collector_results: tuple[AiCorrectionCollectorResult, ...],
    cancellation: Event | None = None,
) -> EngineeringCapabilityCoverage:
    """Build 26-surface coverage without rerunning the 23 Full Audit actions."""
    from kanda_reasoner_app.safety_suite_cli import commands

    catalog = tuple(get_engineering_safety_capability_views())
    cli_names = tuple(commands.available_cli_commands())
    review_by_command = {item.command_name: item for item in review.items}
    collectors = {item.label: item for item in collector_results}
    results: list[EngineeringCapabilityResult] = []

    for tool in catalog:
        if cancellation is not None and cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled(
                "complete review coverage adaptation cancelled"
            )
        section = str(tool.section)
        label = str(tool.label)
        command_name = str(tool.command_name)
        if command_name in _STRUCTURED_GUI_COMMANDS:
            structured = _structured_result(
                command_name,
                section,
                label,
                collectors.get(_STRUCTURED_GUI_COMMANDS[command_name]),
            )
            review_item = review_by_command.get(command_name)
            if review_item is not None:
                review_evidence = "\n".join(
                    part
                    for part in (
                        review_item.stdout.strip(),
                        review_item.stderr.strip(),
                    )
                    if part
                )
                structured = replace(
                    structured,
                    assessment_reason=(
                        structured.assessment_reason
                        + " Complete Engineering Review assessment: "
                        + review_item.assessment
                        + "."
                    ),
                    evidence=(
                        structured.evidence
                        + "\nComplete Engineering Review assessment: "
                        + review_item.assessment
                        + "\nComplete Engineering Review evidence:\n"
                        + bounded_evidence(review_evidence)
                    ),
                )
            results.append(structured)
            continue
        item = review_by_command.get(command_name)
        if item is None:
            results.append(_missing_review_result(section, label, command_name))
            continue
        results.append(_review_item_result(item))

    cli_set = set(cli_names)
    for command_name in _CLI_ONLY_COMMANDS:
        if cancellation is not None and cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled(
                "complete review CLI-only coverage cancelled"
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
                    assessment_reason=(
                        "Expected CLI capability is absent from public inventory."
                    ),
                    execution="NOT_AVAILABLE",
                    correction_guidance=(
                        "Reconcile the public Safety Suite CLI catalog before "
                        "adding duplicate code."
                    ),
                )
            )
            continue
        results.append(_cli_only_result(command_name, review.project_root))

    atlas_failures = tuple(
        item.command_name
        for item in results
        if item.section == "Project Symbol Atlas"
        and item.severity == "ERROR"
    )
    if atlas_failures:
        for index, item in enumerate(results):
            if item.command_name != "atlas-report" or item.severity == "ERROR":
                continue
            results[index] = replace(
                item,
                status="DEGRADED_DEPENDENCY",
                severity="WARNING",
                assessment_reason=(
                    "Complete Engineering Review Atlas evidence has failing "
                    "read-only dependencies: " + ", ".join(atlas_failures) + "."
                ),
                correction_guidance=(
                    "Repair failing read-only Symbol Atlas dependencies first."
                ),
            )
            break

    results.append(_architecture_result(collector_results))
    gui_names = tuple(str(tool.command_name) for tool in catalog)
    return EngineeringCapabilityCoverage(
        results=tuple(results),
        gui_catalog_count=len(gui_names),
        cli_catalog_count=len(cli_names),
        unique_safety_surface_count=len(set(gui_names) | set(cli_names)),
        architecture_surface_count=1,
    )
