#!/usr/bin/env python3
"""Validate mandatory Error Memory owner-canon routing guard v2.

This script is intentionally standard Python 3.10+ and uses only the standard
library so it can run in Windows/PyCharm without external dependencies.
"""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "error-memory-event-mandatory-router-guard-v2"
EXPECTED_MARKER = "VALIDATION OK: " + FEATURE_ID
EXPECTED_SYNC_STATUS = "STATUS: IN_SYNC"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_file(path: Path) -> None:
    require(path.is_file(), "Missing required file: " + str(path))


def require_contains(text: str, needle: str, label: str) -> None:
    require(needle in text, label + " is missing required text: " + needle)


def run_checked(command: list[str], cwd: Path) -> str:
    result = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = result.stdout or ""
    if result.returncode != 0:
        raise AssertionError(
            "Command failed with code " + str(result.returncode) + ": " + " ".join(command) + "\n" + output
        )
    return output


def validate_sources(project_root: Path) -> None:
    canon_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "error_memory_ai_formulary_startup_canon.md"
    router_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_router.md"
    nav_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
    daily_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "daily_patch_delivery_guardrails.md"
    pir_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "patch_install_delivery_error_register.md"
    meta_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "METADATA" / "error_memory_ai_formulary_startup_canon.meta.json"
    source_map_path = project_root / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
    folder_index_path = project_root / "kanda_prompt_workspace" / "prompt_library" / "ROUTING" / "FOLDER_ASSIMILATION_CARDS_INDEX.md"
    freeze_context_path = project_root / "kanda_prompt_workspace" / "prompt_tools" / "startup_freeze_context.py"

    for path in [canon_path, router_path, nav_path, daily_path, pir_path, meta_path, source_map_path, folder_index_path, freeze_context_path]:
        require_file(path)

    canon = read_text(canon_path)
    router = read_text(router_path)
    nav = read_text(nav_path)
    daily = read_text(daily_path)
    pir = read_text(pir_path)
    freeze_context = read_text(freeze_context_path)
    meta = json.loads(read_text(meta_path))
    source_map = json.loads(read_text(source_map_path))

    require_contains(canon, "KANDA_CANON:error_event_owner_box_intake_gate:v2", "owner canon")
    require_contains(canon, "This prompt is the owner canon", "owner canon")
    require_contains(canon, "Installers must not write directly into Lessons", "owner canon")
    require_contains(canon, "pending_ai_assisted_error_lesson_intake", "owner canon")
    require_contains(canon, "A task that began with an error event is not closed by code validation alone", "owner canon")

    require_contains(router, "KANDA_ROUTE:error_event_to_error_memory_owner_canon:v2", "router")
    require_contains(router, "Do not duplicate the full Error Memory doctrine in this router", "router")
    require_contains(router, "derived from `$PROJECT_ROOT`", "router")

    require_contains(nav, "KANDA_NAV:error_event_to_error_memory_owner_canon:v2", "navigation")
    require_contains(nav, "Router/navigation prompts must point to this owner canon", "navigation")

    require_contains(daily, "KANDA_GUARDRAIL:error_event_owner_canon_pointer:v2", "daily guardrail")
    require_contains(pir, "PIR-004 - Error-triggered repair delivered without owner-canon Error Memory intake", "PIR")
    require_contains(freeze_context, "generated exposure copy", "startup freeze context fallback")

    require(meta.get("source_stage") == "error_memory_ai_formulary_startup_canon_v1_2", "Metadata source_stage was not updated")
    require("error-triggered repair" in meta.get("trigger_phrases", []), "Metadata trigger phrase missing")
    require(meta.get("box_logic_required") is True, "Metadata must preserve box_logic_required true")

    startup_sources = source_map.get("startup_sources", [])
    matching = [item for item in startup_sources if item.get("prompt_id") == "error_memory_ai_formulary_startup_canon"]
    require(len(matching) == 1, "Startup source map must contain exactly one Error Memory canon entry")
    require(matching[0].get("generated_filename") == "12_error_memory_ai_formulary_startup_canon.md", "Error Memory generated filename changed unexpectedly")


def validate_error_memory_staging(project_root: Path) -> None:
    drive_root = Path(project_root.anchor)
    show_root = drive_root / (project_root.name + "_show_project_to_AI")
    pending_dir = show_root / "project_error_memory" / "pending_ai_assisted_error_lesson_intake"
    lesson_path = pending_dir / "KANDA_ERROR_LESSON_JSON_error_memory_event_mandatory_router_guard_v2.txt"
    require_file(lesson_path)
    text = read_text(lesson_path)
    require_contains(text, "KANDA_ERROR_LESSON_JSON_BEGIN", "staged Error Memory lesson")
    require_contains(text, "KANDA_ERROR_LESSON_JSON_END", "staged Error Memory lesson")
    body = text.split("KANDA_ERROR_LESSON_JSON_BEGIN", 1)[1].split("KANDA_ERROR_LESSON_JSON_END", 1)[0].strip()
    lesson = json.loads(body)
    require(lesson.get("operation_phase") == "prompt-routing", "Lesson operation_phase must be prompt-routing")
    require("owner canon" in lesson.get("root_cause", ""), "Lesson root cause must mention owner canon")
    require("pending_ai_assisted_error_lesson_intake" in lesson.get("correct_fix", ""), "Lesson correct_fix must mention pending intake")


def validate_generated_artifacts(project_root: Path) -> None:
    workspace = project_root / "kanda_prompt_workspace"
    sync_script = workspace / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    require_file(sync_script)
    output = run_checked([sys.executable, str(sync_script), "--ensure-sync", "--yes"], cwd=project_root)
    if "ENSURE SYNC RESULT: ALREADY_IN_SYNC" not in output and "ENSURE SYNC RESULT: IN_SYNC_AFTER_SYNC" not in output:
        raise AssertionError("Startup sync did not report an in-sync result.\n" + output)

    drive_root = Path(project_root.anchor)
    first_prompt_dir = drive_root / (project_root.name + "_show_project_to_AI") / "first_prompt_files"
    startup_zip = first_prompt_dir / "first_prompts_to_ai.zip"
    prompt_library_zip = first_prompt_dir / "prompt_library.zip"
    require_file(startup_zip)
    require_file(prompt_library_zip)

    with zipfile.ZipFile(startup_zip) as zf:
        names = set(zf.namelist())
        require("12_error_memory_ai_formulary_startup_canon.md" in names, "Startup ZIP missing generated Error Memory canon")
        text = zf.read("12_error_memory_ai_formulary_startup_canon.md").decode("utf-8-sig", errors="replace")
        require_contains(text, "KANDA_CANON:error_event_owner_box_intake_gate:v2", "startup ZIP Error Memory canon")

    with zipfile.ZipFile(prompt_library_zip) as zf:
        names = set(zf.namelist())
        member = "ACTIVE_PROMPTS/01_session_start_and_navigation/error_memory_ai_formulary_startup_canon.md"
        require(member in names, "Prompt library ZIP missing owner canon")
        text = zf.read(member).decode("utf-8-sig", errors="replace")
        require_contains(text, "KANDA_CANON:error_event_owner_box_intake_gate:v2", "prompt library ZIP Error Memory canon")


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    validate_sources(project_root)
    validate_error_memory_staging(project_root)
    validate_generated_artifacts(project_root)
    print(EXPECTED_MARKER)
    print(EXPECTED_SYNC_STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
