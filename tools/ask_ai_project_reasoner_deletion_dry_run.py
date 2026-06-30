# project-path: tools/ask_ai_project_reasoner_deletion_dry_run.py
"""Dry-run removal check for the top-level ask_ai_project_reasoner package.

This tool temporarily moves ask_ai_project_reasoner out of the project root,
runs canonical runtime import checks, then restores the folder.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Sequence

DELETE_TARGET_RELATIVE = "ask_ai_project_reasoner"
DELETED_ENGINE_RELATIVE = os.path.join("kanda_reasoner_app", "project_reasoner_v10")
PUBLIC_API = (
    "DELETE_TARGET_RELATIVE",
    "DELETED_ENGINE_RELATIVE",
    "PUBLIC_API",
    "run_ask_ai_deletion_dry_run",
    "main",
)


def _run_command(args: Sequence[str], root: Path) -> int:
    """Run a subprocess command and stream plain output."""
    print("RUN: " + " ".join(args))
    completed = subprocess.run(
        list(args),
        cwd=str(root),
        env={
            **os.environ,
            "PYTHONPATH": str(root),
            "kanda_reasoner_project_root": str(root),
        },
        text=True,
    )
    print("EXIT: " + str(completed.returncode))
    return int(completed.returncode)


def _make_backup_path(root: Path) -> Path:
    """Build a unique dry-run backup path outside the source tree."""
    drive = Path(root.anchor)
    backup_root = drive / "_kanda_dry_run_backups"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return backup_root / ("ask_ai_project_reasoner_dry_run_%s_%s" % (os.getpid(), stamp))


def run_ask_ai_deletion_dry_run(root: Path) -> int:
    """Temporarily move ask_ai_project_reasoner and verify canonical runtime."""
    project_root = root.resolve()
    delete_target = project_root / DELETE_TARGET_RELATIVE
    deleted_engine = project_root / DELETED_ENGINE_RELATIVE
    backup_target = _make_backup_path(project_root)

    print("PROJECT ROOT: " + str(project_root))
    print("TEMPORARILY MOVING: " + str(delete_target))
    print("TO: " + str(backup_target))

    if not delete_target.exists():
        print("ASK_AI_PROJECT_REASONER_DELETION_DRY_RUN_FAIL")
        print("Delete target not found: " + str(delete_target))
        return 1

    if deleted_engine.exists():
        print("ASK_AI_PROJECT_REASONER_DELETION_DRY_RUN_FAIL")
        print("Deleted engine target unexpectedly exists: " + str(deleted_engine))
        return 1

    backup_target.parent.mkdir(parents=True, exist_ok=True)

    if backup_target.exists():
        shutil.rmtree(str(backup_target))

    moved = False

    try:
        shutil.move(str(delete_target), str(backup_target))
        moved = True

        checks = [
            [
                sys.executable,
                "-c",
                (
                    "import importlib.util; "
                    "spec = importlib.util.find_spec('ask_ai_project_reasoner'); "
                    "raise SystemExit(0 if spec is None else 1)"
                ),
            ],
            [
                sys.executable,
                "-c",
                (
                    "import importlib.util; "
                    "spec = importlib.util.find_spec('kanda_reasoner_app.project_reasoner_v10'); "
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
                    "print('canonical runtime imports ok without ask_ai_project_reasoner')"
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
            exit_code = _run_command(command, project_root)
            if exit_code != 0:
                print("ASK_AI_PROJECT_REASONER_DELETION_DRY_RUN_FAIL")
                return exit_code

        print("ASK_AI_PROJECT_REASONER_DELETION_DRY_RUN_PASS")
        return 0
    finally:
        if moved:
            if delete_target.exists():
                shutil.rmtree(str(delete_target))
            shutil.move(str(backup_target), str(delete_target))
            print("RESTORED: " + str(delete_target))


def _build_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Dry-run deletion of ask_ai_project_reasoner."
    )
    parser.add_argument(
        "--root",
        default=os.environ.get("kanda_reasoner_project_root", "."),
        help="Project root path.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point."""
    parser = _build_argument_parser()
    args = parser.parse_args(argv)
    return run_ask_ai_deletion_dry_run(Path(args.root))


if __name__ == "__main__":
    raise SystemExit(main())
