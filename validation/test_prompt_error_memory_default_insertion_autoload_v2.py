from __future__ import annotations

from pathlib import Path
import json
import sys

FEATURE_ID = "prompt-error-memory-default-insertion-autoload-v2"
MARKERS = {
    "error": "<!-- KANDA_ADDENDUM:error_memory_default_autoload_insertion:v2 -->",
    "bundle": "<!-- KANDA_ADDENDUM:error_memory_default_autoload_patch_delivery:v2 -->",
    "router": "<!-- KANDA_ROUTE:error_memory_default_autoload_insertion:v2 -->",
    "nav": "<!-- KANDA_NAV:error_memory_default_autoload_insertion:v2 -->",
    "folder": "<!-- KANDA_FOLDER_TRIGGER:error_memory_default_autoload_insertion:v2 -->",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_contains(text: str, needle: str, label: str) -> None:
    require(needle in text, f"Missing {label}: {needle}")


def require_marker_once(path: Path, marker: str) -> str:
    text = read_text(path)
    count = text.count(marker)
    require(count == 1, f"Marker count for {path} must be exactly 1, got {count}")
    return text


def main() -> None:
    if len(sys.argv) >= 2:
        project_root = Path(sys.argv[1]).resolve()
    else:
        project_root = Path(r"E:\kanda_reasoner").resolve()

    prompt_root = project_root / "kanda_prompt_workspace" / "prompt_library"
    require(prompt_root.exists(), f"Prompt library root not found: {prompt_root}")
    require("show_project_to_AI" not in str(prompt_root), "Validation is pointed at exported AI copy, not original prompt library")

    files = {
        "error": prompt_root / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "error_memory_ai_formulary_startup_canon.md",
        "bundle": prompt_root / "ACTIVE_PROMPTS" / "05_patch_delivery_and_validation" / "bundle_gated_development_workflow.md",
        "router": prompt_root / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_router.md",
        "nav": prompt_root / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md",
        "folder": prompt_root / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "_FOLDER_ASSIMILATION.md",
        "error_meta": prompt_root / "METADATA" / "error_memory_ai_formulary_startup_canon.meta.json",
        "bundle_meta": prompt_root / "METADATA" / "bundle_gated_development_workflow.meta.json",
        "router_meta": prompt_root / "METADATA" / "prompt_router.meta.json",
        "nav_meta": prompt_root / "METADATA" / "prompt_navigation_index.meta.json",
    }
    for key, path in files.items():
        require(path.exists(), f"Missing expected file {key}: {path}")

    error_text = require_marker_once(files["error"], MARKERS["error"])
    bundle_text = require_marker_once(files["bundle"], MARKERS["bundle"])
    router_text = require_marker_once(files["router"], MARKERS["router"])
    nav_text = require_marker_once(files["nav"], MARKERS["nav"])
    folder_text = require_marker_once(files["folder"], MARKERS["folder"])

    for text, label in [
        (error_text, "error canon"),
        (bundle_text, "bundle workflow"),
        (router_text, "router"),
        (nav_text, "navigation"),
        (folder_text, "folder assimilation"),
    ]:
        require_contains(text, "<drive>", label)
        require("_show_project_to_AI" in text and ("<project" in text), f"Missing {label}: dynamic project Show Project folder token")
        require_contains(text, "project_error_memory", label)

    require_contains(error_text, "AI-assisted error lesson intake = populated first", "default intake target")
    require_contains(error_text, "Error Editor = populated second", "default editor target")
    require_contains(error_text, "Lessons = unchanged until", "no direct lesson save")
    require_contains(error_text, "Direct Error Lesson ZIP", "manual import alternative")
    require_contains(error_text, "Copy error/draft to AI", "clipboard alternative")
    require_contains(error_text, "Paste error formatted from AI", "clipboard receive alternative")
    require_contains(error_text, "lazy tab host", "host trigger requirement")
    require_contains(error_text, "validate the GUI load path and lazy-host trigger", "validation guard")

    require_contains(bundle_text, "zip install validate", "default patch/staging route")
    require_contains(bundle_text, "validation must check py_compile", "validation detail")
    require_contains(bundle_text, "Direct Error Lesson ZIP is manual import only", "manual import boundary")

    require_contains(router_text, "zip, install, validate, error appears in AI-assisted error lesson intake", "router trigger")
    require_contains(router_text, "Do not route this as Direct Error Lesson ZIP", "router boundary")
    require_contains(router_text, "Default output shape", "router output shape")

    require_contains(nav_text, "ZIP -> install -> validate -> populate EM tab", "navigation default")
    require_contains(nav_text, "Use Direct Error Lesson ZIP only", "navigation boundary")

    require_contains(folder_text, "Mode 1 default", "folder mode 1")
    require_contains(folder_text, "Mode 2 explicit", "folder mode 2")
    require_contains(folder_text, "Mode 3 clipboard", "folder mode 3")

    metadata_checks = {
        "error_meta": ["default Error Memory insertion", "Copy error/draft to AI", "Paste error formatted from AI"],
        "bundle_meta": ["pending AI-assisted error lesson intake", "zip install validate populate EM tab"],
        "router_meta": ["error must appear in AI-assisted error lesson intake"],
        "nav_meta": ["Error Memory default insertion autoload", "Direct Error Lesson ZIP"],
    }
    for key, needles in metadata_checks.items():
        data = json.loads(read_text(files[key]))
        flat = json.dumps(data, ensure_ascii=True)
        for needle in needles:
            require_contains(flat, needle, key)

    print("VALIDATION OK: prompt-error-memory-default-insertion-autoload-v2")
    print("STATUS: ORIGINAL_PROMPT_LIBRARY_UPDATED")
    print("Checked:")
    print("- default ZIP -> install -> validate -> populate EM tab canon")
    print("- dynamic <drive>\\<project>_show_project_to_AI\\project_error_memory path rule")
    print("- Direct Error Lesson ZIP remains explicit manual-import alternative")
    print("- Copy error/draft to AI and Paste error formatted from AI remain clipboard/formatted-text alternative")
    print("- router/navigation/folder assimilation/metadata expose the behavior")


if __name__ == "__main__":
    main()
