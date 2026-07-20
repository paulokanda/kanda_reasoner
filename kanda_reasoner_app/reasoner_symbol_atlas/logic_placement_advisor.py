# project-path: kanda_reasoner_app/reasoner_symbol_atlas/logic_placement_advisor.py
"""Read-only logic placement advisor for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .evidence_merger import (
    ProjectSymbolAtlasEvidenceMergeOptions,
    merge_reasoner_symbol_atlas_live_and_json_evidence,
)
from .logic_placement_advisor_helpers_private import (
    _candidate_paths_for_box,
    _choose_primary_record,
    _choose_recommended_box,
    _coerce_project_root,
    _find_symbol_matches,
    _find_target_record,
    _infer_owner_box_from_path,
    _infer_owner_box_from_text,
    _record_for_preferred_symbol,
    _tests_to_run_for_owner_box,
)
from .schemas import (
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY = "ready"
PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET = "wrong_target_file"
PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"

PROJECT_SYMBOL_ATLAS_PLACEMENT_OWNER_BOXES = (
    "reasoner_symbol_atlas",
    "project_analysis_evidence",
    "gui_shell",
    "safety_suite_cli",
    "source_hygiene",
    "engineering_safety",
    "governance_automation",
    "stack_compatibility",
    "reliability_guidance",
    "governance",
    "tests",
    "unknown",
)

__all__ = [
    "PROJECT_SYMBOL_ATLAS_PLACEMENT_OWNER_BOXES",
    "PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW",
    "PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET",
    "ProjectSymbolAtlasLogicPlacementDecision",
    "ProjectSymbolAtlasLogicPlacementOptions",
    "advise_reasoner_symbol_atlas_logic_placement",
    "build_reasoner_symbol_atlas_logic_placement_report",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasLogicPlacementOptions:
    """Options for read-only logic placement advice."""

    project_root: str
    task_description: str = ""
    symbol_name: str = ""
    target_path: str = ""
    json_path: str = ""
    include_tests: bool = False
    include_workbench: bool = False
    include_private: bool = False

    def to_merge_options(self) -> ProjectSymbolAtlasEvidenceMergeOptions:
        """Return compatible live AST plus JSON merge options."""
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
            "task_description": normalize_project_atlas_text(self.task_description),
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "include_private": bool(self.include_private),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasLogicPlacementDecision:
    """Decision output for where new logic should be placed."""

    project_root: str
    task_description: str
    recommended_owner_box: str
    primary_target_path: str = ""
    target_owner_role: str = "unknown"
    status: str = PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_INSUFFICIENT_EVIDENCE
    confidence: str = "low"
    forbidden_boxes: tuple[str, ...] = field(default_factory=tuple)
    related_candidate_paths: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""
        return {
            "project_root": str(Path(self.project_root)),
            "task_description": normalize_project_atlas_text(self.task_description),
            "recommended_owner_box": normalize_project_atlas_text(self.recommended_owner_box),
            "primary_target_path": str(Path(self.primary_target_path))
            if self.primary_target_path
            else "",
            "target_owner_role": normalize_project_atlas_text(self.target_owner_role),
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "forbidden_boxes": normalize_project_atlas_sequence(self.forbidden_boxes),
            "related_candidate_paths": normalize_project_atlas_sequence(
                self.related_candidate_paths
            ),
            "tests_to_run": normalize_project_atlas_sequence(self.tests_to_run),
            "reasons": normalize_project_atlas_sequence(self.reasons),
        }


def advise_reasoner_symbol_atlas_logic_placement(
    options: ProjectSymbolAtlasLogicPlacementOptions,
) -> ProjectSymbolAtlasLogicPlacementDecision:
    """Return read-only guidance about where an implementation belongs."""
    project_root = _coerce_project_root(options.project_root)
    report, merge_summary = merge_reasoner_symbol_atlas_live_and_json_evidence(
        options.to_merge_options()
    )
    modules = report.modules
    task_box = _infer_owner_box_from_text(options.task_description)
    target_record = _find_target_record(project_root, modules, options.target_path)
    symbol_matches = _find_symbol_matches(report.symbols, options.symbol_name)
    symbol_record = _record_for_preferred_symbol(modules, symbol_matches)
    recommended_box = _choose_recommended_box(task_box, target_record, symbol_record)
    primary_record = _choose_primary_record(
        modules, target_record, symbol_record, recommended_box
    )
    primary_path = primary_record.path if primary_record is not None else ""
    target_role = primary_record.owner_role if primary_record is not None else "unknown"
    related = _candidate_paths_for_box(modules, recommended_box, primary_path)
    forbidden = _forbidden_boxes_for_owner_box(recommended_box)
    tests_to_run = _tests_to_run_for_owner_box(recommended_box, primary_path)
    status, confidence, reasons = _make_decision_status(
        task_box=task_box,
        primary_record=primary_record,
        symbol_matches=symbol_matches,
        recommended_box=recommended_box,
        merge_status=merge_summary.status,
        evidence_status=merge_summary.freshness_status,
    )
    return ProjectSymbolAtlasLogicPlacementDecision(
        project_root=str(project_root),
        task_description=options.task_description,
        recommended_owner_box=recommended_box,
        primary_target_path=primary_path,
        target_owner_role=target_role,
        status=status,
        confidence=confidence,
        forbidden_boxes=forbidden,
        related_candidate_paths=related,
        tests_to_run=tests_to_run,
        reasons=reasons,
    )


def build_reasoner_symbol_atlas_logic_placement_report(
    options: ProjectSymbolAtlasLogicPlacementOptions,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas report containing placement advice."""
    decision = advise_reasoner_symbol_atlas_logic_placement(options)
    summary = _format_decision_summary(decision)
    evidence_symbols = (
        ProjectSymbol(
            name="logic_placement_decision",
            kind="unknown",
            module="reasoner_symbol_atlas.logic_placement_advisor",
            path=decision.primary_target_path,
            is_public=False,
            owner_role=decision.recommended_owner_box
            if decision.recommended_owner_box
            in {
                "test_only",
                "generated_or_stale",
                "facade",
                "compatibility_facade",
                "private_helper",
                "ambiguous_owner",
                "canonical_owner",
                "unknown",
            }
            else "unknown",
            evidence=decision.reasons,
        ),
    )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=summary,
        symbols=evidence_symbols,
        input_sources=("live_ast", "complete_json_if_fresh", "logic_placement_advisor"),
    )


