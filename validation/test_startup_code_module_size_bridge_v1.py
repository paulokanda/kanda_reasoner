"""Validate the startup bridge for code module size limits.

This validation is standard-library only and is safe to run from the project
root. It checks canonical prompt sources and, when requested, regenerates the
startup delivery artifacts so the beginning-of-session ZIP exposes the bridge.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "startup-code-module-size-bridge-v1"

BRIDGE_REQUIRED_SNIPPETS = (
    "## Code Module Size Bridge",
    "Ideal code module size: 400 lines or fewer.",
    "Maximum code module size: 500 lines or fewer.",
    "When creating a new code module, do not create a file above 500 lines",
    "This rule applies to code/source modules, especially `.py` files.",
    "This rule does not apply to plain text, Markdown, documentation, prompt,",
    "`.txt`, `.md`, `.json`",
    "route to `large_module_refactor_protocol.md`",
)

FULL_PROTOCOL_REQUIRED_SNIPPETS = (
    "# Large Module Creation and Refactor Protocol",
    "Version: 5.9",
    "Use: Invoke when creating or refactoring a relevant code module",
    "Module-size law for code modules:",
    "When creating a new code module, do not create a file above 500 lines",
    "This rule does not apply to plain text, Markdown, documentation, prompt, manifest, JSON, log, report, or other non-code content files.",
    "v5.9: Extended module-size law to new code module creation",
)

NAV_REQUIRED_SNIPPETS = (
    "new code modules must stay <=500 lines",
    "new code module expected to exceed 500 lines",
    "code file above 500 lines, or new code module expected to exceed 500 lines",
)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise AssertionError(f"Could not read file: {path}: {exc}") from exc


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise AssertionError(f"Required file is missing: {path}")


def _require_snippets(label: str, text: str, snippets: tuple[str, ...]) -> None:
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        formatted = "\n".join(f"- {item}" for item in missing)
        raise AssertionError(f"Missing required snippets in {label}:\n{formatted}")


def _run_sync(project_root: Path) -> None:
    script = project_root / "kanda_prompt_workspace" / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    _require_file(script)
    command = [
        sys.executable,
        str(script),
        "--sync",
        "--yes",
        "--workspace",
        str(project_root / "kanda_prompt_workspace"),
        "--project-root",
        str(project_root),
    ]
    completed = subprocess.run(
        command,
        cwd=str(project_root),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.returncode != 0:
        raise AssertionError(f"Startup sync failed with exit code {completed.returncode}")
    if "SYNC COMPLETE" not in completed.stdout:
        raise AssertionError("Startup sync did not report SYNC COMPLETE.")
    if "STATUS: IN_SYNC" not in completed.stdout:
        raise AssertionError("Startup sync did not report STATUS: IN_SYNC.")


def _default_first_prompt_dir(project_root: Path) -> Path:
    drive = Path(project_root.anchor) if project_root.anchor else project_root.parent
    return drive / f"{project_root.name}_show_project_to_AI" / "first_prompt_files"


def _validate_generated_startup(project_root: Path) -> None:
    first_prompt_dir = _default_first_prompt_dir(project_root)
    startup_zip = first_prompt_dir / "first_prompts_to_ai.zip"
    prompt_zip = first_prompt_dir / "prompt_library.zip"
    tell_file = first_prompt_dir / "tell_AI_read_before_all.md"
    for path in (startup_zip, prompt_zip, tell_file):
        _require_file(path)

    with zipfile.ZipFile(startup_zip, "r") as archive:
        names = set(archive.namelist())
        if "05_start_of_day_master_stack.md" not in names:
            raise AssertionError("05_start_of_day_master_stack.md missing from startup ZIP.")
        generated_start = archive.read("05_start_of_day_master_stack.md").decode(
            "utf-8-sig", errors="replace"
        )
        _require_snippets("generated startup 05_start_of_day_master_stack.md", generated_start, BRIDGE_REQUIRED_SNIPPETS)

    with zipfile.ZipFile(prompt_zip, "r") as archive:
        start_name = "ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md"
        protocol_name = "ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
        nav_name = "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
        names = set(archive.namelist())
        for name in (start_name, protocol_name, nav_name):
            if name not in names:
                raise AssertionError(f"Expected prompt missing from prompt_library.zip: {name}")
        _require_snippets(
            "prompt_library.zip start_of_day_master_stack.md",
            archive.read(start_name).decode("utf-8-sig", errors="replace"),
            BRIDGE_REQUIRED_SNIPPETS,
        )
        _require_snippets(
            "prompt_library.zip large_module_refactor_protocol.md",
            archive.read(protocol_name).decode("utf-8-sig", errors="replace"),
            FULL_PROTOCOL_REQUIRED_SNIPPETS,
        )
        _require_snippets(
            "prompt_library.zip prompt_navigation_index.md",
            archive.read(nav_name).decode("utf-8-sig", errors="replace"),
            NAV_REQUIRED_SNIPPETS,
        )


def validate(project_root: Path, *, skip_sync: bool = False) -> None:
    start_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "start_of_day_master_stack.md"
    protocol_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "06_refactor_and_architecture_hardening" / "large_module_refactor_protocol.md"
    nav_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
    meta_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "METADATA" / "large_module_refactor_protocol.meta.json"
    source_map = project_root / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"

    for path in (start_path, protocol_path, nav_path, meta_path, source_map):
        _require_file(path)

    _require_snippets("start_of_day_master_stack.md", _read(start_path), BRIDGE_REQUIRED_SNIPPETS)
    _require_snippets("large_module_refactor_protocol.md", _read(protocol_path), FULL_PROTOCOL_REQUIRED_SNIPPETS)
    _require_snippets("prompt_navigation_index.md", _read(nav_path), NAV_REQUIRED_SNIPPETS)
    _require_snippets(
        "large_module_refactor_protocol.meta.json",
        _read(meta_path),
        (
            "Large Module Creation and Refactor Protocol",
            "create large module",
            "new module above 500 lines",
            "module size limit",
        ),
    )
    _require_snippets(
        "STARTUP_ROUTING_KERNEL_SOURCES.json",
        _read(source_map),
        (
            "prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md",
            "05_start_of_day_master_stack.md",
            "always_startup",
        ),
    )

    if not skip_sync:
        _run_sync(project_root)
        _validate_generated_startup(project_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate startup code module size bridge v1.")
    parser.add_argument("--project-root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--skip-sync", action="store_true", help="Validate source files only; do not regenerate startup delivery.")
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).resolve()
    try:
        validate(project_root, skip_sync=args.skip_sync)
    except AssertionError as exc:
        print(f"VALIDATION FAILED: {FEATURE_ID}")
        print(str(exc))
        return 1

    print(f"VALIDATION OK: {FEATURE_ID}")
    if not args.skip_sync:
        print("STATUS: IN_SYNC")
    print("MODULE_SIZE_BRIDGE: code creation and refactor limit enforced")
    print("NON_CODE_EXCLUSION: txt md json docs prompts manifests logs reports excluded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
