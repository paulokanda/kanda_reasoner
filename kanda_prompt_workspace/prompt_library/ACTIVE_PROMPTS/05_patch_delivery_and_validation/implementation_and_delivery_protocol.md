# Implementation and Delivery Protocol

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


You are working on my Windows 11 Python project. Follow this complete surgical‑patch workflow exactly.
1. Core working style

    Take your time. Do not rush.

    Before writing code:

        Read the current uploaded project evidence.

        Prefer uploaded handoff/source package over memory.

        Inspect relevant files/contracts.

        Identify the correct feature box before changing anything.

        Make a narrow implementation plan.

        Avoid broad rewrites.

    When creating code:

        Work inside your sandbox/environment first.

        Create or patch files there.

        Check for syntax errors, import errors, BOM/encoding problems.

        Use plain UTF‑8 without BOM.

        Use plain ASCII in Python files (no emojis, Unicode icons, special punctuation, terminal colors, or shell‑specific tricks).

        Use Python 3.10+ compatible code.

        Keep code Windows / PyCharm friendly.

        Prefer standard library unless a clear reason for external dependencies exists.

1.1 Mandatory sandbox pre-delivery gate

Before sending any patch ZIP download link, install block, validation block, or final patch delivery to the user, the AI must validate the deliverable inside its own sandbox/environment first.

Minimum sandbox gate:

    Create the patch ZIP in the sandbox.

    Re-open or extract the ZIP in the sandbox.

    Verify the ZIP contains only intended changed/new installable files.

    Verify the ZIP does not contain cache files, temporary files, installer scripts, validation helpers, README clutter, .git, backup folders, workbench scratch files, or unrelated project files.

    Run python -m py_compile on every changed Python file and every Python helper or validation file generated for the user, when Python files exist.

    Run focused sandbox tests, smoke tests, or exact-text checks that can be run safely without the user's local machine.

    For prompt or startup delivery changes, run exact phrase checks and the available startup/delivery generator or checker when available.

    Inspect the final install block before sending it and confirm it moves the ZIP from the drive root into the delete-after-daily-work staging folder before installing.

    State clearly in the final answer what was validated in sandbox and what still requires user-local validation.

The AI must not send untested code or an uninspected installer block unless it explicitly says which sandbox checks could not be performed and why.

2. Source of truth (priority order)

Do not implement from old memory alone. Use this priority:

    My current instruction.

    Uploaded handoff/source ZIPs and current logs.

    Current project files.

    Current validation output.

    Existing project contracts/governance.

    Memory only as secondary context.

If uploaded evidence conflicts with memory → trust the uploaded evidence.
3. Handoff / source package

At the beginning of a task, ask for or use the current uploaded project evidence package.

Preferred uploads (in order of usefulness):

    <PROJECT_NAME>__ai_handoff_upload.zip – primary

    <PROJECT_NAME>__ai_handoff_reconstruction.zip – only if exact reconstruction needed

    <PROJECT_NAME>__ai_handoff_all_in_one.zip – archive/convenience

Also accept any uploaded logs, screenshots, terminal output, validation output, or error traces.
4. Patch delivery method

Do not send loose code blocks as the main delivery.

Create a small surgical patch ZIP.
The ZIP must contain only files that need to be added or replaced.

ZIP structure:
text

PATCH_NAME.zip
  kanda_reasoner_app\...
  tests\...

Only include changed/new files.
Do not include:

    unrelated files

    caches / __pycache__

    project_analysis_evidence

    workbench

    .git

    venv

    backup folders

    temporary files

5. Project rules (always apply)

    Use standard Python 3.10+.

    Use plain ASCII in Python files.

    Do not hardcode project paths inside implementation code.

    In terminal instructions, use:
    powershell

    $PROJECT_ROOT = "<PROJECT_ROOT>"
    Set-Location $PROJECT_ROOT
    $env:PYTHONPATH = $PROJECT_ROOT

    Implementation code must use dynamic paths and remain project‑agnostic.

    Respect box logic:

        Implement inside the correct feature box.

        Do not modify other boxes unless an explicit boundary reason exists.

        If changing a file consumed by another box → declare the handoff and validate the consumer box.

        Do not change existing public contracts unless required.

        Prefer additive compatibility over breaking changes.

    Keep changes:

        focused

        DRY

        SOLID

        Windows‑compatible

        project‑agnostic

6. Install script requirements (PowerShell)

After the ZIP, provide a Windows PowerShell install script.

The install script must implement the canonical root-to-staging ZIP flow.

The user downloads the patch ZIP to the root of the same drive as the project, for example:

```text
<drive>:\PATCH_NAME.zip
```

The installer must move the ZIP into:

```text
<drive>:\<PROJECT_NAME>_delete_after_daily_work\PATCH_NAME.zip
```

before extracting or installing anything.

6.1 Define fixed project and derived staging paths

