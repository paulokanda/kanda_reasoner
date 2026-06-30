# project-path: kanda_reasoner_app/reasoner_symbol_atlas/atlas_report_builder.py
"""Aggregate report builder for Project Symbol Atlas evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .evidence_freshness import (
    ProjectSymbolAtlasEvidenceFreshnessOptions,
    build_reasoner_symbol_atlas_evidence_freshness_report,
)
from .evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from .existing_code_finder import (
    ProjectSymbolAtlasExistingCodeFinderOptions,
    build_reasoner_symbol_atlas_existing_code_report,
)
from .json_active_scope_quality import (
    ProjectSymbolAtlasJsonActiveScopeQualityOptions,
    build_reasoner_symbol_atlas_json_active_scope_report,
)
from .report_writer import (
    default_reasoner_symbol_atlas_report_dir,
    write_reasoner_symbol_atlas_report,
)
from .schemas import (
    ProjectAtlasWriteResult,
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_BUILT = "built"
PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_WRITTEN = "written"
PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_EMPTY = "empty"

PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_KINDS = (
    "existing_code",
    "evidence_freshness",
    "live_json_merge",
    "json_active_scope_quality",
)

__all__ = [
    "PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_KINDS",
    "PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_BUILT",
    "PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_EMPTY",
    "PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_WRITTEN",
    "ProjectSymbolAtlasReportBuilderOptions",
    "ProjectSymbolAtlasReportBuilderResult",
    "build_reasoner_symbol_atlas_reports",
    "write_reasoner_symbol_atlas_reports",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasReportBuilderOptions:
    """Options for building Project Symbol Atlas reports."""

    project_root: str
    output_dir: str = ""
    query_text: str = ""
    query_type: str = "auto"
    symbol_name: str = ""
    target_path: str = ""
    task_description: str = ""
    json_path: str = ""
    exact: bool = False
    include_private: bool = False
    include_tests: bool = True
    include_workbench: bool = False
    max_matches: int = 25
    include_existing_code_report: bool = True
    include_freshness_report: bool = True
    include_merge_report: bool = True
    include_json_quality_report: bool = True

    def normalized_output_dir(self) -> Path:
        """Return the report output directory."""

        if self.output_dir:
            return Path(self.output_dir).expanduser().resolve(strict=False)
        return default_reasoner_symbol_atlas_report_dir(self.project_root)

    def selected_report_kinds(self) -> tuple[str, ...]:
        """Return report kinds selected by these options."""

        kinds: list[str] = []
        if self.include_existing_code_report:
            kinds.append("existing_code")
        if self.include_freshness_report:
            kinds.append("evidence_freshness")
        if self.include_merge_report:
            kinds.append("live_json_merge")
        if self.include_json_quality_report:
            kinds.append("json_active_scope_quality")
        return tuple(kinds)

    def to_existing_code_options(self) -> ProjectSymbolAtlasExistingCodeFinderOptions:
        """Return compatible existing-code finder options."""

        return ProjectSymbolAtlasExistingCodeFinderOptions(
            project_root=self.project_root,
            query_text=self.query_text,
            query_type=self.query_type,
            symbol_name=self.symbol_name,
            target_path=self.target_path,
            task_description=self.task_description,
            json_path=self.json_path,
            exact=self.exact,
            include_private=self.include_private,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            max_matches=self.max_matches,
        )

    def to_freshness_options(self) -> ProjectSymbolAtlasEvidenceFreshnessOptions:
        """Return compatible evidence-freshness options."""

        return ProjectSymbolAtlasEvidenceFreshnessOptions(
            project_root=self.project_root,
            json_path=self.json_path,
            max_items=max(1, int(self.max_matches)),
        )

    def to_merge_options(self) -> ProjectSymbolAtlasEvidenceMergeOptions:
        """Return compatible live plus JSON merge options."""

        return ProjectSymbolAtlasEvidenceMergeOptions(
            project_root=self.project_root,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_json_quality_options(self) -> ProjectSymbolAtlasJsonActiveScopeQualityOptions:
        """Return compatible complete JSON active-scope quality options."""

        return ProjectSymbolAtlasJsonActiveScopeQualityOptions(
            project_root=self.project_root,
            json_path=self.json_path,
            max_items=max(1, int(self.max_matches)),
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "output_dir": str(self.normalized_output_dir()),
            "query_text": normalize_project_atlas_text(self.query_text),
            "query_type": normalize_project_atlas_text(self.query_type),
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "task_description": normalize_project_atlas_text(self.task_description),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "exact": bool(self.exact),
            "include_private": bool(self.include_private),
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "max_matches": int(self.max_matches),
            "include_json_quality_report": bool(self.include_json_quality_report),
            "selected_report_kinds": list(self.selected_report_kinds()),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasReportBuilderResult:
    """Reports built or written by the atlas report builder."""

    project_root: str
    output_dir: str
    status: str = PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_EMPTY
    reports: tuple[ProjectSymbolAtlasReport, ...] = field(default_factory=tuple)
    written_reports: tuple[ProjectAtlasWriteResult, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible result dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "output_dir": str(Path(self.output_dir)) if self.output_dir else "",
            "status": normalize_project_atlas_text(self.status),
            "report_count": len(self.reports),
            "reports": [report.to_dict() for report in self.reports],
            "written_report_count": len(self.written_reports),
            "written_reports": [item.to_dict() for item in self.written_reports],
            "notes": list(self.notes),
        }


def build_reasoner_symbol_atlas_reports(
    options: ProjectSymbolAtlasReportBuilderOptions,
) -> ProjectSymbolAtlasReportBuilderResult:
    """Build selected Project Symbol Atlas reports without writing files."""

    project_root = str(Path(options.project_root).expanduser().resolve(strict=False))
    reports: list[ProjectSymbolAtlasReport] = []
    notes: list[str] = []

    if options.include_existing_code_report:
        reports.append(
            build_reasoner_symbol_atlas_existing_code_report(
                options.to_existing_code_options()
            )
        )
        notes.append("Built existing-code report.")

    if options.include_freshness_report:
        reports.append(
            build_reasoner_symbol_atlas_evidence_freshness_report(
                options.to_freshness_options()
            )
        )
        notes.append("Built evidence-freshness report.")

    if options.include_merge_report:
        merge_report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
            options.to_merge_options()
        )
        reports.append(_annotate_merge_report(merge_report, merge_summary.status))
        notes.append("Built live-plus-json merge report: " + merge_summary.status + ".")

    if options.include_json_quality_report:
        quality_report = build_reasoner_symbol_atlas_json_active_scope_report(
            options.to_json_quality_options()
        )
        reports.append(quality_report)
        notes.append("Built complete-JSON active-scope quality report.")

    status = PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_BUILT
    if not reports:
        status = PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_EMPTY
        notes.append("No report kinds were selected.")

    return ProjectSymbolAtlasReportBuilderResult(
        project_root=project_root,
        output_dir=str(options.normalized_output_dir()),
        status=status,
        reports=tuple(reports),
        notes=_unique_strings(notes),
    )


def write_reasoner_symbol_atlas_reports(
    options: ProjectSymbolAtlasReportBuilderOptions,
) -> ProjectSymbolAtlasReportBuilderResult:
    """Build and write selected Project Symbol Atlas reports."""

    built = build_reasoner_symbol_atlas_reports(options)
    if not built.reports:
        return built

    output_dir = options.normalized_output_dir()
    written: list[ProjectAtlasWriteResult] = []
    for report in built.reports:
        written.append(write_reasoner_symbol_atlas_report(report, output_dir=output_dir))

    notes = list(built.notes)
    notes.append("Wrote atlas reports to: " + str(output_dir))
    return ProjectSymbolAtlasReportBuilderResult(
        project_root=built.project_root,
        output_dir=str(output_dir),
        status=PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_WRITTEN,
        reports=built.reports,
        written_reports=tuple(written),
        notes=_unique_strings(notes),
    )


def _annotate_merge_report(
    report: ProjectSymbolAtlasReport,
    merge_status: str,
) -> ProjectSymbolAtlasReport:
    """Return a merge report with an explicit merge-status marker."""

    marker = ProjectSymbol(
        name="live_json_merge_status",
        kind="unknown",
        owner_role="unknown",
        evidence=("Merge status: " + normalize_project_atlas_text(merge_status),),
    )
    return ProjectSymbolAtlasReport(
        project_root=report.project_root,
        report_type=report.report_type,
        summary="Live plus JSON evidence merge report. status=" + merge_status + ".",
        modules=report.modules,
        symbols=report.symbols + (marker,),
        query_results=report.query_results,
        input_sources=report.input_sources,
    )


def _unique_strings(values: object) -> tuple[str, ...]:
    """Support unique strings behavior.
    
    Parameters
    ----------
    values : object
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    output: list[str] = []
    seen: set[str] = set()
    for value in normalize_project_atlas_sequence(values):
        if value and value not in seen:
            output.append(value)
            seen.add(value)
    return tuple(output)
