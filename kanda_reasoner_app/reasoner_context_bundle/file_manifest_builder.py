# project-path: kanda_reasoner_app/reasoner_context_bundle/file_manifest_builder.py
"""Build the active-file manifest for one reasoner context bundle."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from .exclusion_engine import decide_path_exclusion
from .exclusion_provider import load_bundle_exclusion_rules
from .file_manifest_records_private import safe_file_record as _safe_file_record
from .hashing import sha256_file
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .path_normalization import relative_posix_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ExclusionDecision, ExclusionRules, ProjectContext

__all__ = [
    "TEXT_FILE_EXTENSIONS",
    "build_file_manifest_payload",
    "iter_active_project_files",
    "is_ignored_project_archive",
    "GENERATED_EVIDENCE_PREFIXES",
    "write_file_manifest_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "file_manifest"
GENERATOR_NAME = "reasoner_context_bundle.file_manifest_builder"
GENERATOR_VERSION = "1.0.4"

GENERATED_EVIDENCE_PREFIXES = (
    "show_project_to_AI/",
    "show_project_to_AI/second_prompt_files/",
    "show_project_to_AI/json_splitted/",
)

TEXT_FILE_EXTENSIONS = (
    ".bat",
    ".cmd",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".qss",
    ".toml",
    ".txt",
    ".ui",
    ".xml",
    ".yaml",
    ".yml",
)



def is_ignored_project_archive(path: Path, context: ProjectContext) -> bool:
    """Return True for stray full-project/handoff ZIP archives to omit from AI handoff.

    The Show Project to AI handoff must not recursively package an uploaded or
    copied full-project archive such as ``<project_slug>.zip``. Such archives can
    make the reconstruction payload huge and cause downstream ZIP parts to exceed
    the selected size. This is deliberately narrow: ordinary project ZIP assets
    are preserved unless their name is the selected project slug or a generated
    AI handoff package name.
    """
    if not path.is_file() or path.suffix.lower() != ".zip":
        return False
    name = path.name.lower()
    slug = context.project_slug.lower()
    return (
        name == slug + ".zip"
        or (name.startswith(slug + "__ai_handoff_") and name.endswith(".zip"))
    )




def is_ignored_legacy_delivery_noise(path: Path) -> bool:
    """Return True for archived/temp prompt artifacts that must not be delivered."""
    parts = {part.lower() for part in path.parts}
    return "_bundle_temp" in parts or "_temp_archived_installers" in parts


def _ignored_legacy_delivery_noise_decision(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Support ignored legacy delivery noise decision behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    relative = relative_posix_path(path, context.root)
    return {
        "path": relative,
        "included": False,
        "excluded": True,
        "matched_rule": "legacy_delivery_noise_guard",
        "rule_type": "folder",
        "reason": "Legacy/temp prompt-delivery artifacts are excluded from Show Project to AI handoff files.",
    }

def _ignored_project_archive_decision(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Support ignored project archive decision behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    relative = relative_posix_path(path, context.root)
    return {
        "path": relative,
        "included": False,
        "excluded": True,
        "matched_rule": "show_project_to_ai_recursive_archive_guard",
        "rule_type": "file",
        "reason": "Stray full-project or generated handoff ZIP archives are ignored while building Show Project to AI ZIP handoff files.",
    }


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    """Support context behavior.
    
    Parameters
    ----------
    project : str | Path | ProjectContext
        The project value.
    
    Returns
    -------
    ProjectContext
        The project context result.
    """
    
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)




def _is_generated_evidence_path(path: Path, context: ProjectContext) -> bool:
    """Support is generated evidence path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    relative = relative_posix_path(path, context.root).replace("\\", "/").lower().lstrip("/")
    return any(relative.startswith(prefix) for prefix in GENERATED_EVIDENCE_PREFIXES)


