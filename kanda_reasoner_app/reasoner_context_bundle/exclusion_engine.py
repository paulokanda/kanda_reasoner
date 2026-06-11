"""Exclusion decision helpers for AI context bundle generation."""

from __future__ import annotations

import fnmatch
from pathlib import Path

from kanda_reasoner_app.project_exclusion_policy import (
    should_exclude_reasoner_project_path,
)

from .path_normalization import relative_posix_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ExclusionDecision, ExclusionRules, ProjectContext

__all__ = ["decide_path_exclusion"]


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _as_policy_dict(rules: ExclusionRules) -> dict[str, list[str]]:
    return {
        "folders": list(rules.folders),
        "files": list(rules.files),
        "extensions": list(rules.extensions),
    }


def _path_for_decision(path: str | Path, root: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return safe_resolve(candidate)
    return safe_resolve(root / candidate)


def _folder_matches(rel_path: str, rule: str) -> bool:
    rule_text = str(rule).strip().lower().replace("\\", "/").strip("/")
    if not rule_text:
        return False
    rel_low = rel_path.lower().replace("\\", "/").strip("/")
    parts = [part.lower() for part in rel_low.split("/") if part]
    return (
        rule_text in parts
        or fnmatch.fnmatch(rel_low, rule_text)
        or fnmatch.fnmatch(rel_low, rule_text + "/*")
        or any(fnmatch.fnmatch(part, rule_text) for part in parts)
    )


def _file_matches(rel_path: str, name: str, rule: str) -> bool:
    pattern = str(rule).strip().lower().replace("\\", "/")
    if not pattern:
        return False
    return fnmatch.fnmatch(name.lower(), pattern) or fnmatch.fnmatch(
        rel_path.lower(), pattern
    )


def _matched_rule(rel_path: str, path: Path, rules: ExclusionRules) -> tuple[str, str, str]:
    for folder in rules.folders:
        if _folder_matches(rel_path, folder):
            return str(folder), "folder", "Matched excluded folder rule."
    for file_rule in rules.files:
        if _file_matches(rel_path, path.name, file_rule):
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
