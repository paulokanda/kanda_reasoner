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

from .implementation_responsibility_helpers_private import (
    _choose_primary_edit_target,
    _extra_reasons,
    _files_not_to_touch,
    _merge_reasons,
    _merge_tests,
    _needs_owner_review,
    _normalized_path,
    _secondary_helper_targets,
    _status_and_confidence,
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