```powershell
$PROJECT_ROOT = "<PROJECT_ROOT>"
$PATCH_NAME = "PATCH_NAME"
$PROJECT_NAME = Split-Path $PROJECT_ROOT -Leaf
$DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
$WORK_DIR = Join-Path $DRIVE_ROOT ($PROJECT_NAME + "_delete_after_daily_work")
$ROOT_PATCH_ZIP = Join-Path $DRIVE_ROOT ($PATCH_NAME + ".zip")
$WORK_PATCH_ZIP = Join-Path $WORK_DIR ($PATCH_NAME + ".zip")
$EXTRACT_DIR = Join-Path $WORK_DIR $PATCH_NAME
$BACKUP_DIR = Join-Path $WORK_DIR ("backup_" + $PATCH_NAME + "_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
```

Do not hardcode `E:\` or any other fixed drive.
Derive the drive from `$PROJECT_ROOT` using `$DRIVE_ROOT`.

6.2 Move or copy-stage the ZIP from drive root into staging, then delete the root copy

The install script must contain this behavior before extraction:

```powershell
if (-not (Test-Path $WORK_DIR)) {
    New-Item -ItemType Directory -Path $WORK_DIR -Force | Out-Null
}

if (Test-Path $ROOT_PATCH_ZIP) {
    Copy-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force
    if (Test-Path $WORK_PATCH_ZIP) {
        Remove-Item -Path $ROOT_PATCH_ZIP -Force
    }
}

if (-not (Test-Path $WORK_PATCH_ZIP)) {
    throw "zip is not in root of drive:\ where project is"
}
```

The final install block must include the phrase and behavior `move the ZIP`.
Do not require the user to manually put the ZIP in the staging folder.
Install only from `$WORK_PATCH_ZIP`.

Forbidden for KANDA/PyArchitect patch installers:

- Do not search `Downloads` or `Desktop` before checking `$ROOT_PATCH_ZIP`.
- Do not use a generic fallback candidate list that can prefer user profile folders over the project drive root.
- Do not leave `$ROOT_PATCH_ZIP` behind after staging succeeds.
- Do not extract or install from any location except `$WORK_PATCH_ZIP` under `$WORK_DIR`.

6.3 Extract ZIP to `$EXTRACT_DIR` under the delete-after-daily-work folder

Do not extract patch ZIPs into the active project root.

6.4 Create surgical backup folder under the delete-after-daily-work folder

Backup only exact target files that will be overwritten.

    Preserve relative paths inside the backup folder.

    If a target file does not exist yet, record that in the manifest if a manifest is used.

    Do not back up the entire project.

    Do not move/delete unrelated folders.

6.5 Copy new files from extracted ZIP into the project

Copy only the files included in the patch manifest or explicit install file list.

6.6 Optional install manifest

If a patch install manifest is created, write it outside the active project root, preferably under the delete-after-daily-work folder. It should contain:

    patch name

    timestamp

    project root

    staged ZIP path

    list of copied files

    list of overwritten files

    list of newly created files

    backup folder path

6.7 Automatic controlled restore inside the install script (failure handler)

If install fails during copy:

    Restore only files touched by this patch.

    If a file existed before install, restore it from the backup copy.

    If a file did not exist before install and was created by this failed patch, delete only that created file.

    Do not restore the whole project.

    Do not delete unrelated files.

    Do not touch files outside the patch manifest or explicit install file list.

    Print clear messages:

```text
INSTALL FAILED
SURGICAL RESTORE STARTED
SURGICAL RESTORE COMPLETED
```

    Return nonzero exit code after restore.

6.8 Install terminal behavior

Install scripts must use this controlled terminal behavior:

- If install succeeds with exit code 0:
    - print a clear success message;
    - wait 5 seconds;
    - clear the terminal after the 5 second pause.

- If install fails with nonzero exit code:
    - print a clear failure message;
    - preserve all visible error output;
    - do not clear the terminal unless the user presses Enter twice in the explicit failure branch.

- Do not use `finally` blocks for terminal cleanup.
- Do not clear the terminal from a shared cleanup path.
- Clearing is allowed only in the explicit success branch after the 5 second pause, or after Enter + Enter in an explicit failure branch.
- Failure branches must leave all logs visible until user confirmation.

7. Manual restore script rule

Do not provide a separate manual surgical restore script by default.

Only provide a separate manual restore script when one of these happens:

    Install fails.

    Validation fails after install.

    I explicitly ask for a restore script.

    The patch is high‑risk and you clearly explain why the restore script should be shown in advance.

    This avoids confusion and prevents me from running restore unnecessarily after a successful validation.

8. Validation script requirements (PowerShell)

Provide validation separately from install.

The validation script must run in this order:

    Focused tests

    Relevant regressions

    py_compile

    Workflow validation

    Architecture validation

Use this exact pattern:
powershell

$PROJECT_ROOT = "<PROJECT_ROOT>"
Set-Location $PROJECT_ROOT
$env:PYTHONPATH = $PROJECT_ROOT

python tests\test_PATCH_NAME.py
Write-Host "PATCH focused direct test exit code: $LASTEXITCODE"

python tests\test_RELEVANT_REGRESSION.py
Write-Host "Regression direct test exit code: $LASTEXITCODE"

python -m py_compile `
path\to\changed_file_1.py `
path\to\changed_file_2.py `
tests\test_PATCH_NAME.py

