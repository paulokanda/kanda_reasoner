# project-path: kanda_prompt_workspace/prompt_tools/startup_kernel/cli.py
"""Command-line interface for startup kernel sync/check operations."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from startup_freeze_context import resolve_active_project_root
from startup_kernel.cli_check import command_check
from startup_kernel.cli_sync import command_ensure_sync, confirm_sync
from startup_kernel.core_helpers import default_first_prompt_output_dir, detect_workspace_root
from startup_kernel.zip_delivery import make_zip


def parse_args(argv: list[str]) -> argparse.Namespace:
    # Safe default for IDE/run-button launches.
    # When no explicit mode is supplied, run the read-only check instead of
    # failing with argparse's "one of the arguments ... is required" error.
    """Parse the args.
    
    Parameters
    ----------
    argv : list[str]
        The argv value.
    
    Returns
    -------
    argparse.Namespace
        The namespace result.
    """
    
    if not argv:
        argv = ["--check"]

    parser = argparse.ArgumentParser(description="Generate/check the KANDA startup prompt request kernel upload ZIP.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Read-only check for missing/stale delivery ZIP and boot command file.")
    mode.add_argument("--sync", action="store_true", help="Regenerate first_prompt_files startup ZIP, prompt_library.zip, and tell_AI_read_before_all.md file, then run a post-sync check.")
    mode.add_argument("--ensure-sync", action="store_true", help="Check first, sync only if missing/stale, then run a post-sync check.")
    mode.add_argument("--dry-run", action="store_true", help="Show what --sync would include without writing files.")
    parser.add_argument("--workspace", type=Path, default=None, help="Workspace root containing prompt_library/. Defaults to script parent/parent when script is in prompt_tools.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory where delivery files are written. Defaults to <project_drive>/<project>_show_project_to_AI/first_prompt_files.")
    parser.add_argument("--project-root", type=Path, default=None, help="Active project root used to generate 09_active_project_freeze_context.md. Defaults to the parent of kanda_prompt_workspace.")
    parser.add_argument("--yes", action="store_true", help="Confirm --sync or --ensure-sync regeneration without interactive prompt.")
    return parser.parse_args(argv)

def main(argv: list[str]) -> int:
    """Support main behavior.
    
    Parameters
    ----------
    argv : list[str]
        The argv value.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    args = parse_args(argv)
    script_path = Path(__file__).resolve()
    workspace_root = detect_workspace_root(script_path, args.workspace)
    active_project_root = resolve_active_project_root(workspace_root, args.project_root)
    output_dir = (args.output_dir.resolve() if args.output_dir else default_first_prompt_output_dir(active_project_root).resolve())

    if not (workspace_root / "prompt_library").exists():
        print("ERROR: workspace root does not contain prompt_library/.")
        print(f"Workspace root: {workspace_root}")
        print("Install this script in kanda_prompt_workspace/prompt_tools or pass --workspace <path>.")
        return 3

    try:
        if args.check:
            return command_check(workspace_root, output_dir, active_project_root)
        if args.dry_run:
            code, _zip_path = make_zip(workspace_root, output_dir, active_project_root, dry_run=True)
            return code
        if args.ensure_sync:
            return command_ensure_sync(workspace_root, output_dir, active_project_root, args)
        if args.sync:
            if not confirm_sync(args):
                print("SYNC CANCELLED BY HUMAN")
                return 4
            code, _zip_path = make_zip(workspace_root, output_dir, active_project_root, dry_run=False)
            if code != 0:
                return code
            print("")
            print("POST-SYNC CHECK")
            print("")
            return command_check(workspace_root, output_dir, active_project_root)
    except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError, zipfile.BadZipFile) as exc:
        print("ERROR:", exc)
        return 3

    print("ERROR: no mode selected")
    return 3
