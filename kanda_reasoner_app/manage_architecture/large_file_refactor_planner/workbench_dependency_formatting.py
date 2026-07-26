# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_dependency_formatting.py
"""Formatting helpers for Workbench dependency readiness."""
from __future__ import annotations

from .workbench_dependency_readiness import WorkbenchDependencyReadinessResult

__all__ = ["format_workbench_dependency_readiness"]


def format_workbench_dependency_readiness(result: WorkbenchDependencyReadinessResult) -> str:
    """Return a readable dependency-readiness report."""
    lines = [
        "Large File Refactor Workbench - Dependency Readiness",
        "",
        f"Status: {result.status}",
        f"Target file: {result.target_file or '<none>'}",
        f"Ready for real preview writer: {_yes_no(result.ready_for_real_preview_writer)}",
        f"Source mutation enabled: {_yes_no(result.source_mutation_enabled)}",
        "",
        "Checked rules:",
    ]
    lines.extend(_bullets(result.checked_rules))
    lines.append("")
    if result.dependency_report is not None:
        report = result.dependency_report
        lines.extend(
            [
                "Source profile:",
                f"- encoding: {report.encoding}",
                f"- newline style: {report.newline_style}",
                f"- symbol count: {len(report.symbols)}",
                f"- import aliases: {len(report.module_import_aliases)}",
                f"- module assignments: {len(report.module_assignments)}",
                "",
                "Symbol dependency summary:",
            ]
        )
        for symbol in report.symbols[:30]:
            lines.append(
                "- {name} ({kind}) internal={internal} imports={imports} "
                "globals={globals} risks={risks}".format(
                    name=symbol.name,
                    kind=symbol.kind,
                    internal=len(symbol.internal_dependencies),
                    imports=len(symbol.import_dependencies),
                    globals=len(symbol.global_dependencies),
                    risks=",".join(symbol.risk_flags) or "none",
                )
            )
        if len(report.symbols) > 30:
            lines.append(f"- ... {len(report.symbols) - 30} more symbols not shown")
        lines.append("")
        lines.append("Report risk flags:")
        lines.extend(_bullets(report.risk_flags) or ["- none"])
        lines.append("")
    lines.append("Blockers:")
    lines.extend(_bullets(result.blockers) or ["- none"])
    lines.append("")
    lines.append("Warnings:")
    lines.extend(_bullets(result.warnings) or ["- none"])
    lines.append("")
    lines.append(
        "Next train: use this dependency topology to generate real LibCST "
        "preview files. This train is read-only."
    )
    return "\n".join(lines)


def _yes_no(value: bool) -> str:
    """Return stable yes/no text."""
    return "YES" if value else "NO"


def _bullets(values: list[str]) -> list[str]:
    """Return bullet lines."""
    return [f"- {value}" for value in values]
