# project-path: kanda_reasoner_app/reasoner_symbol_atlas/logic_placement_advisor.py
"""Read-only logic placement advisor for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

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
            "primary_target_path": str(Path(self.primary_target_path)) if self.primary_target_path else "",
            "target_owner_role": normalize_project_atlas_text(self.target_owner_role),
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "forbidden_boxes": normalize_project_atlas_sequence(self.forbidden_boxes),
            "related_candidate_paths": normalize_project_atlas_sequence(self.related_candidate_paths),
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
    primary_record = _choose_primary_record(modules, target_record, symbol_record, recommended_box)
    primary_path = primary_record.path if primary_record is not None else ""
    target_role = primary_record.owner_role if primary_record is not None else "unknown"
    related = _candidate_paths_for_box(modules, recommended_box, primary_path)
    forbidden = _forbidden_boxes_for_owner_box(recommended_box)
    tests_to_run = _tests_to_run_for_owner_box(recommended_box, primary_path)
    status, confidence, reasons = _make_decision_status(
        task_box=task_box,
        target_record=target_record,
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
            if decision.recommended_owner_box in {"test_only", "generated_or_stale", "facade", "compatibility_facade", "private_helper", "ambiguous_owner", "canonical_owner", "unknown"}
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


def _coerce_project_root(project_root: str | Path) -> Path:
    """Support coerce project root behavior.
    
    Parameters
    ----------
    project_root : str | Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _normalize_token_text(value: str) -> str:
    """Support normalize token text behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return normalize_project_atlas_text(value).lower().replace("-", "_").replace(" ", "_")


def _infer_owner_box_from_text(text: str) -> str:
    """Support infer owner box from text behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    lowered = _normalize_token_text(text)
    rules = (
        ("reasoner_symbol_atlas", ("atlas", "find_symbol", "owner_map", "pre_patch", "existing_code")),
        ("project_analysis_evidence", ("tab_4", "tab4", "collect_project_structure", "json_complete", "project_analysis_evidence", "tab_5", "tab5", "json_splitted", "split_structure")),
        ("gui_shell", ("gui", "tab", "panel", "button", "widget", "window", "pyside", "display")),
        ("safety_suite_cli", ("cli", "command_line", "command", "argparse", "list_tools")),
        ("source_hygiene", ("bom", "shadow", "source_hygiene", "facade_fix", "encoding")),
        ("engineering_safety", ("risk_radar", "risk_change", "crash_triage", "refactor_playbook", "engineering_safety")),
        ("governance_automation", ("release_notes", "push_plan", "on_every_push", "governance_automation")),
        ("stack_compatibility", ("stack", "dependency", "compatibility", "cuda", "pyside6", "numpy")),
        ("reliability_guidance", ("api_contract", "property_test", "reliability")),
        ("governance", ("canon", "governance", "freeze")),
        ("tests", ("test", "tests")),
    )
    for owner_box, tokens in rules:
        if any(token in lowered for token in tokens):
            return owner_box
    return "unknown"


def _infer_owner_box_from_path(path_value: str) -> str:
    """Support infer owner box from path behavior.
    
    Parameters
    ----------
    path_value : str
        The path value value.
    
    Returns
    -------
    str
        The string result.
    """
    
    lowered = str(Path(path_value)).replace("\\", "/").lower()
    path_rules = (
        ("reasoner_symbol_atlas", ("reasoner_symbol_atlas/",)),
        ("project_analysis_evidence", ("project_analysis_evidence", "project_analysis_evidence_paths")),
        ("gui_shell", ("reasoner_tools_gui", "gui_shell", "_gui", "/gui/")),
        ("safety_suite_cli", ("safety_suite_cli",)),
        ("source_hygiene", ("source_hygiene",)),
        ("engineering_safety", ("engineering_safety",)),
        ("governance_automation", ("governance_automation",)),
        ("stack_compatibility", ("stack_compatibility",)),
        ("reliability_guidance", ("reliability_guidance",)),
        ("tests", ("tests/",)),
    )
    for owner_box, tokens in path_rules:
        if any(token in lowered for token in tokens):
            return owner_box
    return "unknown"


