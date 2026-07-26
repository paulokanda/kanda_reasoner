"""Validate the startup Box Logic bridge.

This validation checks that the startup kernel carries only a compact bridge,
that the complete Box Architecture canon remains on-demand, and that startup
sync exposes the bridge in generated startup artifacts without loading the full
canon at session start.
"""

from __future__ import annotations

import zipfile
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

START_PATH = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "start_of_day_master_stack.md"
NAV_PATH = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
BOX_PATH = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "04_box_architecture_and_boundaries" / "box_architecture_canon.md"
SYNC_SCRIPT = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
DELIVERY_ROOT = PROJECT_ROOT.parent / (PROJECT_ROOT.name + "_show_project_to_AI") / "first_prompt_files"
STARTUP_ZIP = DELIVERY_ROOT / "first_prompts_to_ai.zip"
PROMPT_LIBRARY_ZIP = DELIVERY_ROOT / "prompt_library.zip"
READ_BEFORE_ALL = DELIVERY_ROOT / "tell_AI_read_before_all.md"

BRIDGE_REQUIRED_FRAGMENTS = [
    "## Box Logic Startup Bridge",
    "Identify the active box before implementation.",
    "State owner paths.",
    "State files allowed to change.",
    "State files explicitly out of scope.",
    "Declare cross-box touches before touching more than one box.",
    "Preserve public contracts and avoid private reach-in.",
    "Validate the active box and any touched external box.",
    "Do not proceed from memory when box ownership",
    "route to `box_architecture_canon.md` before doing the risky step",
    "Do not load the full Box Architecture prompt during normal startup unless the",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_contains_all(text: str, fragments: list[str], label: str) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise AssertionError(label + " missing fragments: " + "; ".join(missing))


def _assert_startup_bridge() -> None:
    text = _read(START_PATH)
    _assert_contains_all(text, BRIDGE_REQUIRED_FRAGMENTS, "start_of_day_master_stack.md")
    if text.count("## Box Logic Startup Bridge") != 1:
        raise AssertionError("Startup Box Logic bridge must appear exactly once.")
    if "## Code Module Size Bridge" not in text:
        raise AssertionError("Existing Code Module Size Bridge was lost.")

    tier0_block = text.split("### Tier 0 - Session kernel", 1)[1].split("### Tier 1 - Group routing", 1)[0]
    if "box_architecture_canon" in tier0_block:
        raise AssertionError("Full box_architecture_canon must not be loaded in Tier 0 startup.")


def _assert_box_canon_anchor() -> None:
    text = _read(BOX_PATH)
    _assert_contains_all(
        text,
        [
            "## First-Position Box Logic Requirement",
            "## Startup Bridge Canon",
            "The startup prompt may load only a compact Box Logic Startup Bridge",
            "remains on-demand for implementation",
        ],
        "box_architecture_canon.md",
    )


def _assert_navigation_bridge_rule() -> None:
    text = _read(NAV_PATH)
    _assert_contains_all(
        text,
        [
            "## Startup Box Logic bridge rule",
            "must not load the full Box Architecture canon at session start",
            "route to\n`box_architecture_canon.md` before the risky step",
        ],
        "prompt_navigation_index.md",
    )


def _run_startup_sync() -> None:
    if not SYNC_SCRIPT.exists():
        raise AssertionError("Startup sync script is missing: " + str(SYNC_SCRIPT))
    result = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT), "--sync", "--yes", "--workspace", str(PROJECT_ROOT / "kanda_prompt_workspace"), "--project-root", str(PROJECT_ROOT), "--output-dir", str(DELIVERY_ROOT)],
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError("Startup sync failed:\n" + result.stdout)
    if "STATUS: IN_SYNC" not in result.stdout:
        raise AssertionError("Startup sync did not report STATUS: IN_SYNC. Output:\n" + result.stdout)


def _assert_generated_artifacts() -> None:
    for path in (STARTUP_ZIP, PROMPT_LIBRARY_ZIP, READ_BEFORE_ALL):
        if not path.exists():
            raise AssertionError("Missing generated startup artifact: " + str(path))

    with zipfile.ZipFile(STARTUP_ZIP, "r") as archive:
        startup_names = set(archive.namelist())
        if "05_start_of_day_master_stack.md" not in startup_names:
            raise AssertionError("Generated startup ZIP is missing 05_start_of_day_master_stack.md")
        generated_start = archive.read("05_start_of_day_master_stack.md").decode("utf-8-sig", errors="replace")
        _assert_contains_all(generated_start, BRIDGE_REQUIRED_FRAGMENTS, "generated 05_start_of_day_master_stack.md")
        if "box_architecture_canon.md" in startup_names:
            raise AssertionError("Generated startup ZIP must not load full box_architecture_canon.md as a startup file.")

    with zipfile.ZipFile(PROMPT_LIBRARY_ZIP, "r") as archive:
        names = set(archive.namelist())
        box_members = [name for name in names if name.endswith("ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md")]
        if not box_members:
            raise AssertionError("Prompt library ZIP is missing the on-demand box_architecture_canon.md")
        box_text = archive.read(box_members[0]).decode("utf-8-sig", errors="replace")
        if "## Startup Bridge Canon" not in box_text:
            raise AssertionError("Prompt library box canon is missing Startup Bridge Canon anchor.")


def main() -> None:
    _assert_startup_bridge()
    _assert_box_canon_anchor()
    _assert_navigation_bridge_rule()
    _run_startup_sync()
    _assert_generated_artifacts()
    print("VALIDATION OK: startup-box-logic-bridge-v1")
    print("BOX_LOGIC_BRIDGE: startup enforcement active")
    print("BOX_LOGIC_FULL_PROMPT: on-demand only")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
