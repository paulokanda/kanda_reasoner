# project-path: kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py
"""Read-only main file and helper file mapper for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ._main_helper_mapper_contract import (
    _HELPER_SUFFIXES,
    _STATUS_NO_HELPERS_FOUND,
    _STATUS_READY,
)
from ._main_helper_mapper_helper_selection import (
    _decision_status,
    _format_decision_summary,
    _public_helper_warnings,
    _record_is_active,
    _record_is_private_helper,
    _related_tests_to_run,
    _select_helper_records,
    _select_main_record,
    _target_role,
)
from ._main_helper_mapper_path_resolution import (
    _coerce_project_root,
    _find_target_record,
)
from .evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from .schemas import (
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY = _STATUS_READY
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND = "target_not_found"
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND = _STATUS_NO_HELPERS_FOUND
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN = "ambiguous_main"
PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"
PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES = _HELPER_SUFFIXES
__all__ = [
    "PROJECT_SYMBOL_ATLAS_HELPER_SUFFIXES",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_AMBIGUOUS_MAIN",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_NO_HELPERS_FOUND",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND",
    "ProjectSymbolAtlasMainHelperDecision",
    "ProjectSymbolAtlasMainHelperOptions",
    "build_reasoner_symbol_atlas_main_helper_report",
    "map_reasoner_symbol_atlas_main_helpers",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasMainHelperOptions:
    """Options for resolving main-file and helper-file relationships."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = False
    include_workbench: bool = False
    include_private: bool = False
    max_helpers: int = 25

    def to_merge_options(self) -> ProjectSymbolAtlasEvidenceMergeOptions:
        """Return compatible evidence merge options."""

        return ProjectSymbolAtlasEvidenceMergeOptions(
            project_root=self.project_root,
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
            "max_helpers": int(self.max_helpers),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasMainHelperDecision:
    """Decision output for main and helper file mapping."""

    project_root: str
    target_path: str = ""
    target_role: str = "unknown"
    main_path: str = ""
    main_module: str = ""
    helper_paths: tuple[str, ...] = field(default_factory=tuple)
    helper_modules: tuple[str, ...] = field(default_factory=tuple)
    private_helper_paths: tuple[str, ...] = field(default_factory=tuple)
    public_helper_warnings: tuple[str, ...] = field(default_factory=tuple)
    public_api_owner_path: str = ""
    status: str = PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_INSUFFICIENT_EVIDENCE
    confidence: str = "low"
    evidence: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "target_role": normalize_project_atlas_text(self.target_role),
            "main_path": str(Path(self.main_path)) if self.main_path else "",
            "main_module": normalize_project_atlas_text(self.main_module),
            "helper_paths": normalize_project_atlas_sequence(self.helper_paths),
            "helper_modules": normalize_project_atlas_sequence(self.helper_modules),
            "private_helper_paths": normalize_project_atlas_sequence(
                self.private_helper_paths
            ),
            "public_helper_warnings": normalize_project_atlas_sequence(
                self.public_helper_warnings
            ),
            "public_api_owner_path": str(Path(self.public_api_owner_path))
            if self.public_api_owner_path
            else "",
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "evidence": normalize_project_atlas_sequence(self.evidence),
            "tests_to_run": normalize_project_atlas_sequence(self.tests_to_run),
        }


def map_reasoner_symbol_atlas_main_helpers(
    options: ProjectSymbolAtlasMainHelperOptions,
) -> ProjectSymbolAtlasMainHelperDecision:
    """Map the main file and helper files for a target path or symbol."""

    project_root = _coerce_project_root(options.project_root)
    report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        options.to_merge_options()
    )
    modules = tuple(record for record in report.modules if _record_is_active(record))
    target_record = _find_target_record(
        project_root=project_root,
        modules=modules,
        target_path=options.target_path,
        symbol_name=options.symbol_name,
    )
    if target_record is None:
        return ProjectSymbolAtlasMainHelperDecision(
            project_root=str(project_root),
            target_path=options.target_path,
            status=PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND,
            confidence="high" if options.target_path or options.symbol_name else "low",
            evidence=("Target file or symbol was not found in atlas evidence.",),
        )

    target_role = _target_role(target_record)
    main_record = _select_main_record(target_record, modules)
    helper_records = _select_helper_records(
        target_record=target_record,
        main_record=main_record,
        modules=modules,
        max_helpers=options.max_helpers,
    )
    helper_records = tuple(
        record for record in helper_records if record.path != main_record.path
    )
    private_helpers = tuple(
        record.path for record in helper_records if _record_is_private_helper(record)
    )
    warnings = _public_helper_warnings(helper_records)
    status, confidence, evidence = _decision_status(
        target_record=target_record,
        main_record=main_record,
        helper_records=helper_records,
        merge_status=merge_summary.status,
    )
    tests_to_run = _related_tests_to_run(modules, main_record, helper_records)
    return ProjectSymbolAtlasMainHelperDecision(
        project_root=str(project_root),
        target_path=target_record.path,
        target_role=target_role,
        main_path=main_record.path,
        main_module=main_record.module,
        helper_paths=tuple(record.path for record in helper_records),
        helper_modules=tuple(record.module for record in helper_records),
        private_helper_paths=private_helpers,
        public_helper_warnings=warnings,
        public_api_owner_path=main_record.path,
        status=status,
        confidence=confidence,
        evidence=evidence,
        tests_to_run=tests_to_run,
    )


def build_reasoner_symbol_atlas_main_helper_report(
    options: ProjectSymbolAtlasMainHelperOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for main-file and helper-file mapping."""

    decision = map_reasoner_symbol_atlas_main_helpers(options)
    symbols = [
        ProjectSymbol(
            name="main_file",
            kind="unknown",
            module=decision.main_module,
            path=decision.main_path,
            is_public=False,
            owner_role="canonical_owner" if decision.main_path else "unknown",
            evidence=decision.evidence,
        )
    ]
    for helper_path, helper_module in zip(
        decision.helper_paths, decision.helper_modules
    ):
        symbols.append(
            ProjectSymbol(
                name="helper_file",
                kind="unknown",
                module=helper_module,
                path=helper_path,
                is_public=False,
                owner_role="private_helper",
                evidence=("main/helper map helper candidate",),
            )
        )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_decision_summary(decision),
        symbols=tuple(symbols),
        input_sources=("live_ast", "complete_json_if_fresh", "main_helper_mapper"),
    )
