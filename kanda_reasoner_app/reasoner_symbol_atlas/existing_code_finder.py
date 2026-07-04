# project-path: kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder.py
"""Read-only existing code finder for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ._existing_code_finder_support import (
    format_existing_code_summary,
    run_existing_code_component_plan,
    structured_decision_evidence,
)
from .evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from .facade_owner_resolver import (
    ProjectSymbolAtlasFacadeOwnerOptions,
)
from .implementation_responsibility_resolver import (
    ProjectSymbolAtlasImplementationResponsibilityOptions,
)
from .logic_placement_advisor import (
    ProjectSymbolAtlasLogicPlacementOptions,
)
from .main_helper_mapper import (
    ProjectSymbolAtlasMainHelperOptions,
)
from .pre_patch_gate import (
    ProjectSymbolAtlasPrePatchGateOptions,
)
from .related_file_finder import (
    ProjectSymbolAtlasRelatedFileOptions,
)
from .schemas import (
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    ProjectSymbolQuery,
    ProjectSymbolQueryResult,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)
from .shadow_report import (
    ProjectSymbolAtlasShadowReportOptions,
    collect_reasoner_symbol_atlas_shadow_findings,
)

from .existing_code_finder_matching_private import (
    _choose_query_type,
    _matching_duplicate_symbols,
    _matching_symbols,
    _merge_reasons,
    _owner_paths,
    _query_reasons,
    _unique_strings,
)

PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_READY = "ready"
PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NO_MATCHES = "no_matches"
PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_INVALID_QUERY = "invalid_query"

PROJECT_SYMBOL_ATLAS_EXISTING_CODE_QUERY_TYPES = (
    "auto",
    "symbol",
    "owner",
    "facade_owner",
    "main_helpers",
    "related_files",
    "logic_placement",
    "implementation_responsibility",
    "pre_patch_gate",
)

__all__ = [
    "PROJECT_SYMBOL_ATLAS_EXISTING_CODE_QUERY_TYPES",
    "PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_INVALID_QUERY",
    "PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NEEDS_OWNER_REVIEW",
    "PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NO_MATCHES",
    "PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_READY",
    "ProjectSymbolAtlasExistingCodeFinderOptions",
    "ProjectSymbolAtlasExistingCodeFinderResult",
    "build_reasoner_symbol_atlas_existing_code_report",
    "find_reasoner_symbol_atlas_existing_code",
]

@dataclass(frozen=True)
class ProjectSymbolAtlasExistingCodeFinderOptions:
    """Options for the read-only existing-code finder."""

    project_root: str
    query_text: str = ""
    query_type: str = "auto"
    symbol_name: str = ""
    target_path: str = ""
    task_description: str = ""
    json_path: str = ""
    exact: bool = False
    include_private: bool = False
    include_tests: bool = False
    include_workbench: bool = False
    max_matches: int = 25

    def normalized_symbol_name(self) -> str:
        """Return the effective symbol name to search for."""

        return normalize_project_atlas_text(self.symbol_name or self.query_text)

    def normalized_query_type(self) -> str:
        """Return a supported query type."""

        query_type = normalize_project_atlas_text(self.query_type).lower() or "auto"
        if query_type not in PROJECT_SYMBOL_ATLAS_EXISTING_CODE_QUERY_TYPES:
            return "auto"
        return query_type

    def to_merge_options(self) -> ProjectSymbolAtlasEvidenceMergeOptions:
        """Return compatible live plus JSON merge options."""

        return ProjectSymbolAtlasEvidenceMergeOptions(
            project_root=self.project_root,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_facade_options(self) -> ProjectSymbolAtlasFacadeOwnerOptions:
        """Return compatible facade-owner options."""

        return ProjectSymbolAtlasFacadeOwnerOptions(
            project_root=self.project_root,
            target_path=self.target_path,
            symbol_name=self.normalized_symbol_name(),
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_main_helper_options(self) -> ProjectSymbolAtlasMainHelperOptions:
        """Return compatible main/helper options."""

        return ProjectSymbolAtlasMainHelperOptions(
            project_root=self.project_root,
            target_path=self.target_path,
            symbol_name=self.normalized_symbol_name(),
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_related_options(self) -> ProjectSymbolAtlasRelatedFileOptions:
        """Return compatible related-file options."""

        return ProjectSymbolAtlasRelatedFileOptions(
            project_root=self.project_root,
            target_path=self.target_path,
            symbol_name=self.normalized_symbol_name(),
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=True,
            include_private=self.include_private,
            include_evidence_files=True,
            max_related=max(1, int(self.max_matches)),
        )

    def to_logic_placement_options(self) -> ProjectSymbolAtlasLogicPlacementOptions:
        """Return compatible logic-placement options."""

        return ProjectSymbolAtlasLogicPlacementOptions(
            project_root=self.project_root,
            task_description=self.task_description or self.query_text,
            target_path=self.target_path,
            symbol_name=self.normalized_symbol_name(),
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_responsibility_options(self) -> ProjectSymbolAtlasImplementationResponsibilityOptions:
        """Return compatible implementation-responsibility options."""

        return ProjectSymbolAtlasImplementationResponsibilityOptions(
            project_root=self.project_root,
            task_description=self.task_description or self.query_text,
            target_path=self.target_path,
            symbol_name=self.normalized_symbol_name(),
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_pre_patch_options(self) -> ProjectSymbolAtlasPrePatchGateOptions:
        """Return compatible pre-patch gate options."""

        return ProjectSymbolAtlasPrePatchGateOptions(
            project_root=self.project_root,
            task_description=self.task_description or self.query_text,
            target_path=self.target_path,
            symbol_name=self.normalized_symbol_name(),
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_shadow_options(self) -> ProjectSymbolAtlasShadowReportOptions:
        """Return compatible shadow-report options."""

        return ProjectSymbolAtlasShadowReportOptions(
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "query_text": normalize_project_atlas_text(self.query_text),
            "query_type": self.normalized_query_type(),
            "symbol_name": self.normalized_symbol_name(),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "task_description": normalize_project_atlas_text(self.task_description),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "exact": bool(self.exact),
            "include_private": bool(self.include_private),
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "max_matches": int(self.max_matches),
        }

@dataclass(frozen=True)
class ProjectSymbolAtlasExistingCodeFinderResult:
    """Decision output for existing-code queries."""

    project_root: str
    query_text: str = ""
    query_type: str = "auto"
    symbol_name: str = ""
    target_path: str = ""
    status: str = PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_INVALID_QUERY
    confidence: str = "low"
    symbol_matches: tuple[ProjectSymbol, ...] = field(default_factory=tuple)
    owner_paths: tuple[str, ...] = field(default_factory=tuple)
    duplicate_symbols: tuple[ProjectSymbol, ...] = field(default_factory=tuple)
    facade_owner_path: str = ""
    main_path: str = ""
    helper_paths: tuple[str, ...] = field(default_factory=tuple)
    related_files: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)
    primary_edit_target: str = ""
    files_not_to_touch: tuple[str, ...] = field(default_factory=tuple)
    pre_patch_status: str = ""
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible result dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "query_text": normalize_project_atlas_text(self.query_text),
            "query_type": normalize_project_atlas_text(self.query_type),
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "symbol_match_count": len(self.symbol_matches),
            "symbol_matches": [symbol.to_dict() for symbol in self.symbol_matches],
            "owner_paths": list(self.owner_paths),
            "duplicate_symbols": [symbol.to_dict() for symbol in self.duplicate_symbols],
            "facade_owner_path": self.facade_owner_path,
            "main_path": self.main_path,
            "helper_paths": list(self.helper_paths),
            "related_files": list(self.related_files),
            "tests_to_run": list(self.tests_to_run),
            "primary_edit_target": self.primary_edit_target,
            "files_not_to_touch": list(self.files_not_to_touch),
            "pre_patch_status": self.pre_patch_status,
            "reasons": list(self.reasons),
        }

def find_reasoner_symbol_atlas_existing_code(
    options: ProjectSymbolAtlasExistingCodeFinderOptions,
) -> ProjectSymbolAtlasExistingCodeFinderResult:
    """Answer an existing-code question without editing source files."""

    project_root = str(Path(options.project_root).expanduser().resolve(strict=False))
    symbol_name = options.normalized_symbol_name()
    query_type = _choose_query_type(options)
    if not symbol_name and not options.target_path and not options.task_description:
        return ProjectSymbolAtlasExistingCodeFinderResult(
            project_root=project_root,
            query_text=options.query_text,
            query_type=query_type,
            symbol_name=symbol_name,
            target_path=options.target_path,
            status=PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_INVALID_QUERY,
            reasons=("No symbol, target path, or task description was provided.",),
        )

    report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        options.to_merge_options()
    )
    matches = _matching_symbols(
        report.symbols,
        symbol_name=symbol_name,
        exact=options.exact,
        include_private=options.include_private,
        max_matches=options.max_matches,
    )
    duplicate_symbols = _matching_duplicate_symbols(options, symbol_name)
    components = run_existing_code_component_plan(options, query_type)

    owner_paths = _owner_paths(matches, components.facade_owner_path)
    status, confidence = _status_and_confidence(
        query_type=query_type,
        matches=matches,
        duplicate_symbols=duplicate_symbols,
        facade_owner_path=components.facade_owner_path,
        pre_patch_status=components.pre_patch_status,
        primary_edit_target=components.primary_edit_target,
    )
    reasons = _merge_reasons(
        ("Merge status: " + merge_summary.status,),
        ("Freshness status: " + merge_summary.freshness_status,) if merge_summary.freshness_status else (),
        components.placement_reasons,
        components.facade_reasons,
        components.main_evidence,
        components.related_evidence,
        components.responsibility_reasons,
        components.pre_patch_reasons,
        _query_reasons(query_type, matches, duplicate_symbols),
    )
    return ProjectSymbolAtlasExistingCodeFinderResult(
        project_root=project_root,
        query_text=options.query_text,
        query_type=query_type,
        symbol_name=symbol_name,
        target_path=options.target_path,
        status=status,
        confidence=confidence,
        symbol_matches=matches,
        owner_paths=owner_paths,
        duplicate_symbols=duplicate_symbols,
        facade_owner_path=components.facade_owner_path,
        main_path=components.main_path,
        helper_paths=components.helper_paths,
        related_files=components.related_files,
        tests_to_run=_unique_strings(
            components.related_tests + components.responsibility_tests + components.pre_patch_tests
        ),
        primary_edit_target=components.primary_edit_target,
        files_not_to_touch=components.files_not_to_touch,
        pre_patch_status=components.pre_patch_status,
        reasons=reasons,
    )

def build_reasoner_symbol_atlas_existing_code_report(
    options: ProjectSymbolAtlasExistingCodeFinderOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for an existing-code query."""

    result = find_reasoner_symbol_atlas_existing_code(options)
    query = ProjectSymbolQuery(
        project_root=options.project_root,
        name=result.symbol_name or result.query_text or result.target_path,
        exact=options.exact,
        include_private=options.include_private,
        path_hint=options.target_path,
    )
    query_result = ProjectSymbolQueryResult(
        query=query,
        matches=result.symbol_matches,
        summary="Existing code finder status: " + result.status,
        status=result.status,
    )
    decision_symbol = ProjectSymbol(
        name="existing_code_finder_decision",
        kind="unknown",
        path=result.primary_edit_target or result.target_path,
        owner_role="canonical_owner" if result.primary_edit_target else "unknown",
        evidence=structured_decision_evidence(result),
    )
    return ProjectSymbolAtlasReport(
        project_root=result.project_root,
        report_type="reasoner_symbol_atlas",
        summary=format_existing_code_summary(result),
        symbols=result.symbol_matches + (decision_symbol,),
        query_results=(query_result,),
        input_sources=("live_ast", "complete_json_canonical_if_available"),
    )

def _status_and_confidence(
    query_type: str,
    matches: tuple[ProjectSymbol, ...],
    duplicate_symbols: tuple[ProjectSymbol, ...],
    facade_owner_path: str,
    pre_patch_status: str,
    primary_edit_target: str,
) -> tuple[str, str]:
    """Support status and confidence behavior.
    
    Parameters
    ----------
    query_type : str
        The query type value.
    matches : tuple[ProjectSymbol, ...]
        The matches value.
    duplicate_symbols : tuple[ProjectSymbol, ...]
        The duplicate symbols value.
    facade_owner_path : str
        The facade owner path value.
    pre_patch_status : str
        The pre patch status value.
    primary_edit_target : str
        The primary edit target value.
    
    Returns
    -------
    tuple[str, str]
        The tuple of values.
    """
    
    if query_type == "symbol" and not matches and not duplicate_symbols:
        return PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NO_MATCHES, "low"
    if duplicate_symbols or "risk" in pre_patch_status or facade_owner_path:
        return PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NEEDS_OWNER_REVIEW, "medium"
    if matches or primary_edit_target:
        return PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_READY, "high"
    return PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NO_MATCHES, "low"
