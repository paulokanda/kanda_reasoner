# project-path: kanda_reasoner_app/engineering_safety/project_symbol_atlas_integration.py
"""Engineering Safety integration for Project Symbol Atlas signals."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
    ProjectSymbolAtlasExistingCodeFinderOptions,
    find_reasoner_symbol_atlas_existing_code,
)
from kanda_reasoner_app.reasoner_symbol_atlas.pre_patch_gate import (
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_DUPLICATE_SYMBOL_RISK,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_EVIDENCE_STALE,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_FACADE_PATCH_RISK,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_MISSING_TEST_PROTECTION,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_NEEDS_OWNER_REVIEW,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_WRONG_TARGET_FILE,
    ProjectSymbolAtlasPrePatchGateOptions,
    run_reasoner_symbol_atlas_pre_patch_gate,
)
from kanda_reasoner_app.reasoner_symbol_atlas.schemas import (
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

ENGINEERING_SAFETY_ATLAS_STATUS_READY = "ready"
ENGINEERING_SAFETY_ATLAS_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
ENGINEERING_SAFETY_ATLAS_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"
ENGINEERING_SAFETY_ATLAS_STATUS_FAILED = "failed"

ENGINEERING_SAFETY_ATLAS_RISK_LOW = "low"
ENGINEERING_SAFETY_ATLAS_RISK_MEDIUM = "medium"
ENGINEERING_SAFETY_ATLAS_RISK_HIGH = "high"
ENGINEERING_SAFETY_ATLAS_RISK_CRITICAL = "critical"
ENGINEERING_SAFETY_ATLAS_RISK_UNKNOWN = "unknown"

__all__ = [
    "ENGINEERING_SAFETY_ATLAS_RISK_CRITICAL",
    "ENGINEERING_SAFETY_ATLAS_RISK_HIGH",
    "ENGINEERING_SAFETY_ATLAS_RISK_LOW",
    "ENGINEERING_SAFETY_ATLAS_RISK_MEDIUM",
    "ENGINEERING_SAFETY_ATLAS_RISK_UNKNOWN",
    "ENGINEERING_SAFETY_ATLAS_STATUS_FAILED",
    "ENGINEERING_SAFETY_ATLAS_STATUS_INSUFFICIENT_EVIDENCE",
    "ENGINEERING_SAFETY_ATLAS_STATUS_NEEDS_OWNER_REVIEW",
    "ENGINEERING_SAFETY_ATLAS_STATUS_READY",
    "EngineeringSafetyProjectSymbolAtlasContext",
    "EngineeringSafetyProjectSymbolAtlasOptions",
    "build_engineering_safety_reasoner_symbol_atlas_context",
    "engineering_safety_reasoner_symbol_atlas_evidence_lines",
    "format_engineering_safety_reasoner_symbol_atlas_markdown",
]


@dataclass(frozen=True)
class EngineeringSafetyProjectSymbolAtlasOptions:
    """Options for read-only Engineering Safety Atlas integration."""

    project_root: str
    task_description: str = ""
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = True
    include_workbench: bool = True
    include_private: bool = False
    require_test_protection: bool = True
    fail_on_stale_evidence: bool = False
    max_related: int = 25

    def to_existing_code_options(self) -> ProjectSymbolAtlasExistingCodeFinderOptions:
        """Return compatible Existing Code Finder options."""

        query_text = self.symbol_name or self.target_path or self.task_description
        return ProjectSymbolAtlasExistingCodeFinderOptions(
            project_root=self.project_root,
            query_text=query_text,
            symbol_name=self.symbol_name,
            target_path=self.target_path,
            task_description=self.task_description,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
            max_matches=max(1, int(self.max_related)),
        )

    def to_pre_patch_options(self) -> ProjectSymbolAtlasPrePatchGateOptions:
        """Return compatible Pre-Patch Gate options."""

        return ProjectSymbolAtlasPrePatchGateOptions(
            project_root=self.project_root,
            task_description=self.task_description,
            target_path=self.target_path,
            symbol_name=self.symbol_name,
            json_path=self.json_path,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private=self.include_private,
            require_test_protection=self.require_test_protection,
            fail_on_stale_evidence=self.fail_on_stale_evidence,
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "task_description": normalize_project_atlas_text(self.task_description),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "include_tests": bool(self.include_tests),
            "include_workbench": bool(self.include_workbench),
            "include_private": bool(self.include_private),
            "require_test_protection": bool(self.require_test_protection),
            "fail_on_stale_evidence": bool(self.fail_on_stale_evidence),
            "max_related": int(self.max_related),
        }


@dataclass(frozen=True)
class EngineeringSafetyProjectSymbolAtlasContext:
    """Decision-ready Atlas context for Engineering Safety tools."""

    project_root: str
    task_description: str = ""
    target_path: str = ""
    symbol_name: str = ""
    status: str = ENGINEERING_SAFETY_ATLAS_STATUS_INSUFFICIENT_EVIDENCE
    risk_level: str = ENGINEERING_SAFETY_ATLAS_RISK_UNKNOWN
    primary_edit_target: str = ""
    owner_paths: tuple[str, ...] = field(default_factory=tuple)
    facade_owner_path: str = ""
    main_path: str = ""
    helper_paths: tuple[str, ...] = field(default_factory=tuple)
    related_files_to_inspect: tuple[str, ...] = field(default_factory=tuple)
    files_not_to_touch: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)
    duplicate_symbol_risk: bool = False
    facade_patch_risk: bool = False
    wrong_target_file: bool = False
    missing_test_protection: bool = False
    evidence_stale: bool = False
    needs_owner_review: bool = False
    pre_patch_status: str = ""
    existing_code_status: str = ""
    confidence: str = "low"
    warnings: tuple[str, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible context dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "task_description": normalize_project_atlas_text(self.task_description),
            "target_path": str(Path(self.target_path)) if self.target_path else "",
            "symbol_name": normalize_project_atlas_text(self.symbol_name),
            "status": normalize_project_atlas_text(self.status),
            "risk_level": normalize_project_atlas_text(self.risk_level),
            "primary_edit_target": self.primary_edit_target,
            "owner_paths": list(self.owner_paths),
            "facade_owner_path": self.facade_owner_path,
            "main_path": self.main_path,
            "helper_paths": list(self.helper_paths),
            "related_files_to_inspect": list(self.related_files_to_inspect),
            "files_not_to_touch": list(self.files_not_to_touch),
            "tests_to_run": list(self.tests_to_run),
            "duplicate_symbol_risk": bool(self.duplicate_symbol_risk),
            "facade_patch_risk": bool(self.facade_patch_risk),
            "wrong_target_file": bool(self.wrong_target_file),
            "missing_test_protection": bool(self.missing_test_protection),
            "evidence_stale": bool(self.evidence_stale),
            "needs_owner_review": bool(self.needs_owner_review),
            "pre_patch_status": normalize_project_atlas_text(self.pre_patch_status),
            "existing_code_status": normalize_project_atlas_text(self.existing_code_status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "warnings": list(self.warnings),
            "reasons": list(self.reasons),
        }


def build_engineering_safety_reasoner_symbol_atlas_context(
    options: EngineeringSafetyProjectSymbolAtlasOptions,
) -> EngineeringSafetyProjectSymbolAtlasContext:
    """Build read-only Atlas context for Engineering Safety tools."""

    project_root = str(Path(options.project_root).expanduser().resolve(strict=False))
    try:
        existing = find_reasoner_symbol_atlas_existing_code(options.to_existing_code_options())
        gate = run_reasoner_symbol_atlas_pre_patch_gate(options.to_pre_patch_options())
    except Exception as exc:  # pragma: no cover - defensive integration boundary.
        message = type(exc).__name__ + ": " + str(exc)
        return EngineeringSafetyProjectSymbolAtlasContext(
            project_root=project_root,
            task_description=options.task_description,
            target_path=options.target_path,
            symbol_name=options.symbol_name,
            status=ENGINEERING_SAFETY_ATLAS_STATUS_FAILED,
            risk_level=ENGINEERING_SAFETY_ATLAS_RISK_UNKNOWN,
            warnings=("Project Symbol Atlas integration failed: " + message,),
            reasons=("Atlas integration boundary caught an exception.",),
        )

    warnings = _warnings_from_gate(gate)
    reasons = _unique_strings((*existing.reasons, *gate.reasons))
    related_files = _unique_strings((*existing.related_files, *gate.related_files))
    tests_to_run = _unique_strings((*existing.tests_to_run, *gate.tests_to_run, *_global_validation_commands()))
    files_not_to_touch = _unique_strings((*existing.files_not_to_touch, *gate.files_not_to_touch))
    status = _status_from_gate(gate.status)
    risk_level = _risk_level_from_gate(gate.status, gate.to_dict())
    confidence = _confidence_from_gate(gate.confidence, existing.confidence)

    return EngineeringSafetyProjectSymbolAtlasContext(
        project_root=project_root,
        task_description=options.task_description,
        target_path=options.target_path,
        symbol_name=options.symbol_name,
        status=status,
        risk_level=risk_level,
        primary_edit_target=gate.primary_edit_target or existing.primary_edit_target,
        owner_paths=existing.owner_paths,
        facade_owner_path=existing.facade_owner_path,
        main_path=existing.main_path,
        helper_paths=existing.helper_paths,
        related_files_to_inspect=related_files,
        files_not_to_touch=files_not_to_touch,
        tests_to_run=tests_to_run,
        duplicate_symbol_risk=bool(gate.duplicate_symbol_risk),
        facade_patch_risk=bool(gate.facade_patch_risk),
        wrong_target_file=bool(gate.wrong_target_file),
        missing_test_protection=bool(gate.missing_test_protection),
        evidence_stale=bool(gate.evidence_stale),
        needs_owner_review=bool(gate.needs_owner_review),
        pre_patch_status=gate.status,
        existing_code_status=existing.status,
        confidence=confidence,
        warnings=warnings,
        reasons=reasons,
    )


def engineering_safety_reasoner_symbol_atlas_evidence_lines(
    context: EngineeringSafetyProjectSymbolAtlasContext,
) -> tuple[str, ...]:
    """Return concise evidence lines for Engineering Safety reports."""

    lines = [
        "Atlas status: " + context.status,
        "Atlas risk level: " + context.risk_level,
    ]
    if context.primary_edit_target:
        lines.append("Primary edit target: " + context.primary_edit_target)
    if context.facade_patch_risk:
        lines.append("Facade patch risk detected.")
    if context.wrong_target_file:
        lines.append("Wrong target file risk detected.")
    if context.duplicate_symbol_risk:
        lines.append("Duplicate symbol risk detected.")
    if context.missing_test_protection:
        lines.append("Missing focused test protection detected.")
    if context.evidence_stale:
        lines.append("Atlas JSON evidence may be stale.")
    for warning in context.warnings:
        lines.append("Warning: " + warning)
    return tuple(lines)


def format_engineering_safety_reasoner_symbol_atlas_markdown(
    context: EngineeringSafetyProjectSymbolAtlasContext,
) -> str:
    """Format an Engineering Safety Atlas context as Markdown."""

    data = context.to_dict()
    lines = [
        "# Engineering Safety Project Symbol Atlas Context",
        "",
        "- Status: " + str(data["status"]),
        "- Risk level: " + str(data["risk_level"]),
        "- Target path: " + str(data["target_path"]),
        "- Symbol: " + str(data["symbol_name"]),
        "- Primary edit target: " + str(data["primary_edit_target"]),
        "- Pre-patch status: " + str(data["pre_patch_status"]),
        "",
    ]
    _append_markdown_list(lines, "Warnings", context.warnings)
    _append_markdown_list(lines, "Related files to inspect", context.related_files_to_inspect)
    _append_markdown_list(lines, "Files not to touch", context.files_not_to_touch)
    _append_markdown_list(lines, "Tests to run", context.tests_to_run)
    _append_markdown_list(lines, "Reasons", context.reasons)
    return "\n".join(lines).rstrip() + "\n"


def _status_from_gate(gate_status: str) -> str:
    """Support status from gate behavior.
    
    Parameters
    ----------
    gate_status : str
        The gate status value.
    
    Returns
    -------
    str
        The string result.
    """
    
    normalized = normalize_project_atlas_text(gate_status)
    if normalized == PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH:
        return ENGINEERING_SAFETY_ATLAS_STATUS_READY
    if normalized in {
        PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_NEEDS_OWNER_REVIEW,
        PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_WRONG_TARGET_FILE,
        PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_DUPLICATE_SYMBOL_RISK,
        PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_FACADE_PATCH_RISK,
        PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_MISSING_TEST_PROTECTION,
        PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_EVIDENCE_STALE,
    }:
        return ENGINEERING_SAFETY_ATLAS_STATUS_NEEDS_OWNER_REVIEW
    return ENGINEERING_SAFETY_ATLAS_STATUS_INSUFFICIENT_EVIDENCE


def _risk_level_from_gate(gate_status: str, gate_data: dict[str, Any]) -> str:
    """Support risk level from gate behavior.
    
    Parameters
    ----------
    gate_status : str
        The gate status value.
    gate_data : dict[str, Any]
        The gate data value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if gate_data.get("wrong_target_file") or gate_data.get("facade_patch_risk"):
        return ENGINEERING_SAFETY_ATLAS_RISK_HIGH
    if gate_data.get("duplicate_symbol_risk"):
        return ENGINEERING_SAFETY_ATLAS_RISK_HIGH
    if gate_data.get("missing_test_protection") or gate_data.get("evidence_stale"):
        return ENGINEERING_SAFETY_ATLAS_RISK_MEDIUM
    if gate_status == PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH:
        return ENGINEERING_SAFETY_ATLAS_RISK_LOW
    return ENGINEERING_SAFETY_ATLAS_RISK_UNKNOWN


