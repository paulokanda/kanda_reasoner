"""Path helpers for startup prompt candidate audits."""

from __future__ import annotations
__all__: list[str] = []


from pathlib import Path

from .audit_startup_candidates_models import (
    PROMPT_LIBRARY_DIR_NAME,
    SOURCE_MAP_FILENAME,
    TOOLS_DIR_NAME,
)

def normalize_rel_path(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")
def is_hidden_or_cache_path(path: Path) -> bool:
    hidden_or_cache_names = {".git", ".idea", "__pycache__", ".pytest_cache"}
    return any(part in hidden_or_cache_names or part.startswith(".") for part in path.parts)
def is_relative_to_safe(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
def detect_workspace_root(script_path: Path, explicit_workspace: Path | None) -> Path:
    if explicit_workspace is not None:
        workspace = explicit_workspace.resolve()
    else:
        candidates = [
            script_path.parent.parent,
            Path.cwd(),
        ]
        workspace = next(
            (candidate.resolve() for candidate in candidates if is_valid_workspace(candidate)),
            script_path.parent.parent.resolve(),
        )

    if not is_valid_workspace(workspace):
        raise ValueError(
            "Workspace root could not be confirmed. Run from kanda_prompt_workspace "
            "or pass --workspace <path>. Expected prompt_library and prompt_tools."
        )
    return workspace
def is_valid_workspace(path: Path) -> bool:
    return (
        (path / PROMPT_LIBRARY_DIR_NAME).is_dir()
        and (path / TOOLS_DIR_NAME).is_dir()
        and (path / TOOLS_DIR_NAME / SOURCE_MAP_FILENAME).is_file()
    )
