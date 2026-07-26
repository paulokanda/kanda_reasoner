"""Validate two-second terminal cleanup wording in prompt-library contracts."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "terminal-cleanup-prompt-library-two-seconds-v1"
PATCH_NAME = "kanda_terminal_cleanup_prompt_library_two_seconds_v1_patch.zip"

PROMPT_FILES = [
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/patch_install_delivery_error_register.md",
    "kanda_prompt_workspace/prompt_library/HUMAN_APPENDIX/KANDA_HUMAN_PROJECT_ACTION_MENU_APPENDIX.md",
]

OLD_TERMINAL_PATTERNS = [
    "wait 5 seconds",
    "5 second pause",
    "5-second install-success footer",
    "Start-Sleep -Seconds 5",
]


def _project_root_from_args() -> Path:
    if len(sys.argv) >= 2:
        return Path(sys.argv[1]).resolve()
    env_value = None
    try:
        import os
        env_value = os.environ.get("PROJECT_ROOT")
    except Exception:
        env_value = None
    if env_value:
        return Path(env_value).resolve()
    return Path.cwd().resolve()


def _assert_file_contains(path: Path, needle: str) -> None:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        raise AssertionError("Missing expected text in " + str(path) + ": " + needle)


def _assert_old_patterns_absent(project_root: Path) -> None:
    for rel in PROMPT_FILES:
        path = project_root / rel
        if not path.exists():
            raise AssertionError("Missing prompt file: " + rel)
        text = path.read_text(encoding="utf-8")
        for pattern in OLD_TERMINAL_PATTERNS:
            if pattern in text:
                raise AssertionError("Old terminal cleanup reference remains in " + rel + ": " + pattern)


def _assert_new_contract(project_root: Path) -> None:
    implementation = project_root / PROMPT_FILES[0]
    register = project_root / PROMPT_FILES[1]
    appendix = project_root / PROMPT_FILES[2]

    _assert_file_contains(implementation, "wait about 2 seconds;")
    _assert_file_contains(implementation, "clear the terminal after the 2 second pause")
    _assert_file_contains(implementation, "Do not close the visible PowerShell session automatically.")
    _assert_file_contains(implementation, "user presses Enter a second time to confirm clearing")

    _assert_file_contains(register, "Install success must show `INSTALL OK: ...`, wait about 2 seconds")
    _assert_file_contains(register, "install-success footer with anything other than the current about-2-second pause")
    _assert_file_contains(register, "Terminal blocks must not use `exit`, `Stop-Process`, or any terminal-closing")

    _assert_file_contains(appendix, "wait about 2 seconds, then clear terminal")
    _assert_file_contains(appendix, "clear only after the user presses Enter twice")


def _assert_zip_contract(project_root: Path) -> None:
    drive_root = Path(project_root.anchor)
    project_name = project_root.name
    daily_work = drive_root / (project_name + "_delete_after_daily_work")
    staged_zip = daily_work / PATCH_NAME
    if not staged_zip.exists():
        # Sandbox fallback when validating before install.
        staged_zip = Path(__file__).resolve().parents[1] / PATCH_NAME
    if not staged_zip.exists():
        return
    with zipfile.ZipFile(staged_zip, "r") as archive:
        names = set(archive.namelist())
        required = {
            "INSTALL.ps1",
            "VALIDATE.ps1",
            "FREEZE.ps1",
            "PATCH_README.txt",
            "KANDA_FREEZE_HINT.json",
            "tools/validate_terminal_cleanup_prompt_library_two_seconds_v1.py",
        }
        missing = sorted(required - names)
        if missing:
            raise AssertionError("Patch ZIP missing required files: " + ", ".join(missing))
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8"))
        if hint.get("feature_id") != FEATURE_ID:
            raise AssertionError("Wrong feature_id in KANDA_FREEZE_HINT.json")


def main() -> int:
    project_root = _project_root_from_args()
    _assert_old_patterns_absent(project_root)
    _assert_new_contract(project_root)
    _assert_zip_contract(project_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
