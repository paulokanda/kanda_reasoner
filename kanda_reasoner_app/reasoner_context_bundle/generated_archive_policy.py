# project-path: kanda_reasoner_app/reasoner_context_bundle/generated_archive_policy.py
"""Canonical generated-archive policy for Show Project to AI exports."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .path_normalization import safe_resolve
from .schema_models import ProjectContext

__all__ = [
    "GeneratedArchiveClassification",
    "PORTABLE_DISTRIBUTION_CREATION_POLICY",
    "PORTABLE_DISTRIBUTION_NAME_TEMPLATE",
    "SUSPICIOUS_LARGE_ROOT_ARCHIVE_BYTES",
    "classify_generated_project_archive",
    "enforce_large_root_archive_preflight",
    "is_suspicious_large_root_project_archive",
]

SUSPICIOUS_LARGE_ROOT_ARCHIVE_BYTES = 64 * 1024 * 1024
PORTABLE_DISTRIBUTION_NAME_TEMPLATE = "<project>-Windows-Portable.zip"
PORTABLE_DISTRIBUTION_CREATION_POLICY = (
    "Show Project to AI never creates a portable distribution. "
    "A <project>-Windows-Portable.zip is a separate productization/release "
    "artifact created only by an independent workflow after an explicit "
    "user request, outside the selected Project Support root."
)
_RELEASE_TOKENS = (
    "portable",
    "installer",
    "distribution",
    "release",
)


@dataclass(frozen=True)
class GeneratedArchiveClassification:
    """One generated archive exclusion classification."""

    reason_code: str
    matched_rule: str
    reason: str


def _normalized_identity(value: str) -> str:
    """Return a case-insensitive alphanumeric identity string."""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _project_identity_prefixes(context: ProjectContext) -> tuple[str, ...]:
    """Return normalized project identities accepted for release filenames."""
    candidates = (
        context.project_slug,
        context.root.name,
    )
    values: list[str] = []
    for candidate in candidates:
        normalized = _normalized_identity(str(candidate))
        if normalized and normalized not in values:
            values.append(normalized)
    return tuple(values)


def _is_project_root_file(path: Path, context: ProjectContext) -> bool:
    """Return True when path is a direct child of the selected project root."""
    return safe_resolve(path.parent) == safe_resolve(context.root)


def _is_dynamic_windows_portable_name(
    path: Path,
    context: ProjectContext,
) -> bool:
    """Return True for the canonical <project>-Windows-Portable.zip identity.

    Portable distribution identity is filename-owned, not location-owned.  The
    archive remains Portable Box output even when it is misplaced in a nested
    project folder, so Show Project must exclude it everywhere under source.
    """
    if path.suffix.lower() != ".zip":
        return False
    normalized_stem = _normalized_identity(path.stem)
    return any(
        normalized_stem == identity + "windowsportable"
        for identity in _project_identity_prefixes(context)
    )


def _project_prefixed_release_name(path: Path, context: ProjectContext) -> bool:
    """Return True for project-prefixed portable or release archive names."""
    if not _is_project_root_file(path, context):
        return False
    normalized_stem = _normalized_identity(path.stem)
    for identity in _project_identity_prefixes(context):
        if not normalized_stem.startswith(identity):
            continue
        suffix = normalized_stem[len(identity) :]
        if any(token in suffix for token in _RELEASE_TOKENS):
            return True
    return False


def classify_generated_project_archive(
    path: Path,
    context: ProjectContext,
) -> GeneratedArchiveClassification | None:
    """Classify generated ZIPs that must not enter AI source packages."""
    if not path.is_file() or path.suffix.lower() != ".zip":
        return None

    name = path.name.lower()
    slug = context.project_slug.lower()
    if name == slug + ".zip":
        return GeneratedArchiveClassification(
            reason_code="generated_full_project_archive",
            matched_rule="project_slug_zip",
            reason=(
                "Generated full-project archive excluded to prevent recursive "
                "Show Project to AI packaging."
            ),
        )
    if name.startswith(slug + "__ai_handoff_"):
        return GeneratedArchiveClassification(
            reason_code="generated_ai_handoff_archive",
            matched_rule="ai_handoff_archive",
            reason="Generated AI handoff archive excluded from active project source.",
        )
    if name.startswith(slug + "__source_archive_"):
        return GeneratedArchiveClassification(
            reason_code="generated_source_archive_part",
            matched_rule="source_archive_part",
            reason="Generated source-archive part excluded from active project source.",
        )
    if name.startswith(slug + "__png_assets_"):
        return GeneratedArchiveClassification(
            reason_code="generated_png_asset_archive_part",
            matched_rule="png_assets_part",
            reason="Generated PNG-asset archive part excluded from active project source.",
        )
    if name.startswith("rss_"):
        return GeneratedArchiveClassification(
            reason_code="generated_rss_archive",
            matched_rule="rss_archive",
            reason="Generated RSS archive excluded from active project source.",
        )
    if _is_dynamic_windows_portable_name(path, context):
        return GeneratedArchiveClassification(
            reason_code="generated_portable_distribution",
            matched_rule="dynamic_windows_portable_archive",
            reason=(
                "Portable Box distribution excluded from Show Project to AI "
                "source packaging regardless of its location under project source."
            ),
        )
    if _project_prefixed_release_name(path, context):
        return GeneratedArchiveClassification(
            reason_code="generated_portable_distribution",
            matched_rule="project_prefixed_release_archive",
            reason=(
                "Existing generated portable, installer, distribution, or release "
                "archive excluded from Show Project to AI source packaging. "
                + PORTABLE_DISTRIBUTION_CREATION_POLICY
            ),
        )
    return None


def is_suspicious_large_root_project_archive(
    path: Path,
    context: ProjectContext,
) -> bool:
    """Return True for unclassified large project-prefixed root ZIP files."""
    if not path.is_file() or path.suffix.lower() != ".zip":
        return False
    if not _is_project_root_file(path, context):
        return False
    if classify_generated_project_archive(path, context) is not None:
        return False
    try:
        if path.stat().st_size < SUSPICIOUS_LARGE_ROOT_ARCHIVE_BYTES:
            return False
    except OSError:
        return False
    normalized_stem = _normalized_identity(path.stem)
    return any(
        normalized_stem.startswith(identity)
        for identity in _project_identity_prefixes(context)
    )

def enforce_large_root_archive_preflight(
    path: Path,
    context: ProjectContext,
) -> None:
    """Fail before hashing or compression of an unknown large root ZIP."""
    if not is_suspicious_large_root_project_archive(path, context):
        return
    raise ValueError(
        "Suspicious large project-prefixed ZIP at project root: "
        + str(path)
        + ". Show Project to AI must not create this archive. Move an existing "
        + "generated release outside the project root or add an explicit Project "
        + "Exclusion Rule. Portable builds belong to a separate workflow invoked "
        + "only after an explicit user request."
    )

