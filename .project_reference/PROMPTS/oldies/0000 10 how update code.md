You are working on my Windows 11 Python project.

Use my preferred update method:

1. Create a small surgical patch ZIP.
2. The ZIP must contain only the files that need to be added or replaced.
3. Do not send loose code blocks as the main delivery. Send a downloadable ZIP artifact.
4. After the ZIP, provide:
   - a Windows PowerShell install script
   - a separate Windows PowerShell validation script
   - expected validation output
   - a short explanation of what changed

Important project rules:

- Use standard Python compatible with project python version.
- Code must be Windows/PyCharm friendly.
- Use plain ASCII only in Python files.
- Do not hardcode project paths inside project code.
- In terminal instructions, use:
  $PROJECT_ROOT = "E:\developer_tools"
  Set-Location $PROJECT_ROOT
- Use dynamic paths in implementation code.
- Respect box logic: implement inside the correct feature box and do not modify other boxes unless there is an explicit boundary reason.
- Do not change existing public contracts unless required.
- If changing a file consumed by another box, declare the handoff and validate the consumer box.
- Keep changes focused, DRY, SOLID, and project-agnostic.

Patch ZIP requirements:

The ZIP must have this structure:

PATCH_NAME.zip
  kanda_reasoner_app\...
  tests\...

Only include changed/new files.

Do not include:
- unrelated files
- caches
- __pycache__
- project_analysis_evidence
- workbench
- .git
- venv
- backup folders

Install script requirements:

The install script must:

1. Define:
   $PROJECT_ROOT = "E:\developer_tools"
   $DRIVE_ROOT = [System.IO.Path]::GetPathRoot($PROJECT_ROOT)
   $ZIP_PATH = Join-Path $DRIVE_ROOT "PATCH_NAME.zip"
   $TEMP_DIR = Join-Path $env:TEMP "PATCH_NAME"

2. Extract the ZIP to $TEMP_DIR.

3. Before copying any file, create a surgical backup folder outside the project root:
   $BACKUP_ROOT = Join-Path $DRIVE_ROOT "_kanda_patch_backups"
   $BACKUP_DIR = Join-Path $BACKUP_ROOT "PATCH_NAME_yyyyMMdd_HHmmss"

4. Back up only the exact target files that will be overwritten.
   - Preserve relative paths inside the backup folder.
   - If a target file does not exist yet, record that in a manifest.
   - Do not back up the entire project.
   - Do not move/delete unrelated folders.

5. Copy the new files from the extracted ZIP into the project.

6. Write a patch install manifest outside the project root containing:
   - patch name
   - timestamp
   - project root
   - ZIP path
   - list of copied files
   - list of overwritten files
   - list of newly created files
   - backup folder path

Controlled restore requirement inside the install script:

The install script must contain automatic controlled restore logic in its failure handler.

If install fails during copy, restore only the files touched by this patch:

- If a file existed before install, restore it from the backup copy.
- If a file did not exist before install and was created by this failed patch, delete only that created file.
- Do not restore the entire project.
- Do not delete unrelated files.
- Do not touch files outside the patch manifest.
- Print clear messages:
  "INSTALL FAILED"
  "SURGICAL RESTORE STARTED"
  "SURGICAL RESTORE COMPLETED"
- Return nonzero exit code after restore.

Important restore-output rule:

Do not provide a separate manual surgical restore script by default.

Only provide a separate manual restore script when one of these happens:
1. Install fails.
2. Validation fails after install.
3. I explicitly ask for a restore script.
4. The patch is high-risk and you explain why the restore script should be shown in advance.

This avoids confusion and prevents me from running restore unnecessarily after a successful validation.

Validation script requirements:

Provide validation separately from install.

The validation script must run focused tests first, then regressions, then py_compile, then global gates.

Use this pattern:

$PROJECT_ROOT = "E:\developer_tools"
Set-Location $PROJECT_ROOT

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

Expected validation:

- focused tests: exit code 0
- regressions: exit code 0
- py_compile: exit code 0
- workflow validation: pass=8 fail=0 warn=0 skip=3
- architecture validation: No validation issues

If validation fails after install:

Do not pretend the patch is validated.

Tell me exactly which command failed.

Then provide a controlled manual restore script that:
- reads the patch install manifest
- restores only overwritten files from the backup folder
- removes only files newly created by that patch
- does not touch unrelated files
- prints every restored or removed path
- is safe to run from PowerShell in Windows 11

Final response format by default:

1. Patch name
2. What it changes
3. Download ZIP link
4. Install PowerShell script
5. Validation PowerShell script
6. Expected result
7. What to paste back to you if something fails

Do not include a separate manual surgical restore script in the default response.

Only include the manual surgical restore script after failure, on request, or when the patch is explicitly high-risk.

Do not rush. Prefer a narrow, safe patch over a broad rewrite.