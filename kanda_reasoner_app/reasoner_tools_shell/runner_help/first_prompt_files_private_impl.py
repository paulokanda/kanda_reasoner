# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/first_prompt_files_private_impl.py
"""First-prompt startup delivery helpers for the Show Project to AI tab."""

from __future__ import annotations

import shutil
import subprocess
import sys
from kanda_reasoner_app.tool_process_environment import build_tool_child_environment
from pathlib import Path
from typing import Any

from kanda_reasoner_app.generated_artifact_hygiene import cleanup_project_generated_zip_noise
from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_first_prompt_files_dir,
)

__all__ = [
    "REQUIRED_FIRST_PROMPT_FILENAMES",
    "clear_first_prompt_files_dir",
    "run_create_first_prompt_files",
]

REQUIRED_FIRST_PROMPT_FILENAMES = (
    "first_prompts_to_ai.zip",
    "prompt_library.zip",
    "tell_AI_read_before_all.md",
    "zz_read_only_if_modifying_startup_delivery.md",
)


def _append_log(window: Any, text: str) -> None:
    """Support append log behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    text : str
        The text value.
    """
    
    try:
        target = getattr(window, "first_prompt_log_box", None)
        if target is not None:
            target.appendPlainText(str(text))
            scroll_bar = target.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())
            return
    except Exception:
        pass
    try:
        window._append_log(str(text))
    except Exception:
        pass


def _set_status(window: Any, text: str) -> None:
    """Support set status behavior.
    
    Parameters
    ----------
    window : Any
        The window value.
    text : str
        The text value.
    """
    
    try:
        getattr(window, "first_prompt_status_label").setText(str(text))
    except Exception:
        pass


def _process_helpers() -> Any:
    """Support process helpers behavior.
    
    Returns
    -------
    Any
        The any result.
    """
    
    from kanda_reasoner_app.reasoner_tools_shell.runner_help import window_process_private_impl

    return window_process_private_impl


