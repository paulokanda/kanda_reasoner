"""Shared constants and path helpers for source-tree archive export."""

from __future__ import annotations

__all__: list[str] = []


from pathlib import Path
from typing import Any

from .exclusion_engine import decide_path_exclusion
from .path_normalization import relative_posix_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ExclusionRules, ProjectContext

SOURCE_ARCHIVE_MANIFEST_SUFFIX = "__source_archive_manifest.json"
GENERATOR_NAME = "reasoner_context_bundle.source_tree_exporter"
GENERATOR_VERSION = "1.4.0"
SCHEMA_VERSION = "1.0"
PLANNING_TARGET_RATIO = 0.90
_BYTES_PER_MB = 1024 * 1024
_ZIP_OVERHEAD_ESTIMATE_BYTES = 2048
_REBALANCE_LAST_PART_MIN_RATIO = 0.50
_REBALANCE_PREVIOUS_PART_MIN_RATIO = 0.50
_PNG_ASSET_EXTENSIONS = {".png"}

_ALWAYS_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".nox",
    ".ruff_cache",
    ".ipynb_checkpoints",
    "build",
    "dist",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    ".project_reference",
    "workbench",
    "runtime_scenarios",
    "logs",
    "log",
    "tmp",
    "temp",
    "backup",
    "backups",
    "_bundle_temp",
    "_temp_archived_installers",
}

_ALWAYS_EXCLUDED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
}

_ALWAYS_EXCLUDED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
    ".cache",
}

_GENERATED_OUTPUT_NAMES = {
    "show_project_to_AI",
    "second_prompt_files",
    "second_prompt_files_building",
    "first_prompt_files",
    "json_splitted",
}

def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)

def build_source_archive_manifest_path(destination: str | Path, context: ProjectContext) -> Path:
    """Return the source-archive manifest path for one destination folder."""
    return Path(destination).expanduser().resolve(strict=False) / (
        context.project_slug + SOURCE_ARCHIVE_MANIFEST_SUFFIX
    )

def _posix_rel(path: Path, context: ProjectContext) -> str:
    return relative_posix_path(path, context.root)

def _exclusion_record(
    path: Path,
    context: ProjectContext,
    *,
    reason_code: str,
    reason: str,
    path_type: str,
    matched_rule: str = "",
) -> dict[str, Any]:
    try:
        rel_path = _posix_rel(path, context)
    except ValueError:
        rel_path = str(path).replace("\\", "/")
    size = 0
    if path.is_file():
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
    return {
        "path": rel_path,
        "path_type": path_type,
        "reason_code": reason_code,
        "reason": reason,
        "matched_rule": matched_rule,
        "size_bytes": size,
    }

def _is_path_same_or_inside(path: Path, parent: Path) -> bool:
    path_resolved = safe_resolve(path)
    parent_resolved = safe_resolve(parent)
    if path_resolved == parent_resolved:
        return True
    try:
        path_resolved.relative_to(parent_resolved)
        return True
    except ValueError:
        return False

def _is_generated_output_path(path: Path, context: ProjectContext, output_dir: Path) -> bool:
    """Return True for active/generated output roots that must not be re-archived."""
    if _is_path_same_or_inside(path, output_dir):
        return True
    try:
        rel = _posix_rel(path, context).strip("/")
    except ValueError:
        return False
    first = rel.split("/", 1)[0]
    return first in _GENERATED_OUTPUT_NAMES

def _is_generated_project_archive(path: Path, context: ProjectContext) -> bool:
    if not path.is_file() or path.suffix.lower() != ".zip":
        return False
    name = path.name.lower()
    slug = context.project_slug.lower()
    return (
        name == slug + ".zip"
        or name.startswith(slug + "__ai_handoff_")
        or name.startswith(slug + "__source_archive_")
        or name.startswith(slug + "__png_assets_")
        or name.startswith("rss_")
    )

def _excluded_by_project_rules(
    entry: Path,
    context: ProjectContext,
    rules: ExclusionRules,
) -> dict[str, Any] | None:
    decision = decide_path_exclusion(entry, context, rules)
    if not decision.excluded:
        return None
    record = decision.as_dict()
    return {
        "path": record.get("path", str(entry).replace("\\", "/")),
        "path_type": "directory" if entry.is_dir() else "file",
        "reason_code": "project_exclusion_rule",
        "reason": str(record.get("reason", "Matched project exclusion rule.")),
        "matched_rule": str(record.get("matched_rule", "")),
        "rule_type": str(record.get("rule_type", "")),
        "size_bytes": entry.stat().st_size if entry.is_file() else 0,
    }

def _is_png_asset_record(record: dict[str, Any]) -> bool:
    return Path(str(record.get("path", ""))).suffix.lower() in _PNG_ASSET_EXTENSIONS

def _split_png_asset_records(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_records: list[dict[str, Any]] = []
    png_records: list[dict[str, Any]] = []
    for record in records:
        if _is_png_asset_record(record):
            png_records.append(record)
        else:
            source_records.append(record)
    return source_records, png_records
