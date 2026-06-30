# project-path: kanda_reasoner_app/reasoner_symbol_atlas/implementation_responsibility_resolver.py
"""Read-only implementation responsibility resolver for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .output_policy import is_active_atlas_path, is_active_test_command
from .facade_owner_resolver import (
    PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW,
    PROJECT_SYMBOL_ATLAS_FACADE_STATUS_READY,
    ProjectSymbolAtlasFacadeOwnerOptions,
    resolve_reasoner_symbol_atlas_facade_owner,
)
from .logic_placement_advisor import (
    PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY,
    PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET,
    ProjectSymbolAtlasLogicPlacementOptions,
    advise_reasoner_symbol_atlas_logic_placement,
)
from .main_helper_mapper import (
    PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY,
    ProjectSymbolAtlasMainHelperOptions,
    map_reasoner_symbol_atlas_main_helpers,
)
from .schemas import (
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY = "ready"
PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_WRONG_TARGET = "wrong_target_file"
PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_TARGET_NOT_FOUND = "target_not_found"
PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_INSUFFICIENT_EVIDENCE = "insufficient_evidence"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_INSUFFICIENT_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW",
    "PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY",
    "PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_TARGET_NOT_FOUND",
    "PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_WRONG_TARGET",
    "ProjectSymbolAtlasImplementationResponsibilityDecision",
    "ProjectSymbolAtlasImplementationResponsibilityOptions",
    "build_reasoner_symbol_atlas_implementation_responsibility_report",
    "resolve_reasoner_symbol_atlas_implementation_responsibility",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasImplementationResponsibilityOptions:
    """Options for resolving implementation responsibility before a patch."""

    project_root: str
    task_description: str = ""
    target_path: str = ""
    symbol_name: str = ""
    json_path: str = ""
    include_tests: bool = False
    include_workbench: bool = False
    include_private: bool = False

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
        }

    def to_placement_options(self) -> ProjectSymbolAtlasLogicPlacementOptions:
        """Return compatible logic placement options."""

        return ProjectSymbolAtlasLogicPlacementOptions(
            project_root=self.project_root,
            task_description=self.task_description,
            symbol_name=self.symbol_name,
            target_path=self.target_path,
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


@dataclass(frozen=True)
class ProjectSymbolAtlasImplementationResponsibilityDecision:
    """Decision output for implementation responsibility."""

    project_root: str
    task_description: str = ""
    recommended_owner_box: str = "unknown"
    primary_edit_target: str = ""
    secondary_helper_targets: tuple[str, ...] = field(default_factory=tuple)
    files_not_to_touch: tuple[str, ...] = field(default_factory=tuple)
    tests_to_run: tuple[str, ...] = field(default_factory=tuple)
    status: str = PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_INSUFFICIENT_EVIDENCE
    confidence: str = "low"
    facade_patch_risk: bool = False
    helper_public_api_risk: bool = False
    wrong_box_risk: bool = False
    needs_owner_review: bool = False
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible decision dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "task_description": normalize_project_atlas_text(self.task_description),
            "recommended_owner_box": normalize_project_atlas_text(self.recommended_owner_box),
            "primary_edit_target": str(Path(self.primary_edit_target)) if self.primary_edit_target else "",
            "secondary_helper_targets": normalize_project_atlas_sequence(self.secondary_helper_targets),
            "files_not_to_touch": normalize_project_atlas_sequence(self.files_not_to_touch),
            "tests_to_run": normalize_project_atlas_sequence(self.tests_to_run),
            "status": normalize_project_atlas_text(self.status),
            "confidence": normalize_project_atlas_text(self.confidence),
            "facade_patch_risk": bool(self.facade_patch_risk),
            "helper_public_api_risk": bool(self.helper_public_api_risk),
            "wrong_box_risk": bool(self.wrong_box_risk),
            "needs_owner_review": bool(self.needs_owner_review),
            "reasons": normalize_project_atlas_sequence(self.reasons),
        }


def resolve_reasoner_symbol_atlas_implementation_responsibility(
    options: ProjectSymbolAtlasImplementationResponsibilityOptions,
) -> ProjectSymbolAtlasImplementationResponsibilityDecision:
    """Resolve which file is responsible for the requested implementation."""

    placement = advise_reasoner_symbol_atlas_logic_placement(
        options.to_placement_options()
    )
    facade = resolve_reasoner_symbol_atlas_facade_owner(options.to_facade_options())
    main_helper = map_reasoner_symbol_atlas_main_helpers(options.to_main_helper_options())

    primary_target = _choose_primary_edit_target(
        placement_primary=placement.primary_target_path,
        facade_owner=facade.likely_real_owner_path,
        facade_patch_risk=facade.target_is_facade,
        main_path=main_helper.main_path,
        helper_target=_normalized_path(options.target_path),
    )
    secondary_helpers = _secondary_helper_targets(
        primary_target=primary_target,
        helper_paths=main_helper.helper_paths,
    )
    files_not_to_touch = _files_not_to_touch(
        target_path=options.target_path,
        primary_target=primary_target,
        facade_target=facade.target_path if facade.target_is_facade else "",
        forbidden_boxes=placement.forbidden_boxes,
    )
    tests_to_run = _merge_tests(
        placement.tests_to_run,
        main_helper.tests_to_run,
        primary_target,
    )
    helper_public_api_risk = bool(main_helper.public_helper_warnings)
    wrong_box_risk = placement.status == PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET
    needs_owner_review = _needs_owner_review(
        placement_status=placement.status,
        facade_status=facade.status,
        facade_patch_risk=facade.target_is_facade,
        helper_public_api_risk=helper_public_api_risk,
    )
    status, confidence = _status_and_confidence(
        primary_target=primary_target,
        facade_patch_risk=facade.target_is_facade,
        wrong_box_risk=wrong_box_risk,
        needs_owner_review=needs_owner_review,
        placement_status=placement.status,
        main_helper_status=main_helper.status,
    )
    reasons = _merge_reasons(
        placement.reasons,
        facade.reasons,
        facade.facade_evidence,
        main_helper.evidence,
        _extra_reasons(
            primary_target=primary_target,
            facade_patch_risk=facade.target_is_facade,
            helper_public_api_risk=helper_public_api_risk,
            wrong_box_risk=wrong_box_risk,
        ),
    )
    return ProjectSymbolAtlasImplementationResponsibilityDecision(
        project_root=str(Path(options.project_root).expanduser().resolve(strict=False)),
        task_description=options.task_description,
        recommended_owner_box=placement.recommended_owner_box,
        primary_edit_target=primary_target,
        secondary_helper_targets=secondary_helpers,
        files_not_to_touch=files_not_to_touch,
        tests_to_run=tests_to_run,
        status=status,
        confidence=confidence,
        facade_patch_risk=facade.target_is_facade,
        helper_public_api_risk=helper_public_api_risk,
        wrong_box_risk=wrong_box_risk,
        needs_owner_review=needs_owner_review,
        reasons=reasons,
    )


def build_reasoner_symbol_atlas_implementation_responsibility_report(
    options: ProjectSymbolAtlasImplementationResponsibilityOptions,
) -> ProjectSymbolAtlasReport:
    """Build a report for implementation responsibility."""

    decision = resolve_reasoner_symbol_atlas_implementation_responsibility(options)
    evidence = decision.reasons + (
        "Implementation responsibility status: " + decision.status,
        "Recommended owner box: " + decision.recommended_owner_box,
    )
    symbol = ProjectSymbol(
        name="implementation_responsibility_decision",
        kind="unknown",
        module="reasoner_symbol_atlas.implementation_responsibility_resolver",
        path=decision.primary_edit_target,
        is_public=False,
        owner_role="unknown",
        evidence=evidence,
    )
    return ProjectSymbolAtlasReport(
        project_root=decision.project_root,
        report_type="reasoner_symbol_atlas",
        summary=_format_decision_summary(decision),
        symbols=(symbol,),
        input_sources=(
            "live_ast",
            "complete_json_if_fresh",
            "logic_placement_advisor",
            "facade_owner_resolver",
            "main_helper_mapper",
            "implementation_responsibility_resolver",
        ),
    )


def _normalized_path(path_text: str) -> str:
    """Support normalized path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not path_text:
        return ""
    return str(Path(path_text)).replace("\\", "/")


