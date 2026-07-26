"""Validate external freeze-root cleanup and startup AI awareness.

This regression test is intentionally local and offline. It verifies that stale
in-source freeze-memory paths are removed from active prompt/startup surfaces,
that runtime helpers resolve new freeze state to the external show-project root,
and that Create First Prompt Files inserts the active freeze context into the
startup ZIP.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path, PureWindowsPath


FEATURE_ID = "freeze-after-update-external-root-cleanup-v1"
VALIDATION_MARKER = "VALIDATION OK: " + FEATURE_ID
STATUS_MARKER = "STATUS: IN_SYNC"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_INSERTION = PROJECT_ROOT / (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "07_prompt_authoring_and_audit/"
    "prompt_insertion_and_router_registration_protocol.md"
)
FREEZE_INTAKE_PROTOCOL = PROJECT_ROOT / (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/"
    "freeze_code_intake_and_form_protocol.md"
)
STARTUP_FREEZE_CONTEXT = PROJECT_ROOT / "kanda_prompt_workspace/prompt_tools/startup_freeze_context.py"
SYNC_TOOL = PROJECT_ROOT / "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
NO_ISOLATED_UPDATE_SCRIPT = PROJECT_ROOT / "scripts/update_no_isolated_zip_freeze_hint_after_validation.py"
PROJECT_PATH_HELPERS = PROJECT_ROOT / "kanda_reasoner_app/project_analysis_evidence_paths.py"

OLD_HARDCODED_WINDOWS = "E:\\kanda_reasoner\\project_freeze_after_update\\frozen_features_memory"
OLD_HARDCODED_POSIX = "E:/kanda_reasoner/project_freeze_after_update/frozen_features_memory"
OLD_ACTIVE_ROOT_PLACEHOLDER = "<active_project_root>/project_freeze_after_update/frozen_features_memory/"
DYNAMIC_FREEZE_MEMORY = (
    "<project_drive>/<project_name>_show_project_to_AI/"
    "project_freeze_after_update/frozen_features_memory/"
)
DYNAMIC_FREEZE_MEMORY_BACKSLASH = (
    "<project_drive>\\<project_name>_show_project_to_AI\\"
    "project_freeze_after_update\\frozen_features_memory"
)


def read_text(path: Path) -> str:
    """Read UTF-8 text with explicit replacement."""
    return path.read_text(encoding="utf-8", errors="replace")


def require(condition: bool, message: str) -> None:
    """Raise AssertionError with a clear message when condition is false."""
    if not condition:
        raise AssertionError(message)


def import_module_from_path(name: str, path: Path):
    """Import a Python module from an exact file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load module spec for " + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def expected_show_project_root_for_selected_project(project_root: Path) -> Path:
    """Return the expected external support root for a selected project root."""
    root = project_root.expanduser().resolve(strict=False)
    folder_name = root.name + "_show_project_to_AI"
    if root.drive:
        return Path(root.anchor) / folder_name
    return root.parent / folder_name


def expected_freeze_root_for_selected_project(project_root: Path) -> Path:
    """Return the expected external project_freeze_after_update root."""
    return expected_show_project_root_for_selected_project(project_root) / "project_freeze_after_update"


def expected_freeze_memory_for_selected_project(project_root: Path) -> Path:
    """Return the expected external frozen_features_memory root."""
    return expected_freeze_root_for_selected_project(project_root) / "frozen_features_memory"



def normalize_path_text(value: object) -> str:
    """Normalize a path-like manifest value for cross-platform comparison."""
    text = str(value or "").strip().replace("\\", "/")
    if len(text) >= 3 and text[1] == ":" and text[2] == "/":
        return PureWindowsPath(text).as_posix().rstrip("/")
    return text.rstrip("/")

def test_prompt_surfaces() -> None:
    """Validate prompt-library path cleanup."""
    prompt_text = read_text(PROMPT_INSERTION)
    require(
        DYNAMIC_FREEZE_MEMORY_BACKSLASH in prompt_text,
        "prompt insertion protocol does not use the dynamic external freeze path",
    )
    require(
        OLD_HARDCODED_WINDOWS not in prompt_text,
        "prompt insertion protocol still contains the old hardcoded KANDA freeze path",
    )

    freeze_text = read_text(FREEZE_INTAKE_PROTOCOL)
    require(
        "<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/freeze_hint_intake" in freeze_text,
        "freeze intake protocol is missing external freeze_hint_intake path",
    )
    require(
        "<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/frozen_features_memory" in freeze_text,
        "freeze intake protocol is missing external frozen_features_memory path",
    )
    require(
        "_show_project_to_AI/<project>_show_project_to_AI" not in freeze_text,
        "freeze intake protocol still contains duplicated show_project_to_AI path",
    )


