"""Path helpers for generated project-analysis evidence artifacts.

Generated evidence resolves outside the selected project source tree.
The active output root is the external ``show project to AI`` folder for the
selected/analyzed project. Complete Project Structure Map files are generated
inside its ``second_prompt_files`` child folder:
``<project_drive>:/<project_name>_show_project_to_AI/second_prompt_files``.
During a Run Collector rebuild, child processes may temporarily write to
``second_prompt_files_building`` via a guarded environment override before the
finished files are published to ``second_prompt_files``.

The historical names ``project_analysis_evidence`` and ``json_complete`` are
retained in helper/function names for compatibility with existing callers, but
complete Project Structure Map artifacts now resolve to the dynamic
``*_show_project_to_AI/second_prompt_files`` folder rather than to an
architecture-audit ``current/json_complete`` subfolder.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from kanda_reasoner_app.storage_policy.path_resolver import (
    make_safe_slug,
    normalize_path,
)

__all__ = [
    "PROJECT_REFERENCE_DIR",
    "PROJECT_ANALYSIS_EVIDENCE_DIR",
    "JSON_COMPLETE_DIR",
    "SECOND_PROMPT_FILES_DIR",
    "SECOND_PROMPT_FILES_BUILDING_DIR",
    "FIRST_PROMPT_FILES_DIR",
    "PROJECT_ERROR_MEMORY_DIR",
    "SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV",
    "SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV",
    "SHOW_PROJECT_TO_AI_SUFFIX",
    "DELETE_AFTER_DAILY_WORK_SUFFIX",
    "JSON_PARTS_DIR",
    "project_name_from_root",
    "show_project_to_ai_root_from_hint",
    "project_analysis_evidence_root",
    "analysis_json_complete_dir",
    "analysis_json_building_dir",
    "analysis_first_prompt_files_dir",
    "analysis_project_error_memory_dir",
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
PROJECT_ANALYSIS_EVIDENCE_DIR = "show_project_to_AI"
SHOW_PROJECT_TO_AI_SUFFIX = "_show_project_to_AI"
DELETE_AFTER_DAILY_WORK_SUFFIX = "_delete_after_daily_work"
SECOND_PROMPT_FILES_DIR = "second_prompt_files"
SECOND_PROMPT_FILES_BUILDING_DIR = "second_prompt_files_building"
FIRST_PROMPT_FILES_DIR = "first_prompt_files"
PROJECT_ERROR_MEMORY_DIR = "project_error_memory"
SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV = "KANDA_SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR"
SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV = "KANDA_SHOW_PROJECT_TO_AI_PROJECT_ROOT"
JSON_COMPLETE_DIR = SECOND_PROMPT_FILES_DIR
JSON_PARTS_DIR = "json_splitted"

_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def project_name_from_root(project_root: str | Path) -> str:
    """Return a stable project name derived from a selected project root."""
    raw = str(project_root).replace("\\", "/").rstrip("/")
    name = raw.rsplit("/", 1)[-1].strip() or "project"
    cleaned = _SAFE_NAME_RE.sub("_", name).strip("._-")
    return cleaned or "project"


def _folder_name_for_slug(root: Path, slug: str) -> Path:
    """Return the external show-project folder for a safe project slug."""
    folder_name = f"{slug}{SHOW_PROJECT_TO_AI_SUFFIX}"

    if root.drive:
        return Path(root.anchor) / folder_name

    return root.parent / folder_name


def _base_slug_from_suffixed_name(name: str, suffix: str) -> str:
    """Return a safe base slug after removing a known generated-folder suffix."""
    if name.endswith(suffix):
        return make_safe_slug(name[: -len(suffix)])
    return make_safe_slug(name)


def show_project_to_ai_root_from_hint(project_root: str | Path) -> Path:
    """Return the canonical show-project root for a project or output hint.

    Accepted hints include the real project root, the already generated
    ``*_show_project_to_AI`` root, its direct children, Error Memory child
    folders, and the daily-work maintenance folder.  This prevents accidental
    sibling folders such as ``project_error_memory_show_project_to_AI`` or
    ``<partial_typo>_show_project_to_AI`` from being derived from output paths.
    """
    root = normalize_path(project_root)

    error_memory_children = {
        "pending_ai_assisted_error_lesson_intake",
        "lessons",
        "exports",
        "schemas",
    }
    if root.name in error_memory_children:
        parent = root.parent
        if parent.name == PROJECT_ERROR_MEMORY_DIR and parent.parent.name.endswith(SHOW_PROJECT_TO_AI_SUFFIX):
            return parent.parent

    if root.name == PROJECT_ERROR_MEMORY_DIR and root.parent.name.endswith(SHOW_PROJECT_TO_AI_SUFFIX):
        return root.parent

    show_children = {
        FIRST_PROMPT_FILES_DIR,
        SECOND_PROMPT_FILES_DIR,
        SECOND_PROMPT_FILES_BUILDING_DIR,
        PROJECT_ERROR_MEMORY_DIR,
        JSON_PARTS_DIR,
    }
    if root.name in show_children and root.parent.name.endswith(SHOW_PROJECT_TO_AI_SUFFIX):
        return root.parent

    if root.name.endswith(SHOW_PROJECT_TO_AI_SUFFIX):
        return root

    if root.name.endswith(DELETE_AFTER_DAILY_WORK_SUFFIX):
        slug = _base_slug_from_suffixed_name(root.name, DELETE_AFTER_DAILY_WORK_SUFFIX)
        return _folder_name_for_slug(root, slug)

    return _folder_name_for_slug(root, make_safe_slug(root.name))


def _show_project_to_ai_root(project_root: str | Path) -> Path:
    """Return <drive>/<project>_show_project_to_AI without creating it."""
    return show_project_to_ai_root_from_hint(project_root)


def project_analysis_evidence_root(project_root: str | Path) -> Path:
    """Return the active external show-project-to-AI root."""
    return _show_project_to_ai_root(project_root)


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


def analysis_json_building_dir(project_root: str | Path) -> Path:
    """Return the guarded temporary Run Collector build folder.

    The GUI writes new second-prompt artifacts here first so the previously
    published ``second_prompt_files`` delivery remains visible while long JSON
    collection and bundle generation are running. Only after successful JSON
    generation are the files published into ``second_prompt_files``.
    """
    return project_analysis_evidence_root(project_root) / SECOND_PROMPT_FILES_BUILDING_DIR


def _show_project_to_ai_override_project_root(project_root: str | Path) -> Path:
    """Return the selected project root that owns an active output override.

    Some collector child processes can be imported from the tool package while
    operating on a user-selected project.  The output-folder override must be
    validated against that selected project, not against a stale/default package
    root that may still exist in inherited process state.
    """
    raw = os.environ.get(SHOW_PROJECT_TO_AI_PROJECT_ROOT_ENV, "").strip()
    if raw:
        return Path(raw).expanduser().resolve(strict=False)
    return Path(project_root).expanduser().resolve(strict=False)


def _active_artifact_project_root(project_root: str | Path) -> Path:
    """Return the project root used for generated evidence filenames."""
    if os.environ.get(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV, "").strip():
        return _show_project_to_ai_override_project_root(project_root)
    return Path(project_root).expanduser().resolve(strict=False)


def _analysis_json_complete_dir_override(project_root: str | Path) -> Path | None:
    """Return a guarded child-process output override, when explicitly set."""
    raw = os.environ.get(SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV, "").strip()
    if not raw:
        return None
    override = Path(raw).expanduser().resolve(strict=False)
    selected_project_root = _show_project_to_ai_override_project_root(project_root)
    evidence_root = project_analysis_evidence_root(selected_project_root).expanduser().resolve(strict=False)
    try:
        override.relative_to(evidence_root)
    except ValueError as exc:
        raise ValueError(
            SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV
            + " must stay under the selected project's show_project_to_AI folder: "
            + str(evidence_root)
            + "; received: "
            + str(override)
        ) from exc
    if override.name not in {SECOND_PROMPT_FILES_DIR, SECOND_PROMPT_FILES_BUILDING_DIR}:
        raise ValueError(
            SHOW_PROJECT_TO_AI_JSON_COMPLETE_DIR_ENV
            + " must target second_prompt_files or second_prompt_files_building: "
            + str(override)
        )
    return override


def analysis_json_complete_dir(project_root: str | Path) -> Path:
    """Return the external second_prompt_files folder for AI-delivery artifacts.

    Compatibility note: the function name is retained because many callers
    already ask for the complete JSON artifact directory, but the normal
    returned folder is the Run Collector delivery child folder:
    ``<project_drive>:/<project_name>_show_project_to_AI/second_prompt_files``.

    A child-process-only guarded environment override may point generation to
    ``second_prompt_files_building`` during a rebuild. The GUI later publishes
    those files back to ``second_prompt_files`` before ZIP export.
    """
    override = _analysis_json_complete_dir_override(project_root)
    if override is not None:
        return override
    return project_analysis_evidence_root(project_root) / SECOND_PROMPT_FILES_DIR



def analysis_project_error_memory_dir(project_root: str | Path) -> Path:
    """Return the external canonical Error Memory folder for the selected project.

    The folder is a sibling of first_prompt_files and second_prompt_files under
    the dynamic ``*_show_project_to_AI`` root:
    ``<project_drive>:/<project_name>_show_project_to_AI/project_error_memory``.
    It is persistent project-specific memory, not disposable upload output.
    """
    return project_analysis_evidence_root(project_root) / PROJECT_ERROR_MEMORY_DIR

def analysis_first_prompt_files_dir(project_root: str | Path) -> Path:
    """Return the external first_prompt_files folder for startup delivery artifacts.

    Compatibility helper for Freeze Feature After Update and first-prompt
    delivery callers. The folder is a sibling of second_prompt_files under the
    selected project's dynamic show_project_to_AI root:
    ``<project_drive>:/<project_name>_show_project_to_AI/first_prompt_files``.
    """
    return project_analysis_evidence_root(project_root) / FIRST_PROMPT_FILES_DIR


def analysis_json_parts_dir(project_root: str | Path) -> Path:
    """Return the legacy external folder for generated split JSON artifacts."""
    return project_analysis_evidence_root(project_root) / JSON_PARTS_DIR


def ensure_project_analysis_evidence_dirs(project_root: str | Path) -> Path:
    """Create and return the external evidence root and child folders."""
    evidence_root = project_analysis_evidence_root(project_root)
    analysis_first_prompt_files_dir(project_root).mkdir(parents=True, exist_ok=True)
    analysis_project_error_memory_dir(project_root).mkdir(parents=True, exist_ok=True)
    analysis_json_complete_dir(project_root).mkdir(parents=True, exist_ok=True)
    # Normal Show Project to AI root must only contain first_prompt_files and
    # second_prompt_files after a successful run. The temporary building folder
    # is created only by the runner while work is active, and legacy
    # json_splitted is not created by normal directory preparation.
    return evidence_root


def _project_name(project_root: str | Path) -> str:
    """Return the sanitized project name used in generated filenames."""
    return project_name_from_root(_active_artifact_project_root(project_root))


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
    """Return a portable POSIX relative path for generated evidence.

    ``analysis_json_complete_dir`` now points at
    ``*_show_project_to_AI/second_prompt_files``. Avoid duplicating the logical
    folder name when callers pass retained compatibility constants.
    """
    cleaned = [str(part).strip("/\\") for part in parts if str(part).strip("/\\")]
    if cleaned and cleaned[0] == PROJECT_ANALYSIS_EVIDENCE_DIR:
        cleaned = cleaned[1:]
    return str(
        Path(PROJECT_ANALYSIS_EVIDENCE_DIR) / Path(*cleaned)
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
