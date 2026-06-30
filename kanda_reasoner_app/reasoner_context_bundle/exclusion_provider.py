# project-path: kanda_reasoner_app/reasoner_context_bundle/exclusion_provider.py
"""Adapter for loading active project exclusion rules.

This module reads the existing project exclusion policy through its public
functions. It does not modify Tab 8 settings or duplicate project-specific
ignore data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_exclusion_policy import (
    load_reasoner_project_exclusion_rules,
    normalize_project_exclusion_rules,
)

from .schema_models import ExclusionRules, ProjectContext
from .project_context import resolve_project_context

__all__ = [
    "EXCLUSION_RULES_SOURCE",
    "load_bundle_exclusion_rules",
]

EXCLUSION_RULES_SOURCE = (
    "kanda_reasoner_app.project_exclusion_policy."
    "load_reasoner_project_exclusion_rules"
)


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


def load_bundle_exclusion_rules(project: str | Path | ProjectContext) -> ExclusionRules:
    """Load normalized exclusion rules for one active project.

    The rules come from the existing central project exclusion policy. This
    keeps Tab 8/project-ignore semantics in one owner box while allowing this
    package to export the rules used for an AI context bundle.
    """
    context = _context(project)
    raw_rules: dict[str, Any] = load_reasoner_project_exclusion_rules(context.root)
    normalized = normalize_project_exclusion_rules(raw_rules)
    return ExclusionRules(
        folders=tuple(normalized.get("folders", [])),
        files=tuple(normalized.get("files", [])),
        extensions=tuple(normalized.get("extensions", [])),
        source=EXCLUSION_RULES_SOURCE,
    )
