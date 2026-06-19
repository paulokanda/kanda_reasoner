"""Path normalization helpers for the reasoner context bundle box."""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "artifact_logical_posix_path",
    "relative_posix_path",
    "resolve_logical_artifact_path",
    "safe_resolve",
    "to_posix_path",
]


def safe_resolve(path: str | Path) -> Path:
    """Resolve a path without failing on paths that do not yet exist."""
    return Path(path).expanduser().resolve(strict=False)


def to_posix_path(path: str | Path) -> str:
    """Return a stable POSIX-style string for JSON output."""
    return str(path).replace("\\", "/")


def relative_posix_path(path: str | Path, root: str | Path) -> str:
    """Return path relative to root using POSIX separators.

    Raises ValueError when path is outside root. This protects snapshot and
    bundle logic from writing or reporting paths outside the active project.
    """
    resolved_path = safe_resolve(path)
    resolved_root = safe_resolve(root)
    try:
        relative = resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("Path is outside the project root: " + str(path)) from exc
    return relative.as_posix()


def artifact_logical_posix_path(path: str | Path, context) -> str:
    """Return a logical artifact path for project or external audit files.

    Source files are still reported relative to the selected project root. The
    generated architecture-audit artifacts are intentionally outside that source
    tree, under the external audit root for the selected project. Those files are
    reported with the stable logical prefix ``project_analysis_evidence`` so the
    bundle manifest and ZIP layout remain portable without leaking absolute
    machine paths.
    """
    resolved_path = safe_resolve(path)
    project_root = safe_resolve(context.root)
    evidence_root = safe_resolve(context.evidence_root)

    try:
        return resolved_path.relative_to(project_root).as_posix()
    except ValueError:
        pass

    try:
        relative_to_evidence = resolved_path.relative_to(evidence_root)
    except ValueError as exc:
        raise ValueError(
            "Path is outside the project root and architecture audit root: "
            + str(path)
        ) from exc

    return (Path("project_analysis_evidence") / relative_to_evidence).as_posix()


def resolve_logical_artifact_path(context, logical_path: str | Path) -> Path:
    """Resolve a portable artifact path to its actual filesystem path.

    ``project_analysis_evidence/...`` is a logical compatibility prefix for the
    external architecture-audit current folder. Other relative paths are resolved
    against the selected project root and must stay inside it.
    """
    text = str(logical_path).strip().replace("\\", "/")
    if not text:
        raise ValueError("Artifact path is empty")
    if text.startswith("../") or text == ".." or Path(text).is_absolute():
        raise ValueError("Artifact path escapes allowed roots: " + text)

    legacy_prefix = "project_analysis_evidence/"
    if text == "project_analysis_evidence":
        return safe_resolve(context.evidence_root)
    if text.startswith(legacy_prefix):
        artifact = safe_resolve(context.evidence_root / text[len(legacy_prefix):])
        evidence_root = safe_resolve(context.evidence_root)
        try:
            artifact.relative_to(evidence_root)
        except ValueError as exc:
            raise ValueError("Artifact path escapes architecture audit root: " + text) from exc
        return artifact

    artifact = safe_resolve(context.root / text)
    project_root = safe_resolve(context.root)
    try:
        artifact.relative_to(project_root)
    except ValueError as exc:
        raise ValueError("Artifact path escapes project root: " + text) from exc
    return artifact

