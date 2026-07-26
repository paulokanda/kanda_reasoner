from __future__ import annotations

import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ACTIVE_PROMPT_FILES = [
    PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "ai_prompt_request_canon.md",
    PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "daily_patch_delivery_guardrails.md",
    PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "kanda_routing_system_canon.md",
    PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md",
    PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "07_prompt_authoring_and_audit" / "prompt_identity_code_registry_canon.md",
    PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "07_prompt_authoring_and_audit" / "prompt_insertion_and_router_registration_protocol.md",
]

README_FILE = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "README_kanda_startup_prompt_request_kernel_generator.md"

STARTUP_ZIP_LIVE_FILES = {
    "01_ai_prompt_request_canon.md",
    "02_prompt_navigation_index.md",
    "07_daily_patch_delivery_guardrails.md",
}


def _show_project_first_prompt_dir(project_root: Path) -> Path:
    root = project_root.resolve(strict=False)
    anchor = root.anchor or str(root.parent)
    slug = root.name.strip().lower() or "project"
    if anchor.endswith(":\\") or anchor.endswith(":/"):
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    elif anchor.endswith(":"):
        base = Path(f"{anchor}\\{slug}_show_project_to_AI")
    else:
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    return base / "first_prompt_files"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_active_prompt_sources_use_first_prompt_files_not_first_ai_deliver() -> None:
    for path in ACTIVE_PROMPT_FILES:
        text = _read_text(path)
        assert "first_AI_deliver" not in text, path
        assert "first_prompt_files" in text, path


def test_startup_generator_readme_has_no_stale_first_ai_deliver_reference() -> None:
    text = _read_text(README_FILE)
    assert "first_AI_deliver" not in text
    assert "first_prompt_files" in text


def test_sync_generator_only_keeps_legacy_first_ai_deliver_internal_marker() -> None:
    path = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    lines = _read_text(path).splitlines()
    stale = [line for line in lines if "first_AI_deliver" in line]
    assert stale == [
        "  (legacy kanda_prompt_workspace/first_AI_deliver is deprecated for normal generated startup delivery.)",
        'LEGACY_DELIVER_DIR_NAME = "first_AI_deliver"',
    ]


def test_generated_first_prompt_zip_if_present_has_no_live_stale_references() -> None:
    zip_path = _show_project_first_prompt_dir(PROJECT_ROOT) / "first_prompts_to_ai.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as zf:
        for name in STARTUP_ZIP_LIVE_FILES:
            text = zf.read(name).decode("utf-8")
            assert "first_AI_deliver" not in text, name
            assert "first_prompt_files" in text, name


def test_generated_prompt_library_zip_if_present_has_no_active_stale_references() -> None:
    zip_path = _show_project_first_prompt_dir(PROJECT_ROOT) / "prompt_library.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if not name.startswith("ACTIVE_PROMPTS/") or name.endswith("/"):
                continue
            try:
                text = zf.read(name).decode("utf-8")
            except UnicodeDecodeError:
                continue
            assert "first_AI_deliver" not in text, name


if __name__ == "__main__":
    test_active_prompt_sources_use_first_prompt_files_not_first_ai_deliver()
    test_startup_generator_readme_has_no_stale_first_ai_deliver_reference()
    test_sync_generator_only_keeps_legacy_first_ai_deliver_internal_marker()
    test_generated_first_prompt_zip_if_present_has_no_live_stale_references()
    test_generated_prompt_library_zip_if_present_has_no_active_stale_references()
    print("VALIDATION OK: show_project_to_ai_startup_reference_cleanup_v1")
    print("VALIDATION OK: show project to AI startup reference cleanup")
