# project-path: kanda_reasoner_app/reasoner_symbol_atlas/evidence_merger.py
"""Merge live AST Project Symbol Atlas evidence with complete JSON evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .complete_json_adapter import (
    ProjectSymbolAtlasCompleteJsonOptions,
    build_reasoner_symbol_atlas_complete_json_report,
    collect_reasoner_symbol_atlas_complete_json_files,
)
from .evidence_freshness import (
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT,
    ProjectSymbolAtlasEvidenceFreshnessOptions,
    check_reasoner_symbol_atlas_evidence_freshness,
)
from .owner_classifier import (
    ProjectSymbolAtlasOwnerClassifyOptions,
    classify_reasoner_symbol_atlas_owners,
)
from .review_session import _review_cache_get, _review_cache_put
from .schemas import (
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

from .evidence_merger_helpers_private import (
    _input_sources_for_non_enriched_merge,
    _merge_canonical_modules,
    _merge_fresh_modules,
    _merge_fresh_symbols,
    _symbols_from_modules,
    _tag_live_modules_for_advisory_status,
)

PROJECT_SYMBOL_ATLAS_MERGE_STATUS_LIVE_ONLY = "live_only"
PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ENRICHED = "json_enriched"
PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_CANONICAL = "json_canonical"
PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ADVISORY = "json_advisory"
PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_REJECTED = "json_rejected"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ADVISORY",
    "PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_CANONICAL",
    "PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ENRICHED",
    "PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_REJECTED",
    "PROJECT_SYMBOL_ATLAS_MERGE_STATUS_LIVE_ONLY",
    "ProjectSymbolAtlasEvidenceMergeOptions",
    "ProjectSymbolAtlasEvidenceMergeSummary",
    "build_reasoner_symbol_atlas_live_json_merge_report",
    "build_reasoner_symbol_atlas_merged_evidence_report",
    "merge_reasoner_symbol_atlas_live_and_json_evidence",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasEvidenceMergeOptions:
    """Options for read-only live AST plus complete JSON evidence merging."""

    project_root: str
    json_path: str = ""
    include_tests: bool = True
    include_workbench: bool = False
    include_private: bool = False
    include_constants: bool = True
    include_private_reexports: bool = False
    include_wildcard_symbols: bool = False
    max_json_modules: int = 2000
    max_json_symbols: int = 5000

    def to_owner_classify_options(self) -> ProjectSymbolAtlasOwnerClassifyOptions:
        """Return compatible live AST owner-classification options."""

        return ProjectSymbolAtlasOwnerClassifyOptions(
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
            include_constants=self.include_constants,
            include_private_reexports=self.include_private_reexports,
            include_wildcard_symbols=self.include_wildcard_symbols,
        )

    def to_json_options(self) -> ProjectSymbolAtlasCompleteJsonOptions:
        """Return compatible complete JSON adapter options."""

        return ProjectSymbolAtlasCompleteJsonOptions(
            project_root=self.project_root,
            json_path=self.json_path,
            max_modules=self.max_json_modules,
            max_symbols=self.max_json_symbols,
        )

    def to_freshness_options(self) -> ProjectSymbolAtlasEvidenceFreshnessOptions:
        """Return compatible evidence freshness options."""

        return ProjectSymbolAtlasEvidenceFreshnessOptions(
            project_root=self.project_root,
            json_path=self.json_path,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "include_private": bool(self.include_private),
            "include_constants": bool(self.include_constants),
            "include_private_reexports": bool(self.include_private_reexports),
            "include_wildcard_symbols": bool(self.include_wildcard_symbols),
            "max_json_modules": int(self.max_json_modules),
            "max_json_symbols": int(self.max_json_symbols),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasEvidenceMergeSummary:
    """Summary for live AST plus complete JSON evidence merging."""

    project_root: str
    status: str
    freshness_status: str = ""
    json_path: str = ""
    live_module_count: int = 0
    live_symbol_count: int = 0
    json_module_count: int = 0
    json_symbol_count: int = 0
    merged_module_count: int = 0
    merged_symbol_count: int = 0
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible summary dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "status": normalize_project_atlas_text(self.status),
            "freshness_status": normalize_project_atlas_text(self.freshness_status),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "live_module_count": int(self.live_module_count),
            "live_symbol_count": int(self.live_symbol_count),
            "json_module_count": int(self.json_module_count),
            "json_symbol_count": int(self.json_symbol_count),
            "merged_module_count": int(self.merged_module_count),
            "merged_symbol_count": int(self.merged_symbol_count),
            "notes": list(self.notes),
        }


def merge_reasoner_symbol_atlas_live_and_json_evidence(
    options: ProjectSymbolAtlasEvidenceMergeOptions,
) -> tuple[ProjectSymbolAtlasReport, ProjectSymbolAtlasEvidenceMergeSummary]:
    """Merge live AST evidence with generated complete JSON evidence.

    Live AST evidence always wins for current file existence and current public
    symbols. Fresh JSON enriches matching live records. Stale JSON is advisory
    only. Wrong-project and invalid JSON evidence is rejected. During an
    explicit Complete Review session, identical immutable merge results may be
    reused while the selected Project source/evidence freshness stamp matches.
    """

    project_root = Path(options.project_root).expanduser().resolve(strict=False)
    cache_key = (
        "merged_evidence",
        str(project_root),
        str(Path(options.json_path).expanduser().resolve(strict=False))
        if options.json_path
        else "",
        bool(options.include_tests),
        bool(options.include_workbench),
        bool(options.include_private),
        bool(options.include_constants),
        bool(options.include_private_reexports),
        bool(options.include_wildcard_symbols),
        int(options.max_json_modules),
        int(options.max_json_symbols),
    )
    evidence_paths = _selected_merge_evidence_paths(options, project_root)
    cached = _review_cache_get(
        project_root,
        cache_key,
        evidence_paths=evidence_paths,
    )
    if cached is not None:
        report, summary = cached
        if isinstance(report, ProjectSymbolAtlasReport) and isinstance(
            summary, ProjectSymbolAtlasEvidenceMergeSummary
        ):
            return report, summary

    live_modules = classify_reasoner_symbol_atlas_owners(
        project_root,
        options=options.to_owner_classify_options(),
    )
    live_symbols = _symbols_from_modules(live_modules)
    freshness = check_reasoner_symbol_atlas_evidence_freshness(
        options.to_freshness_options()
    )
    json_report = _build_json_report_safely(options)
    json_modules = json_report.modules
    json_symbols = json_report.symbols
    merge_status, notes = _classify_merge_status(freshness.status)

    if merge_status == PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ENRICHED:
        merged_modules = _merge_fresh_modules(live_modules, json_modules)
        merged_symbols = _merge_fresh_symbols(
            _symbols_from_modules(merged_modules), json_symbols
        )
        input_sources = (
            "live_ast",
            "owner_classifier",
            "complete_json_fresh",
            freshness.json_path,
        )
    elif merge_status == PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_CANONICAL:
        merged_modules = _merge_canonical_modules(live_modules, json_modules)
        merged_symbols = _merge_fresh_symbols(
            _symbols_from_modules(merged_modules), json_symbols
        )
        input_sources = (
            "complete_json_canonical",
            freshness.json_path,
            "live_ast_supplement",
            "owner_classifier",
        )
    else:
        merged_modules = _tag_live_modules_for_advisory_status(
            live_modules, merge_status
        )
        merged_symbols = _symbols_from_modules(merged_modules)
        input_sources = _input_sources_for_non_enriched_merge(
            merge_status, freshness.json_path
        )

    summary = ProjectSymbolAtlasEvidenceMergeSummary(
        project_root=str(project_root),
        status=merge_status,
        freshness_status=freshness.status,
        json_path=freshness.json_path,
        live_module_count=len(live_modules),
        live_symbol_count=len(live_symbols),
        json_module_count=len(json_modules),
        json_symbol_count=len(json_symbols),
        merged_module_count=len(merged_modules),
        merged_symbol_count=len(merged_symbols),
        notes=notes,
    )
    report = ProjectSymbolAtlasReport(
        project_root=str(project_root),
        report_type="reasoner_symbol_atlas",
        summary=_format_merge_summary(summary),
        modules=merged_modules,
        symbols=merged_symbols,
        input_sources=input_sources,
    )
    result = (report, summary)
    _review_cache_put(
        project_root,
        cache_key,
        result,
        evidence_paths=evidence_paths,
    )
    return result



def _selected_merge_evidence_paths(
    options: ProjectSymbolAtlasEvidenceMergeOptions,
    project_root: Path,
) -> tuple[str, ...]:
    """Return the exact JSON evidence path that can affect this merge."""
    if options.json_path:
        path = Path(options.json_path).expanduser().resolve(strict=False)
        return (str(path),)
    candidates = collect_reasoner_symbol_atlas_complete_json_files(project_root)
    if not candidates:
        return ()
    return (str(candidates[0].resolve(strict=False)),)

def build_reasoner_symbol_atlas_live_json_merge_report(
    options: ProjectSymbolAtlasEvidenceMergeOptions,
) -> ProjectSymbolAtlasReport:
    """Build the public live-plus-JSON merge report.

    This compatibility name preserves the PA023 public contract.  It delegates
    to the canonical merged-evidence report builder without changing behavior.
    """

    return build_reasoner_symbol_atlas_merged_evidence_report(options)


def build_reasoner_symbol_atlas_merged_evidence_report(
    options: ProjectSymbolAtlasEvidenceMergeOptions,
) -> ProjectSymbolAtlasReport:
    """Build a merged live AST plus complete JSON Project Symbol Atlas report."""

    report, _summary = merge_reasoner_symbol_atlas_live_and_json_evidence(options)
    return report


def _build_json_report_safely(
    options: ProjectSymbolAtlasEvidenceMergeOptions,
) -> ProjectSymbolAtlasReport:
    """Support build json report safely behavior.
    
    Parameters
    ----------
    options : ProjectSymbolAtlasEvidenceMergeOptions
        The option values.
    
    Returns
    -------
    ProjectSymbolAtlasReport
        The project symbol atlas report result.
    """
    
    try:
        return build_reasoner_symbol_atlas_complete_json_report(
            options.to_json_options()
        )
    except (OSError, ValueError):
        return ProjectSymbolAtlasReport(
            project_root=options.project_root,
            report_type="reasoner_symbol_atlas",
            summary="Complete JSON evidence unavailable or invalid.",
            input_sources=("complete_json_error",),
        )


def _classify_merge_status(freshness_status: str) -> tuple[str, tuple[str, ...]]:
    """Support classify merge status behavior.
    
    Parameters
    ----------
    freshness_status : str
        The freshness status value.
    
    Returns
    -------
    tuple[str, tuple[str, ...]]
        The tuple of values.
    """
    
    if freshness_status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH:
        return (
            PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ENRICHED,
            ("Fresh complete JSON evidence enriched live AST evidence.",),
        )
    if freshness_status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL:
        return (
            PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_CANONICAL,
            ("Complete JSON evidence is canonical; live AST is supplemental.",),
        )
    if freshness_status in {
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE,
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE,
    }:
        return (
            PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_ADVISORY,
            (
                "Complete JSON conflicts with live source; "
                "live AST evidence is advisory context.",
            ),
        )
    if freshness_status == PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE:
        return (
            PROJECT_SYMBOL_ATLAS_MERGE_STATUS_LIVE_ONLY,
            ("No complete JSON evidence was available; live AST evidence only.",),
        )
    if freshness_status in {
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT,
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL,
    }:
        return (
            PROJECT_SYMBOL_ATLAS_MERGE_STATUS_JSON_REJECTED,
            ("Complete JSON evidence was rejected; live AST evidence only.",),
        )
    return (
        PROJECT_SYMBOL_ATLAS_MERGE_STATUS_LIVE_ONLY,
        ("Unrecognized freshness status; live AST evidence only.",),
    )


def _format_merge_summary(summary: ProjectSymbolAtlasEvidenceMergeSummary) -> str:
    """Support format merge summary behavior.
    
    Parameters
    ----------
    summary : ProjectSymbolAtlasEvidenceMergeSummary
        The summary value.
    
    Returns
    -------
    str
        The string result.
    """
    
    data = summary.to_dict()
    notes = normalize_project_atlas_sequence(data.get("notes"))
    suffix = ""
    if notes:
        suffix = "; note=" + notes[0]
    return (
        "Evidence merge status="
        + str(data["status"])
        + "; freshness="
        + str(data["freshness_status"])
        + "; live_modules="
        + str(data["live_module_count"])
        + "; json_modules="
        + str(data["json_module_count"])
        + "; merged_modules="
        + str(data["merged_module_count"])
        + "; live_symbols="
        + str(data["live_symbol_count"])
        + "; json_symbols="
        + str(data["json_symbol_count"])
        + "; merged_symbols="
        + str(data["merged_symbol_count"])
        + suffix
    )