def _active_path_or_empty(path_text: str) -> str:
    """Support active path or empty behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    normalized = _normalized_path(path_text)
    if normalized and is_active_atlas_path(normalized):
        return normalized
    return ""


def _choose_primary_edit_target(
    placement_primary: str,
    facade_owner: str,
    facade_patch_risk: bool,
    main_path: str,
    helper_target: str,
) -> str:
    """Support choose primary edit target behavior.
    
    Parameters
    ----------
    placement_primary : str
        The placement primary value.
    facade_owner : str
        The facade owner value.
    facade_patch_risk : bool
        The facade patch risk value.
    main_path : str
        The main path value.
    helper_target : str
        The helper target value.
    
    Returns
    -------
    str
        The string result.
    """
    
    active_helper = _active_path_or_empty(helper_target)
    active_placement = _active_path_or_empty(placement_primary)
    active_facade_owner = _active_path_or_empty(facade_owner)
    active_main = _active_path_or_empty(main_path)

    if facade_patch_risk and active_facade_owner:
        return active_facade_owner
    if active_helper and active_main and active_helper.lower() != active_main.lower():
        return active_main
    if active_helper:
        return active_helper
    if active_main:
        return active_main
    if active_placement:
        return active_placement
    if active_facade_owner:
        return active_facade_owner
    return ""


def _secondary_helper_targets(
    primary_target: str,
    helper_paths: tuple[str, ...],
) -> tuple[str, ...]:
    """Support secondary helper targets behavior.
    
    Parameters
    ----------
    primary_target : str
        The primary target value.
    helper_paths : tuple[str, ...]
        The helper paths value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    primary_key = _normalized_path(primary_target).lower()
    for path in helper_paths:
        key = _active_path_or_empty(path)
        if key and key.lower() != primary_key and key not in values:
            values.append(key)
    return tuple(values)