def _forbidden_boxes_for_owner_box(owner_box: str) -> tuple[str, ...]:
    all_boxes = tuple(
        box for box in PROJECT_SYMBOL_ATLAS_PLACEMENT_OWNER_BOXES if box != "unknown"
    )
    if owner_box == "unknown":
        return tuple()
    allowed_related = {
        "gui_shell": {"gui_shell", "safety_suite_cli", "tests"},
        "safety_suite_cli": {"safety_suite_cli", "tests"},
        "project_analysis_evidence": {"project_analysis_evidence", "tests"},
        "reasoner_symbol_atlas": {"reasoner_symbol_atlas", "tests"},
    }.get(owner_box, {owner_box, "tests"})
    return tuple(box for box in all_boxes if box not in allowed_related)


def _make_decision_status(
    task_box: str,
    primary_record: object | None,
    symbol_matches: tuple[ProjectSymbol, ...],
    recommended_box: str,
    merge_status: str,
    evidence_status: str,
) -> tuple[str, str, tuple[str, ...]]:
    reasons: list[str] = []
    if merge_status:
        reasons.append("Evidence merge status: " + merge_status)
    if evidence_status:
        reasons.append("JSON freshness status: " + evidence_status)
    if task_box != "unknown":
        reasons.append("Task text implies owner box: " + task_box)
    if symbol_matches:
        reasons.append("Found existing symbol matches: " + str(len(symbol_matches)))
    if primary_record is None:
        reasons.append("No concrete primary target file was identified.")
        return (
            PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_INSUFFICIENT_EVIDENCE,
            "low",
            tuple(reasons),
        )
    primary_path = getattr(primary_record, "path", "")
    owner_role = getattr(primary_record, "owner_role", "unknown")
    target_box = _infer_owner_box_from_path(primary_path)
    if owner_role in {"facade", "compatibility_facade", "ambiguous_owner"}:
        reasons.append("Primary target is not a clean canonical owner: " + owner_role)
        return (
            PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW,
            "medium",
            tuple(reasons),
        )
    if recommended_box != "unknown" and target_box != "unknown" and recommended_box != target_box:
        reasons.append("Target path owner box differs from recommended owner box: " + target_box)
        return (
            PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET,
            "high",
            tuple(reasons),
        )
    if task_box != "unknown" or symbol_matches:
        reasons.append("Primary target is compatible with recommended owner box.")
        return PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY, "high", tuple(reasons)
    reasons.append("Placement is heuristic only.")
    return PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW, "low", tuple(reasons)


def _format_decision_summary(decision: ProjectSymbolAtlasLogicPlacementDecision) -> str:
    parts = [
        "Logic placement: " + decision.status,
        "owner_box=" + decision.recommended_owner_box,
    ]
    if decision.primary_target_path:
        parts.append("primary_target=" + decision.primary_target_path)
    parts.append("confidence=" + decision.confidence)
    return "; ".join(parts) + "."
