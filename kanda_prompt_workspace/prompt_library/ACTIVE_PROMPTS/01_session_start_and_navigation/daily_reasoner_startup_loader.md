---
audit_id: A033
audit_decision: UPDATE
audit_classification: ACTIVE_DAILY_REASONER_LOADER
audit_batch: prompt_audit_chunk_003
review_status: sandbox_checked
---

> Audit note: This file was reviewed in batch mode. The content below is the real updated file for this audit decision.

# Daily Reasoner Startup Loader

## Box Logic Requirement

Before any implementation, repair, refactor, prompt update, governance update, or bundle creation, the AI must:

- Identify the active box before implementation.
- State owner paths.
- State files allowed to change.
- State files explicitly out of scope.
- Declare cross-box touches.
- Preserve public contracts.
- Validate the active box and any touched external box.


Version: 14.2
Status: Daily Reasoner startup loader
Use: Paste after the Reasoner startup canon.
Project:
- <PROJECT_ROOT>
- Package: <PROJECT_ROOT>\kanda_reasoner_app

Active governance folder:
_project_reference\ACTIVE_PROJECT_ GOVERNANCE\

Important:
- Preserve the folder name exactly.
- There is a space between the underscore and GOVERNANCE.
- Do not normalize it to ACTIVE_PROJECT_GOVERNANCE.
- Do not use tools\architecture as the active governance delivery path.

Active governance files:
1. _project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.md
2. _project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.json
3. _project_reference\ACTIVE_PROJECT_ GOVERNANCE\check_reasoner_project_canon.py
4. _project_reference\ACTIVE_PROJECT_ GOVERNANCE\test_reasoner_project_canon.py
5. _project_reference\ACTIVE_PROJECT_ GOVERNANCE\accepted_warning_baseline.json


Daily first task:
Ask the user to upload the current active governance ZIP or these five files.
If they are missing, create a governance-only ZIP containing exactly those five
files and no runtime/source files.

PowerShell request for current governance:
cd <PROJECT_ROOT>

$root = "<PROJECT_ROOT>"
$out = "<PROJECT_ROOT>\reasoner_daily_canon_files.zip"

$files = @(
    "_project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.md",
    "_project_reference\ACTIVE_PROJECT_ GOVERNANCE\REASONER_PROJECT_CANON.json",
    "_project_reference\ACTIVE_PROJECT_ GOVERNANCE\check_reasoner_project_canon.py",
    "_project_reference\ACTIVE_PROJECT_ GOVERNANCE\test_reasoner_project_canon.py",
    "_project_reference\ACTIVE_PROJECT_ GOVERNANCE\accepted_warning_baseline.json"
)

$missing = @()
foreach ($rel in $files) {
    $path = Join-Path $root $rel
    if (-not (Test-Path $path)) {
        $missing += $rel
    }
}

if ($missing.Count -eq 0) {
    if (Test-Path $out) {
        Remove-Item $out -Force
    }
    $staging = Join-Path $env:TEMP ("reasoner_daily_canon_" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $staging | Out-Null
    foreach ($rel in $files) {
        $src = Join-Path $root $rel
        $dst = Join-Path $staging $rel
        New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
        Copy-Item $src $dst -Force
    }
    Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $out -Force
    Remove-Item $staging -Recurse -Force
    Write-Host "Upload this ZIP:"
    Write-Host $out
} else {
    Write-Host "REASONER CANON FILES MISSING"
    $missing | ForEach-Object { Write-Host $_ }
}

Daily workflow:
1. Load prompt stack.
2. Load active governance.
3. Load latest 0000 6.0 handoff.
4. Read current task and logs.
5. Identify current box and forbidden boxes.
6. Request source files if needed.
7. Warn if complex.
8. Roadmap first for complex tasks.
9. Implement one focused bundle.
10. Validate targeted files.
11. Deliver one direct ZIP with project-relative folders.
12. Wait for user validation.
13. Only then update governance if a freeze is approved.

Unified delivery rule:
- Runtime/source bundles use _bundle_temp\BUNDLE_MANIFEST_<task_slug>.txt.
- Governance-only bundles use _project_reference\ACTIVE_PROJECT_ GOVERNANCE.
- Do not use the older Reasoner-specific manifest folder for active source-bundle manifests.
- Do not require a separate backup-script folder or a install script.
- Do not ask the user to unzip to a temp folder before installing.
- The ZIP must extract directly into <PROJECT_ROOT>.

Canon update rule:
Update governance only when:
- implementation validated;
- user explicitly approves freeze/canon update;
all five governance files are updated consistently.

Do not update governance for proposals, unvalidated work, experiments, or local
conversation preferences.
## AI Prompt Request Canon Requirement

At the start of the session and before any non-trivial project action, load or enforce i_prompt_request_canon.

The AI must classify the user's request and, when the needed prompt stack or project evidence is missing, ask the human for the correct prompts/files before implementation, refactor, prompt-library modification, architecture change, database/storage work, validation, freeze, or handoff.

For example, if the human says "we will start creating a new folder with a databank," the AI must recognize a new architecture/data-storage task and request the relevant prompt stack: session start, AI prompt request canon, Box Logic, folder organization, database design, validation/type safety, security, implementation roadmap, and bundle-gated workflow.