def _generated_artifact_decision(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Support generated artifact decision behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    relative = relative_posix_path(path, context.root)
    return {
        "path": relative,
        "included": False,
        "excluded": True,
        "matched_rule": "generated_evidence_artifact",
        "rule_type": "generated_artifact",
        "reason": "Generated project evidence is listed as bundle metadata, not active source.",
    }


def _iter_project_entries(root: Path) -> Iterator[Path]:
    """Support iter project entries behavior.
    
    Parameters
    ----------
    root : Path
        The root path.
    
    Returns
    -------
    Iterator[Path]
        The iterator result.
    """
    
    try:
        entries = sorted(root.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
    except OSError:
        return
    for entry in entries:
        yield entry


def iter_active_project_files(
    project: str | Path | ProjectContext,
    rules: ExclusionRules | None = None,
) -> Iterator[Path]:
    """Yield active files for one project using that project's own rules."""
    context = _context(project)
    active_rules = rules if rules is not None else load_bundle_exclusion_rules(context)
    root = safe_resolve(context.root)

    def walk(current: Path) -> Iterator[Path]:
        for entry in _iter_project_entries(current):
            if entry.is_symlink():
                continue
            if _is_generated_evidence_path(entry, context):
                continue
            if is_ignored_project_archive(entry, context):
                continue
            if is_ignored_legacy_delivery_noise(entry):
                continue
            decision = decide_path_exclusion(entry, context, active_rules)
            if decision.excluded:
                continue
            if entry.is_dir():
                yield from walk(entry)
            elif entry.is_file():
                yield entry

    yield from walk(root)


def _iter_manifest_rows(
    context: ProjectContext,
    rules: ExclusionRules,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Support iter manifest rows behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    rules : ExclusionRules
        The rules value.
    
    Returns
    -------
    tuple[list[dict[str, Any]], list[dict[str, Any]]]
        The tuple of values.
    """
    
    files: list[dict[str, Any]] = []
    excluded_samples: list[dict[str, Any]] = []
    generated_artifact_samples: list[dict[str, Any]] = []
    root = safe_resolve(context.root)

    def walk(current: Path) -> None:
        for entry in _iter_project_entries(current):
            if entry.is_symlink():
                continue
            if _is_generated_evidence_path(entry, context):
                if len(generated_artifact_samples) < 50:
                    generated_artifact_samples.append(_generated_artifact_decision(entry, context))
                continue
            if is_ignored_project_archive(entry, context):
                if len(excluded_samples) < 50:
                    excluded_samples.append(_ignored_project_archive_decision(entry, context))
                continue
            if is_ignored_legacy_delivery_noise(entry):
                if len(excluded_samples) < 50:
                    excluded_samples.append(_ignored_legacy_delivery_noise_decision(entry, context))
                continue
            decision = decide_path_exclusion(entry, context, rules)
            if decision.excluded:
                if len(excluded_samples) < 50:
                    excluded_samples.append(decision.as_dict())
                continue
            if entry.is_dir():
                walk(entry)
            elif entry.is_file():
                record = _safe_file_record(entry, context)
                record["exclusion"] = decision.as_dict()
                files.append(record)

    walk(root)
    return files, excluded_samples, generated_artifact_samples


def _counts(
    files: list[dict[str, Any]],
    excluded_samples: list[dict[str, Any]],
    generated_artifact_samples: list[dict[str, Any]],
) -> dict[str, int]:
    """Support counts behavior.
    
    Parameters
    ----------
    files : list[dict[str, Any]]
        The files value.
    excluded_samples : list[dict[str, Any]]
        The excluded samples value.
    generated_artifact_samples : list[dict[str, Any]]
        The generated artifact samples value.
    
    Returns
    -------
    dict[str, int]
        The mapped values.
    """
    
    return {
        "active_files": len(files),
        "text_files": sum(1 for item in files if item.get("kind") == "text"),
        "binary_files": sum(1 for item in files if item.get("kind") == "binary"),
        "unreadable_files": sum(1 for item in files if item.get("kind") == "unreadable"),
        "included_in_active_snapshot": sum(
            1 for item in files if item.get("included_in_active_snapshot") is True
        ),
        "excluded_path_samples": len(excluded_samples),
        "generated_artifact_path_samples": len(generated_artifact_samples),
    }


def build_file_manifest_payload(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Build the file manifest payload for one active project."""
    context = _context(project)
    rules = load_bundle_exclusion_rules(context)
    files, excluded_samples, generated_artifact_samples = _iter_manifest_rows(context, rules)
    files.sort(key=lambda item: str(item.get("path", "")).lower())
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "project": {
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
        },
        "source": {
            "exclusion_rules": rules.as_dict(),
            "contract": "project_specific_dynamic_rules",
        },
        "counts": _counts(files, excluded_samples, generated_artifact_samples),
        "files": files,
        "excluded_path_samples": excluded_samples,
        "generated_artifact_path_samples": generated_artifact_samples,
    }


def write_file_manifest_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__file_manifest.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_file_manifest_payload(context)
    return write_json_atomic(paths.file_manifest_json, payload)
