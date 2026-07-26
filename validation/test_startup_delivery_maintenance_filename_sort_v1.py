#!/usr/bin/env python3
"""Validate startup delivery maintenance filename sorting and sync."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "startup-delivery-maintenance-filename-sort-v1"
OLD_NAME = "paste_if_modify" + "_startup_delivery.md"
NEW_NAME = "zz_read_only_if_modifying_startup_delivery.md"
NORMAL_FILES = [
    "first_prompts_to_ai.zip",
    "prompt_library.zip",
    "tell_AI_read_before_all.md",
]
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt", ".csv"}
SCAN_DIRS = [
    "kanda_prompt_workspace/prompt_library",
    "kanda_prompt_workspace/prompt_tools",
]


def fail(message: str) -> int:
    print(f"VALIDATION ERROR: {message}")
    return 1


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def run_command(args: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(
        args,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout


def scan_source(project_root: Path) -> list[str]:
    hits = []
    for rel_dir in SCAN_DIRS:
        base = project_root / rel_dir
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if OLD_NAME in read_text(path):
                hits.append(path.relative_to(project_root).as_posix())
    return hits


def zip_contains_text(zip_path: Path, needle: str) -> bool:
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            if not name.lower().endswith((".md", ".json", ".txt", ".csv", ".py")):
                continue
            data = zf.read(name).decode("utf-8", errors="replace")
            if needle in data:
                return True
    return False


def main() -> int:
    project_root = Path.cwd().resolve(strict=False)
    workspace = project_root / "kanda_prompt_workspace"
    if not workspace.is_dir():
        return fail(f"kanda_prompt_workspace not found under {project_root}")

    generator = workspace / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    freeze_context = workspace / "prompt_tools" / "startup_freeze_context.py"
    if not generator.is_file():
        return fail(f"generator not found: {generator}")
    if not freeze_context.is_file():
        return fail(f"startup freeze context helper not found: {freeze_context}")

    if OLD_NAME in read_text(generator):
        return fail("obsolete filename remains as an exact literal in generator")
    if NEW_NAME not in read_text(generator):
        return fail("new maintenance filename is missing from generator")

    source_hits = scan_source(project_root)
    if source_hits:
        print("Obsolete source references found:")
        for rel in source_hits:
            print(f"- {rel}")
        return fail("obsolete filename remains in active startup source files")

    code, output = run_command(
        [sys.executable, "prompt_tools/sync_startup_routing_kernel_pack.py", "--sync", "--yes"],
        workspace,
    )
    print(output, end="")
    if code != 0:
        return fail(f"startup generator sync failed with code {code}")
    if "STATUS: IN_SYNC" not in output:
        return fail("generator output did not report STATUS: IN_SYNC")

    drive_root = Path(project_root.anchor) if project_root.anchor else project_root.parent
    first_prompt_dir = drive_root / f"{project_root.name}_show_project_to_AI" / "first_prompt_files"
    if not first_prompt_dir.is_dir():
        return fail(f"first_prompt_files folder not found: {first_prompt_dir}")

    for name in NORMAL_FILES:
        if not (first_prompt_dir / name).is_file():
            return fail(f"normal startup file missing: {name}")

    if not (first_prompt_dir / NEW_NAME).is_file():
        return fail(f"new maintenance file missing: {NEW_NAME}")
    if (first_prompt_dir / OLD_NAME).exists():
        return fail(f"old maintenance file still exists: {OLD_NAME}")

    sorted_names = sorted(
        [name for name in NORMAL_FILES + [NEW_NAME]],
        key=lambda item: item.lower(),
    )
    expected_order = NORMAL_FILES + [NEW_NAME]
    if sorted_names != expected_order:
        return fail(f"unexpected Windows-like sort order: {sorted_names}")

    tell_path = first_prompt_dir / "tell_AI_read_before_all.md"
    tell_text = read_text(tell_path)
    if NEW_NAME not in tell_text:
        return fail("read-before-all file does not mention new maintenance filename")
    if OLD_NAME in tell_text:
        return fail("read-before-all file still mentions old maintenance filename")

    startup_zip = first_prompt_dir / "first_prompts_to_ai.zip"
    with zipfile.ZipFile(startup_zip, "r") as zf:
        names = set(zf.namelist())
        if NEW_NAME in names or OLD_NAME in names:
            return fail("maintenance file is inside first_prompts_to_ai.zip")
        if "00_START_HERE_FOR_AI.md" not in names:
            return fail("00_START_HERE_FOR_AI.md missing from startup ZIP")
        boot_text = zf.read("00_START_HERE_FOR_AI.md").decode("utf-8", errors="replace")
        if NEW_NAME not in boot_text:
            return fail("startup boot file does not mention new maintenance filename")
        if OLD_NAME in boot_text:
            return fail("startup boot file still mentions old maintenance filename")

    prompt_library_zip = first_prompt_dir / "prompt_library.zip"
    if zip_contains_text(prompt_library_zip, OLD_NAME):
        return fail("prompt_library.zip still contains old maintenance filename")
    if not zip_contains_text(prompt_library_zip, NEW_NAME):
        return fail("prompt_library.zip does not contain new maintenance filename")

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
