"""Models for bounded Workbench Local AI correction execution."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = ["LocalAIWorkbenchCorrectionCandidate"]


@dataclass(frozen=True)
class LocalAIWorkbenchCorrectionCandidate:
    """Bounded Local AI candidate produced outside the Qt GUI thread."""

    ok: bool
    message: str
    report: Any = None
    corrected_plan: Any = None
    proposals: tuple[Any, ...] = ()
    review_status: str = ""
    corrections_applied: int = 0
    model_name: str = ""
