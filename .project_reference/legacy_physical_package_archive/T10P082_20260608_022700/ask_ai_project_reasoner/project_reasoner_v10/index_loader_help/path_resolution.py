"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

__all__ = [
    "resolve_runtime_source_file",
]

from typing import Any


def resolve_runtime_source_file(index: Any, source_file: str) -> str:
    source_file = index._safe_text(source_file)
    if not source_file:
        return ""

    if source_file in index.files_by_path:
        return source_file

    source_file_low = source_file.replace("\\", "/").lower()
    candidates: list[str] = []

    for known_path in index.files_by_path.keys():
        known_low = known_path.replace("\\", "/").lower()
        if known_low == source_file_low:
            return known_path
        if known_low.endswith("/" + source_file_low) or known_low.endswith(source_file_low):
            candidates.append(known_path)

    if len(candidates) == 1:
        return candidates[0]

    for candidate in candidates:
        candidate_low = candidate.replace("\\", "/").lower()
        if "runtime_collector" in candidate_low or "reasoner_runtime_collector" in candidate_low:
            return candidate

    return candidates[0] if candidates else source_file