def _find_target_record(
    project_root: Path,
    modules: Iterable[ProjectModuleRecord],
    target_path: str,
) -> ProjectModuleRecord | None:
    """Support find target record behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    modules : Iterable[ProjectModuleRecord]
        The modules value.
    target_path : str
        The target path value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    if not target_path:
        return None
    target = Path(target_path)
    if target.is_absolute():
        try:
            target_key = str(target.resolve(strict=False).relative_to(project_root)).replace("\\", "/").lower()
        except ValueError:
            target_key = str(target.resolve(strict=False)).replace("\\", "/").lower()
    else:
        target_key = str(target).replace("\\", "/").lower()
    for record in modules:
        record_key = str(Path(record.path)).replace("\\", "/").lower()
        if record_key == target_key or record_key.endswith("/" + target_key):
            return record
    return None


def _find_symbol_matches(symbols: Iterable[ProjectSymbol], symbol_name: str) -> tuple[ProjectSymbol, ...]:
    """Support find symbol matches behavior.
    
    Parameters
    ----------
    symbols : Iterable[ProjectSymbol]
        The symbols value.
    symbol_name : str
        The symbol name value.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    name = normalize_project_atlas_text(symbol_name)
    if not name:
        return tuple()
    lowered = name.lower()
    exact = [symbol for symbol in symbols if symbol.name.lower() == lowered]
    if exact:
        return tuple(exact)
    return tuple(symbol for symbol in symbols if lowered in symbol.name.lower())


def _record_for_preferred_symbol(
    modules: Iterable[ProjectModuleRecord],
    matches: tuple[ProjectSymbol, ...],
) -> ProjectModuleRecord | None:
    """Support record for preferred symbol behavior.
    
    Parameters
    ----------
    modules : Iterable[ProjectModuleRecord]
        The modules value.
    matches : tuple[ProjectSymbol, ...]
        The matches value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    if not matches:
        return None
    records_by_path = {record.path: record for record in modules}
    preferred_roles = ("canonical_owner", "private_helper", "facade", "compatibility_facade", "ambiguous_owner")
    for role in preferred_roles:
        for symbol in matches:
            if symbol.owner_role == role and symbol.path in records_by_path:
                return records_by_path[symbol.path]
    for symbol in matches:
        if symbol.path in records_by_path:
            return records_by_path[symbol.path]
    return None


def _choose_recommended_box(
    task_box: str,
    target_record: ProjectModuleRecord | None,
    symbol_record: ProjectModuleRecord | None,
) -> str:
    """Support choose recommended box behavior.
    
    Parameters
    ----------
    task_box : str
        The task box value.
    target_record : ProjectModuleRecord | None
        The target record value.
    symbol_record : ProjectModuleRecord | None
        The symbol record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if task_box != "unknown":
        return task_box
    if target_record is not None:
        path_box = _infer_owner_box_from_path(target_record.path)
        if path_box != "unknown":
            return path_box
    if symbol_record is not None:
        path_box = _infer_owner_box_from_path(symbol_record.path)
        if path_box != "unknown":
            return path_box
    return "unknown"


def _choose_primary_record(
    modules: Iterable[ProjectModuleRecord],
    target_record: ProjectModuleRecord | None,
    symbol_record: ProjectModuleRecord | None,
    recommended_box: str,
) -> ProjectModuleRecord | None:
    """Support choose primary record behavior.
    
    Parameters
    ----------
    modules : Iterable[ProjectModuleRecord]
        The modules value.
    target_record : ProjectModuleRecord | None
        The target record value.
    symbol_record : ProjectModuleRecord | None
        The symbol record value.
    recommended_box : str
        The recommended box value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    if target_record is not None:
        return target_record
    if symbol_record is not None:
        return symbol_record
    candidates = [record for record in modules if _infer_owner_box_from_path(record.path) == recommended_box]
    for role in ("canonical_owner", "private_helper", "facade", "compatibility_facade", "unknown"):
        for record in candidates:
            if record.owner_role == role:
                return record
    return candidates[0] if candidates else None


def _candidate_paths_for_box(
    modules: Iterable[ProjectModuleRecord],
    owner_box: str,
    primary_path: str,
) -> tuple[str, ...]:
    """Support candidate paths for box behavior.
    
    Parameters
    ----------
    modules : Iterable[ProjectModuleRecord]
        The modules value.
    owner_box : str
        The owner box value.
    primary_path : str
        The primary path value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    paths: list[str] = []
    for record in modules:
        if record.path == primary_path:
            continue
        if _infer_owner_box_from_path(record.path) == owner_box:
            paths.append(record.path)
    return tuple(paths[:8])


