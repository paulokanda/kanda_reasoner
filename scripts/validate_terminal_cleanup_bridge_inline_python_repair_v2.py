# project-path: scripts/validate_terminal_cleanup_bridge_inline_python_repair_v2.py
"""Validate terminal cleanup bridge repair that forbids inline python -c."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "terminal-cleanup-bridge-inline-python-repair-v2"


def _assert(condition: bool, message: str) -> None:
    """Raise AssertionError when a validation condition fails."""
    if not condition:
        raise AssertionError(message)


def _read(relative_path: str) -> str:
    """Read a project file as UTF-8 text."""
    path = PROJECT_ROOT / relative_path
    _assert(path.is_file(), "missing file: " + relative_path)
    return path.read_text(encoding="utf-8", errors="replace")


def _assert_contains(relative_path: str, fragments: list[str]) -> None:
    """Assert all fragments appear in a file."""
    text = _read(relative_path)
    for fragment in fragments:
        _assert(fragment in text, "missing fragment in " + relative_path + ": " + fragment)


def validate_prompt_bridge_text() -> None:
    """Validate prompt files explain the no-inline-python rule."""
    expected = [
        "python -c",
        "temporary UTF-8 `.py` helper",
        "_delete_after_daily_work",
    ]
    paths = [
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
        "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py",
    ]
    for path in paths:
        _assert_contains(path, expected)


def validate_generator_visible_bridge() -> None:
    """Validate beginning-of-day text mentions temp helper rather than python -c."""
    sys.path.insert(0, str(PROJECT_ROOT))
    sys.path.insert(0, str(PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"))
    from kanda_prompt_workspace.prompt_tools import sync_startup_routing_kernel_pack as sync_pack

    expected_files = [
        "01_ai_prompt_request_canon.md",
        "02_prompt_navigation_index.md",
        "03_GROUP_ASSIMILATION_INDEX.md",
    ]
    boot_text = sync_pack.make_boot_command_text(expected_files)
    _, start_text = sync_pack.make_start_here_file(
        "test-cert",
        "2026-06-29T00:00:00Z",
        expected_files,
    )
    for label, text in (("boot command", boot_text), ("start here", start_text)):
        _assert("Terminal Cleanup Bridge" in text, "missing terminal bridge in " + label)
        _assert("temp .py helper" in text, "missing temp helper rule in " + label)
        _assert("not python -c" in text, "missing python -c warning in " + label)


def _response_with_freeze_block(use_inline_python: bool) -> str:
    """Build a minimal response that includes install, validation, and freeze blocks."""
    if use_inline_python:
        freeze_body = 'python -c "print(\'FREEZE READY\')"'
    else:
        freeze_body = textwrap.dedent(
            '''
            $HELPER_PY = Join-Path $WORK_DIR "freeze_prep_helper.py"
            $env:KANDA_PROJECT_ROOT = $PROJECT_ROOT
            $oldPythonPath = $env:PYTHONPATH
            if ([string]::IsNullOrWhiteSpace($oldPythonPath)) {
                $env:PYTHONPATH = $PROJECT_ROOT
            }
            else {
                $env:PYTHONPATH = $PROJECT_ROOT + ";" + $oldPythonPath
            }
            $helperCode = @'
            import os
            import sys
            from pathlib import Path

            project_root = Path(os.environ["KANDA_PROJECT_ROOT"])
            sys.path.insert(0, str(project_root))

            from kanda_reasoner_app.freeze_hint_intake.contract import (
                merge_validation_evidence_into_latest_hint,
                scan_and_save_latest_freeze_hint,
            )
            print("merge_validation_evidence_into_latest_hint")
            print("FREEZE READY")
            '@
            Set-Content -Path $HELPER_PY -Value $helperCode -Encoding UTF8
            python $HELPER_PY
            '''
        ).strip()
    raw_text = textwrap.dedent(
        f'''
        PATCH DELIVERY GATE
        ZIP purpose: test patch
        ZIP placement path: <drive>:\\kanda_reasoner_delete_after_daily_work\\test_patch.zip
        What this ZIP is: source patch
        What this ZIP is not: not a root temp folder
        Install code present: yes
        Validation code present: yes
        Expected validation markers: VALIDATION OK: {FEATURE_ID}
        Changed files: scripts/validate_terminal_cleanup_bridge_inline_python_repair_v2.py
        Allowed write paths: <drive>:\\kanda_reasoner_delete_after_daily_work\\ and changed project files only
        Forbidden write paths: active project root transient install temp patch correction validation helper staging files
        Freeze/freeze-intake: root KANDA_FREEZE_HINT.json included
        Error Memory payload: n/a
        Post-validation steps: run validation then freeze prep
        What not to do: do not use Desktop or Downloads fallback
        Beginner-safe: yes
        GATE STATUS: PASS

        RECEIVER DELIVERY CHECK
        Receiver classification: FREEZE_HINT_INTAKE
        Actual receiver path or action: <project_drive>\\<project_name>_show_project_to_AI\\project_freeze_after_update\\freeze_hint_intake
        Installer stages to receiver: yes
        Manual paste required: no
        Storage-only helper: no
        Receiver proof: freeze-prep scans the staged root KANDA_FREEZE_HINT.json into freeze_hint_intake.
        RECEIVER STATUS: PASS

        test_patch.zip

        ```powershell
        try {{
            $PROJECT_ROOT = "E:\\kanda_reasoner"
            $PATCH_NAME = "test_patch"
            $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
            $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
            $WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
            $ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT ($PATCH_NAME + ".zip")
            $WORK_PATCH_ZIP = Join-Path $WORK_DIR ($PATCH_NAME + ".zip")
            Add-Type -AssemblyName System.IO.Compression.FileSystem
            $zip = [System.IO.Compression.ZipFile]::OpenRead($WORK_PATCH_ZIP)
            foreach ($entry in $zip.Entries) {{
                $name = $entry.FullName
                if ($name -match "[.][.]") {{ throw "Unsafe ZIP member" }}
            }}
            $zip.Dispose()
            Expand-Archive -Path $WORK_PATCH_ZIP -DestinationPath $WORK_DIR -Force
            Write-Host "INSTALL OK. Terminal will clear in 2 seconds..."
            Start-Sleep -Seconds 2
            Clear-Host
        }}
        catch {{
            Write-Host "INSTALL ERROR: $($_.Exception.Message)"
            Read-Host "Press Enter to clear terminal"
            Read-Host "Press Enter again to clear"
            Clear-Host
            return
        }}
        ```

        ```powershell
        try {{
            Set-Location "E:\\kanda_reasoner"
            python scripts\\validate_terminal_cleanup_bridge_inline_python_repair_v2.py
            Write-Host "VALIDATION OK: {FEATURE_ID}"
            Read-Host "Press Enter to clear terminal"
            Read-Host "Press Enter again to clear"
            Clear-Host
        }}
        catch {{
            Write-Host "VALIDATION ERROR: $($_.Exception.Message)"
            Read-Host "Press Enter to clear terminal"
            Read-Host "Press Enter again to clear"
            Clear-Host
            return
        }}
        ```

        ```powershell
        try {{
            $PROJECT_ROOT = "E:\\kanda_reasoner"
            $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
            $PROJECT_NAME = Split-Path -Leaf $PROJECT_ROOT
            $WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
            {freeze_body}
            Write-Host "FREEZE READY: {FEATURE_ID}"
            Read-Host "Press Enter to clear terminal"
            Read-Host "Press Enter again to clear"
            Clear-Host
        }}
        catch {{
            Write-Host "FREEZE ERROR: $($_.Exception.Message)"
            Read-Host "Press Enter to clear terminal"
            Read-Host "Press Enter again to clear"
            Clear-Host
            return
        }}
        ```
        '''
    )
    return "\n".join(line.lstrip() for line in raw_text.splitlines())


def validate_response_contract() -> None:
    """Validate response gate rejects python -c and accepts temp helper files."""
    sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.validate_ai_response_patch_delivery import (
        ResponseValidationError,
        validate_response_text,
    )

    validate_response_text(_response_with_freeze_block(use_inline_python=False))
    try:
        validate_response_text(_response_with_freeze_block(use_inline_python=True))
    except ResponseValidationError:
        return
    raise AssertionError("response validator accepted inline python -c in freeze-prep block")


def main() -> int:
    """Run validation checks."""
    validate_prompt_bridge_text()
    validate_generator_visible_bridge()
    validate_response_contract()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
