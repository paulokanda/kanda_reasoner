# project-path: kanda_reasoner_app/error_memory_gui/_project_roots.py
"""Non-GUI project-root resolution helpers for the Error Memory tab."""
from __future__ import annotations

from pathlib import Path

GENERATED_OUTPUT_SUFFIXES = ("_show_project_to_AI", "_delete_after_daily_work")
DEFAULT_PENDING_INTAKE_DIR_NAME = "pending_ai_assisted_error_lesson_intake"
ERROR_MEMORY_CHILD_NAMES = frozenset({
    DEFAULT_PENDING_INTAKE_DIR_NAME,
    "lessons",
    "exports",
    "schemas",
})
SHOW_PROJECT_CHILD_NAMES = frozenset({
    "first_prompt_files",
    "second_prompt_files",
    "second_prompt_files_building",
    "project_error_memory",
    "json_splitted",
})

__all__ = [
    "DEFAULT_PENDING_INTAKE_DIR_NAME",
    "ERROR_MEMORY_CHILD_NAMES",
    "GENERATED_OUTPUT_SUFFIXES",
    "SHOW_PROJECT_CHILD_NAMES",
    "existing_directory_from_text",
    "source_root_from_directory_hint",
    "source_root_peer_from_generated_output",
]


def source_root_peer_from_generated_output(path: Path) -> Path | None:
    """Return the existing source-root peer for a generated output path."""
    candidate = Path(path).expanduser().resolve(strict=False)
    for suffix in GENERATED_OUTPUT_SUFFIXES:
        if not candidate.name.endswith(suffix):
            continue
        base_name = candidate.name[:-len(suffix)].strip()
        if not base_name:
            return None
        peer = (candidate.parent / base_name).expanduser().resolve(strict=False)
        if peer.exists() and peer.is_dir():
            return peer
        return None
    return None


def source_root_from_directory_hint(
    path: Path,
    *,
    pending_dir_name: str = DEFAULT_PENDING_INTAKE_DIR_NAME,
) -> Path | None:
    """Resolve generated-output folder hints back to a real source project root."""
    candidate = Path(path).expanduser().resolve(strict=False)
    error_memory_children = set(ERROR_MEMORY_CHILD_NAMES)
    error_memory_children.add(str(pending_dir_name or DEFAULT_PENDING_INTAKE_DIR_NAME))
    if candidate.name in error_memory_children:
        parent = candidate.parent
        if parent.name == "project_error_memory":
            candidate = parent
    if candidate.name in SHOW_PROJECT_CHILD_NAMES:
        parent = candidate.parent
        if parent.name.endswith("_show_project_to_AI"):
            candidate = parent
    return source_root_peer_from_generated_output(candidate)


def existing_directory_from_text(
    text: str,
    *,
    pending_dir_name: str = DEFAULT_PENDING_INTAKE_DIR_NAME,
) -> Path | None:
    """Return a safe existing project source directory, or None.

    Existing generated-output folders are accepted only when they can be
    resolved back to an existing sibling source project root.
    """
    cleaned = str(text or "").strip()
    if not cleaned:
        return None
    root = Path(cleaned).expanduser().resolve(strict=False)
    source_root = source_root_from_directory_hint(root, pending_dir_name=pending_dir_name)
    if source_root is not None:
        return source_root
    if root.name.endswith(GENERATED_OUTPUT_SUFFIXES):
        return None
    generated_child_names = set(SHOW_PROJECT_CHILD_NAMES)
    generated_child_names.update(ERROR_MEMORY_CHILD_NAMES)
    generated_child_names.add(str(pending_dir_name or DEFAULT_PENDING_INTAKE_DIR_NAME))
    if root.name in generated_child_names:
        return None
    if not root.exists() or not root.is_dir():
        return None
    return root