def _forbidden_boxes_for_owner_box(owner_box: str) -> tuple[str, ...]:
    """Support forbidden boxes for owner box behavior.
    
    Parameters
    ----------
    owner_box : str
        The owner box value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    all_boxes = tuple(box for box in PROJECT_SYMBOL_ATLAS_PLACEMENT_OWNER_BOXES if box != "unknown")
    if owner_box == "unknown":
        return tuple()
    allowed_related = {
        "gui_shell": {"gui_shell", "safety_suite_cli", "tests"},
        "safety_suite_cli": {"safety_suite_cli", "tests"},
        "project_analysis_evidence": {"project_analysis_evidence", "tests"},
        "reasoner_symbol_atlas": {"reasoner_symbol_atlas", "tests"},
    }.get(owner_box, {owner_box, "tests"})
    return tuple(box for box in all_boxes if box not in allowed_related)


def _tests_to_run_for_owner_box(owner_box: str, primary_path: str) -> tuple[str, ...]:
    """Support tests to run for owner box behavior.
    
    Parameters
    ----------
    owner_box : str
        The owner box value.
    primary_path : str
        The primary path value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    commands = [
        "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root <PROJECT_ROOT> --validate",
        "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root <PROJECT_ROOT> --validate",
    ]
    if primary_path:
        commands.insert(0, "python -m py_compile " + primary_path)
    return tuple(commands)


def _make_decision_status(
    task_box: str,
    target_record: ProjectModuleRecord | None,
    primary_record: ProjectModuleRecord | None,
    symbol_matches: tuple[ProjectSymbol, ...],
    recommended_box: str,
    merge_status: str,
    evidence_status: str,
) -> tuple[str, str, tuple[str, ...]]:
    """Support make decision status behavior.
    
    Parameters
    ----------
    task_box : str
        The task box value.
    target_record : ProjectModuleRecord | None
        The target record value.
    primary_record : ProjectModuleRecord | None
        The primary record value.
    symbol_matches : tuple[ProjectSymbol, ...]
        The symbol matches value.
    recommended_box : str
        The recommended box value.
    merge_status : str
        The merge status value.
    evidence_status : str
        The evidence status value.
    
    Returns
    -------
    tuple[str, str, tuple[str, ...]]
        The tuple of values.
    """
    
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
        return PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_INSUFFICIENT_EVIDENCE, "low", tuple(reasons)
    target_box = _infer_owner_box_from_path(primary_record.path)
    if primary_record.owner_role in {"facade", "compatibility_facade", "ambiguous_owner"}:
        reasons.append("Primary target is not a clean canonical owner: " + primary_record.owner_role)
        return PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW, "medium", tuple(reasons)
    if recommended_box != "unknown" and target_box != "unknown" and recommended_box != target_box:
        reasons.append("Target path owner box differs from recommended owner box: " + target_box)
        return PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET, "high", tuple(reasons)
    if task_box != "unknown" or symbol_matches:
        reasons.append("Primary target is compatible with recommended owner box.")
        return PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY, "high", tuple(reasons)
    reasons.append("Placement is heuristic only.")
    return PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_NEEDS_OWNER_REVIEW, "low", tuple(reasons)


def _format_decision_summary(decision: ProjectSymbolAtlasLogicPlacementDecision) -> str:
    """Support format decision summary behavior.
    
    Parameters
    ----------
    decision : ProjectSymbolAtlasLogicPlacementDecision
        The decision value.
    
    Returns
    -------
    str
        The string result.
    """
    
    parts = [
        "Logic placement: " + decision.status,
        "owner_box=" + decision.recommended_owner_box,
    ]
    if decision.primary_target_path:
        parts.append("primary_target=" + decision.primary_target_path)
    parts.append("confidence=" + decision.confidence)
    return "; ".join(parts) + "."
