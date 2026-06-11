"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help
# PURPOSE       : Resolve the active project profile and expose normalized alias helpers.
# EXPORTS       : resolve_project_profile, get_profile_alias_terms, question_has_profile_alias, text_has_profile_alias, get_profile_owner_paths
# DEPENDS ON    : query_text.py
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import norm_text
from kanda_reasoner_app.reasoner_engine.project_profile import (
    GENERIC_PROJECT_PROFILE,
    ProjectProfile,
    infer_project_profile,
)

__all__ = [
    "resolve_project_profile",
    "get_profile_alias_terms",
    "question_has_profile_alias",
    "text_has_profile_alias",
    "get_profile_owner_paths",
]


def resolve_project_profile(project_index, project_profile: ProjectProfile | None) -> ProjectProfile:
    """
    Resolve the active project profile without changing retrieval behavior.
    """
    if isinstance(project_profile, ProjectProfile):
        return project_profile

    project_summary = (
        project_index.project_summary
        if isinstance(project_index.project_summary, dict)
        else {}
    )
    project_root = str(project_summary.get("project_root", "")).strip()
    packaging_metadata = (
        project_index.packaging_metadata
        if isinstance(project_index.packaging_metadata, dict)
        else {}
    )
    documentation_intent = (
        project_index.documentation_intent
        if isinstance(project_index.documentation_intent, dict)
        else {}
    )

    inferred = infer_project_profile(
        project_root=project_root,
        project_summary=project_summary,
        packaging_metadata=packaging_metadata,
        documentation_intent=documentation_intent,
    )

    if isinstance(inferred, ProjectProfile):
        return inferred

    return GENERIC_PROJECT_PROFILE


def get_profile_alias_terms(project_profile: ProjectProfile, alias_key: str) -> tuple[str, ...]:
    flags = project_profile.feature_flags if isinstance(project_profile.feature_flags, dict) else {}
    if not bool(flags.get("use_profile_question_aliases", False)):
        return ()

    alias_map = project_profile.question_aliases if isinstance(project_profile.question_aliases, dict) else {}
    raw_values = alias_map.get(alias_key, ())
    if not isinstance(raw_values, (list, tuple)):
        return ()

    out: list[str] = []
    for value in raw_values:
        normalized = norm_text(value)
        if normalized:
            out.append(normalized)

    return tuple(out)


def question_has_profile_alias(project_profile: ProjectProfile, question: str, alias_key: str) -> bool:
    return any(term in question for term in get_profile_alias_terms(project_profile, alias_key))


def text_has_profile_alias(project_profile: ProjectProfile, text: str, alias_key: str) -> bool:
    return any(term in text for term in get_profile_alias_terms(project_profile, alias_key))


def get_profile_owner_paths(project_profile: ProjectProfile, alias_key: str) -> tuple[str, ...]:
    return get_profile_alias_terms(project_profile, alias_key)






