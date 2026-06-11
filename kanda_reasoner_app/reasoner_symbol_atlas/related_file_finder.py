"""Read-only related help and support file finder for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import _related_file_finder_support as _related_support
from .output_policy import is_active_atlas_path, is_active_project_source_path, is_active_test_command
from .evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from .facade_owner_resolver import (
    ProjectSymbolAtlasFacadeOwnerOptions,
    resolve_reasoner_symbol_atlas_facade_owner,
)
from .main_helper_mapper import (
    ProjectSymbolAtlasMainHelperOptions,
    map_reasoner_symbol_atlas_main_helpers,
)
from .schemas import (
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_RELATED_STATUS_READY = "ready"
PROJECT_SYMBOL_ATLAS_RELATED_STATUS_TARGET_NOT_FOUND = "target_not_found"
PROJECT_SYMBOL_ATLAS_RELATED_STATUS_NO_RELATED_FILES = "no_related_files"
PROJECT_SYMBOL_ATLAS_RELATED_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"

PROJECT_SYMBOL_ATLAS_RELATED_SUPPORT_SUFFIXES = _related_support._RELATED_SUPPORT_SUFFIXES

__all__ = [
    "PROJECT_SYMBOL_ATLAS_RELATED_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_RELATED_STATUS_NO_RELATED_FILES",
    "PROJECT_SYMBOL_ATLAS_RELATED_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_RELATED_STATUS_TARGET_NOT_FOUND",
    "PROJECT_SYMBOL_ATLAS_RELATED_SUPPORT_SUFFIXES",
    "ProjectSymbolAtlasRelatedFileDecision",
    "ProjectSymbolAtlasRelatedFileOptions",
    "build_reasoner_symbol_atlas_related_file_report",
    "find_reasoner_symbol_atlas_related_files",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasRelatedFileOptions:
    """Options for finding related help and support files."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = False
    include_workbench: bool = True
    include_private: bool = False
    include_evidence_files: bool = False
    max_related: int = 50

    def to_merge_options(self) -> ProjectSymbolAtlasEvidenceMergeOptions:
        """Return compatible evidence merge options."""

        return ProjectSymbolAtlasEvidenceMergeOptions(
            project_root=self.project_root,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_facade_options(self) -> ProjectSymbolAtlasFacadeOwnerOptions:
        """Return compatible facade owner options."""

        return ProjectSymbolAtlasFacadeOwnerOptions(
            project_root=self.project_root,
            target_path=self.target_path,
            symbol_name=self.symbol_name,
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
            symbol_name=self.symbol_name,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "include_private": bool(self.include_private),
            "include_evidence_files": bool(self.include_evidence_files),
            "max_related": int(self.max_related),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasRelatedFileDecision:
    """Decision output for related help and support files."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    main_files: tuple[str, ...] = field(default_factory=tuple)
    helper_files: tuple[str, ...] = field(default_factory=tuple)
    facade_files: tuple[str, ...] = field(default_factory=tuple)
    real_owner_files: tuple[str, ...] = field(default_factory=tuple)
    test_files: tuple[str, ...] = field(default_factory=tuple)
    manifest_files: tuple[str, ...] = field(default_factory=tuple)
    diagnostic_files: tuple[str, ...] = field(default_factory=tuple)
    patch_apply_files: tuple[str, ...] = field(default_factory=tuple)
    evidence_files: tuple[str, ...] = field(default_factory=tuple)
    related_files: tuple[str, ...] = field(default_factory=tuple)
    do_not_edit_files: tuple[str, ...] = field(default_factory=tuple)
    status: str = PROJECT_SYMBOL_ATLAS_RELATED_STATUS_INSUFFICIENT_EVIDENCE
    confidence: str = "low"
    evidence: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "main_files": normalize_project_atlas_sequence(self.main_files),
            "helper_files": normalize_project_atlas_sequence(self.helper_files),
            "facade_files": normalize_project_atlas_sequence(self.facade_files),
            "real_owner_files": normalize_project_atlas_sequence(self.real_owner_files),
            "test_files": normalize_project_atlas_sequence(self.test_files),
            "manifest_files": normalize_project_atlas_sequence(self.manifest_files),
            "diagnostic_files": normalize_project_atlas_sequence(self.diagnostic_files),
            "patch_apply_files": normalize_project_atlas_sequence(self.patch_apply_files),
            "evidence_files": normalize_project_atlas_sequence(self.evidence_files),
            "related_files": normalize_project_atlas_sequence(self.related_files),
            "do_not_edit_files": normalize_project_atlas_sequence(self.do_not_edit_files),
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "evidence": normalize_project_atlas_sequence(self.evidence),
            "tests_to_run": normalize_project_atlas_sequence(self.tests_to_run),
        }


def find_reasoner_symbol_atlas_related_files(
    options: ProjectSymbolAtlasRelatedFileOptions,
) -> ProjectSymbolAtlasRelatedFileDecision:
    """Find related help and support files for a target path or symbol."""

    project_root = Path(options.project_root).expanduser().resolve(strict=False)
    report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        options.to_merge_options()
    )
    modules = tuple(report.modules)
    target = _related_support._resolve_target_module(
        modules, options.target_path, options.symbol_name
    )
    if target is None and not options.symbol_name:
        return ProjectSymbolAtlasRelatedFileDecision(
            project_root=str(project_root),
            target_path=options.target_path,
            symbol_name=options.symbol_name,
            status=PROJECT_SYMBOL_ATLAS_RELATED_STATUS_TARGET_NOT_FOUND,
            evidence=("No target path or symbol could be resolved.",),
        )

    target_path = target.path if target is not None else normalize_project_atlas_text(options.target_path)
    search_terms = _related_support._search_terms(target_path, options.symbol_name)
    main_helper = map_reasoner_symbol_atlas_main_helpers(options.to_main_helper_options())
    facade = resolve_reasoner_symbol_atlas_facade_owner(options.to_facade_options())

    main_files = _active_paths(
        _related_support._unique_paths(
            (main_helper.main_path, target_path if _related_support._looks_like_main(target_path) else "")
        )
    )
    helper_files = _active_paths(
        _related_support._unique_paths(
            main_helper.helper_paths
            + _related_support._support_helpers_from_modules(modules, search_terms)
        )
    )
    facade_files = _active_paths(
        _related_support._unique_paths(
            (facade.target_path,) if facade.target_is_facade else tuple()
        )
    )
    real_owner_files = _active_paths(_related_support._unique_paths((facade.likely_real_owner_path,)))
    test_files = _related_support._related_test_files(
        project_root, modules, search_terms, options.include_tests
    )
    manifest_files = _related_support._related_workbench_files(
        project_root, search_terms, "manifest", options.include_workbench
    )
    diagnostic_files = _related_support._related_workbench_files(
        project_root, search_terms, "diagnostic", options.include_workbench
    )
    patch_apply_files = _related_support._related_workbench_files(
        project_root, search_terms, "patch_apply", options.include_workbench
    )
    evidence_files = _active_paths(
        _related_support._related_evidence_files(
            project_root, search_terms, options.include_evidence_files
        )
    )
    do_not_edit_files = _related_support._unique_paths(
        facade_files if facade.target_is_facade else tuple()
    )
    related_files = _active_related_source_paths(
        _related_support._limited_unique_paths(
            main_files
            + helper_files
            + facade_files
            + real_owner_files
            + manifest_files
            + diagnostic_files
            + patch_apply_files,
            max_items=options.max_related,
        ),
        target_path=target_path,
    )
    status, confidence = _status_and_confidence(
        target_found=target is not None,
        related_files=related_files,
        main_files=main_files,
        helper_files=helper_files,
        test_files=test_files,
        real_owner_files=real_owner_files,
    )
    evidence = _related_support._evidence_lines(
        merge_status=merge_summary.status,
        target_path=target_path,
        main_helper_status=main_helper.status,
        facade_status=facade.status,
        search_terms=search_terms,
        related_files=related_files,
    )
    tests_to_run = tuple(
        command for command in _related_support._tests_to_run(test_files, target_path)
        if is_active_test_command(command)
    )

    return ProjectSymbolAtlasRelatedFileDecision(
        project_root=str(project_root),
        target_path=target_path,
        symbol_name=options.symbol_name,
        main_files=main_files,
        helper_files=helper_files,
        facade_files=facade_files,
        real_owner_files=real_owner_files,
        test_files=test_files,
        manifest_files=manifest_files,
        diagnostic_files=diagnostic_files,
        patch_apply_files=patch_apply_files,
        evidence_files=evidence_files,
        related_files=related_files,
        do_not_edit_files=do_not_edit_files,
        status=status,
        confidence=confidence,
        evidence=evidence,
        tests_to_run=tests_to_run,
    )


def build_reasoner_symbol_atlas_related_file_report(
    options: ProjectSymbolAtlasRelatedFileOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for related help and support files."""

    decision = find_reasoner_symbol_atlas_related_files(options)
    symbol = ProjectSymbol(
        name="related_file_finder_decision",
        kind="unknown",
        module="reasoner_symbol_atlas.related_file_finder",
        path=decision.target_path,
        is_public=False,
        owner_role="unknown",
        evidence=decision.evidence,
    )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_decision_summary(decision),
        symbols=(symbol,),
        input_sources=("related_file_finder", "live_ast", "complete_json_if_available"),
    )



def _active_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(path for path in paths if is_active_atlas_path(path))


def _active_source_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(path for path in paths if is_active_project_source_path(path))


def _active_related_source_paths(paths: tuple[str, ...], target_path: str) -> tuple[str, ...]:
    return tuple(
        path
        for path in paths
        if is_active_project_source_path(path)
        and _is_public_or_direct_target(path, target_path)
    )


def _is_public_or_direct_target(path_value: str, target_path: str) -> bool:
    normalized_path = path_value.replace("\\", "/").lower()
    normalized_target = target_path.replace("\\", "/").lower()
    if normalized_path == normalized_target:
        return True
    return not Path(normalized_path).name.startswith("_")


def _status_and_confidence(
    target_found: bool,
    related_files: tuple[str, ...],
    main_files: tuple[str, ...],
    helper_files: tuple[str, ...],
    test_files: tuple[str, ...],
    real_owner_files: tuple[str, ...],
) -> tuple[str, str]:
    if not target_found and not related_files:
        return PROJECT_SYMBOL_ATLAS_RELATED_STATUS_TARGET_NOT_FOUND, "low"
    if not related_files:
        return PROJECT_SYMBOL_ATLAS_RELATED_STATUS_NO_RELATED_FILES, "low"
    score = 0
    if main_files:
        score += 1
    if helper_files:
        score += 1
    if test_files:
        score += 1
    if real_owner_files:
        score += 1
    if score >= 3:
        return PROJECT_SYMBOL_ATLAS_RELATED_STATUS_READY, "high"
    if score >= 1:
        return PROJECT_SYMBOL_ATLAS_RELATED_STATUS_READY, "medium"
    return PROJECT_SYMBOL_ATLAS_RELATED_STATUS_NO_RELATED_FILES, "low"


def _format_decision_summary(decision: ProjectSymbolAtlasRelatedFileDecision) -> str:
    return (
        "Related help/support files: "
        + decision.status
        + "; related_files="
        + str(len(decision.related_files))
        + "; tests="
        + str(len(decision.test_files))
    )
