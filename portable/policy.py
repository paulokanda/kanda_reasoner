"""Path-aware content policy for Portable release staging."""

from __future__ import annotations

from pathlib import PurePosixPath

from kanda_reasoner_app.source_hygiene.tool_archive_policy import (
    is_project_capture_forbidden_relative,
)

from portable.constants import (
    FORBIDDEN_GENERATED_FILE_MARKERS,
    FORBIDDEN_GENERATED_FOLDER_NAMES,
    FORBIDDEN_GENERATED_PATH_SEQUENCES,
    NON_RUNTIME_BACKUP_MARKERS,
    NON_RUNTIME_BACKUP_SUFFIXES,
    NON_RUNTIME_CACHE_FOLDER_NAMES,
    NON_RUNTIME_DEBRIS_FILE_NAMES,
    PORTABLE_ARCHIVE_SUFFIX,
    RUNTIME_PACKAGE_PATH_SEQUENCES,
)


def _normalized_parts(relative_path: str) -> tuple[str, ...]:
    normalized = relative_path.replace("\\", "/").strip("/")
    if not normalized:
        return ()
    return tuple(
        part.casefold()
        for part in PurePosixPath(normalized).parts
        if part not in {"", "."}
    )


def _contains_sequence(
    parts: tuple[str, ...],
    sequence: tuple[str, ...],
) -> bool:
    if not sequence or len(sequence) > len(parts):
        return False

    width = len(sequence)
    return any(
        parts[index : index + width] == sequence
        for index in range(len(parts) - width + 1)
    )


def is_runtime_package_path(relative_path: str) -> bool:
    """Return whether a path belongs to a protected runtime source package."""

    parts = _normalized_parts(relative_path)
    return any(
        _contains_sequence(parts, sequence)
        for sequence in RUNTIME_PACKAGE_PATH_SEQUENCES
    )


def is_generated_handoff_or_release_path(relative_path: str) -> bool:
    """Return whether a path is an actual generated handoff/release artifact."""

    parts = _normalized_parts(relative_path)
    if not parts:
        return False

    if any(
        part in FORBIDDEN_GENERATED_FOLDER_NAMES
        for part in parts
    ):
        return True

    if any(
        _contains_sequence(parts, sequence)
        for sequence in FORBIDDEN_GENERATED_PATH_SEQUENCES
    ):
        return True

    basename = parts[-1]
    if basename.endswith(PORTABLE_ARCHIVE_SUFFIX):
        return True

    return any(
        marker in basename
        for marker in FORBIDDEN_GENERATED_FILE_MARKERS
    )


def is_non_runtime_debris_path(relative_path: str) -> bool:
    """Return whether a path is cache, editor debris, or a source backup."""

    parts = _normalized_parts(relative_path)
    if not parts:
        return False

    if any(
        part in NON_RUNTIME_CACHE_FOLDER_NAMES
        for part in parts
    ):
        return True

    basename = parts[-1]
    if basename in NON_RUNTIME_DEBRIS_FILE_NAMES:
        return True
    if any(
        marker in basename
        for marker in NON_RUNTIME_BACKUP_MARKERS
    ):
        return True
    return basename.endswith(NON_RUNTIME_BACKUP_SUFFIXES)


def is_forbidden_tool_capture_path(relative_path: str) -> bool:
    """Return whether a staged or archived path contains Tool-owned capture output."""
    return is_project_capture_forbidden_relative(relative_path)