def _files_not_to_touch(
    target_path: str,
    primary_target: str,
    facade_target: str,
    forbidden_boxes: tuple[str, ...],
) -> tuple[str, ...]:
    """Support files not to touch behavior.
    
    Parameters
    ----------
    target_path : str
        The target path value.
    primary_target : str
        The primary target value.
    facade_target : str
        The facade target value.
    forbidden_boxes : tuple[str, ...]
        The forbidden boxes value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    target = _active_path_or_empty(target_path)
    primary = _active_path_or_empty(primary_target)
    facade = _active_path_or_empty(facade_target)
    if target and primary and target.lower() != primary.lower():
        values.append(target)
    if facade and facade not in values and facade.lower() != primary.lower():
        values.append(facade)
    for box in forbidden_boxes:
        marker = "box:" + normalize_project_atlas_text(box)
        if marker not in values:
            values.append(marker)
    return tuple(values)


def _merge_tests(
    placement_tests: tuple[str, ...],
    helper_tests: tuple[str, ...],
    primary_target: str,
) -> tuple[str, ...]:
    """Support merge tests behavior.
    
    Parameters
    ----------
    placement_tests : tuple[str, ...]
        The placement tests value.
    helper_tests : tuple[str, ...]
        The helper tests value.
    primary_target : str
        The primary target value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    tests: list[str] = []
    if primary_target and is_active_atlas_path(primary_target):
        command = "python -m py_compile " + primary_target
        if is_active_test_command(command):
            tests.append(command)
    for value in placement_tests + helper_tests:
        if value and is_active_test_command(value) and value not in tests:
            tests.append(value)
    required = (
        "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root <PROJECT_ROOT> --validate",
        "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root <PROJECT_ROOT> --validate",
    )
    for value in required:
        if value not in tests:
            tests.append(value)
    return tuple(tests)


