# project-path: kanda_prompt_workspace/prompt_tools/startup_kernel/cli_sync.py
"""Startup delivery sync command helpers."""

from __future__ import annotations

import argparse
from pathlib import Path

from startup_kernel.cli_check import command_check
from startup_kernel.zip_delivery import make_zip


def confirm_sync(args: argparse.Namespace) -> bool:
    """Support confirm sync behavior.
    
    Parameters
    ----------
    args : argparse.Namespace
        The positional arguments.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if args.yes:
        return True
    print("This will regenerate first_prompt_files with the current startup ZIP, prompt_library.zip, and tell_AI_read_before_all.md file.")
    print("Old generated startup ZIPs and startup instruction files in first_prompt_files will be removed.")
    print("Canonical source files will not be modified.")
    answer = input("Proceed with sync/regeneration? Type YES to continue: ").strip()
    return answer == "YES"

def command_ensure_sync(workspace_root: Path, output_dir: Path, active_project_root: Path, args: argparse.Namespace) -> int:
    """Support command ensure sync behavior.
    
    Parameters
    ----------
    workspace_root : Path
        The workspace root value.
    output_dir : Path
        The output dir value.
    active_project_root : Path
        The active project root value.
    args : argparse.Namespace
        The positional arguments.
    
    Returns
    -------
    int
        The integer result.
    """
    
    print("STARTUP PROMPT REQUEST KERNEL ENSURE SYNC")
    print("Step 1/3: checking current delivery.")
    print("")

    check_code = command_check(workspace_root, output_dir, active_project_root)

    if check_code == 0:
        print("")
        print("ENSURE SYNC RESULT: ALREADY_IN_SYNC")
        print("No regeneration was needed.")
        return 0

    if check_code == 2:
        print("")
        print("ENSURE SYNC RESULT: ABORTED_MISSING_SOURCE")
        print("One or more canonical source files are missing. Sync was not attempted.")
        return check_code

    print("")
    print("Step 2/3: delivery is missing or stale. Sync is required.")

    if not confirm_sync(args):
        print("ENSURE SYNC CANCELLED BY HUMAN")
        return 4

    sync_code, _zip_path = make_zip(workspace_root, output_dir, active_project_root, dry_run=False)
    if sync_code != 0:
        print("")
        print("ENSURE SYNC RESULT: SYNC_FAILED")
        return sync_code

    print("")
    print("Step 3/3: running post-sync check.")
    print("")
    final_check_code = command_check(workspace_root, output_dir, active_project_root)

    if final_check_code == 0:
        print("")
        print("ENSURE SYNC RESULT: IN_SYNC_AFTER_SYNC")
    else:
        print("")
        print("ENSURE SYNC RESULT: POST_SYNC_CHECK_FAILED")

    return final_check_code
