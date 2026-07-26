from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT_MARKER = "<!-- KANDA_ADDENDUM:prompt_error_lesson_zip_direct_import_canon:v1 -->"
ROUTER_MARKER = "<!-- KANDA_ROUTE:error_memory_direct_error_lesson_zip:v1 -->"
NAV_MARKER = "<!-- KANDA_NAV:error_memory_direct_error_lesson_zip:v1 -->"
FOLDER_MARKER = "<!-- KANDA_FOLDER_TRIGGER:error_memory_direct_error_lesson_zip:v1 -->"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def assert_once(text: str, marker: str, label: str) -> None:
    count = text.count(marker)
    if count != 1:
        raise AssertionError(f"{label} marker count is {count}; expected 1")


def get_project_root() -> Path:
    if len(sys.argv) >= 2:
        return Path(sys.argv[1]).resolve()
    return Path(r"E:\kanda_reasoner").resolve()


def main() -> None:
    project_root = get_project_root()
    prompt_root = project_root / "kanda_prompt_workspace" / "prompt_library"
    if not prompt_root.exists():
        raise FileNotFoundError(str(prompt_root))
    prompt_root_text = str(prompt_root)
    if "show_project_to_AI" in prompt_root_text or "first_prompt_files" in prompt_root_text or "second_prompt_files" in prompt_root_text:
        raise RuntimeError("Validation path is an exported AI copy, not original prompt library.")

    error_canon = prompt_root / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "error_memory_ai_formulary_startup_canon.md"
    router = prompt_root / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_router.md"
    nav = prompt_root / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
    folder = prompt_root / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "_FOLDER_ASSIMILATION.md"
    error_meta = prompt_root / "METADATA" / "error_memory_ai_formulary_startup_canon.meta.json"
    router_meta = prompt_root / "METADATA" / "prompt_router.meta.json"
    nav_meta = prompt_root / "METADATA" / "prompt_navigation_index.meta.json"

    error_text = read_text(error_canon)
    router_text = read_text(router)
    nav_text = read_text(nav)
    folder_text = read_text(folder)

    assert_once(error_text, ROOT_MARKER, "error memory canon")
    assert_once(router_text, ROUTER_MARKER, "router")
    assert_once(nav_text, NAV_MARKER, "navigation index")
    assert_once(folder_text, FOLDER_MARKER, "folder assimilation")

    for text, label in [(error_text, "error memory canon"), (router_text, "router"), (nav_text, "navigation index")]:
        assert_contains(text, "bundle_manifest.json", label)
        assert_contains(text, "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_", label)
        assert_contains(text, "payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_", label)
        assert_contains(text, "patch ZIP -> install -> validate", label)
        assert_contains(text, "Direct Error Lesson ZIP", label)

    assert_contains(error_text, "If the user says only `send/gimme Error Lesson ZIP`", "direct fast path rule")
    assert_contains(router_text, "Do not use kanda_bundle_gated_development_workflow as the primary route unless project/source code is being changed.", "router direct-vs-patch rule")
    assert_contains(nav_text, "Fast Path when only packaging the formatted Error Lesson ZIP", "navigation fast path rule")
    assert_contains(folder_text, "Direct Error Lesson ZIP packages are not code patches", "folder boundary rule")

    error_meta_data = json.loads(read_text(error_meta))
    router_meta_data = json.loads(read_text(router_meta))
    nav_meta_data = json.loads(read_text(nav_meta))
    for data, label in [(error_meta_data, "error meta"), (router_meta_data, "router meta"), (nav_meta_data, "nav meta")]:
        if "Error Lesson ZIP" not in data.get("trigger_phrases", []):
            raise AssertionError(f"{label} missing Error Lesson ZIP trigger")
    if "error_memory_ai_formulary_startup_canon" not in router_meta_data.get("required_companion_prompts", []):
        raise AssertionError("router metadata missing Error Memory canon companion")

    print("VALIDATION OK: prompt-error-lesson-zip-router-canon-v1")
    print("STATUS: ORIGINAL_PROMPT_LIBRARY_UPDATED")
    print("Checked Direct Error Lesson ZIP route and default patch ZIP install/validate reminder.")


if __name__ == "__main__":
    main()