def _same_path(first: Path, second: Path) -> bool:
    """Support same path behavior.
    
    Parameters
    ----------
    first : Path
        The first value.
    second : Path
        The second value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    try:
        return first.resolve(strict=False) == second.resolve(strict=False)
    except Exception:
        return str(first) == str(second)


def clear_first_prompt_files_dir(output_dir: str | Path) -> int:
    """Clear only the approved first_prompt_files output directory contents."""
    resolved_dir = Path(output_dir).expanduser().resolve()
    if resolved_dir.name != "first_prompt_files":
        raise ValueError(
            "Refusing to clear output folder because it is not first_prompt_files: "
            + str(resolved_dir)
        )
    parent = resolved_dir.parent
    if not parent.name.endswith("_show_project_to_AI"):
        raise ValueError(
            "Refusing to clear output folder because parent is not *_show_project_to_AI: "
            + str(resolved_dir)
        )

    resolved_dir.mkdir(parents=True, exist_ok=True)
    removed = 0
    for child in list(resolved_dir.iterdir()):
        if child.is_dir():
            shutil.rmtree(child)
            removed += 1
        else:
            child.unlink()
            removed += 1
    return removed


def _tool_runtime_roots() -> tuple[Path, ...]:
    """Return ordered Tool-owned roots that may contain runtime resources."""
    candidates: list[Path] = []

    def add(candidate: Path) -> None:
        resolved = candidate.expanduser().resolve(strict=False)
        if resolved not in candidates:
            candidates.append(resolved)

    add(Path(__file__).resolve().parents[3])

    frozen_root = getattr(sys, "_MEIPASS", None)
    if frozen_root:
        add(Path(str(frozen_root)))

    executable_parent = Path(sys.executable).expanduser().resolve(strict=False).parent
    add(executable_parent / "_internal")
    add(executable_parent)
    return tuple(candidates)


def _find_tool_workspace_root() -> Path:
    """Return the Tool-owned prompt workspace in source or Portable runtime."""
    relative_script = (
        Path("kanda_prompt_workspace")
        / "prompt_tools"
        / "sync_startup_routing_kernel_pack.py"
    )
    checked: list[str] = []
    for tool_root in _tool_runtime_roots():
        script = tool_root / relative_script
        workspace = tool_root / "kanda_prompt_workspace"
        checked.append(str(tool_root))
        if script.is_file() and (workspace / "prompt_library").is_dir():
            return workspace

    raise FileNotFoundError(
        "Could not find Tool-owned "
        "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py "
        "in KANDA Tool runtime roots: " + "; ".join(checked)
    )


def _validate_generated_files(output_dir: Path) -> list[str]:
    """Support validate generated files behavior.
    
    Parameters
    ----------
    output_dir : Path
        The output dir value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    missing = [name for name in REQUIRED_FIRST_PROMPT_FILENAMES if not (output_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "First-prompt delivery generation completed but required files are missing: "
            + ", ".join(missing)
        )
    return [name for name in REQUIRED_FIRST_PROMPT_FILENAMES]


def run_create_first_prompt_files(window: Any) -> None:
    """Generate startup first-prompt files into show_project_to_AI/first_prompt_files."""
    if getattr(window, "_process", None) is not None:
        _append_log(window, "[WARN] Create First Prompt Files skipped because another process is active.")
        _set_status(window, "Busy")
        return

    try:
        raw_root = window.project_root_edit.text().strip()
        project_root = _process_helpers()._tab4_resolve_project_root(raw_root)
    except Exception as exc:
        _append_log(window, "[ERROR] Could not resolve selected project root: " + str(exc))
        _set_status(window, "Invalid project root")
        return

    try:
        cleanup_result = cleanup_project_generated_zip_noise(project_root)
        if cleanup_result.get("removed"):
            _append_log(window, "Cleaned deprecated in-project ZIP delivery artifacts:")
            for item in cleanup_result.get("removed", []):
                _append_log(window, "  " + str(item.get("path", "")) + " (" + str(item.get("reason_code", "")) + ")")
        if cleanup_result.get("errors"):
            raise RuntimeError("Generated ZIP artifact cleanup failed: " + str(cleanup_result.get("errors")))

        output_dir = analysis_first_prompt_files_dir(project_root).expanduser().resolve()
        expected_output_dir = analysis_first_prompt_files_dir(project_root).expanduser().resolve()
        if not _same_path(output_dir, expected_output_dir):
            raise ValueError("Resolved first_prompt_files path drifted unexpectedly.")

        workspace_root = _find_tool_workspace_root()
        script = workspace_root / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
        removed_count = clear_first_prompt_files_dir(output_dir)

        _append_log(window, "Starting first-prompt startup delivery generation...")
        _append_log(window, "  root       : " + str(project_root))
        _append_log(window, "  workspace  : " + str(workspace_root))
        _append_log(window, "  destination: " + str(output_dir))
        _append_log(window, "  cleared existing first_prompt_files items: " + str(removed_count))
        _set_status(window, "Creating first prompt files...")

        env = build_tool_child_environment()
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--sync",
                "--yes",
                "--workspace",
                str(workspace_root),
                "--output-dir",
                str(output_dir),
                "--project-root",
                str(project_root),
            ],
            cwd=str(workspace_root),
            text=True,
            capture_output=True,
            env=env,
        )

        if completed.stdout.strip():
            _append_log(window, completed.stdout.strip())
        if completed.stderr.strip():
            _append_log(window, completed.stderr.strip())

        if completed.returncode != 0:
            raise RuntimeError(
                "sync_startup_routing_kernel_pack.py failed with return code "
                + str(completed.returncode)
            )

        files = _validate_generated_files(output_dir)
        _append_log(window, "[OK] First prompt files generated.")
        for name in files:
            _append_log(window, "  " + name)
        _set_status(window, "First prompt files ready")
    except Exception as exc:
        _append_log(window, "[ERROR] First prompt files generation failed:")
        _append_log(window, str(exc))
        _set_status(window, "First prompt files failed")
