"""Collection and advisory-note helpers for similarity runtime."""

from __future__ import annotations

from typing import Mapping, Sequence

from .advisory import _coerce_score
from .models import SIMILARITY_PROMOTION_THRESHOLD


def _similarity_expected_values(
    matches: Sequence[Mapping[str, object]],
    key: str,
) -> list[str]:
    """Collect promoted list values from similarity matches.

    Values keep their source order. Matches below the promotion threshold and
    non-sequence payloads are ignored.
    """

    values: list[str] = []
    for match in matches:
        score = _coerce_score(match.get("similarity_score", 0.0))
        if score < SIMILARITY_PROMOTION_THRESHOLD:
            continue
        raw_values = match.get(key, [])
        if not isinstance(raw_values, Sequence) or isinstance(
            raw_values,
            (str, bytes),
        ):
            continue
        values.extend(str(item) for item in raw_values if str(item))
    return values


def _merge_string_lists(*items: object) -> list[str]:
    """Merge ordered string sequences without duplicates.

    Non-sequence values and text-like scalar values are ignored so callers can
    safely pass advisory fields with defensive runtime typing.
    """

    result: list[str] = []
    seen: set[str] = set()
    for raw in items:
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
            continue
        for item in raw:
            value = str(item)
            if not value or value in seen:
                continue
            seen.add(value)
            result.append(value)
    return result


def _merge_route_family_suggestions(
    *groups: object,
) -> list[dict[str, object]]:
    """Merge ordered route-family suggestions by family identity."""

    result: list[dict[str, object]] = []
    seen: set[str] = set()
    for group in groups:
        if not isinstance(group, Sequence) or isinstance(group, (str, bytes)):
            continue
        for item in group:
            if not isinstance(item, Mapping):
                continue
            family = str(item.get("family") or "")
            if not family or family in seen:
                continue
            seen.add(family)
            result.append(dict(item))
    return result


def _similarity_notes(
    matches: Sequence[Mapping[str, object]],
) -> list[str]:
    """Build advisory-only notes for the similarity result."""

    notes = [
        (
            "Runtime-lite similarity is advisory only and must not replace "
            "deterministic KANDA routing."
        ),
        (
            "The canon decides final route, required prompts, missing context, "
            "and May proceed now."
        ),
        (
            "No embeddings, TF-IDF dependency, vector store, self-learning, "
            "or cross-project memory is used."
        ),
    ]
    if matches:
        notes.append(
            "Similar corpus cases are scenario anchors, not final route decisions."
        )
    else:
        notes.append("No corpus case met the conservative similarity threshold.")
    return notes
