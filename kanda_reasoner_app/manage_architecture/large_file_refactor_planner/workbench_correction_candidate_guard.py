"""Deterministic material-change guards for Workbench correction candidates."""
from __future__ import annotations

import json
from typing import Any

from .planner_version_state import (
    PLANNER_VERSION_WEB_AI,
    get_planner_version_bundle,
)

__all__ = ["plans_materially_different", "web_ai_plan_materially_changes"]


def plans_materially_different(before: Any, after: Any) -> bool:
    """Return whether two plan objects differ by canonical serialized content."""
    return _canonical_plan_text(before) != _canonical_plan_text(after)


def web_ai_plan_materially_changes(window: object, current_plan: Any) -> bool:
    """Return whether the accepted Web AI version changes the current plan."""
    bundle = get_planner_version_bundle(window, PLANNER_VERSION_WEB_AI)
    return plans_materially_different(current_plan, getattr(bundle, "plan", None))


def _canonical_plan_text(plan: Any) -> str:
    if plan is None:
        return "<none>"
    to_dict = getattr(plan, "to_dict", None)
    if callable(to_dict):
        try:
            payload = to_dict()
            return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        except (TypeError, ValueError):
            pass
    return repr(plan)
