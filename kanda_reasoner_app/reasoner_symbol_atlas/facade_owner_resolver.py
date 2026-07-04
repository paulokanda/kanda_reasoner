# project-path: kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver.py
"""Read-only facade versus real-owner resolver for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from .schemas import (
    ProjectModuleRecord,
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

from .facade_owner_resolver_helpers_private import (
    _candidate_owner_paths,
    _coerce_project_root,
    _decision_status,
    _facade_evidence,
    _find_target_record,
    _record_is_facade,
    _select_likely_owner,
)

PROJECT_SYMBOL_ATLAS_FACADE_STATUS_READY = "ready"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NO_FACADE = "not_a_facade"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND = "target_not_found"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_OWNER_NOT_FOUND = "owner_not_found"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
PROJECT_SYMBOL_ATLAS_FACADE_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NO_FACADE",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_OWNER_NOT_FOUND",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND",
    "ProjectSymbolAtlasFacadeOwnerDecision",
    "ProjectSymbolAtlasFacadeOwnerOptions",
    "build_reasoner_symbol_atlas_facade_owner_report",
    "resolve_reasoner_symbol_atlas_facade_owner",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasFacadeOwnerOptions:
    """Options for resolving whether a target is a facade or true owner."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = True
    include_workbench: bool = False
    include_private: bool = False

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
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasFacadeOwnerDecision:
    """Decision output for facade versus real-owner resolution."""

    project_root: str
    target_path: str = ""
    symbol_name: str = ""
    target_is_facade: bool = False
    target_owner_role: str = "unknown"
    likely_real_owner_path: str = ""
    likely_real_owner_module: str = ""
    should_patch_target: bool = False
    status: str = PROJECT_SYMBOL_ATLAS_FACADE_STATUS_INSUFFICIENT_EVIDENCE
    confidence: str = "low"
    owner_candidates: tuple[str, ...] = field(default_factory=tuple)
    facade_evidence: tuple[str, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "target_is_facade": bool(self.target_is_facade),
            "target_owner_role": normalize_project_atlas_text(self.target_owner_role),
            "likely_real_owner_path": str(Path(self.likely_real_owner_path)) if self.likely_real_owner_path else "",
            "likely_real_owner_module": normalize_project_atlas_text(self.likely_real_owner_module),
            "should_patch_target": bool(self.should_patch_target),
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "owner_candidates": normalize_project_atlas_sequence(self.owner_candidates),
            "facade_evidence": normalize_project_atlas_sequence(self.facade_evidence),
            "reasons": normalize_project_atlas_sequence(self.reasons),
        }


def resolve_reasoner_symbol_atlas_facade_owner(
    options: ProjectSymbolAtlasFacadeOwnerOptions,
) -> ProjectSymbolAtlasFacadeOwnerDecision:
    """Resolve whether the target path is a facade and identify likely owner."""

    project_root = _coerce_project_root(options.project_root)
    report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        options.to_merge_options()
    )
    modules = report.modules
    symbols = report.symbols
    target_record = _find_target_record(project_root, modules, options.target_path)
    if target_record is None:
        return ProjectSymbolAtlasFacadeOwnerDecision(
            project_root=str(project_root),
            target_path=options.target_path,
            symbol_name=options.symbol_name,
            status=PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND,
            confidence="high" if options.target_path else "low",
            reasons=("Target file was not found in live atlas evidence.",),
        )

    target_is_facade = _record_is_facade(target_record)
    facade_evidence = _facade_evidence(target_record)
    owner_candidates = _candidate_owner_paths(
        target_record=target_record,
        modules=modules,
        symbols=symbols,
        symbol_name=options.symbol_name,
    )
    likely_owner = _select_likely_owner(modules, owner_candidates)
    likely_owner_path = likely_owner.path if likely_owner is not None else ""
    likely_owner_module = likely_owner.module if likely_owner is not None else ""
    status, confidence, should_patch_target, reasons = _decision_status(
        target_record=target_record,
        target_is_facade=target_is_facade,
        likely_owner=likely_owner,
        owner_candidates=owner_candidates,
        merge_status=merge_summary.status,
    )
    return ProjectSymbolAtlasFacadeOwnerDecision(
        project_root=str(project_root),
        target_path=target_record.path,
        symbol_name=options.symbol_name,
        target_is_facade=target_is_facade,
        target_owner_role=target_record.owner_role,
        likely_real_owner_path=likely_owner_path,
        likely_real_owner_module=likely_owner_module,
        should_patch_target=should_patch_target,
        status=status,
        confidence=confidence,
        owner_candidates=owner_candidates,
        facade_evidence=facade_evidence,
        reasons=reasons,
    )


def build_reasoner_symbol_atlas_facade_owner_report(
    options: ProjectSymbolAtlasFacadeOwnerOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for facade versus real-owner resolution."""

    decision = resolve_reasoner_symbol_atlas_facade_owner(options)
    evidence_symbol = ProjectSymbol(
        name="facade_owner_decision",
        kind="unknown",
        module="reasoner_symbol_atlas.facade_owner_resolver",
        path=decision.likely_real_owner_path or decision.target_path,
        is_public=False,
        owner_role="unknown",
        evidence=decision.reasons + decision.facade_evidence,
    )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_decision_summary(decision),
        symbols=(evidence_symbol,),
        input_sources=("live_ast", "complete_json_if_fresh", "facade_owner_resolver"),
    )


def _format_decision_summary(decision: ProjectSymbolAtlasFacadeOwnerDecision) -> str:
    """Support format decision summary behavior.
    
    Parameters
    ----------
    decision : ProjectSymbolAtlasFacadeOwnerDecision
        The decision value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if decision.target_is_facade and decision.likely_real_owner_path:
        return (
            "Target appears to be a facade. Likely real owner: "
            + decision.likely_real_owner_path
            + "."
        )
    if decision.target_is_facade:
        return "Target appears to be a facade, but no real owner candidate was found."
    if decision.status == PROJECT_SYMBOL_ATLAS_FACADE_STATUS_TARGET_NOT_FOUND:
        return "Target file was not found in atlas evidence."
    return "Target does not appear to be a facade from current atlas evidence."