def _needs_owner_review(
    placement_status: str,
    facade_status: str,
    facade_patch_risk: bool,
    helper_public_api_risk: bool,
) -> bool:
    """Support needs owner review behavior.
    
    Parameters
    ----------
    placement_status : str
        The placement status value.
    facade_status : str
        The facade status value.
    facade_patch_risk : bool
        The facade patch risk value.
    helper_public_api_risk : bool
        The helper public api risk value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if facade_patch_risk:
        return True
    if helper_public_api_risk:
        return True
    if placement_status != PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY:
        return True
    if facade_status in {
        PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW,
        PROJECT_SYMBOL_ATLAS_FACADE_STATUS_READY,
    }:
        return facade_patch_risk
    return False


def _status_and_confidence(
    primary_target: str,
    facade_patch_risk: bool,
    wrong_box_risk: bool,
    needs_owner_review: bool,
    placement_status: str,
    main_helper_status: str,
) -> tuple[str, str]:
    """Support status and confidence behavior.
    
    Parameters
    ----------
    primary_target : str
        The primary target value.
    facade_patch_risk : bool
        The facade patch risk value.
    wrong_box_risk : bool
        The wrong box risk value.
    needs_owner_review : bool
        The needs owner review value.
    placement_status : str
        The placement status value.
    main_helper_status : str
        The main helper status value.
    
    Returns
    -------
    tuple[str, str]
        The tuple of values.
    """
    
    if not primary_target:
        return PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_TARGET_NOT_FOUND, "low"
    if wrong_box_risk or placement_status == PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET:
        return PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_WRONG_TARGET, "high"
    if facade_patch_risk or needs_owner_review:
        return PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW, "high"
    if main_helper_status == PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY:
        return PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY, "high"
    return PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_READY, "medium"


def _merge_reasons(*groups: tuple[str, ...]) -> tuple[str, ...]:
    """Support merge reasons behavior.
    
    Parameters
    ----------
    *groups : tuple[str, ...]
        The groups value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    for group in groups:
        for value in group:
            cleaned = normalize_project_atlas_text(value)
            if cleaned and cleaned not in values:
                values.append(cleaned)
    return tuple(values)


def _extra_reasons(
    primary_target: str,
    facade_patch_risk: bool,
    helper_public_api_risk: bool,
    wrong_box_risk: bool,
) -> tuple[str, ...]:
    """Support extra reasons behavior.
    
    Parameters
    ----------
    primary_target : str
        The primary target value.
    facade_patch_risk : bool
        The facade patch risk value.
    helper_public_api_risk : bool
        The helper public api risk value.
    wrong_box_risk : bool
        The wrong box risk value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    reasons: list[str] = []
    if primary_target:
        reasons.append("Primary edit target selected: " + primary_target)
    if facade_patch_risk:
        reasons.append("Target appears to be a facade; edit the real owner instead.")
    if helper_public_api_risk:
        reasons.append("Helper exposes public API and needs owner review.")
    if wrong_box_risk:
        reasons.append("Target box differs from recommended owner box.")
    return tuple(reasons)


def _format_decision_summary(
    decision: ProjectSymbolAtlasImplementationResponsibilityDecision,
) -> str:
    """Support format decision summary behavior.
    
    Parameters
    ----------
    decision : ProjectSymbolAtlasImplementationResponsibilityDecision
        The decision value.
    
    Returns
    -------
    str
        The string result.
    """
    
    parts = [
        "Implementation responsibility: " + decision.status,
        "owner_box=" + decision.recommended_owner_box,
    ]
    if decision.primary_edit_target:
        parts.append("primary_edit_target=" + decision.primary_edit_target)
    parts.append("confidence=" + decision.confidence)
    return "; ".join(parts) + "."
