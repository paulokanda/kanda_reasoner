"""Validate beginning-of-day terminal cleanup bridge visibility and enforcement."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "terminal-cleanup-bridge-initial-prompts-v1"


def _assert(condition: bool, message: str) -> None:
    """Raise AssertionError when a validation condition fails."""
    if not condition:
        raise AssertionError(message)


def _read(relative_path: str) -> str:
    """Read a project file as UTF-8 text."""
    path = PROJECT_ROOT / relative_path
    _assert(path.is_file(), "missing file: " + relative_path)
    return path.read_text(encoding="utf-8", errors="replace")


def _assert_contains(path: str, fragments: list[str]) -> None:
    """Assert all fragments appear in a file."""
    text = _read(path)
    for fragment in fragments:
        _assert(fragment in text, "missing fragment in " + path + ": " + fragment)


def _assert_not_contains(path: str, fragments: list[str]) -> None:
    """Assert forbidden fragments do not appear in operational prompt files."""
    text = _read(path)
    lowered = text.lower()
    for fragment in fragments:
        _assert(fragment.lower() not in lowered, "forbidden fragment in " + path + ": " + fragment)


def validate_startup_bridge_text() -> None:
    """Validate that startup prompt sources expose the terminal cleanup bridge."""
    _assert_contains(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md",
        [
            "BEGINNING_OF_DAY_TERMINAL_CLEANUP_BRIDGE",
            "Install success",
            "wait about 2 seconds",
            "Validation success",
            "Freeze success or freeze-ready commands",
            "Any error",
            "Any other terminal situation",
            "Enter twice",
            "one final `Clear-Host`",
            "keep the terminal open",
        ],
    )


def validate_operational_prompt_contracts() -> None:
    """Validate operational prompt files carry the updated terminal contract."""
    operational_paths = [
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
        "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py",
    ]
    for path in operational_paths:
        file_text = _read(path)
        _assert(
            "2 seconds" in file_text or "2-second" in file_text,
            "missing 2-second rule in " + path,
        )
        _assert(
            "keep the terminal open" in file_text or "keep terminal open" in file_text,
            "missing keep-open rule in " + path,
        )
        _assert(
            "Enter, Enter, Clear-Host" in file_text
            or "Enter/Enter/Clear-Host" in file_text
            or "Enter, Enter, `Clear-Host`" in file_text
            or "`Enter`, `Enter`, one final `Clear-Host`" in file_text,
            "missing Enter Enter Clear-Host shorthand in " + path,
        )

    _assert_contains(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
        [
            "INSTALL OK. Terminal will clear in 2 seconds...",
            "Start-Sleep -Seconds 2",
            "Read-Host \"Press Enter again to clear\"",
            "Do not close the terminal",
        ],
    )
    _assert_contains(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
        [
            "TERMINAL_OUTPUT_CONTRACT",
            "INSTALL_SUCCESS",
            "FREEZE_ERROR",
            "Read-Host \"Press Enter again to clear\"",
            "Never deliver a KANDA install block without the 2-second success clear footer",
        ],
    )


def validate_no_old_operational_footer() -> None:
    """Validate old terminal footer text is absent from operational prompts/templates."""
    paths = [
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
        "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py",
        "kanda_reasoner_app/patch_governance/installer_template.ps1",
    ]
    forbidden = [
        "INSTALL OK. Terminal will clear in 5 seconds...",
        "Start-Sleep -Seconds 5",
        "Press Enter again to finish",
    ]
    for path in paths:
        _assert_not_contains(path, forbidden)


def validate_installer_template() -> None:
    """Validate the patch governance installer template uses the new footer."""
    _assert_contains(
        "kanda_reasoner_app/patch_governance/installer_template.ps1",
        [
            "INSTALL OK. Terminal will clear in 2 seconds...",
            "Start-Sleep -Seconds 2",
            "INSTALL ERROR",
            "Read-Host \"Press Enter to clear terminal\"",
            "Read-Host \"Press Enter again to clear\"",
            "Clear-Host",
        ],
    )
    _assert_not_contains(
        "kanda_reasoner_app/patch_governance/installer_template.ps1",
        ["exit 1", "Stop-Process"],
    )


def validate_generator_visible_bridge() -> None:
    """Validate generator text exposes the bridge in startup output."""
    sys.path.insert(0, str(PROJECT_ROOT))
    sys.path.insert(0, str(PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"))
    from kanda_prompt_workspace.prompt_tools import sync_startup_routing_kernel_pack as sync_pack

    expected_files = [
        "01_ai_prompt_request_canon.md",
        "02_prompt_navigation_index.md",
        "03_GROUP_ASSIMILATION_INDEX.md",
    ]
    boot_text = sync_pack.make_boot_command_text(expected_files)
    start_name, start_text = sync_pack.make_start_here_file(
        "test-cert",
        "2026-06-29T00:00:00Z",
        expected_files,
    )
    _assert(start_name == "00_START_HERE_FOR_AI.md", "unexpected startup filename")
    for output_name, output in [("boot command", boot_text), ("start here", start_text)]:
        _assert("Beginning-of-day active bridges" in output, "missing bridge section in " + output_name)
        _assert("Code Module Size Bridge" in output, "missing module bridge in " + output_name)
        _assert("Terminal Cleanup Bridge" in output, "missing terminal bridge in " + output_name)
        _assert("2 seconds" in output, "missing 2-second rule in " + output_name)
        _assert("Enter Enter" in output, "missing Enter Enter rule in " + output_name)
        _assert("keep terminal open" in output, "missing keep-open rule in " + output_name)


def _sample_response(use_old_footer: bool) -> str:
    """Build a minimal patch delivery response for output-contract validation."""
    install_success_seconds = "5" if use_old_footer else "2"
    install_success_text = "5 seconds" if use_old_footer else "2 seconds"
    second_prompt = "Press Enter again to finish" if use_old_footer else "Press Enter again to clear"
    validation_sleep = "Start-Sleep -Seconds 5\n" if use_old_footer else ""
    return textwrap.dedent(
        f'''
        PATCH DELIVERY GATE
        ZIP purpose: test patch
        ZIP placement path: <drive>:\\kanda_reasoner_delete_after_daily_work\\test_patch.zip
        What this ZIP is: source patch
        What this ZIP is not: not a root temp folder
        Install code present: yes
        Validation code present: yes
        Expected validation markers: VALIDATION OK: {FEATURE_ID}
        Changed files: scripts/validate_terminal_cleanup_bridge_initial_prompts_v1.py
        Allowed write paths: <drive>:\\kanda_reasoner_delete_after_daily_work\\ and changed project files only
        Forbidden write paths: active project root transient install temp patch correction validation helper staging files
        Freeze/freeze-intake: none
        Error Memory payload: n/a
        Post-validation steps: run validation then freeze
        What not to do: do not use Desktop or Downloads fallback
        Beginner-safe: yes
        GATE STATUS: PASS

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
            Write-Host "INSTALL OK. Terminal will clear in {install_success_text}..."
            Start-Sleep -Seconds {install_success_seconds}
            Clear-Host
        }}
        catch {{
            Write-Host "INSTALL ERROR: $($_.Exception.Message)"
            Read-Host "Press Enter to clear terminal"
            Read-Host "{second_prompt}"
            Clear-Host
            return
        }}
        ```

        ```powershell
        try {{
            Set-Location "E:\\kanda_reasoner"
            python scripts\\validate_terminal_cleanup_bridge_initial_prompts_v1.py
            Write-Host "VALIDATION OK: {FEATURE_ID}"
            {validation_sleep}Read-Host "Press Enter to clear terminal"
            Read-Host "{second_prompt}"
            Clear-Host
        }}
        catch {{
            Write-Host "VALIDATION ERROR: $($_.Exception.Message)"
            Read-Host "Press Enter to clear terminal"
            Read-Host "{second_prompt}"
            Clear-Host
            return
        }}
        ```
        '''
    )


def validate_response_contract() -> None:
    """Validate output contract accepts new footer and rejects old footer."""
    sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.validate_ai_response_patch_delivery import (
        ResponseValidationError,
        validate_response_text,
    )

    validate_response_text(_sample_response(use_old_footer=False))
    try:
        validate_response_text(_sample_response(use_old_footer=True))
    except ResponseValidationError:
        return
    raise AssertionError("old 5-second / finish-prompt terminal footer was accepted")


def main() -> int:
    """Run validation checks."""
    validate_startup_bridge_text()
    validate_operational_prompt_contracts()
    validate_no_old_operational_footer()
    validate_installer_template()
    validate_generator_visible_bridge()
    validate_response_contract()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
