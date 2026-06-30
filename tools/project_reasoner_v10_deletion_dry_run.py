# project-path: tools/project_reasoner_v10_deletion_dry_run.py
"""Dry-run removal check for the retired reasoner engine package.

The script temporarily moves the old package folder out of the import path,
runs canonical import checks, then restores the folder before exiting.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DELETE_TARGET_RELATIVE_PATH = (
    "kanda_reasoner_app/project_reasoner_v10"
)

__all__ = (
    "DELETE_TARGET_RELATIVE_PATH",
    "main",
    "run_command",
    "run_dry_run",
)


def run_command(command: list[str], cwd: Path) -> int:
    """Run a command, print its output, and return its exit code."""
    print("RUN: " + " ".join(command))
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )

    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)

    print("EXIT: " + str(completed.returncode))
    return int(completed.returncode)


def _build_argument_parser() -> argparse.ArgumentParser:
    """Support build argument parser behavior.
    
    Returns
    -------
    argparse.ArgumentParser
        The argument parser result.
    """
    
    parser = argparse.ArgumentParser(
        description="Dry-run deletion of kanda_reasoner_app/project_reasoner_v10."
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Project root path.",
    )
    return parser


def _dry_run_backup_path(project_root: Path) -> Path:
    """Support dry run backup path behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    drive_root = Path(os.path.splitdrive(str(project_root))[0] + os.sep)
    backup_root = drive_root / "_kanda_dry_run_backups"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return backup_root / (
        "project_reasoner_v10_dry_run_"
        + str(os.getpid())
        + "_"
        + timestamp
    )


def run_dry_run(project_root: Path) -> int:
    """Temporarily move the deletion target and run canonical checks."""
    project_root = project_root.resolve()
    target_path = project_root / DELETE_TARGET_RELATIVE_PATH
    backup_path = _dry_run_backup_path(project_root)

    print("PROJECT ROOT: " + str(project_root))

    if not target_path.exists():
        print("Target folder not found: " + str(target_path), file=sys.stderr)
        return 1

    backup_path.parent.mkdir(parents=True, exist_ok=True)

    print("TEMPORARILY MOVING: " + str(target_path))
    print("TO: " + str(backup_path))

    restored = False

    try:
        shutil.move(str(target_path), str(backup_path))

        checks = [
            [
                sys.executable,
                "-c",
                (
                    "import importlib.util; "
                    "spec = importlib.util.find_spec("
                    "'kanda_reasoner_app.project_reasoner_v10'"
                    "); "
                    "raise SystemExit(0 if spec is None else 1)"
                ),
            ],
            [
                sys.executable,
                "-c",
                (
                    "import kanda_reasoner_app.reasoner_engine; "
                    "import kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window; "
                    "import kanda_reasoner_app.reasoner_engine.query_router; "
                    "import kanda_reasoner_app.reasoner_engine.reasoner_retriever; "
                    "import reasoner_tools_gui; "
                    "print('canonical runtime imports ok without retired package')"
                ),
            ],
            [
                sys.executable,
                "kanda_reasoner_app/manage_architecture/manage_architecture.py",
                "--root",
                str(project_root),
                "--validate",
            ],
        ]

        for command in checks:
            exit_code = run_command(command, project_root)
            if exit_code != 0:
                print("PROJECT_REASONER_V10_DELETION_DRY_RUN_FAIL")
                return exit_code

        print("PROJECT_REASONER_V10_DELETION_DRY_RUN_PASS")
        return 0

    finally:
        if backup_path.exists() and not target_path.exists():
            shutil.move(str(backup_path), str(target_path))
            restored = True
        if restored:
            print("RESTORED: " + str(target_path))


def main(argv: list[str] | None = None) -> int:
    """Command line entry point."""
    parser = _build_argument_parser()
    args = parser.parse_args(argv)
    return run_dry_run(Path(args.root))


if __name__ == "__main__":
    raise SystemExit(main())
