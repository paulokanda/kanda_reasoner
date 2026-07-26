# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_workbench_handoff.py
"""Public immutable export contract from Planner to Workbench."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

__all__ = [
    "PLANNER_WORKBENCH_HANDOFF_FEATURE_ID",
    "PlannerWorkbenchHandoff",
    "export_latest_planner_workbench_handoff",
    "planner_workbench_handoff_hash_valid",
]

PLANNER_WORKBENCH_HANDOFF_FEATURE_ID = (
    "large-file-refactor-planner-workbench-handoff-v1"
)


@dataclass(frozen=True)
class PlannerWorkbenchHandoff:
    """Immutable serialized Planner export for one explicit Workbench load."""

    schema_version: str
    feature_id: str
    plan_json: str
    analysis_json: str
    candidate_paths: tuple[str, ...]
    handoff_hash: str


def export_latest_planner_workbench_handoff(
    window: object,
) -> PlannerWorkbenchHandoff:
    """Export latest Planner state through one public immutable contract."""

    plan = getattr(window, "_large_file_refactor_last_plan", None)
    analysis = getattr(window, "_large_file_refactor_last_analysis", None)
    candidates = getattr(window, "_large_file_refactor_planner_candidates", [])
    plan_json = _canonical_object_json(plan)
    analysis_json = _canonical_object_json(analysis)
    candidate_paths = _candidate_path_tuple(candidates)
    handoff_hash = _handoff_hash(
        plan_json=plan_json,
        analysis_json=analysis_json,
        candidate_paths=candidate_paths,
    )
    return PlannerWorkbenchHandoff(
        schema_version="1.0",
        feature_id=PLANNER_WORKBENCH_HANDOFF_FEATURE_ID,
        plan_json=plan_json,
        analysis_json=analysis_json,
        candidate_paths=candidate_paths,
        handoff_hash=handoff_hash,
    )


def planner_workbench_handoff_hash_valid(
    handoff: PlannerWorkbenchHandoff,
) -> bool:
    """Return whether handoff payload matches its own canonical hash."""

    return handoff.handoff_hash == _handoff_hash(
        plan_json=handoff.plan_json,
        analysis_json=handoff.analysis_json,
        candidate_paths=handoff.candidate_paths,
    )


def _canonical_object_json(value: Any) -> str:
    """Return canonical JSON from a Planner contract object."""

    if value is None:
        return ""
    to_dict = getattr(value, "to_dict", None)
    if not callable(to_dict):
        raise TypeError("Planner handoff object must expose to_dict().")
    return json.dumps(
        to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def _candidate_path_tuple(candidates: list[object]) -> tuple[str, ...]:
    """Return stable paths without sharing Planner candidate objects."""

    return tuple(
        sorted(
            {
                str(getattr(candidate, "path", "") or "").strip()
                for candidate in candidates
                if str(getattr(candidate, "path", "") or "").strip()
            }
        )
    )


def _handoff_hash(
    *,
    plan_json: str,
    analysis_json: str,
    candidate_paths: tuple[str, ...],
) -> str:
    """Return canonical SHA-256 for one Planner handoff."""

    payload = json.dumps(
        {
            "plan_json": plan_json,
            "analysis_json": analysis_json,
            "candidate_paths": list(candidate_paths),
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