Write-Host "py_compile exit code: $LASTEXITCODE"

python kanda_reasoner_app\manage_workflows\manage_workflows.py --root "$PROJECT_ROOT" --validate
Write-Host "workflow validation exit code: $LASTEXITCODE"

python kanda_reasoner_app\manage_architecture\manage_architecture.py --root "$PROJECT_ROOT" --validate
Write-Host "architecture validation exit code: $LASTEXITCODE"

8.1 Validation terminal behavior

Validation scripts must preserve output until the user has copied it.

Use this interaction pattern after validation output is printed:

1. Prompt: `Press Enter after copying this validation output.`
2. Wait for Enter.
3. Prompt: `Press Enter again to clear the terminal.`
4. Wait for Enter again.
5. Clear the terminal only after the second Enter.

Validation output must not clear automatically.
Validation failure output must remain visible until the same Enter + Enter sequence is completed.
Do not close the terminal session automatically.

Expected clean validation output

    focused tests: exit code 0

    regressions: exit code 0

    py_compile: exit code 0

    workflow validation: pass=8 fail=0 warn=0 skip=3

    architecture validation: No validation issues

9. Freeze rule

Do not say a patch is frozen until I paste successful validation output.

    If validation fails:

        Do not pretend the patch is validated.

        Tell me exactly which command failed.

        Explain whether the failure is caused by the patch or an existing unrelated issue.

        Provide a controlled manual restore script only if needed (per manual restore script rule).

        Prepare a narrow repair patch if appropriate.

    When validation passes cleanly:

        Confirm the patch is validated.

        State the exact clean outputs.

        Then mark it frozen only if I ask or the series is clearly complete.

10. Final response format for patch delivery (default)

Use this exact format:

    Patch name

    What it changes (bulleted list or short paragraph)

    Download ZIP link (or instructions to obtain the ZIP)

    Install PowerShell script (full script in a code block)

    Validation PowerShell script (full script in a code block)

    Expected result (copy the clean validation output table/values)

    What to paste back to me if something fails (e.g., “Paste the output of the failed command”)

Do not include a separate manual surgical restore script in the default response.
11. Ongoing communication

For long work:

    Keep me updated briefly.

    Say what you are checking or fixing.

    Do not spam low-level details.

    Do not promise background work.

    Complete as much as possible in the current response.

12. Important current project conventions

    Active evidence folder: project_analysis_evidence

    Canonical complete JSON path pattern:
    text

    <PROJECT_ROOT>\project_analysis_evidence\json_complete\<PROJECT_SLUG>__complete.json

    Example: developer_tools__complete.json

    _project_reference and project_freeze_ledger are memo/reference only – not active code.

    project_analysis_evidence is evidence, not source code.

    Tests can be used for validation, but Tab 8 / Atlas should not treat tests as active project files.

    Do not physically rename _project_reference unless we explicitly decide to do that in a separate validated patch.

13. Final reminder

Work carefully, validate before delivery, and prefer a narrow safe patch over a broad rewrite.

When in doubt: make the patch smaller, not larger.

14. Terminal output preservation and controlled clearing rule

Terminal output is audit evidence, but Kanda patch scripts use controlled clearing so the terminal remains usable after successful operations.

Canonical rule:

- Installation logs must remain visible on failure.
- Validation logs must remain visible until the user confirms they copied them.
- Terminal clearing is allowed only in the exact controlled cases below.
- Do not use broad cleanup paths or `finally` blocks to clear the terminal.
- Do not close the visible PowerShell session automatically.
- Do not delete, truncate, overwrite, or remove log files.

Allowed terminal clearing:

1. Install success only:
   - if install exits with code 0;
   - show success message;
   - wait 5 seconds;
   - then clear the terminal.

2. Validation completion only:
   - after validation output is shown;
   - user presses Enter once after copying the output;
   - user presses Enter a second time to confirm clearing;
   - then clear the terminal.

Forbidden terminal behavior:

- clearing on install failure;
- clearing before validation output is copied;
- clearing from `finally`;
- clearing from shared cleanup code;
- deleting audit, install, validation, diagnostic, or traceback logs;
- commands that close the visible PowerShell session.

15. Patch lifecycle and freeze gate

For Kanda Reasoner and any complex Python app, patch delivery must make the lifecycle status explicit:

```text
created but not installed
installed but not validated
focused validated but not globally validated
fully validated but not frozen
frozen
failed and restored
abandoned
```

A ZIP delivery is not enough by itself.

The process is not finished when the ZIP is delivered.
The process is not finished when the patch is installed.
The process is finished only after validation output is reviewed.

If validation passes cleanly, the patch becomes freezeable.
Do not mark it frozen unless the user explicitly approves freezing or the series is clearly complete and the user agrees.

If validation fails:

- do not pretend the patch is validated;
- identify the failed command;
- preserve the failure output;
- explain whether the failure appears patch-related or unrelated;
- provide a controlled repair or restore path only when needed.

If the project has a patch registry, update it instead of relying on chat memory.
If the project has a unified validation runner, provide commands for that runner instead of manually listing every command, unless the runner itself is being built.
