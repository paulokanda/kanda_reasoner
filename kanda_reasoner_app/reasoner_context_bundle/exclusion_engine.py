# project-path: kanda_reasoner_app/reasoner_context_bundle/exclusion_engine.py
"""Exclusion decision helpers for AI context bundle generation."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.project_exclusion_path_matching import (
    file_rule_matches,
    folder_rule_matches,
)
from kanda_reasoner_app.project_exclusion_policy import (
    should_exclude_reasoner_project_path,
)

from .path_normalization import relative_posix_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ExclusionDecision, ExclusionRules, ProjectContext

__all__ = ["decide_path_exclusion"]


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    """Support context behavior.
    
    Parameters
    ----------
    project : str | Path | ProjectContext
        The project value.
    
    Returns
    -------
    ProjectContext
        The project context result.
    """
    
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _as_policy_dict(rules: ExclusionRules) -> dict[str, list[str]]:
    """Support as policy dict behavior.
    
    Parameters
    ----------
    rules : ExclusionRules
        The rules value.
    
    Returns
    -------
    dict[str, list[str]]
        The mapped values.
    """
    
    return {
        "folders": list(rules.folders),
        "files": list(rules.files),
        "extensions": list(rules.extensions),
    }


def _path_for_decision(path: str | Path, root: Path) -> Path:
    """Support path for decision behavior.
    
    Parameters
    ----------
    path : str | Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    candidate = Path(path)
    if candidate.is_absolute():
        return safe_resolve(candidate)
    return safe_resolve(root / candidate)


def _matched_rule(rel_path: str, path: Path, rules: ExclusionRules) -> tuple[str, str, str]:
    """Support matched rule behavior.
    
    Parameters
    ----------
    rel_path : str
        The rel path value.
    path : Path
        The file or folder path.
    rules : ExclusionRules
        The rules value.
    
    Returns
    -------
    tuple[str, str, str]
        The tuple of values.
    """
    
    for folder in rules.folders:
        if folder_rule_matches(rel_path, folder, path_is_dir=path.is_dir()):
            return str(folder), "folder", "Matched excluded folder rule."
    for file_rule in rules.files:
        if file_rule_matches(rel_path, path.name, file_rule):
            return str(file_rule), "file", "Matched excluded file pattern."
    suffix_low = path.suffix.lower()
    for extension in rules.extensions:
        if suffix_low == str(extension).lower():
            return str(extension), "extension", "Matched excluded extension."
    return "", "", "No exclusion rule matched."


def decide_path_exclusion(
    path: str | Path,
    project: str | Path | ProjectContext,
    rules: ExclusionRules,
) -> ExclusionDecision:
    """Return a detailed inclusion or exclusion decision for one path.

    The authoritative include/exclude decision delegates to the existing central
    project exclusion policy. The matched rule detail is computed locally from
    the same normalized rules for reporting in exclusion_rules.json.
    """
    context = _context(project)
    root = safe_resolve(context.root)
    candidate = _path_for_decision(path, root)
    try:
        rel_path = relative_posix_path(candidate, root)
    except ValueError:
        return ExclusionDecision(
            path=str(path).replace("\\", "/"),
            included=False,
            excluded=True,
            matched_rule="outside_project_root",
            rule_type="boundary",
            reason="Path is outside the active project root.",
        )

    excluded = should_exclude_reasoner_project_path(
        candidate,
        root,
        _as_policy_dict(rules),
    )
    matched_rule, rule_type, reason = _matched_rule(rel_path, candidate, rules)
    if not excluded:
        matched_rule = ""
        rule_type = ""
        reason = "Path is included by active project exclusion rules."
    elif not matched_rule:
        matched_rule = "central_policy"
        rule_type = "unknown"
        reason = "Central exclusion policy excluded this path."

    return ExclusionDecision(
        path=rel_path,
        included=not excluded,
        excluded=excluded,
        matched_rule=matched_rule,
        rule_type=rule_type,
        reason=reason,
    )
