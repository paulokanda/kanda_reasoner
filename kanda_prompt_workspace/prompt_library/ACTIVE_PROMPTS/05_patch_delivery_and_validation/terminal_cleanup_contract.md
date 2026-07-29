---
prompt_id: terminal_cleanup_contract
prompt_code: KPR-05-007
title: Terminal Cleanup Contract
version: 2.1
status: active
load_type: always_startup
owner_box: 05_patch_delivery_and_validation
source_stage: powershell-paste-safe-operational-output-v1
---

# Terminal Cleanup Contract

## Purpose

Own the user-facing Windows PowerShell entry and cleanup behavior for install,
validation, freeze, diagnostic, recovery, and error blocks. This prompt does not
own command semantics, patch staging, validation logic, or freeze authorization.

## Clean-prompt entry guard

Before every long interactive block, tell the user to begin at a clean primary
PowerShell prompt such as `PS E:\\project>`. If `>>` is visible, require
`Ctrl+C` before pasting anything else. Do not wrap a long block in an unnecessary
outer `& { ... }` script block.

## Paste-unit contract

Each user-visible PowerShell code fence is one complete paste unit. Prefer a
direct invocation of a packaged script. Do not split a control-flow statement
across messages, code fences, or console submissions.

For `INTERACTIVE_USER_TERMINAL` entry blocks:

- do not use `else`, `elseif`, or `finally`;
- do not emit standalone `catch`;
- keep `try/catch` logic inside packaged scripts rather than the entry command;
- use independent complete `if` checks only when a direct script call cannot own
  the preflight;
- target Windows PowerShell 5.1-compatible APIs unless another runtime is
  explicitly verified;
- verify human-selected or generated paths before use.

If a previous paste left the console at `>>`, require `Ctrl+C`, return to the
primary prompt, and restart with the complete paste unit.

## Execution environment classification

Classify the consumer before emitting a footer:

```text
INTERACTIVE_USER_TERMINAL
PACKAGED_INTERACTIVE_SCRIPT
NONINTERACTIVE_AUTOMATION
```

`Read-Host` is valid only for interactive user-visible execution. Automation and
machine-run validators must use exit codes and captured output, not interactive
prompts or automatic terminal clearing.

## Operation classification

Classify the block as exactly one of:

```text
INSTALL_SUCCESS
INSTALL_ERROR
VALIDATION
FREEZE
DIAGNOSTIC
VALIDATION_ERROR
FREEZE_ERROR
RECOVERY
OTHER_TERMINAL
```

If successful installation is not proven, use the non-install-success path.

## Install-success cleanup

Use only after the installer returned success and all receiver-level installed
hash checks passed. Show success, wait about two seconds, call `Clear-Host`, keep
the terminal open, and do not ask for Enter.

```powershell
if (-not $InstallFailed) {
    Write-Host ""
    Write-Host "INSTALL OK. Terminal will clear in 2 seconds..."
    Start-Sleep -Seconds 2
    Clear-Host
}
```

## Non-install-success cleanup

For interactive validation, freeze, diagnostics, recovery, and every error path,
preserve all relevant output, ask for Enter twice, run one final `Clear-Host`, and
keep the terminal open.

```powershell
Write-Host ""
Read-Host "Press Enter to clear terminal"
Read-Host "Press Enter again to clear"
Clear-Host
```

## Error provenance

Every guarded block must retain:

```text
PHASE
ERROR TYPE
ERROR MESSAGE
INVOCATION, when available
LAST SUCCESSFUL MARKER, when available
```

Install errors use the interactive Enter, Enter cleanup and must never fall
through to the timed success footer. Do not print PASS after a preceding command
failed.

## PowerShell safety

- Do not use `exit`, `Stop-Process`, `Restart-Computer`, or terminal-closing
  commands.
- Do not mix the timed success footer and Enter, Enter footer.
- Do not use `finally` for terminal clearing.
- User-facing and packaged PowerShell must not use `else` or `elseif`.
- Validate every critical path before passing it to `-LiteralPath`.
- Do not use inline `python -c` for KANDA operational helpers; create a temporary
  UTF-8 `.py` file under project-linked `_delete_after_daily_work`.
- Do not clear error, validation, freeze, diagnostic, or recovery output before
  the second Enter.

## Output-time audit

Before showing a block, verify its operation class, execution environment,
error path, success marker ordering, clean-prompt instruction, and final footer.
If any element conflicts, block and repair the command before output.
