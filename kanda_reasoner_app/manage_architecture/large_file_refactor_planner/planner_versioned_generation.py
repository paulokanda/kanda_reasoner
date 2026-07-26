# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_versioned_generation.py
"""Pure routing contract for locally generated Planner versions."""

from __future__ import annotations

from dataclasses import dataclass

from .planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_WEB_AI,
)

__all__ = ["PlannerGenerationRoute", "planner_generation_route"]


@dataclass(frozen=True)
class PlannerGenerationRoute:
    """Describe post-heuristic work for locally generated version intents."""

    version_name: str
    generate_docstrings_automatically: bool
    start_local_ai_review: bool
    prepare_web_ai_exchange: bool


def planner_generation_route(version_name: str) -> PlannerGenerationRoute:
    """Return the deterministic route for one selected Planner version intent."""

    if version_name == PLANNER_VERSION_HEURISTIC:
        return PlannerGenerationRoute(
            version_name=version_name,
            generate_docstrings_automatically=True,
            start_local_ai_review=False,
            prepare_web_ai_exchange=False,
        )
    if version_name == PLANNER_VERSION_LOCAL_AI:
        return PlannerGenerationRoute(
            version_name=version_name,
            generate_docstrings_automatically=True,
            start_local_ai_review=True,
            prepare_web_ai_exchange=False,
        )
    if version_name == PLANNER_VERSION_WEB_AI:
        return PlannerGenerationRoute(
            version_name=version_name,
            generate_docstrings_automatically=False,
            start_local_ai_review=False,
            prepare_web_ai_exchange=False,
        )
    raise ValueError("Unknown Planner version route: " + str(version_name))
