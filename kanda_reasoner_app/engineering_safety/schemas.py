# project-path: kanda_reasoner_app/engineering_safety/schemas.py
"""Shared report schemas for Engineering Safety tools."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

ENGINEERING_SAFETY_VALID_REPORT_TYPES = (
    "risk_change_radar",
    "crash_triage",
    "refactor_playbook",
)

ENGINEERING_SAFETY_VALID_RISK_LEVELS = (
    "low",
    "medium",
    "high",
    "critical",
    "unknown",
)

ENGINEERING_SAFETY_VALID_CONFIDENCE = (
    "low",
    "medium",
    "high",
    "unknown",
)

DEFAULT_HUMAN_DECISION = "pending"
DEFAULT_VALIDATION_STATUS = "not_run"

__all__ = [
    "DEFAULT_HUMAN_DECISION",
    "DEFAULT_VALIDATION_STATUS",
    "EngineeringSafetyReport",
    "ENGINEERING_SAFETY_VALID_CONFIDENCE",
    "ENGINEERING_SAFETY_VALID_REPORT_TYPES",
    "ENGINEERING_SAFETY_VALID_RISK_LEVELS",
    "make_engineering_safety_report_id",
    "make_utc_timestamp",
    "normalize_engineering_safety_report_type",
    "normalize_report_sequence",
    "normalize_report_text",
]


def make_utc_timestamp() -> str:
    """Return an ISO 8601 UTC timestamp for report metadata."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_engineering_safety_report_id(report_type: str) -> str:
    """Create a stable human-readable report id."""
    safe_type = normalize_engineering_safety_report_type(report_type)
    return safe_type + "_" + uuid4().hex[:12]


def normalize_engineering_safety_report_type(report_type: str) -> str:
    """Validate and normalize an engineering safety report type."""
    normalized = str(report_type or "").strip().lower()
    if normalized not in ENGINEERING_SAFETY_VALID_REPORT_TYPES:
        raise ValueError("Unsupported engineering safety report type: " + str(report_type))
    return normalized


def normalize_report_text(value: object) -> str:
    """Return a clean string for report fields."""
    if value is None:
        return ""
    return str(value).strip()


def normalize_report_sequence(values: object) -> list[str]:
    """Normalize report list fields while preserving order."""
    if values is None:
        return []
    if isinstance(values, (str, bytes)):
        text = normalize_report_text(values.decode("utf-8", errors="replace") if isinstance(values, bytes) else values)
        return [text] if text else []
    try:
        result = []
        for item in values:  # type: ignore[operator]
            text = normalize_report_text(item)
            if text:
                result.append(text)
        return result
    except TypeError:
        text = normalize_report_text(values)
        return [text] if text else []


@dataclass(slots=True)
class EngineeringSafetyReport:
    """Structured report shared by Engineering Safety commands."""

    report_type: str
    project_root: str
    risk_level: str = "unknown"
    owning_box: str = ""
    affected_files: list[str] = field(default_factory=list)
    root_cause_or_risk_hypothesis: str = ""
    suggested_first_action: str = ""
    tests_to_run: list[str] = field(default_factory=list)
    rollback_plan: str = ""
    confidence: str = "unknown"
    input_sources: list[str] = field(default_factory=list)
    human_decision: str = DEFAULT_HUMAN_DECISION
    validation_status: str = DEFAULT_VALIDATION_STATUS
    evidence: list[str] = field(default_factory=list)
    report_id: str = ""
    created_at: str = ""

    def __post_init__(self) -> None:
        """Normalize fields after initialization."""
        self.report_type = normalize_engineering_safety_report_type(self.report_type)
        self.project_root = str(Path(self.project_root)) if self.project_root else ""
        self.risk_level = self._normalize_choice(self.risk_level, ENGINEERING_SAFETY_VALID_RISK_LEVELS, "unknown")
        self.confidence = self._normalize_choice(self.confidence, ENGINEERING_SAFETY_VALID_CONFIDENCE, "unknown")
        self.owning_box = normalize_report_text(self.owning_box)
        self.root_cause_or_risk_hypothesis = normalize_report_text(
            self.root_cause_or_risk_hypothesis
        )
        self.suggested_first_action = normalize_report_text(self.suggested_first_action)
        self.rollback_plan = normalize_report_text(self.rollback_plan)
        self.human_decision = normalize_report_text(self.human_decision) or DEFAULT_HUMAN_DECISION
        self.validation_status = normalize_report_text(self.validation_status) or DEFAULT_VALIDATION_STATUS
        self.affected_files = normalize_report_sequence(self.affected_files)
        self.tests_to_run = normalize_report_sequence(self.tests_to_run)
        self.input_sources = normalize_report_sequence(self.input_sources)
        self.evidence = normalize_report_sequence(self.evidence)
        self.report_id = normalize_report_text(self.report_id) or make_engineering_safety_report_id(
            self.report_type
        )
        self.created_at = normalize_report_text(self.created_at) or make_utc_timestamp()

    @staticmethod
    def _normalize_choice(value: object, choices: tuple[str, ...], fallback: str) -> str:
        """Support normalize choice behavior.
        
        Parameters
        ----------
        value : object
            The input value.
        choices : tuple[str, ...]
            The choices value.
        fallback : str
            The fallback value.
        
        Returns
        -------
        str
            The string result.
        """
        
        normalized = normalize_report_text(value).lower()
        return normalized if normalized in choices else fallback

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable report dictionary."""
        return asdict(self)
