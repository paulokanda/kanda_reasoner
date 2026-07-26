# project-path: kanda_reasoner_app/reasoner_symbol_atlas/implementation_responsibility_helpers_private.py
"""Private helpers for Project Symbol Atlas responsibility resolution."""

from __future__ import annotations

from pathlib import Path

from .output_policy import is_active_atlas_path, is_active_test_command
from .facade_owner_resolver import (
    PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW,
    PROJECT_SYMBOL_ATLAS_FACADE_STATUS_READY,
)
from .logic_placement_advisor import (
    PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_READY,
    PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET,
)
from .main_helper_mapper import PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY
from .schemas import normalize_project_atlas_text

_STATUS_READY = "ready"
_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
_STATUS_WRONG_TARGET = "wrong_target_file"
_STATUS_TARGET_NOT_FOUND = "target_not_found"

__all__: list[str] = []


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
        return _STATUS_TARGET_NOT_FOUND, "low"
    if wrong_box_risk or placement_status == PROJECT_SYMBOL_ATLAS_PLACEMENT_STATUS_WRONG_TARGET:
        return _STATUS_WRONG_TARGET, "high"
    if facade_patch_risk or needs_owner_review:
        return _STATUS_NEEDS_OWNER_REVIEW, "high"
    if main_helper_status == PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY:
        return _STATUS_READY, "high"
    return _STATUS_READY, "medium"


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