def _warnings_from_gate(gate: Any) -> tuple[str, ...]:
    """Support warnings from gate behavior.
    
    Parameters
    ----------
    gate : Any
        The gate value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    warnings = []
    if getattr(gate, "facade_patch_risk", False):
        warnings.append("Target may be a facade; review the real owner before patching.")
    if getattr(gate, "wrong_target_file", False):
        warnings.append("Target differs from the recommended primary edit target.")
    if getattr(gate, "duplicate_symbol_risk", False):
        warnings.append("Requested symbol has duplicate public-symbol risk.")
    if getattr(gate, "missing_test_protection", False):
        warnings.append("Focused test protection may be missing for this change.")
    if getattr(gate, "evidence_stale", False):
        warnings.append("Project Analysis Evidence may be stale or advisory only.")
    return tuple(warnings)


def _confidence_from_gate(gate_confidence: str, existing_confidence: str) -> str:
    """Support confidence from gate behavior.
    
    Parameters
    ----------
    gate_confidence : str
        The gate confidence value.
    existing_confidence : str
        The existing confidence value.
    
    Returns
    -------
    str
        The string result.
    """
    
    gate = normalize_project_atlas_text(gate_confidence).lower()
    existing = normalize_project_atlas_text(existing_confidence).lower()
    if gate == "high" or existing == "high":
        return "high"
    if gate == "medium" or existing == "medium":
        return "medium"
    if gate or existing:
        return "low"
    return "unknown"


def _global_validation_commands() -> tuple[str, ...]:
    """Support global validation commands behavior.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return (
        "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root <PROJECT_ROOT> --validate",
        "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root <PROJECT_ROOT> --validate",
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
    
    result = []
    for value in normalize_project_atlas_sequence(values):
        if value not in result:
            result.append(value)
    return tuple(result)


def _append_markdown_list(lines: list[str], title: str, values: tuple[str, ...]) -> None:
    """Support append markdown list behavior.
    
    Parameters
    ----------
    lines : list[str]
        The line values.
    title : str
        The title value.
    values : tuple[str, ...]
        The input values.
    """
    
    lines.append("## " + title)
    if not values:
        lines.append("- None")
    else:
        for value in values:
            lines.append("- " + value)
    lines.append("")
