# project-path: kanda_reasoner_app/engineering_diagnostics/baseline.py
"""Pure baseline comparison rules for Engineering Diagnostics."""

from __future__ import annotations

from collections.abc import Iterable

__all__ = ["compare_issue_fingerprints"]


def compare_issue_fingerprints(
    current: Iterable[str],
    baseline: Iterable[str],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Return new, persistent, and resolved fingerprints in stable order."""
    current_set = frozenset(str(item) for item in current)
    baseline_set = frozenset(str(item) for item in baseline)
    new_items = tuple(sorted(current_set - baseline_set))
    persistent_items = tuple(sorted(current_set & baseline_set))
    resolved_items = tuple(sorted(baseline_set - current_set))
    return new_items, persistent_items, resolved_items
