# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/module_size_policy.py
"""Canonical physical-line policy for Large File Refactor outputs."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

__all__ = [
    "MIN_RESULTING_PHYSICAL_LINES",
    "MAX_RESULTING_PHYSICAL_LINES",
    "ResultingModuleSizeCheck",
    "count_physical_lines",
    "check_resulting_module_size",
    "module_size_blockers",
    "module_size_policy_summary",
]

MIN_RESULTING_PHYSICAL_LINES = 101
MAX_RESULTING_PHYSICAL_LINES = 499


@dataclass(frozen=True)
class ResultingModuleSizeCheck:
    """Stable size-policy evidence for one resulting Python source file."""

    relative_path: str
    physical_lines: int
    minimum_allowed: int
    maximum_allowed: int
    valid: bool
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready policy result."""
        return asdict(self)


def count_physical_lines(text: str) -> int:
    """Count physical source lines with one canonical project interpretation.

    The Workbench historically used ``str.splitlines()`` in Planner, Preview,
    payload, and post-apply validators.  Keeping that convention here avoids a
    silent contract change around a final newline while centralizing the rule.
    """
    return len(text.splitlines())


def check_resulting_module_size(
    text: str,
    *,
    relative_path: str,
) -> ResultingModuleSizeCheck:
    """Validate one resulting source file against the strict 101-499 policy."""
    physical_lines = count_physical_lines(text)
    blockers = module_size_blockers(
        physical_lines,
        relative_path=relative_path,
    )
    return ResultingModuleSizeCheck(
        relative_path=relative_path,
        physical_lines=physical_lines,
        minimum_allowed=MIN_RESULTING_PHYSICAL_LINES,
        maximum_allowed=MAX_RESULTING_PHYSICAL_LINES,
        valid=not blockers,
        blockers=blockers,
    )


def module_size_blockers(
    physical_lines: int,
    *,
    relative_path: str,
) -> list[str]:
    """Return deterministic blockers for one physical line count.

    Every resulting Python source file is governed identically.  There is no
    facade exception and no helper exception in this policy.
    """
    blockers: list[str] = []
    path = relative_path or "<unknown>"
    if physical_lines < MIN_RESULTING_PHYSICAL_LINES:
        blockers.append(
            f"MODULE_BELOW_MINIMUM:{path}:{physical_lines}:"
            f"MIN={MIN_RESULTING_PHYSICAL_LINES}"
        )
    if physical_lines > MAX_RESULTING_PHYSICAL_LINES:
        blockers.append(
            f"MODULE_ABOVE_MAXIMUM:{path}:{physical_lines}:"
            f"MAX={MAX_RESULTING_PHYSICAL_LINES}"
        )
    return blockers


def module_size_policy_summary() -> dict[str, object]:
    """Return stable policy metadata for manifests and operator displays."""
    return {
        "rule": "100 < physical_lines < 500",
        "minimum_allowed": MIN_RESULTING_PHYSICAL_LINES,
        "maximum_allowed": MAX_RESULTING_PHYSICAL_LINES,
        "facade_exception_allowed": False,
        "helper_exception_allowed": False,
        "artificial_padding_allowed": False,
        "counter": "len(text.splitlines())",
    }
