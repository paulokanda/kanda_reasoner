# project-path: kanda_reasoner_app/routing_signal_scorer/precomputed_semantic_evidence_artifact_design_helpers_private.py
"""Private validation helpers for the precomputed artifact design contract."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

__all__: list[str] = []


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _as_strings(value: Any) -> set[str]:
    if not _is_sequence(value):
        return set()
    return {item for item in value if isinstance(item, str)}


def _append_missing(errors: list[str], label: str, missing: set[str]) -> None:
    if missing:
        errors.append(f"missing {label}: {', '.join(sorted(missing))}")


def _find_forbidden_fields(
    mapping: Mapping[str, Any], forbidden: set[str] | frozenset[str]
) -> set[str]:
    found: set[str] = set()
    for key, value in mapping.items():
        if key in forbidden:
            found.add(key)
        if isinstance(value, Mapping):
            found.update(_find_forbidden_fields(value, forbidden))
        elif _is_sequence(value):
            for item in value:
                if isinstance(item, Mapping):
                    found.update(_find_forbidden_fields(item, forbidden))
    return found
