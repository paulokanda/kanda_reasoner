# project-path: scripts/validate_sync_startup_kernel_refactor_train_car_2_path_detection_repair_v1.py
"""Validate train car 2 startup workspace auto-detection repair.

The refactor moved CLI implementation into prompt_tools/startup_kernel. The
startup generator must still auto-detect kanda_prompt_workspace as the
workspace root when called through the public prompt_tools entrypoint without
an explicit --workspace argument.
"""

from __future__ import annotations

import os
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "sync-startup-kernel-refactor-train-car-2-path-detection-repair-v1"
ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = ROOT / "kanda_prompt_workspace" / "prompt_tools"
WORKSPACE_ROOT = ROOT / "kanda_prompt_workspace"
TARGET = PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py"
CORE_HELPERS = PROMPT_TOOLS / "startup_kernel" / "core_helpers.py"
TRAIN_CAR_2_VALIDATOR = ROOT / "scripts" / "validate_sync_startup_kernel_refactor_train_car_2_v1.py"


def _assert(condition: bool, message: str) -> None:
    """Support assert behavior.
    
    Parameters
    ----------
    condition : bool
        The condition value.
    message : str
        The message text.
    """
    
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    """Support read behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return path.read_text(encoding="utf-8")


def _run(command: list[str], cwd: Path) -> str:
    """Support run behavior.
    
    Parameters
    ----------
    command : list[str]
        The command value.
    cwd : Path
        The cwd value.
    
    Returns
    -------
    str
        The string result.
    """
    
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    paths = [str(PROMPT_TOOLS), str(ROOT)]
    if existing_pythonpath:
        paths.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    result = subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            "command failed with exit code "
            + str(result.returncode)
            + ": "
            + " ".join(command)
            + "\n"
            + result.stdout
        )
    return result.stdout


def validate_compile() -> None:
    """Validate the compile.
    """
    
    for path in [TARGET, CORE_HELPERS, TRAIN_CAR_2_VALIDATOR, Path(__file__)]:
        py_compile.compile(str(path), doraise=True)


def validate_detection_source_contract() -> None:
    """Validate the detection source contract.
    """
    
    text = _read(CORE_HELPERS)
    required = [
        "for candidate in (start, *start.parents):",
        "if (candidate / \"prompt_library\").exists():",
        "does not mistake startup_kernel for",
    ]
    for fragment in required:
        _assert(fragment in text, "core_helpers.py missing detection repair fragment: " + fragment)

    forbidden = [
        "script_path.parent.parent,   # v2: script in prompt_tools",
        "return script_path.parent.resolve()",
    ]
    for fragment in forbidden:
        _assert(fragment not in text, "stale fixed-depth workspace detection remains: " + fragment)


def validate_auto_workspace_sync_cycle() -> None:
    """Validate the auto workspace sync cycle.
    """
    
    with tempfile.TemporaryDirectory(prefix="kanda_sync_kernel_path_repair_") as tmp_name:
        out_dir = Path(tmp_name) / "first_prompt_files"
        sync_output = _run(
            [
                sys.executable,
                str(TARGET),
                "--sync",
                "--yes",
                "--project-root",
                str(ROOT),
                "--output-dir",
                str(out_dir),
            ],
            cwd=ROOT,
        )
        _assert(
            "Workspace root: " + str(WORKSPACE_ROOT) in sync_output,
            "auto-detected workspace root was not kanda_prompt_workspace",
        )
        _assert("startup_kernel" not in sync_output.split("Workspace root:", 1)[1].splitlines()[0],
                "workspace root still points inside startup_kernel")
        _assert("STATUS: IN_SYNC" in sync_output, "auto-workspace sync did not finish in sync")

        check_output = _run(
            [
                sys.executable,
                str(TARGET),
                "--check",
                "--project-root",
                str(ROOT),
                "--output-dir",
                str(out_dir),
            ],
            cwd=ROOT,
        )
        _assert(
            "Workspace root: " + str(WORKSPACE_ROOT) in check_output,
            "auto-detected workspace root regressed during check",
        )
        _assert("STATUS: IN_SYNC" in check_output, "auto-workspace check did not finish in sync")


def main() -> int:
    """Support main behavior.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    validate_compile()
    validate_detection_source_contract()
    validate_auto_workspace_sync_cycle()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
