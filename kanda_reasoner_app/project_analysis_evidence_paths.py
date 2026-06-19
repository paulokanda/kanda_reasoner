"""Path helpers for generated project-analysis evidence artifacts.

Generated evidence now resolves outside the selected project source tree.
The active output root is the external architecture-audit folder for the
selected/analyzed project. The historical in-source folder name
``project_analysis_evidence`` is retained as a legacy label for compatibility,
relative display helpers, and migration tools only.
"""

from __future__ import annotations

import re
from pathlib import Path

from kanda_reasoner_app.storage_policy.architecture_audit_resolver import (
    get_architecture_audit_current_root,
    get_architecture_audit_subfolder,
)

__all__ = [
    "PROJECT_REFERENCE_DIR",
    "PROJECT_ANALYSIS_EVIDENCE_DIR",
    "JSON_COMPLETE_DIR",
    "JSON_PARTS_DIR",
    "project_name_from_root",
    "project_analysis_evidence_root",
    "analysis_json_complete_dir",
    "analysis_json_parts_dir",
    "ensure_project_analysis_evidence_dirs",
    "primary_evidence_json_path",
    "secondary_evidence_json_path",
    "parts_manifest_file_path",
    "parts_index_file_path",
    "route_manifest_file_path",
    "working_copy_json_path",
    "working_copy_metadata_path",
    "relative_evidence_path",
    "relative_primary_evidence_json_path",
    "relative_secondary_evidence_json_path",
    "relative_parts_manifest_file_path",
    "relative_parts_index_file_path",
    "relative_route_manifest_file_path",
    "relative_working_copy_json_path",
    "relative_working_copy_metadata_path",
    "normalize_evidence_artifact_path",
]

PROJECT_REFERENCE_DIR = "project_freeze_ledger"
PROJECT_ANALYSIS_EVIDENCE_DIR = "project_analysis_evidence"
JSON_COMPLETE_DIR = "json_complete"
JSON_PARTS_DIR = "json_splitted"

_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def project_name_from_root(project_root: str | Path) -> str:
    """Return a stable project name derived from a selected project root."""
    raw = str(project_root).replace("\\", "/").rstrip("/")
    name = raw.rsplit("/", 1)[-1].strip() or "project"
    cleaned = _SAFE_NAME_RE.sub("_", name).strip("._-")
    return cleaned or "project"


def project_analysis_evidence_root(project_root: str | Path) -> Path:
    """Return the active external evidence root for generated artifacts."""
    return get_architecture_audit_current_root(project_root)


def _normalize_project_analysis_evidence_dir_casing(project_root: str | Path) -> None:
    """Retained compatibility no-op for legacy callers.

    The active evidence root is external to the project source tree, so this
    helper must not rename or create in-source folders anymore.
    """
    return None


def _paths_refer_to_same_location(first: Path, second: Path) -> bool:
    """Return True when two paths resolve to the same filesystem entry."""
    try:
        return first.samefile(second)
    except OSError:
        return False


def analysis_json_complete_dir(project_root: str | Path) -> Path:
    """Return the external folder for complete generated JSON artifacts."""
    return get_architecture_audit_subfolder(project_root, JSON_COMPLETE_DIR)


def analysis_json_parts_dir(project_root: str | Path) -> Path:
    """Return the external folder for generated split JSON artifacts."""
    return project_analysis_evidence_root(project_root) / JSON_PARTS_DIR


def ensure_project_analysis_evidence_dirs(project_root: str | Path) -> Path:
    """Create and return the external evidence root and child folders."""
    evidence_root = project_analysis_evidence_root(project_root)
    analysis_json_complete_dir(project_root).mkdir(parents=True, exist_ok=True)
    analysis_json_parts_dir(project_root).mkdir(parents=True, exist_ok=True)
    return evidence_root


def _project_name(project_root: str | Path) -> str:
    """Return the sanitized project name used in generated filenames."""
    return project_name_from_root(project_root)


