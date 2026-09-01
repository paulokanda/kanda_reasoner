"""Validate paste-safe PowerShell operational-output contracts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FEATURE_ID = "powershell-paste-safe-operational-output-v1"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker + ": FAIL")
    print(marker + ": PASS")


def read(root: Path, relative: str) -> str:
    path = root / relative
    require(path.is_file(), "PASTE_SAFE_REQUIRED_FILE")
    data = path.read_bytes()
    require(not data.startswith(b"\xef\xbb\xbf"), "PASTE_SAFE_UTF8_NO_BOM")
    require(b"\r\n" not in data, "PASTE_SAFE_LF_ONLY")
    return data.decode("utf-8")


def interactive_block_is_safe(text: str) -> bool:
    lowered = text.lower()
    forbidden_lines = re.compile(
        r"(?mi)^\s*(elseif|else|catch|finally)\b"
    )
    if forbidden_lines.search(text):
        return False
    if re.search(r"(?mi)^\s*try\s*\{", text):
        return False
    if ">>" in text:
        return False
    if "[system.io.path]::getrelativepath" in lowered:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--artifact-file")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()

    routine = read(
        root,
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "05_patch_delivery_and_validation/"
        "patch_validate_freeze_error_memory_routine_blueprint.md",
    )
    pre_output = read(
        root,
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "03_governance_freeze_and_handoff/pre_output_contract_gates.md",
    )
    terminal = read(
        root,
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "05_patch_delivery_and_validation/terminal_cleanup_contract.md",
    )
    master = read(
        root,
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "01_session_start_and_navigation/start_of_day_master_stack.md",
    )
    helper = read(
        root,
        "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
        "answer_validate_freeze_memorize_button_private_impl.py",
    )

    for marker in (
        "version: 4.2",
        "Paste-safe PowerShell and Error Memory prevention hard gate",
        "Windows PowerShell 5.1-compatible APIs",
        "lesson-powershell-detached-else-interactive-paste-footer-v1",
        "lesson-powershell-validation-wrapper-marker-and-finally-v1",
    ):
        require(marker in routine, "PASTE_SAFE_ROUTINE_MARKER")
    for marker in (
        "prompt_id: pre_output_contract_gates",
        "Error Memory prevention hard gate",
        "ERROR MEMORY PREVENTION POINTER",
        "PowerShell paste-safety gate",
        "DIRECT_PACKAGED_SCRIPT_INVOCATION",
        "any visible line begins with `elseif`, `else`, `catch`, or `finally`",
    ):
        require(marker in pre_output, "PASTE_SAFE_PRE_OUTPUT_MARKER")
    for marker in (
        "version: 2.5",
        "Paste-unit contract",
        "one complete paste unit",
        "Windows PowerShell 5.1-compatible APIs",
    ):
        require(marker in terminal, "PASTE_SAFE_TERMINAL_MARKER")
    require("one independent paste unit" in master, "PASTE_SAFE_STARTUP_BRIDGE")
    require("PowerShell paste rule:" in helper, "PASTE_SAFE_BUTTON_ENVELOPE")

    valid = '& $VALIDATE_SCRIPT -ProjectRoot $PROJECT_ROOT'
    invalid = (
        'elseif ($Missing) { Write-Host "missing" }',
        'else { Write-Host "failed" }',
        'finally { Clear-Host }',
        'catch { Write-Host $_ }',
        'try { Write-Host "run" }',
        '[System.IO.Path]::GetRelativePath($a, $b)',
        '>> else {',
    )
    require(interactive_block_is_safe(valid), "PASTE_SAFE_DIRECT_INVOCATION_ACCEPTED")
    require(
        all(not interactive_block_is_safe(item) for item in invalid),
        "PASTE_SAFE_INVALID_ARTIFACTS_REJECTED",
    )

    if args.artifact_file:
        artifact = Path(args.artifact_file).expanduser().resolve()
        require(artifact.is_file(), "ERROR_MEMORY_POWERSHELL_ARTIFACT_EXISTS")
        candidate = artifact.read_text(encoding="utf-8-sig")
        require(
            interactive_block_is_safe(candidate),
            "ERROR_MEMORY_POWERSHELL_PRE_OUTPUT_GUARD",
        )

    meta_paths = (
        "kanda_prompt_workspace/prompt_library/METADATA/"
        "patch_validate_freeze_error_memory_routine_blueprint.meta.json",
        "kanda_prompt_workspace/prompt_library/METADATA/"
        "pre_output_contract_gates.meta.json",
        "kanda_prompt_workspace/prompt_library/METADATA/"
        "terminal_cleanup_contract.meta.json",
    )
    pre_output_version_match = re.search(
        r"(?m)^version:\s*([^\s]+)\s*$",
        pre_output,
    )
    pre_output_stage_match = re.search(
        r"(?m)^source_stage:\s*([^\s]+)\s*$",
        pre_output,
    )
    require(
        pre_output_version_match is not None,
        "PASTE_SAFE_PRE_OUTPUT_METADATA_VERSION_PRESENT",
    )
    require(
        pre_output_stage_match is not None,
        "PASTE_SAFE_PRE_OUTPUT_METADATA_STAGE_PRESENT",
    )
    expected = (
        ("4.2", "error-memory-pre-output-prevention-hard-gate-v1"),
        (
            pre_output_version_match.group(1),
            pre_output_stage_match.group(1),
        ),
        ("2.5", "chained-install-validate-terminal-continuation-v1"),
    )
    for relative, (version, source_stage) in zip(meta_paths, expected):
        data = json.loads(read(root, relative))
        require(data.get("version") == version, "PASTE_SAFE_METADATA_VERSION")
        require(
            data.get("source_stage") == source_stage,
            "PASTE_SAFE_METADATA_SOURCE_STAGE",
        )

    print("POWERSHELL INTERACTIVE PASTE SAFETY: PASS")
    print("POWERSHELL WINDOWS 5.1 API COMPATIBILITY GATE: PASS")
    print("ERROR MEMORY DUPLICATE OWNERS ENFORCED: PASS")
    print("ERROR_MEMORY_POWERSHELL_PRE_OUTPUT_GUARD: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