def test_runtime_path_helpers() -> None:
    """Validate runtime helpers route new freeze state to external root."""
    helpers = import_module_from_path("project_analysis_evidence_paths_under_test", PROJECT_PATH_HELPERS)
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_path_test_") as tmp:
        selected_project = Path(tmp) / "kanda_reasoner"
        selected_project.mkdir()
        freeze_root = helpers.analysis_project_freeze_after_update_dir(selected_project)
        legacy_root = helpers.legacy_project_freeze_after_update_dir(selected_project)
        expected = expected_freeze_root_for_selected_project(selected_project)
        require(
            freeze_root == expected,
            "external freeze root resolver returned the wrong folder: "
            + str(freeze_root)
            + " != "
            + str(expected),
        )
        require(legacy_root == selected_project / "project_freeze_after_update", "legacy root resolver changed unexpectedly")
        require(freeze_root != legacy_root, "external and legacy freeze roots must remain separate")

    update_script_text = read_text(NO_ISOLATED_UPDATE_SCRIPT)
    require(
        "analysis_project_freeze_after_update_dir" in update_script_text,
        "validation-evidence updater must use external freeze-root resolver",
    )
    require(
        'project_root / "project_freeze_after_update"' not in update_script_text,
        "validation-evidence updater still writes directly under selected project root",
    )


def test_startup_freeze_context_builder() -> None:
    """Validate generated active freeze context text."""
    module = import_module_from_path("startup_freeze_context_under_test", STARTUP_FREEZE_CONTEXT)
    with tempfile.TemporaryDirectory(prefix="kanda_startup_context_test_") as tmp:
        selected_project = Path(tmp) / "kanda_reasoner"
        selected_project.mkdir()
        name, payload, record = module.build_active_project_freeze_context(
            workspace_root=PROJECT_ROOT / "kanda_prompt_workspace",
            active_project_root=selected_project,
            generated_at="2026-06-27T00:00:00Z",
        )
        text = payload.decode("utf-8")
        expected_source = expected_freeze_memory_for_selected_project(selected_project).as_posix()
        require(name == "09_active_project_freeze_context.md", "wrong freeze context filename")
        require("First-prompt delivery certification" in text, "freeze context lacks delivery certification")
        require("Create First Prompt Files must insert this file into first_prompts_to_ai.zip" in text, "freeze context lacks ZIP insertion rule")
        require("Runtime source is completely correct" in text, "freeze context lacks runtime correctness certification")
        require(DYNAMIC_FREEZE_MEMORY in text, "freeze context lacks dynamic external source-of-truth phrase")
        require(expected_source in text, "freeze context does not expose the selected external freeze source")
        require(OLD_ACTIVE_ROOT_PLACEHOLDER not in text, "freeze context still has stale active_project_root path")
        require(OLD_HARDCODED_WINDOWS not in text, "freeze context still has old Windows hardcoded path")
        require(OLD_HARDCODED_POSIX not in text, "freeze context still has old POSIX hardcoded path")
        require(record.get("generated_filename") == name, "manifest record does not name the freeze context file")
        resolved_source = normalize_path_text(record.get("resolved_source"))
        expected_record_source = normalize_path_text(expected_source)
        require(
            resolved_source == expected_record_source,
            "manifest record resolved_source is not external freeze memory: "
            + resolved_source
            + " != "
            + expected_record_source,
        )


def test_create_first_prompt_files_zip_awareness() -> None:
    """Validate startup ZIP contract inserts freeze context for AI awareness."""
    sys.path.insert(0, str(PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"))
    try:
        sync_tool = import_module_from_path("sync_startup_routing_kernel_pack_under_test", SYNC_TOOL)
        with tempfile.TemporaryDirectory(prefix="kanda_first_prompts_test_") as tmp:
            tmp_root = Path(tmp)
            selected_project = tmp_root / "kanda_reasoner"
            selected_project.mkdir()
            output_dir = tmp_root / "kanda_reasoner_show_project_to_AI" / "first_prompt_files"
            code, zip_path = sync_tool.make_zip(
                PROJECT_ROOT / "kanda_prompt_workspace",
                output_dir,
                selected_project,
                dry_run=False,
            )
            require(code == 0, "startup ZIP generation failed")
            require(zip_path is not None and zip_path.exists(), "startup ZIP was not created")
            with zipfile.ZipFile(zip_path, "r") as archive:
                names = set(archive.namelist())
                require("09_active_project_freeze_context.md" in names, "startup ZIP lacks active freeze context")
                require("STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json" in names, "startup ZIP lacks manifest")
                freeze_text = archive.read("09_active_project_freeze_context.md").decode("utf-8")
                manifest_text = archive.read("STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json").decode("utf-8")
            require("First-prompt delivery certification" in freeze_text, "ZIP freeze context lacks certification")
            require("Runtime source is completely correct" in freeze_text, "ZIP freeze context lacks runtime correctness certification")
            require(DYNAMIC_FREEZE_MEMORY in freeze_text, "ZIP freeze context lacks dynamic external source-of-truth path")
            require(OLD_ACTIVE_ROOT_PLACEHOLDER not in freeze_text, "ZIP freeze context contains stale active root placeholder")
            require("active_project_freeze_context" in manifest_text, "manifest lacks active_project_freeze_context record")
            require("kanda_reasoner_show_project_to_AI/project_freeze_after_update/frozen_features_memory" in manifest_text, "manifest does not expose external freeze memory source")
    finally:
        try:
            sys.path.remove(str(PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"))
        except ValueError:
            pass


def main() -> int:
    """Run all local regression checks."""
    test_prompt_surfaces()
    test_runtime_path_helpers()
    test_startup_freeze_context_builder()
    test_create_first_prompt_files_zip_awareness()
    print(VALIDATION_MARKER)
    print(STATUS_MARKER)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