def primary_evidence_json_path(project_root: str | Path) -> Path:
    """Return the primary complete generated JSON path."""
    return analysis_json_complete_dir(project_root) / f"{_project_name(project_root)}__complete.json"


def secondary_evidence_json_path(project_root: str | Path) -> Path:
    """Return the runtime-trace JSON path paired with the primary file."""
    name = f"{_project_name(project_root)}__complete_runtime_trace.json"
    return analysis_json_complete_dir(project_root) / name


def working_copy_json_path(project_root: str | Path) -> Path:
    """Return the local-AI working-copy JSON path."""
    name = f"{_project_name(project_root)}__complete_local_AI.json"
    return analysis_json_complete_dir(project_root) / name


def working_copy_metadata_path(project_root: str | Path) -> Path:
    """Return the local-AI working-copy metadata path."""
    name = f"{_project_name(project_root)}__complete_local_AI.meta.json"
    return analysis_json_complete_dir(project_root) / name


def parts_manifest_file_path(project_root: str | Path) -> Path:
    """Return the normalized generated split manifest path."""
    name = f"{_project_name(project_root)}_split_manifest.json"
    return analysis_json_parts_dir(project_root) / name


def parts_index_file_path(project_root: str | Path) -> Path:
    """Return the normalized generated split index path."""
    return analysis_json_parts_dir(project_root) / f"{_project_name(project_root)}_split_index.json"


def route_manifest_file_path(project_root: str | Path) -> Path:
    """Return the deterministic route manifest path for split artifacts."""
    name = f"{_project_name(project_root)}__complete__web_ai_route_manifest.json"
    return analysis_json_parts_dir(project_root) / name


def normalize_evidence_artifact_path(project_root: str | Path, raw_path: str | Path) -> Path:
    """Return a Path for raw_path or the canonical primary JSON path."""
    raw_text = str(raw_path).strip()
    if raw_text:
        return Path(raw_path)
    return primary_evidence_json_path(project_root)


def relative_evidence_path(*parts: str) -> str:
    """Return a legacy POSIX relative path for display compatibility."""
    return str(
        Path(PROJECT_ANALYSIS_EVIDENCE_DIR) / Path(*parts)
    ).replace("\\", "/")


def relative_primary_evidence_json_path(project_name: str = "project") -> str:
    """Return the primary generated JSON relative path for a project name."""
    return relative_evidence_path(JSON_COMPLETE_DIR, f"{project_name}__complete.json")


def relative_secondary_evidence_json_path(project_name: str = "project") -> str:
    """Return the runtime-trace JSON relative path for a project name."""
    return relative_evidence_path(
        JSON_COMPLETE_DIR,
        f"{project_name}__complete_runtime_trace.json",
    )


def relative_working_copy_json_path(project_name: str = "project") -> str:
    """Return the generated working-copy JSON relative path."""
    return relative_evidence_path(
        JSON_COMPLETE_DIR,
        f"{project_name}__complete_local_AI.json",
    )


def relative_working_copy_metadata_path(project_name: str = "project") -> str:
    """Return the generated working-copy metadata relative path."""
    return relative_evidence_path(
        JSON_COMPLETE_DIR,
        f"{project_name}__complete_local_AI.meta.json",
    )


def relative_parts_manifest_file_path(project_name: str = "project") -> str:
    """Return the split manifest relative path for a project name."""
    return relative_evidence_path(JSON_PARTS_DIR, f"{project_name}_split_manifest.json")


def relative_parts_index_file_path(project_name: str = "project") -> str:
    """Return the split index relative path for a project name."""
    return relative_evidence_path(JSON_PARTS_DIR, f"{project_name}_split_index.json")


def relative_route_manifest_file_path(project_name: str = "project") -> str:
    """Return the route manifest relative path for a project name."""
    return relative_evidence_path(
        JSON_PARTS_DIR,
        f"{project_name}__complete__web_ai_route_manifest.json",
    )
