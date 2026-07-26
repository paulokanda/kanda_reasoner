# project-path: kanda_reasoner_app/generated_artifact_hygiene.py
"""Cleanup helpers for generated ZIP artifacts that must not live in project source.

The Show Project to AI source archive should reconstruct the selected project
source tree, not historical delivery ZIPs or temporary AI-send artifacts.  This
module performs explicit cleanup of known generated ZIP-output locations inside
the selected project root.  It is intentionally narrow and auditable: only the
legacy/generated paths listed in PROJECT_GENERATED_ZIP_NOISE_TARGETS are removed.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "ProjectGeneratedZipNoiseTarget",
    "PROJECT_GENERATED_ZIP_NOISE_TARGETS",
    "cleanup_project_generated_zip_noise",
    "project_delete_after_daily_work_dir",
]


@dataclass(frozen=True)
class ProjectGeneratedZipNoiseTarget:
    """One generated project-local ZIP artifact location to remove."""

    relative_path: str
    path_type: str
    reason_code: str
    replacement_policy: str


PROJECT_GENERATED_ZIP_NOISE_TARGETS: tuple[ProjectGeneratedZipNoiseTarget, ...] = (
    ProjectGeneratedZipNoiseTarget(
        "kanda_prompt_workspace/first_AI_deliver",
        "directory",
        "legacy_first_ai_deliver_output",
        "Startup delivery is generated outside the project under <drive>/<project>_show_project_to_AI/first_prompt_files.",
    ),
    ProjectGeneratedZipNoiseTarget(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS.zip",
        "file",
        "legacy_prompt_library_archive",
        "Prompt-library delivery ZIP is generated outside the project under first_prompt_files/prompt_library.zip.",
    ),
    ProjectGeneratedZipNoiseTarget(
        "kanda_prompt_workspace/prompt_library/prompt_library.zip",
        "file",
        "legacy_prompt_library_archive",
        "Prompt-library delivery ZIP is generated outside the project under first_prompt_files/prompt_library.zip.",
    ),
    ProjectGeneratedZipNoiseTarget(
        "kanda_prompt_workspace/prompt_audit_zips",
        "directory",
        "legacy_prompt_audit_zip_output",
        "Prompt-audit ZIP outputs belong in <drive>/<project>_delete_after_daily_work, not inside the project source tree.",
    ),
    ProjectGeneratedZipNoiseTarget(
        "project_freeze_after_update/files_to_send_ai",
        "directory",
        "deprecated_freeze_ai_send_pack_output",
        "Freeze memory is exported through Show Project to AI project ZIP/source archive; project-local files_to_send_ai packs are deprecated.",
    ),
)


def _safe_project_root(project_root: str | Path) -> Path:
    """Support safe project root behavior.
    
    Parameters
    ----------
    project_root : str | Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    root = Path(project_root).expanduser().resolve(strict=False)
    if not str(root).strip() or root == root.anchor:
        raise ValueError("Refusing generated-artifact cleanup for broad root: " + str(root))
    if len(root.parts) < 2:
        raise ValueError("Refusing generated-artifact cleanup for unsafe project root: " + str(root))
    return root


def _inside_root(path: Path, root: Path) -> bool:
    """Support inside root behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    resolved_path = path.expanduser().resolve(strict=False)
    resolved_root = root.expanduser().resolve(strict=False)
    try:
        resolved_path.relative_to(resolved_root)
        return True
    except ValueError:
        return False


def project_delete_after_daily_work_dir(project_root: str | Path) -> Path:
    """Return <project_drive>/<project>_delete_after_daily_work for generated temporary outputs."""
    root = _safe_project_root(project_root)
    anchor = root.anchor or str(root.parent)
    folder_name = root.name + "_delete_after_daily_work"
    if anchor.endswith(":\\") or anchor.endswith(":/"):
        return Path(anchor) / folder_name
    if anchor.endswith(":"):
        return Path(f"{anchor}\\{folder_name}")
    return Path(anchor) / folder_name


def _remove_path(path: Path) -> int:
    """Support remove path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    int
        The integer result.
    """
    
    if not path.exists() and not path.is_symlink():
        return 0
    if path.is_dir() and not path.is_symlink():
        count = sum(1 for _ in path.rglob("*")) + 1
        shutil.rmtree(path)
        return count
    path.unlink()
    return 1


def cleanup_project_generated_zip_noise(project_root: str | Path) -> dict[str, Any]:
    """Delete known generated ZIP-output noise from inside the selected project.

    This is not a source-archive exclusion rule.  It corrects the project tree by
    removing deprecated generated locations that should never be recreated inside
    the project.  The function is deliberately limited to exact relative paths in
    PROJECT_GENERATED_ZIP_NOISE_TARGETS.
    """
    root = _safe_project_root(project_root)
    removed: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for target in PROJECT_GENERATED_ZIP_NOISE_TARGETS:
        path = root / Path(target.relative_path)
        if not _inside_root(path, root):
            errors.append(
                {
                    "path": target.relative_path,
                    "reason_code": "unsafe_target_outside_project_root",
                    "message": "Resolved cleanup target is outside selected project root.",
                }
            )
            continue
        if not path.exists() and not path.is_symlink():
            missing.append(
                {
                    "path": target.relative_path,
                    "path_type": target.path_type,
                    "reason_code": target.reason_code,
                    "replacement_policy": target.replacement_policy,
                }
            )
            continue
        try:
            removed_count = _remove_path(path)
            removed.append(
                {
                    "path": target.relative_path,
                    "path_type": target.path_type,
                    "reason_code": target.reason_code,
                    "replacement_policy": target.replacement_policy,
                    "removed_items": removed_count,
                }
            )
        except OSError as exc:
            errors.append(
                {
                    "path": target.relative_path,
                    "path_type": target.path_type,
                    "reason_code": target.reason_code,
                    "message": str(exc),
                }
            )

    return {
        "project_root": str(root),
        "delete_after_daily_work_dir": str(project_delete_after_daily_work_dir(root)),
        "removed": removed,
        "missing": missing,
        "errors": errors,
        "ok": not errors,
    }
