# project-path: tools/validate_project_ready_check_project_in_use_v1.py
"""Validate the PROJECT READY CHECK active-project display contract."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path, PurePosixPath


FEATURE_ID = "project-ready-check-active-project-display-v1"
PROJECT_IN_USE_TEMPLATE = "PROJECT IN USE: <ACTIVE PROJECT DISPLAY NAME>"
READY_TAIL = (
    "Next action:\n"
    + PROJECT_IN_USE_TEMPLATE
    + "\nWAIT_FOR_TASK"
)


class ValidationError(RuntimeError):
    """Raised when the focused contract validation fails."""


def require(condition: bool, message: str) -> None:
    """Raise a focused validation error when a condition is false."""
    if not condition:
        raise ValidationError(message)


def read_text(path: Path) -> str:
    """Read UTF-8 source text with explicit replacement handling."""
    return path.read_text(encoding="utf-8", errors="replace")


def load_startup_modules(project_root: Path) -> tuple[object, object, object]:
    """Load startup generator modules from the selected source snapshot."""
    tools_root = project_root / "kanda_prompt_workspace" / "prompt_tools"
    tools_text = str(tools_root)
    if tools_text not in sys.path:
        sys.path.insert(0, tools_text)

    names = importlib.import_module("startup_kernel.startup_names")
    start_here = importlib.import_module("startup_kernel.start_here_text")
    paste_readme = importlib.import_module("startup_kernel.paste_readme_text")
    return names, start_here, paste_readme


def validate_canonical_prompt(project_root: Path) -> None:
    """Validate the canonical Class 01 prompt owns the new output rule."""
    prompt_path = (
        project_root
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "ACTIVE_PROMPTS"
        / "01_session_start_and_navigation"
        / "session_start_upload_checklist.md"
    )
    text = read_text(prompt_path)
    require(PROJECT_IN_USE_TEMPLATE in text, "CANONICAL_PROMPT_TEMPLATE_MISSING")
    require(READY_TAIL in text, "CANONICAL_PROMPT_READY_TAIL_ORDER_INVALID")
    require(
        "Replace underscores with spaces and convert" in text,
        "CANONICAL_PROMPT_NORMALIZATION_RULE_MISSING",
    )
    require(
        "not from the KANDA Tool name" in text,
        "CANONICAL_PROMPT_TOOL_NAME_GUARD_MISSING",
    )
    require(
        "`my_project` becomes `MY PROJECT`" in text,
        "CANONICAL_PROMPT_EXAMPLE_MISSING",
    )
    print("CANONICAL_PROJECT_READY_PROMPT: PASS")



def validate_prompt_metadata(project_root: Path) -> None:
    """Validate source and metadata identity for the updated prompt."""
    import json

    metadata_path = (
        project_root
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "METADATA"
        / "session_start_upload_checklist.meta.json"
    )
    data = json.loads(read_text(metadata_path))
    require(data.get("prompt_id") == "session_start_upload_checklist", "PROMPT_METADATA_ID_INVALID")
    require(data.get("version") == "2.1", "PROMPT_METADATA_VERSION_INVALID")
    require(
        data.get("source_stage") == FEATURE_ID,
        "PROMPT_METADATA_SOURCE_STAGE_INVALID",
    )
    require(
        data.get("updated_for") == FEATURE_ID,
        "PROMPT_METADATA_UPDATED_FOR_INVALID",
    )
    print("PROJECT_READY_PROMPT_METADATA: PASS")

def validate_constants(names: object) -> None:
    """Validate the public startup constants and required-field order."""
    template = getattr(names, "PROJECT_IN_USE_TEMPLATE", "")
    fields = tuple(getattr(names, "PROJECT_READY_CHECK_REQUIRED_FIELDS", ()))
    require(template == PROJECT_IN_USE_TEMPLATE, "PROJECT_IN_USE_TEMPLATE_INVALID")
    require("Next action:" in fields, "NEXT_ACTION_FIELD_MISSING")
    require("PROJECT IN USE:" in fields, "PROJECT_IN_USE_FIELD_MISSING")
    require(
        fields.index("PROJECT IN USE:") == fields.index("Next action:") + 1,
        "PROJECT_IN_USE_FIELD_ORDER_INVALID",
    )
    print("PROJECT_READY_CONSTANTS: PASS")


def validate_generated_text(start_here: object, paste_readme: object) -> None:
    """Generate current artifacts and verify the exact readiness tail."""
    make_start_here_file = getattr(start_here, "make_start_here_file")
    make_paste_after_uploading_file = getattr(
        paste_readme,
        "make_paste_after_uploading_file",
    )
    make_readme = getattr(paste_readme, "make_readme")

    expected = ["01_ai_prompt_request_canon.md"]
    _start_name, start_text = make_start_here_file(
        "2026-07-30",
        "2026-07-30T00:00:00Z",
        expected,
    )
    _filename, paste_text = make_paste_after_uploading_file(
        "2026-07-30",
        "2026-07-30T00:00:00Z",
        "first_prompts_to_ai.zip",
        expected,
    )
    readme_text = make_readme(
        "2026-07-30",
        "2026-07-30T00:00:00Z",
        "first_prompts_to_ai.zip",
        [{"generated_filename": expected[0], "role": "test"}],
        "tell_AI_read_before_all.md",
    )

    for label, text in (
        ("START_HERE", start_text),
        ("TELL_AI", paste_text),
    ):
        require(READY_TAIL in text, label + "_READY_TAIL_ORDER_INVALID")
        require(
            "selected active Project name or slug" in text,
            label + "_ACTIVE_PROJECT_SOURCE_RULE_MISSING",
        )
        require(
            "not from the KANDA Tool name" in text
            or "never from the KANDA Tool name" in text,
            label + "_TOOL_NAME_GUARD_MISSING",
        )
        require(
            "`my_project` becomes `MY PROJECT`" in text,
            label + "_NORMALIZATION_EXAMPLE_MISSING",
        )
        require(
            "PROJECT IN USE: KANDA REASONER\nWAIT_FOR_TASK" not in text,
            label + "_HARDCODED_TOOL_PROJECT_NAME_FOUND",
        )

    require(
        PROJECT_IN_USE_TEMPLATE in readme_text,
        "README_PROJECT_IN_USE_TEMPLATE_MISSING",
    )
    require("WAIT_FOR_TASK" in readme_text, "README_READY_TOKEN_MISSING")
    print("GENERATED_PROJECT_READY_TEXT: PASS")



def validate_generated_delivery(delivery_dir: Path | None) -> None:
    """Validate regenerated first-prompt artifacts when a directory is supplied."""
    if delivery_dir is None:
        print("GENERATED_DELIVERY_ARTIFACTS: NOT_REQUESTED")
        return

    import zipfile

    tell_path = delivery_dir / "tell_AI_read_before_all.md"
    startup_zip = delivery_dir / "first_prompts_to_ai.zip"
    require(tell_path.is_file(), "GENERATED_TELL_AI_FILE_MISSING")
    require(startup_zip.is_file(), "GENERATED_STARTUP_ZIP_MISSING")
    tell_text = read_text(tell_path)
    require(READY_TAIL in tell_text, "GENERATED_TELL_AI_READY_TAIL_INVALID")

    with zipfile.ZipFile(startup_zip, "r") as archive:
        start_text = archive.read("00_START_HERE_FOR_AI.md").decode(
            "utf-8",
            errors="replace",
        )
        checklist_text = archive.read(
            "06_session_start_upload_checklist.md"
        ).decode("utf-8", errors="replace")

    require(READY_TAIL in start_text, "GENERATED_START_HERE_READY_TAIL_INVALID")
    require(READY_TAIL in checklist_text, "GENERATED_CHECKLIST_READY_TAIL_INVALID")
    print("GENERATED_DELIVERY_ARTIFACTS: PASS")


def validate_patch_package(project_root: Path, patch_zip: Path | None) -> None:
    """Validate the exact final patch ZIP when one is supplied."""
    if patch_zip is None:
        print("PATCH_PACKAGE_CONTRACT: NOT_REQUESTED")
        return

    import zipfile

    project_text = str(project_root)
    if project_text not in sys.path:
        sys.path.insert(0, project_text)
    from kanda_reasoner_app.patch_governance.validator import (
        validate_install_script_text,
        validate_patch_zip,
    )

    report = validate_patch_zip(patch_zip, expect_freeze_hint=True)
    require(report.get("ok") is True, "PATCH_ZIP_CONTRACT_FAILED")
    with zipfile.ZipFile(patch_zip, "r") as archive:
        install_text = archive.read("INSTALL.ps1").decode(
            "ascii",
            errors="strict",
        )
    install_report = validate_install_script_text(install_text)
    require(
        install_report.get("ok") is True,
        "INSTALLER_TEXT_CONTRACT_FAILED",
    )
    print("ZIP CONTRACT: PASS")
    print("INSTALLER CONTRACT: PASS")
    print("PATCH_PACKAGE_CONTRACT: PASS")

def validate_no_generated_source_edit(
    project_root: Path,
    patch_zip: Path | None,
) -> None:
    """Confirm this feature edits canonical owners, not generated outputs."""
    canonical_source_paths = (
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "01_session_start_and_navigation/session_start_upload_checklist.md",
        "kanda_prompt_workspace/prompt_library/METADATA/"
        "session_start_upload_checklist.meta.json",
        "kanda_prompt_workspace/prompt_tools/"
        "README_kanda_startup_prompt_request_kernel_generator.md",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/startup_names.py",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/"
        "start_here_body_intro.py",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/"
        "paste_after_uploading_body.py",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/readme_body.py",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/"
        "startup_literal_texts.py",
        "scripts/validate_sync_startup_kernel_refactor_train_car_7_v1.py",
        "tools/validate_project_ready_check_project_in_use_v1.py",
    )

    for relative_path in canonical_source_paths:
        source_path = project_root / relative_path
        require(
            source_path.is_file(),
            "CANONICAL_SOURCE_FILE_MISSING: " + relative_path,
        )
        relative_parts = tuple(
            part.lower() for part in Path(relative_path).parts
        )
        require(
            "first_prompt_files" not in relative_parts,
            "GENERATED_ARTIFACT_PATH_USED_AS_CANONICAL_SOURCE: "
            + relative_path,
        )

    if patch_zip is not None:
        import json
        import zipfile

        with zipfile.ZipFile(patch_zip, "r") as archive:
            members = tuple(archive.namelist())
            manifest = json.loads(
                archive.read("INSTALL_MANIFEST.json").decode(
                    "utf-8",
                    errors="replace",
                )
            )

        payload_paths = []
        for member in members:
            if member.startswith("payload/") and not member.endswith("/"):
                payload_paths.append(member[len("payload/"):])
        manifest_paths = [
            str(row.get("path", "")) for row in manifest.get("files", [])
        ]

        for relative_path in payload_paths + manifest_paths:
            normalized_parts = tuple(
                part.lower()
                for part in PurePosixPath(relative_path).parts
            )
            require(
                "first_prompt_files" not in normalized_parts,
                "GENERATED_ARTIFACT_INCLUDED_IN_PATCH_PAYLOAD: "
                + relative_path,
            )

    print("GENERATED_ARTIFACT_SOURCE_SEPARATION: PASS")


def main() -> int:
    """Run the focused source and generated-text validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--delivery-dir")
    parser.add_argument("--patch-zip")
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    delivery_dir = (
        Path(args.delivery_dir).expanduser().resolve()
        if args.delivery_dir
        else None
    )
    patch_zip = (
        Path(args.patch_zip).expanduser().resolve()
        if args.patch_zip
        else None
    )

    try:
        names, start_here, paste_readme = load_startup_modules(project_root)
        validate_canonical_prompt(project_root)
        validate_prompt_metadata(project_root)
        validate_constants(names)
        validate_generated_text(start_here, paste_readme)
        validate_generated_delivery(delivery_dir)
        validate_patch_package(project_root, patch_zip)
        validate_no_generated_source_edit(project_root, patch_zip)
    except Exception as exc:
        print(
            "VALIDATION ERROR: "
            + type(exc).__name__
            + ": "
            + str(exc)
        )
        return 1

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
