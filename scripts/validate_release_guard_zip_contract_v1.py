# project-path: scripts/validate_release_guard_zip_contract_v1.py
"""Run release guard local validation without fragile PowerShell stderr handling.

This script is intentionally small and standard-library only. It runs the same
checks that the delivered PowerShell validation block used to run, but captures
native command output through Python subprocess instead of a PowerShell pipeline.
That avoids false failures when unittest writes progress dots to stderr.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


FEATURE_ID = "release_guard_zip_delivery_contract_v1"
PATCH_NAME = "release_guard_zip_contract_v1_patch"
TEST_MODULES = [
    "tests.test_patch_release_governor_contract",
    "tests.test_patch_delivery_prompt_release_gate_contract",
]


def _timestamp() -> str:
    """Support timestamp behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _write_line(path: Path, text: str = "") -> None:
    """Support write line behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    text : str, optional
        The text value.
    """
    
    with path.open("a", encoding="utf-8", errors="replace") as handle:
        handle.write(text + "\n")


def _run_step(
    title: str,
    command: Sequence[str],
    cwd: Path,
    evidence_file: Path,
) -> None:
    """Support run step behavior.
    
    Parameters
    ----------
    title : str
        The title value.
    command : Sequence[str]
        The command value.
    cwd : Path
        The cwd value.
    evidence_file : Path
        The evidence file value.
    """
    
    print("")
    print(title)
    _write_line(evidence_file, "")
    _write_line(evidence_file, title)
    _write_line(evidence_file, "> " + " ".join(command))

    completed = subprocess.run(
        list(command),
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    output = completed.stdout or ""
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
        with evidence_file.open("a", encoding="utf-8", errors="replace") as handle:
            handle.write(output)
            if not output.endswith("\n"):
                handle.write("\n")

    if completed.returncode != 0:
        message = f"VALIDATION STEP FAILED: {title} (exit code {completed.returncode})"
        print(message)
        _write_line(evidence_file, message)
        raise SystemExit(completed.returncode)


def _default_staged_zip(project_root: Path, patch_name: str) -> Path:
    """Support default staged zip behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    patch_name : str
        The patch name value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    drive_root = Path(project_root.anchor)
    work_dir = drive_root / f"{project_root.name}_delete_after_daily_work"
    return work_dir / f"{patch_name}.zip"


def _require_files(project_root: Path, paths: Iterable[str]) -> None:
    """Support require files behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    paths : Iterable[str]
        The file or folder paths.
    """
    
    missing = []
    for relative in paths:
        if not (project_root / relative).exists():
            missing.append(relative)
    if missing:
        print("VALIDATION BLOCKED: required installed files are missing.")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)


def main(argv: Sequence[str] | None = None) -> int:
    """Support main behavior.
    
    Parameters
    ----------
    argv : Sequence[str] | None, optional
        The optional argv value.
    
    Returns
    -------
    int
        The integer status code.
    """
    
    parser = argparse.ArgumentParser(
        description="Validate Release Guard ZIP Delivery Contract v1 locally."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path.cwd()),
        help="Installed project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--patch-name",
        default=PATCH_NAME,
        help="Patch basename without .zip.",
    )
    parser.add_argument(
        "--zip-path",
        default=None,
        help="Optional staged ZIP path. Defaults to drive-root staging folder.",
    )
    parser.add_argument(
        "--evidence-file",
        default=None,
        help="Optional evidence output path.",
    )
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        print(f"VALIDATION BLOCKED: project root does not exist: {project_root}")
        return 1

    zip_path = Path(args.zip_path).resolve() if args.zip_path else _default_staged_zip(
        project_root, args.patch_name
    )
    if args.evidence_file:
        evidence_file = Path(args.evidence_file).resolve()
    else:
        evidence_file = zip_path.with_name(f"{args.patch_name}_local_validation_evidence.txt")

    evidence_file.parent.mkdir(parents=True, exist_ok=True)
    evidence_file.write_text(
        "LOCAL VALIDATION EVIDENCE\n"
        f"Feature ID: {FEATURE_ID}\n"
        f"Project root: {project_root}\n"
        f"Staged ZIP: {zip_path}\n"
        f"Started: {_timestamp()}\n",
        encoding="utf-8",
    )

    if not zip_path.exists():
        print(f"VALIDATION BLOCKED: staged ZIP not found: {zip_path}")
        return 1

    _require_files(
        project_root,
        [
            "scripts/validate_patch_zip.py",
            "scripts/validate_release_guard_zip_contract_v1.py",
            "tests/test_patch_release_governor_contract.py",
            "tests/test_patch_delivery_prompt_release_gate_contract.py",
            "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py",
        ],
    )

    python_exe = sys.executable

    _run_step(
        "Step 1/3: validating patch ZIP contract...",
        [python_exe, "scripts/validate_patch_zip.py", str(zip_path)],
        project_root,
        evidence_file,
    )

    # Startup sync must happen before tests that inspect generated startup files.
    _run_step(
        "Step 2/3: checking startup sync before prompt contract tests...",
        [
            python_exe,
            "prompt_tools/sync_startup_routing_kernel_pack.py",
            "--ensure-sync",
            "--yes",
        ],
        project_root / "kanda_prompt_workspace",
        evidence_file,
    )

    _run_step(
        "Step 3/3: running release guard unit tests...",
        [python_exe, "-m", "unittest", *TEST_MODULES],
        project_root,
        evidence_file,
    )

    final = (
        f"VALIDATION OK: {FEATURE_ID}\n"
        "STATUS: IN_SYNC\n"
        "CONTRACT_TEST_OK: patch release governor validator and prompt hooks passed\n"
        "ZIP CONTRACT: PASS\n"
        f"Completed: {_timestamp()}\n"
        f"Evidence file: {evidence_file}"
    )
    print("")
    print(final)
    _write_line(evidence_file, "")
    for line in final.splitlines():
        _write_line(evidence_file, line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
